"""Open-Meteo günlük tahmin istemcisi (ROS'tan bağımsız).

Kullanılan alanlar (https://open-meteo.com/en/docs):
  daily = precipitation_sum, precipitation_probability_max,
          et0_fao_evapotranspiration, temperature_2m_max

İnternet yoksa veya API hata verirse son başarılı yanıt önbellekten okunur.
"""
import json
import os
import time
import urllib.parse
import urllib.request
from dataclasses import dataclass, field, asdict
from typing import List, Optional

API_URL = "https://api.open-meteo.com/v1/forecast"
DAILY_FIELDS = (
    "precipitation_sum",
    "precipitation_probability_max",
    "et0_fao_evapotranspiration",
    "temperature_2m_max",
)


@dataclass
class DailyForecast:
    latitude: float
    longitude: float
    dates: List[str] = field(default_factory=list)
    precipitation_mm: List[float] = field(default_factory=list)
    precipitation_probability_pct: List[float] = field(default_factory=list)
    et0_mm: List[float] = field(default_factory=list)
    temperature_max_c: List[float] = field(default_factory=list)
    source: str = "open-meteo"
    fetched_at: float = 0.0

    def __len__(self):
        return len(self.dates)

    def to_dict(self):
        return asdict(self)


def build_url(latitude: float, longitude: float, forecast_days: int = 7,
              timezone: str = "auto") -> str:
    if not -90.0 <= latitude <= 90.0 or not -180.0 <= longitude <= 180.0:
        raise ValueError("Geçersiz koordinat: %s, %s" % (latitude, longitude))
    if not 1 <= forecast_days <= 16:
        raise ValueError("forecast_days 1-16 aralığında olmalı")
    params = {
        "latitude": "%.4f" % latitude,
        "longitude": "%.4f" % longitude,
        "daily": ",".join(DAILY_FIELDS),
        "forecast_days": str(forecast_days),
        "timezone": timezone,
    }
    return API_URL + "?" + urllib.parse.urlencode(params, safe=",")


def _clean(values, n) -> List[float]:
    """None değerleri 0.0 yapar, uzunluğu n'e eşitler."""
    values = list(values or [])
    out = [float(v) if v is not None else 0.0 for v in values[:n]]
    return out + [0.0] * (n - len(out))


def parse_response(data: dict, source: str = "open-meteo") -> DailyForecast:
    if "daily" not in data or "time" not in data["daily"]:
        reason = data.get("reason", "beklenmeyen yanıt biçimi")
        raise ValueError("Open-Meteo yanıtı ayrıştırılamadı: %s" % reason)
    daily = data["daily"]
    n = len(daily["time"])
    return DailyForecast(
        latitude=float(data.get("latitude", 0.0)),
        longitude=float(data.get("longitude", 0.0)),
        dates=list(daily["time"]),
        precipitation_mm=_clean(daily.get("precipitation_sum"), n),
        precipitation_probability_pct=_clean(daily.get("precipitation_probability_max"), n),
        et0_mm=_clean(daily.get("et0_fao_evapotranspiration"), n),
        temperature_max_c=_clean(daily.get("temperature_2m_max"), n),
        source=source,
        fetched_at=time.time(),
    )


class OpenMeteoClient:
    def __init__(self, latitude: float, longitude: float, forecast_days: int = 7,
                 cache_path: Optional[str] = None, timeout_s: float = 10.0):
        self.latitude = latitude
        self.longitude = longitude
        self.forecast_days = forecast_days
        self.cache_path = cache_path
        self.timeout_s = timeout_s

    @property
    def url(self) -> str:
        return build_url(self.latitude, self.longitude, self.forecast_days)

    def _download(self) -> dict:
        req = urllib.request.Request(self.url, headers={"User-Agent": "akilli-vana-sulama/0.1"})
        with urllib.request.urlopen(req, timeout=self.timeout_s) as resp:
            return json.loads(resp.read().decode("utf-8"))

    def _save_cache(self, data: dict):
        if not self.cache_path:
            return
        os.makedirs(os.path.dirname(os.path.abspath(self.cache_path)), exist_ok=True)
        tmp = self.cache_path + ".tmp"
        with open(tmp, "w", encoding="utf-8") as f:
            json.dump(data, f)
        os.replace(tmp, self.cache_path)

    def load_cache(self) -> Optional[DailyForecast]:
        if not self.cache_path or not os.path.exists(self.cache_path):
            return None
        with open(self.cache_path, encoding="utf-8") as f:
            return parse_response(json.load(f), source="cache")

    def fetch(self) -> DailyForecast:
        """Canlı veriyi çeker; başarısız olursa önbelleğe düşer.

        Hiçbiri yoksa son hatayı yükseltir.
        """
        try:
            data = self._download()
            forecast = parse_response(data)
            self._save_cache(data)
            return forecast
        except Exception as err:  # ağ, zaman aşımı, ayrıştırma
            cached = self.load_cache()
            if cached is not None:
                return cached
            raise RuntimeError("Open-Meteo alınamadı ve önbellek yok: %s" % err) from err

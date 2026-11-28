import json
import os

import pytest

from irrigation_weather.open_meteo_client import OpenMeteoClient, build_url, parse_response

DATA = os.path.join(os.path.dirname(__file__), "data", "sample_response.json")


def load_sample():
    with open(DATA, encoding="utf-8") as f:
        return json.load(f)


def test_build_url_contains_required_fields():
    url = build_url(37.8746, 32.4932, forecast_days=3)
    assert url.startswith("https://api.open-meteo.com/v1/forecast?")
    for name in ("precipitation_sum", "et0_fao_evapotranspiration", "forecast_days=3"):
        assert name in url


@pytest.mark.parametrize("lat,lon,days", [(95, 0, 7), (0, 200, 7), (0, 0, 0), (0, 0, 17)])
def test_build_url_rejects_bad_input(lat, lon, days):
    with pytest.raises(ValueError):
        build_url(lat, lon, days)


def test_parse_response_replaces_nulls():
    fc = parse_response(load_sample())
    assert len(fc) == 3
    assert fc.dates[1] == "2026-11-29"
    assert fc.precipitation_mm == [0.0, 6.4, 0.0]
    assert fc.et0_mm[0] == pytest.approx(1.21)


def test_parse_response_error_body():
    with pytest.raises(ValueError):
        parse_response({"error": True, "reason": "Cannot initialize WeatherVariable"})


def test_fetch_saves_cache_and_falls_back(tmp_path):
    cache = str(tmp_path / "cache" / "last.json")
    client = OpenMeteoClient(37.87, 32.49, cache_path=cache)

    client._download = load_sample            # başarılı çağrı -> önbelleğe yazılır
    assert client.fetch().source == "open-meteo"
    assert os.path.exists(cache)

    def offline():
        raise OSError("ağ yok")
    client._download = offline                # ağ yok -> önbellekten okunur
    fc = client.fetch()
    assert fc.source == "cache" and len(fc) == 3


def test_fetch_without_cache_raises(tmp_path):
    client = OpenMeteoClient(37.87, 32.49, cache_path=str(tmp_path / "yok.json"))

    def offline():
        raise OSError("ağ yok")
    client._download = offline
    with pytest.raises(RuntimeError):
        client.fetch()

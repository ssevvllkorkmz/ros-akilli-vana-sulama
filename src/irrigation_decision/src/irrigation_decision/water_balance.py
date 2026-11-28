"""Hava tahminine dayalı sanal su bütçesi (FAO-56 'checkbook'). Sorumlu: Kişi A — Hafta 2.

Formüller (docs/yol_haritasi.md):
    ETc = Kc * ET0
    Pe  = factor * P   (P >= min_mm ise, aksi halde 0)
    D_t = clip(D_{t-1} + ETc - Pe - I_{t-1}, 0, TAW)
    sulama gerekli  <=>  D_t >= RAW = mad * TAW
    hacim [L] = D [mm] * alan [m2]
"""


def effective_rain(precip_mm, factor=0.8, min_mm=5.0):
    # TODO(Hafta 2 - A): uygulayın ve test/test_water_balance.py yazın
    raise NotImplementedError


def update_deficit(prev_deficit_mm, kc, et0_mm, effective_rain_mm, irrigation_mm, taw_mm):
    # TODO(Hafta 2 - A)
    raise NotImplementedError


def compute_demand(parcel, forecast, state):
    """parcel: parcels.yaml'daki tek kayıt, forecast: WeatherForecast alanları,
    state: parsel başına önceki açık. Dönüş: WaterDemand alanlarını içeren dict.
    48 saat içinde açığın >= %70'ini karşılayacak etkili yağış varsa postponed=True."""
    # TODO(Hafta 2 - A)
    raise NotImplementedError

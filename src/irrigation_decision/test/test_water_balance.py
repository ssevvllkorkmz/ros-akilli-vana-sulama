"""Sanal su bütçesi testleri (önce test, sonra kod).

Fonksiyonlar Hafta 2'de uygulanacak. O zamana kadar testler `xfail` ile işaretli:
CI yeşil kalır. Uygulama bitince testler geçmeye başlar, `strict=True` sayesinde
pytest "XPASS(strict)" hatası verir; bu, `@todo_hafta2` işaretlerini silme zamanı demektir.
"""
import pytest

from irrigation_decision.water_balance import compute_demand, effective_rain, update_deficit

todo_hafta2 = pytest.mark.xfail(raises=NotImplementedError, strict=True,
                                reason="Hafta 2'de uygulanacak")

PARCEL = {"id": "parcel_1", "crop": "domates", "area_m2": 400, "kc": 1.15,
          "taw_mm": 60, "mad": 0.40, "max_flow_lpm": 60}


# ---------------- effective_rain ----------------
@todo_hafta2
@pytest.mark.parametrize("precip,expected", [
    (0.0, 0.0),     # yağış yok
    (4.9, 0.0),     # eşiğin altı: toprağa yararlı değil sayılır
    (5.0, 4.0),     # eşik dahil: 0.8 * 5
    (10.0, 8.0),
])
def test_effective_rain(precip, expected):
    assert effective_rain(precip, factor=0.8, min_mm=5.0) == pytest.approx(expected)


# ---------------- update_deficit ----------------
@todo_hafta2
def test_deficit_grows_with_etc():
    # 10 + 1.2*5 = 16
    assert update_deficit(10.0, kc=1.2, et0_mm=5.0, effective_rain_mm=0.0,
                          irrigation_mm=0.0, taw_mm=100.0) == pytest.approx(16.0)


@todo_hafta2
def test_deficit_clipped_at_taw():
    assert update_deficit(98.0, 1.2, 5.0, 0.0, 0.0, taw_mm=100.0) == pytest.approx(100.0)


@todo_hafta2
def test_deficit_not_negative_after_rain():
    assert update_deficit(5.0, 1.0, 2.0, effective_rain_mm=8.0,
                          irrigation_mm=0.0, taw_mm=100.0) == pytest.approx(0.0)


@todo_hafta2
def test_irrigation_reduces_deficit():
    # 30 + 4 - 20 = 14
    assert update_deficit(30.0, 1.0, 4.0, 0.0, irrigation_mm=20.0,
                          taw_mm=100.0) == pytest.approx(14.0)


# ---------------- compute_demand ----------------
def forecast(precip):
    return {"dates": ["2026-12-07", "2026-12-08", "2026-12-09"],
            "precipitation_mm": precip,
            "et0_mm": [2.0, 2.0, 2.0]}


@todo_hafta2
def test_dry_forecast_triggers_irrigation():
    # 22 + 1.15*2 = 24.3 >= RAW = 0.4*60 = 24  -> sulama gerekli
    d = compute_demand(PARCEL, forecast([0.0, 0.0, 0.0]), {"deficit_mm": 22.0})
    assert d["parcel_id"] == "parcel_1"
    assert d["deficit_mm"] == pytest.approx(24.3)
    assert d["raw_mm"] == pytest.approx(24.0)
    assert d["postponed"] is False
    assert d["volume_liters"] == pytest.approx(24.3 * 400)   # 1 mm x 1 m2 = 1 L
    assert d["priority"] == pytest.approx(24.3 / 24.0)


@todo_hafta2
def test_rain_within_48h_postpones():
    # Yarın 30 mm -> etkili 24 mm >= 0.7 * 24.3 -> ertele
    d = compute_demand(PARCEL, forecast([0.0, 30.0, 0.0]), {"deficit_mm": 22.0})
    assert d["postponed"] is True
    assert d["volume_liters"] == pytest.approx(0.0)
    assert d["reason"]


@todo_hafta2
def test_below_raw_no_irrigation():
    d = compute_demand(PARCEL, forecast([0.0, 0.0, 0.0]), {"deficit_mm": 5.0})
    assert d["postponed"] is False
    assert d["volume_liters"] == pytest.approx(0.0)

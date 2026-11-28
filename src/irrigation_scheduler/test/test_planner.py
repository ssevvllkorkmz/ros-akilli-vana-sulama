"""Çizelgeleme testleri (önce test, sonra kod). Uygulama Hafta 2'de; o zamana kadar xfail."""
import pytest

from irrigation_scheduler.planner import ALLOWED_ANGLES, flow_for_angle, make_plan

todo_hafta2 = pytest.mark.xfail(raises=NotImplementedError, strict=True,
                                reason="Hafta 2'de uygulanacak")

PARCELS = [
    {"id": "parcel_1", "max_flow_lpm": 60},
    {"id": "parcel_2", "max_flow_lpm": 80},
    {"id": "parcel_3", "max_flow_lpm": 45},
    {"id": "parcel_4", "max_flow_lpm": 70},
]
PUMP = 120.0
START, END = 5 * 60, 9 * 60      # 05:00 - 09:00

# docs/scheduler_tasarim.md bölüm 6'daki elle çözülmüş örnek
DEMANDS = [
    {"parcel_id": "parcel_1", "volume_liters": 3600, "priority": 1.20, "postponed": False},
    {"parcel_id": "parcel_2", "volume_liters": 4800, "priority": 1.05, "postponed": False},
    {"parcel_id": "parcel_3", "volume_liters": 2700, "priority": 1.60, "postponed": False},
    {"parcel_id": "parcel_4", "volume_liters": 0, "priority": 0.90, "postponed": True},
]


def max_usage(slots):
    """Planın herhangi bir anındaki en yüksek toplam debi."""
    starts = [s["start_min"] for s in slots]
    return max(
        (sum(s["flow_lpm"] for s in slots
             if s["start_min"] <= t < s["start_min"] + s["duration_min"])
         for t in starts),
        default=0.0,
    )


@todo_hafta2
@pytest.mark.parametrize("angle,expected", [(30, 20.0), (60, 40.0), (90, 60.0)])
def test_flow_for_angle_linear(angle, expected):
    assert flow_for_angle(60, angle) == pytest.approx(expected)


@todo_hafta2
def test_flow_for_angle_rejects_other_angles():
    with pytest.raises(ValueError):
        flow_for_angle(60, 45)


@todo_hafta2
def test_capacity_never_exceeded():
    slots = make_plan(DEMANDS, PARCELS, PUMP, START, END)
    assert max_usage(slots) <= PUMP + 1e-6


@todo_hafta2
def test_postponed_parcel_not_planned():
    slots = make_plan(DEMANDS, PARCELS, PUMP, START, END)
    assert "parcel_4" not in {s["parcel_id"] for s in slots}


@todo_hafta2
def test_priority_order():
    slots = {s["parcel_id"]: s for s in make_plan(DEMANDS, PARCELS, PUMP, START, END)}
    assert slots["parcel_3"]["start_min"] <= slots["parcel_1"]["start_min"] <= slots["parcel_2"]["start_min"]


@todo_hafta2
def test_volume_window_and_angles():
    for s in make_plan(DEMANDS, PARCELS, PUMP, START, END):
        demand = next(d for d in DEMANDS if d["parcel_id"] == s["parcel_id"])
        assert s["planned_volume_liters"] == pytest.approx(demand["volume_liters"])
        assert s["flow_lpm"] * s["duration_min"] == pytest.approx(demand["volume_liters"])
        assert s["angle_deg"] in ALLOWED_ANGLES
        assert START <= s["start_min"] and s["start_min"] + s["duration_min"] <= END + 1e-6


@todo_hafta2
def test_hand_solved_example():
    slots = {s["parcel_id"]: s for s in make_plan(DEMANDS, PARCELS, PUMP, START, END)}
    assert (slots["parcel_3"]["start_min"], slots["parcel_3"]["angle_deg"]) == (300, 90.0)
    assert (slots["parcel_1"]["start_min"], slots["parcel_1"]["angle_deg"]) == (300, 90.0)
    assert (slots["parcel_2"]["start_min"], slots["parcel_2"]["angle_deg"]) == (360, 90.0)
    assert slots["parcel_2"]["duration_min"] == pytest.approx(60.0)

"""Hidrolik çizelgeleme. Sorumlu: Kişi B — tasarım Hafta 1, uygulama Hafta 2.

Tasarım: docs/scheduler_tasarim.md

Kısıt: herhangi bir anda açık vanaların toplam debisi <= pump_capacity_lpm.
Amaç:  yüksek öncelikli (deficit/RAW büyük) parseller önce, tüm hacim sulama penceresine sığsın.
Açılar: 30° / 60° / 90° -> debi = max_flow_lpm * (angle / 90)  (C'nin debi modeli ile aynı olmalı)
"""

ALLOWED_ANGLES = (30.0, 60.0, 90.0)


def flow_for_angle(max_flow_lpm, angle_deg):
    """Vana açısına göre debi [L/dk]. İzinli olmayan açıda ValueError."""
    # TODO(Hafta 2 - B)
    raise NotImplementedError


def make_plan(demands, parcels, pump_capacity_lpm, window_start, window_end):
    """Öncelik sıralı açgözlü yerleştirme.

    demands:  [{"parcel_id", "volume_liters", "priority", "postponed"}, ...]
    parcels:  [{"id", "max_flow_lpm", ...}, ...]   (parcels.yaml)
    window_start, window_end: gece yarısından itibaren dakika (05:00 -> 300)

    Dönüş: [{"parcel_id", "angle_deg", "start_min", "duration_min",
             "flow_lpm", "planned_volume_liters"}, ...]
    """
    # TODO(Hafta 2 - B): docs/scheduler_tasarim.md bölüm 5
    raise NotImplementedError

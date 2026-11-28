"""Hidrolik çizelgeleme. Sorumlu: Kişi B — tasarım Hafta 1, uygulama Hafta 2.

Kısıt: herhangi bir anda açık vanaların toplam debisi <= pump_capacity_lpm.
Amaç:  yüksek öncelikli (deficit/RAW büyük) parseller önce, tüm hacim sulama penceresine sığsın.
Açılar: 30° / 60° / 90° -> debi = max_flow_lpm * (angle / 90)  (C'nin debi modeli ile aynı olmalı)
"""

ALLOWED_ANGLES = (30.0, 60.0, 90.0)


def flow_for_angle(max_flow_lpm, angle_deg):
    # TODO(Hafta 2 - B): C ile ortak debi modeline göre güncelleyin
    raise NotImplementedError


def make_plan(demands, parcels, pump_capacity_lpm, window_start, window_end):
    """demands: WaterDemand dict listesi. Dönüş: IrrigationSlot dict listesi."""
    # TODO(Hafta 2 - B): öncelik kuyruğu + açgözlü yerleştirme (docs/scheduler_tasarim.md)
    raise NotImplementedError

"""Uç düğüm mantığı (ROS'tan bağımsız). Sorumlu: Kişi C (fail-safe: D).

- Yalnızca 0/30/60/90° kabul edilir; diğerleri en yakın izinli açıya yuvarlanır mı, reddedilir mi? -> Hafta 2'de karar verin.
- Debi modeli (Hafta 3): flow = max_flow_lpm * f(angle)
- Fail-safe (Hafta 4): son heartbeat'ten bu yana > timeout_s geçtiyse hedef açı = 0, mode = FAILSAFE
"""
import math

ALLOWED_ANGLES = (0.0, 30.0, 60.0, 90.0)


def deg_to_rad(angle_deg):
    return math.radians(angle_deg)


def validate_angle(angle_deg):
    # TODO(Hafta 2 - C)
    raise NotImplementedError


def should_failsafe(now_s, last_heartbeat_s, timeout_s):
    # TODO(Hafta 4 - D)
    raise NotImplementedError

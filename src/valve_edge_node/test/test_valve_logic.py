"""Uç düğüm vana mantığı testleri. validate_angle Hafta 2'de uygulanacak (xfail)."""
import math

import pytest

from valve_edge_node.valve_logic import ALLOWED_ANGLES, deg_to_rad, validate_angle

todo_hafta2 = pytest.mark.xfail(raises=NotImplementedError, strict=True,
                                reason="Hafta 2'de uygulanacak")


@pytest.mark.parametrize("deg,rad", [(0, 0.0), (30, math.pi / 6), (60, math.pi / 3), (90, math.pi / 2)])
def test_deg_to_rad(deg, rad):
    assert deg_to_rad(deg) == pytest.approx(rad)


def test_allowed_angles_within_joint_limits():
    # URDF limiti: 0 - pi/2 rad
    for a in ALLOWED_ANGLES:
        assert 0.0 <= deg_to_rad(a) <= math.pi / 2 + 1e-9


@todo_hafta2
@pytest.mark.parametrize("angle", [0.0, 30.0, 60.0, 90.0])
def test_validate_angle_accepts_allowed(angle):
    assert validate_angle(angle) == angle


@todo_hafta2
@pytest.mark.parametrize("angle", [-10.0, 15.0, 45.0, 95.0, 180.0])
def test_validate_angle_rejects_others(angle):
    # Karar (docs/vana_modeli.md §3): yuvarlama yok, reddet
    with pytest.raises(ValueError):
        validate_angle(angle)

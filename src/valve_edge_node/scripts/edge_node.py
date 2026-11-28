#!/usr/bin/env python3
"""Parsel uç düğümü. Kendi namespace'inde çalışır (ör. /parcel_1).
valve/command (ValveCommand) -> valve_position_controller/command (Float64, rad)
valve/state (ValveState) yayınlar; heartbeat kesilince vanayı kapatır. Sorumlu: Kişi C."""
import rospy
from std_msgs.msg import Float64
from irrigation_msgs.msg import Heartbeat, ValveCommand, ValveState

from valve_edge_node.valve_logic import deg_to_rad


def main():
    rospy.init_node("valve_edge_node")
    parcel_id = rospy.get_param("~parcel_id", rospy.get_namespace().strip("/") or "parcel_1")
    ctrl_pub = rospy.Publisher("valve_position_controller/command", Float64, queue_size=1)
    state_pub = rospy.Publisher("valve/state", ValveState, queue_size=1)

    def on_command(cmd):
        if cmd.parcel_id and cmd.parcel_id != parcel_id:
            return
        rospy.loginfo("[%s] Vana komutu: %.0f°", parcel_id, cmd.angle_deg)
        # TODO(Hafta 2 - C): validate_angle ile doğrula
        ctrl_pub.publish(Float64(deg_to_rad(cmd.angle_deg)))

    def on_heartbeat(_hb):
        pass  # TODO(Hafta 4 - D): son heartbeat zamanını sakla, timer'da should_failsafe kontrolü

    rospy.Subscriber("valve/command", ValveCommand, on_command, queue_size=5)
    rospy.Subscriber("/irrigation/heartbeat", Heartbeat, on_heartbeat, queue_size=1)
    _ = state_pub  # TODO(Hafta 3 - C): joint_states'ten açı oku, debi hesapla, 5 Hz yayınla
    rospy.spin()


if __name__ == "__main__":
    main()

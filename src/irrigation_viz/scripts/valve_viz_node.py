#!/usr/bin/env python3
"""Parselleri RViz'de kutu olarak çizer; Hafta 2'de vana açısı/debi metni ve renklendirme eklenecek.
Sorumlu: Kişi D."""
import rospy
from visualization_msgs.msg import Marker, MarkerArray


def parcel_marker(idx, parcel):
    m = Marker()
    m.header.frame_id = "world"
    m.ns = "parcels"
    m.id = idx
    m.type = Marker.CUBE
    m.action = Marker.ADD
    m.pose.position.x = parcel["position"]["x"]
    m.pose.position.y = parcel["position"]["y"]
    m.pose.position.z = -0.01
    m.pose.orientation.w = 1.0
    m.scale.x = m.scale.y = 1.8
    m.scale.z = 0.02
    m.color.r, m.color.g, m.color.b, m.color.a = 0.45, 0.30, 0.15, 0.8   # toprak rengi
    return m


def main():
    rospy.init_node("valve_viz_node")
    parcels = rospy.get_param("/irrigation/parcels", [])
    pub = rospy.Publisher("/irrigation/markers", MarkerArray, queue_size=1)
    rate = rospy.Rate(2)
    while not rospy.is_shutdown():
        arr = MarkerArray(markers=[parcel_marker(i, p) for i, p in enumerate(parcels)])
        # TODO(Hafta 2 - D): /parcel_N/valve/state dinle; açı ve debiyi TEXT_VIEW_FACING marker ile göster
        # TODO(Hafta 3 - D): /irrigation/plan'daki planlanan / gerçekleşen litreyi göster
        pub.publish(arr)
        rate.sleep()


if __name__ == "__main__":
    main()

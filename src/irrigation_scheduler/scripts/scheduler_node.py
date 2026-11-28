#!/usr/bin/env python3
"""/irrigation/demand -> /irrigation/plan ve zamanı gelen slotlar için /parcel_N/valve/command.
Ayrıca /irrigation/heartbeat yayınlar (fail-safe). Sorumlu: Kişi B (heartbeat: D)."""
import rospy
from irrigation_msgs.msg import Heartbeat, IrrigationPlan, WaterDemandArray


def main():
    rospy.init_node("scheduler_node")
    plan_pub = rospy.Publisher("/irrigation/plan", IrrigationPlan, queue_size=1, latch=True)
    hb_pub = rospy.Publisher("/irrigation/heartbeat", Heartbeat, queue_size=1)
    seq = [0]

    def on_demand(msg):
        rospy.loginfo("%d parsel için ihtiyaç alındı", len(msg.demands))
        # TODO(Hafta 2 - B): planner.make_plan -> IrrigationPlan yayınla
        _ = plan_pub

    def heartbeat(_event):
        hb = Heartbeat(source="scheduler_node", seq=seq[0])
        hb.header.stamp = rospy.Time.now()
        hb_pub.publish(hb)
        seq[0] += 1

    rospy.Subscriber("/irrigation/demand", WaterDemandArray, on_demand, queue_size=1)
    rospy.Timer(rospy.Duration(0.5), heartbeat)
    rospy.spin()


if __name__ == "__main__":
    main()

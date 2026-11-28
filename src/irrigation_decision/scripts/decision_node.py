#!/usr/bin/env python3
"""/weather/forecast -> parsel bazlı su ihtiyacı -> /irrigation/demand. Sorumlu: Kişi A."""
import rospy
from irrigation_msgs.msg import WeatherForecast, WaterDemandArray


def main():
    rospy.init_node("decision_node")
    parcels = rospy.get_param("/irrigation/parcels", [])
    pub = rospy.Publisher("/irrigation/demand", WaterDemandArray, queue_size=1, latch=True)

    def on_forecast(msg):
        rospy.loginfo("Tahmin alındı: %d gün, %d parsel", len(msg.dates), len(parcels))
        # TODO(Hafta 2 - A): water_balance.compute_demand ile WaterDemandArray doldur ve yayınla
        _ = pub

    rospy.Subscriber("/weather/forecast", WeatherForecast, on_forecast, queue_size=1)
    rospy.spin()


if __name__ == "__main__":
    main()

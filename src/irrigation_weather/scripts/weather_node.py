#!/usr/bin/env python3
"""Open-Meteo tahminini periyodik olarak /weather/forecast topic'ine yayınlar (latched)."""
import os

import rospy
import rospkg
from irrigation_msgs.msg import WeatherForecast

from irrigation_weather import OpenMeteoClient


def to_msg(fc):
    msg = WeatherForecast()
    msg.header.stamp = rospy.Time.now()
    msg.header.frame_id = "field"
    msg.source = fc.source
    msg.latitude = fc.latitude
    msg.longitude = fc.longitude
    msg.dates = fc.dates
    msg.precipitation_mm = fc.precipitation_mm
    msg.precipitation_probability_pct = fc.precipitation_probability_pct
    msg.et0_mm = fc.et0_mm
    msg.temperature_max_c = fc.temperature_max_c
    return msg


def main():
    rospy.init_node("weather_node")
    pkg_path = rospkg.RosPack().get_path("irrigation_weather")
    client = OpenMeteoClient(
        latitude=rospy.get_param("~latitude", 37.8746),
        longitude=rospy.get_param("~longitude", 32.4932),
        forecast_days=rospy.get_param("~forecast_days", 7),
        cache_path=rospy.get_param("~cache_path", os.path.join(pkg_path, "cache", "last_forecast.json")),
    )
    period_s = rospy.get_param("~update_period_s", 3600.0)
    pub = rospy.Publisher("/weather/forecast", WeatherForecast, queue_size=1, latch=True)

    def update(_event=None):
        try:
            fc = client.fetch()
        except RuntimeError as err:
            rospy.logerr("Tahmin yok: %s", err)
            return
        pub.publish(to_msg(fc))
        rospy.loginfo("Tahmin yayınlandı (%s): %d gün, bugün yağış=%.1f mm, ET0=%.2f mm",
                      fc.source, len(fc), fc.precipitation_mm[0], fc.et0_mm[0])

    update()
    rospy.Timer(rospy.Duration(period_s), update)
    rospy.spin()


if __name__ == "__main__":
    main()

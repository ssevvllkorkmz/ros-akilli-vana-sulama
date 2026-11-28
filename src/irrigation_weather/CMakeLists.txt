cmake_minimum_required(VERSION 3.0.2)
project(irrigation_weather)

find_package(catkin REQUIRED COMPONENTS rospy std_msgs irrigation_msgs)
catkin_python_setup()
catkin_package(CATKIN_DEPENDS rospy std_msgs irrigation_msgs)

catkin_install_python(PROGRAMS
  scripts/weather_node.py
  DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION})

install(DIRECTORY config launch
  DESTINATION ${CATKIN_PACKAGE_SHARE_DESTINATION}
  OPTIONAL)

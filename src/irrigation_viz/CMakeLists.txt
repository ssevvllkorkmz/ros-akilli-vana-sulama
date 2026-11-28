cmake_minimum_required(VERSION 3.0.2)
project(irrigation_viz)
find_package(catkin REQUIRED COMPONENTS rospy visualization_msgs irrigation_msgs)
catkin_package()
catkin_install_python(PROGRAMS scripts/valve_viz_node.py
  DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION})
install(DIRECTORY rviz DESTINATION ${CATKIN_PACKAGE_SHARE_DESTINATION})

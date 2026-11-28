cmake_minimum_required(VERSION 3.0.2)
project(irrigation_msgs)

find_package(catkin REQUIRED COMPONENTS message_generation std_msgs)

add_message_files(FILES
  WeatherForecast.msg
  WaterDemand.msg
  WaterDemandArray.msg
  IrrigationSlot.msg
  IrrigationPlan.msg
  ValveCommand.msg
  ValveState.msg
  Heartbeat.msg
)

generate_messages(DEPENDENCIES std_msgs)

catkin_package(CATKIN_DEPENDS message_runtime std_msgs)

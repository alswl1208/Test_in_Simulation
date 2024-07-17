cmake_minimum_required(VERSION 3.16)
project(btcpp_ros2_project)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

find_package(ament_cmake REQUIRED)
find_package(behaviortree_ros2 REQUIRED)
find_package(btcpp_ros2_interfaces REQUIRED)
find_package(rclcpp REQUIRED) # 추가된 패키지
find_package(sensor_msgs REQUIRED) # 추가된 패키지
find_package(behaviortree_cpp_v3 REQUIRED) # 추가된 패키지

# 직접 경로를 지정하여 BehaviorTree.CPP 라이브러리를 포함시키는 부분 추가
set(behaviortree_cpp_INCLUDE_DIRS "/usr/local/include/behaviortree_cpp")
set(behaviortree_cpp_LIBRARIES "/usr/local/lib/libbehaviortree_cpp.so")

set(THIS_PACKAGE_DEPS
    behaviortree_ros2
    btcpp_ros2_interfaces
    rclcpp # 추가된 패키지
    sensor_msgs # 추가된 패키지
    behaviortree_cpp_v3
)

include_directories(
    src
    ${behaviortree_ros2_INCLUDE_DIRS}
    ${behaviortree_cpp_v3_INCLUDE_DIRS}# 추가된 include 디렉토리
) 

link_directories(${behaviortree_cpp_v3_LIBRARY_DIRS}) # 수정된 부분: BehaviorTree.CPP 라이브러리 경로 추가

######################################################
# New Action Node for capturing images (추가된 부분)
add_library(capture_image_plugin SHARED src/capture_image.cpp)
target_compile_definitions(capture_image_plugin PRIVATE BT_PLUGIN_EXPORT)
ament_target_dependencies(capture_image_plugin ${THIS_PACKAGE_DEPS})

######################################################
#project_bt_executor
add_executable(project_bt_executor src/project_bt_executor.cpp)
ament_target_dependencies(project_bt_executor ${THIS_PACKAGE_DEPS})
target_link_libraries(project_bt_executor ${behaviortree_cpp_v3_LIBRARIES}) # 추가된 부분
target_link_libraries(project_bt_executor ${rclcpp_LIBRARIES}) # rclcpp 라이브러리 추가


######################################################
# INSTALL

install(TARGETS
  capture_image_plugin # 추가된 부분
  project_bt_executor
  DESTINATION lib/${PROJECT_NAME}
)

######################################################
# INSTALL plugins for other packages to load

install(TARGETS
  capture_image_plugin # 추가된 부분
  LIBRARY DESTINATION share/${PROJECT_NAME}/bt_plugins
  ARCHIVE DESTINATION share/${PROJECT_NAME}/bt_plugins
  RUNTIME DESTINATION share/${PROJECT_NAME}/bt_plugins
)

######################################################
# INSTALL Behavior.xml's, ROS config and launch files

install(DIRECTORY
    behavior_trees
    config
    launch
    DESTINATION share/${PROJECT_NAME}/
)

ament_export_dependencies(behaviortree_ros2 btcpp_ros2_interfaces)

ament_package()

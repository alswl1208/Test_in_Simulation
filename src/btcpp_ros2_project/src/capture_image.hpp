#ifndef BTCPP_ROS2_PROJECT__CAPTURE_IMAGE_HPP_
#define BTCPP_ROS2_PROJECT__CAPTURE_IMAGE_HPP_

#include <string>
#include <memory>
#include "rclcpp/rclcpp.hpp"
#include "sensor_msgs/msg/image.hpp"
#include "behaviortree_cpp/action_node.h"


namespace btcpp_ros2_project
{

class CaptureImageAction : public BT::SyncActionNode
{
public:
    CaptureImageAction(const std::string& name, const BT::NodeConfiguration& config);
    static BT::PortsList providedPorts();
    BT::NodeStatus tick() override;

private:
    void imageCB(const sensor_msgs::msg::Image::SharedPtr msg);
    void saveImage(const sensor_msgs::msg::Image::SharedPtr& img, const std::string& filename, const std::string& metadata);

    rclcpp::Subscription<sensor_msgs::msg::Image>::SharedPtr image_sub_;
    sensor_msgs::msg::Image::SharedPtr current_image_;
    rclcpp::Node::SharedPtr node_;
};

}  // namespace btcpp_ros2_project

#endif  // BTCPP_ROS2_PROJECT__CAPTURE_IMAGE_HPP_

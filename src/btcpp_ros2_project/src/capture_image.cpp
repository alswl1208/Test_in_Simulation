#include "capture_image.hpp"
#include <fstream>
#include <sstream>

namespace btcpp_ros2_project
{

CaptureImageAction::CaptureImageAction(const std::string& name, const BT::NodeConfiguration& config)
    : BT::SyncActionNode(name, config), node_(rclcpp::Node::make_shared("capture_image_node"))
{
    image_sub_ = node_->create_subscription<sensor_msgs::msg::Image>(
        "/webots/camera_topic", 10, std::bind(&CaptureImageAction::imageCB, this, std::placeholders::_1));
}

BT::PortsList CaptureImageAction::providedPorts()
{
    return { BT::InputPort<std::string>("metadata") };
}

BT::NodeStatus CaptureImageAction::tick()
{
    auto metadata = getInput<std::string>("metadata");
    if (!metadata)
    {
        throw BT::RuntimeError("missing required input [metadata]: ", metadata.error());
    }

    if (current_image_)
    {
        std::stringstream ss;
        ss << "image_" << node_->now().nanoseconds() << ".png";

        saveImage(current_image_, ss.str(), metadata.value());
        return BT::NodeStatus::SUCCESS;
    }
    else
    {
        return BT::NodeStatus::FAILURE;
    }
}

void CaptureImageAction::imageCB(const sensor_msgs::msg::Image::SharedPtr msg)
{
    current_image_ = msg;
}

void CaptureImageAction::saveImage(const sensor_msgs::msg::Image::SharedPtr& img, const std::string& filename, const std::string& metadata)
{
    std::ofstream file(filename.c_str(), std::ios::out | std::ios::binary);
    file.write(reinterpret_cast<const char*>(&img->data[0]), img->data.size());
    file.close();

    std::string metadata_filename = filename + ".txt";
    std::ofstream metadata_file(metadata_filename.c_str());
    metadata_file << metadata;
    metadata_file.close();
}

}  // namespace btcpp_ros2_project

#include "behaviortree_cpp/bt_factory.h"

BT_REGISTER_NODES(factory)
{
    factory.registerNodeType<btcpp_ros2_project::CaptureImageAction>("CaptureImage");
}

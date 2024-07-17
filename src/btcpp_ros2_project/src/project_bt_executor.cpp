#include <rclcpp/rclcpp.hpp>
#include <behaviortree_cpp_v3/bt_factory.h>
#include <behaviortree_cpp_v3/loggers/bt_cout_logger.h>
#include <behaviortree_cpp_v3/loggers/bt_file_logger.h>

class ProjectBTExecutor : public rclcpp::Node
{
public:
    ProjectBTExecutor()
    : Node("project_bt_executor")
    {
        // Behavior Tree factory
        BT::BehaviorTreeFactory factory;

        // Load behavior tree from XML file
        std::string xml_file;
        this->declare_parameter("bt_xml_file", "behavior_trees/inspection_tree.xml");
        this->get_parameter("bt_xml_file", xml_file);

        // Create the tree
        auto tree = factory.createTreeFromFile(xml_file);

        // Optional: Create a logger to visualize the tree
        BT::StdCoutLogger logger_cout(tree);
        BT::FileLogger logger_file(tree, "bt_trace.fbl");

        // Tick the tree repeatedly
        rclcpp::Rate rate(10);
        while (rclcpp::ok())
        {
            tree.tickRoot();
            rate.sleep();
        }
    }
};

int main(int argc, char **argv)
{
    rclcpp::init(argc, argv);
    auto node = std::make_shared<ProjectBTExecutor>();
    rclcpp::spin(node);
    rclcpp::shutdown();
    return 0;
}

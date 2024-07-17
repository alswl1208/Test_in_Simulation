import sys
import os
import numpy as np
from controller import Robot
# controllers 디렉토리의 경로를 추가
sys.path.append('/home/minji/my_study/webots_ros2_ld90/controllers')

#!/usr/bin/env python3
"""my_controller_salus controller."""

# 모듈 경로를 지정
module_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(module_path)

# You may need to import some classes of the controller module. Ex:
#  from controller import Robot, Motor, DistanceSensor


# ROS 2 관련 모듈 추가
#import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from cv_bridge import CvBridge

#import cv2
#from my_interfaces.action import CaptureImage

# ROS 2 노드 클래스 추가
class CameraNode(Node):
    def __init__(self):
        super().__init__('camera_node')
        self.publisher_ = self.create_publisher(Image, 'camera/image_raw', 10)
        self.bridge = CvBridge()
        # self.action_server = ActionServer(
        #     self,
        #     CaptureImage,
        #     'capture_image',
        #     self.execute_callback
        # )
        # self.current_image = None
        self.get_logger().info("CameraNode initialized and Action Server started")
    
    # def execute_callback(self, goal_handle):
    #     self.get_logger().info('Executing goal...')
        
    #     if self.current_image is None:
    #         goal_handle.abort()
    #         return CaptureImage.Result()

    #     # Save the image
    #     cv2.imwrite('captured_image.png', self.current_image)
        
    #     # Save metadata (Example: save robot's current position)
    #     metadata = {
    #         'position': 'example_position',  # Replace with actual position retrieval code
    #         'timestamp': rclpy.time.Time().to_msg()
    #     }
    #     with open('image_metadata.txt', 'w') as metadata_file:
    #         metadata_file.write(str(metadata))

    #     goal_handle.succeed()
    #     result = CaptureImage.Result()
    #     return result
    
    def publish_image(self, image):
        img_msg = self.bridge.cv2_to_imgmsg(image, "rgb8")
        self.publisher_.publish(img_msg)
        self.get_logger().info("Image published")  # 퍼블리시 로그

# ROS 2 노드 초기화
def main(args=None):
    rclpy.init(args=args)
    camera_node = CameraNode()
    camera_node.get_logger().info("Node initialized")

    # create the Robot instance.
    robot = Robot()

    # get the time step of the current world.
    timestep = int(robot.getBasicTimeStep())
    camera_node.get_logger().info("Robot instance created")


    # You should insert a getDevice-like function in order to get the
    # instance of a device of the robot. Something like:
    #  motor = robot.getDevice('motorname')
    #  ds = robot.getDevice('dsname')
    #  ds.enable(timestep)


    # initialise sensors - 360 camera
    camera_360 = robot.getDevice("360_camera")
    camera_360.enable(timestep)
    camera_node.get_logger().info("360 Camera enabled")
    # initialise sensors - depth camera (in MiR100)
    # camera_depth = robot.getDevice("depth_camera")
    # camera_depth.enable(timestep)

    # Main loop:
    # - perform simulation steps until Webots is stopping the controller
    while robot.step(timestep) != -1:
        # Read the sensors:
        image = np.array(camera_360.getImage(), dtype=np.uint8).reshape((camera_360.getHeight(), camera_360.getWidth(), 4))
        rgb_image = image[:, :, :3]  # Remove the alpha channel
        camera_node.publish_image(rgb_image)
        camera_node.get_logger().info("Image captured and published")

        # Enter here functions to read sensor data, like:
        #  val = ds.getValue()

        # Process sensor data here.

        # Enter here functions to send actuator commands, like:
        #  motor.setPosition(10.0)
    # Clean up
    rclpy.shutdown()  

# Enter here exit cleanup code.
if __name__ == '__main__':
    main()


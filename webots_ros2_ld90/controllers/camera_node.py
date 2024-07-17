import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from std_srvs.srv import Trigger
from cv_bridge import CvBridge
import cv2

class CameraNode(Node):
    def __init__(self):
        super().__init__('camera_node')
        self.subscription = self.create_subscription(
            Image,
            '/webots_ros2/camera',
            self.image_callback,
            10)
        self.br = CvBridge()
        self.latest_image = None
        self.service = self.create_service(Trigger, '/capture_image', self.capture_image_callback)

    def image_callback(self, msg):
        self.get_logger().info('Receiving video frame')
        self.latest_image = self.br.imgmsg_to_cv2(msg, "bgr8")

    def capture_image_callback(self, request, response):
        if self.latest_image is not None:
            filename = 'captured_image.jpg'
            cv2.imwrite(filename, self.latest_image)
            self.get_logger().info(f'Image saved: {filename}')
            response.success = True
            response.message = f'Image saved as {filename}'
        else:
            response.success = False
            response.message = 'No image available'
        return response

def main(args=None):
    rclpy.init(args=args)
    camera_node = CameraNode()
    rclpy.spin(camera_node)
    camera_node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
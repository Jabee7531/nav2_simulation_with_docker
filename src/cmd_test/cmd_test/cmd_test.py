# Copyright 2016 Open Source Robotics Foundation, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import rclpy
from rclpy.executors import ExternalShutdownException
from rclpy.node import Node


from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan


class CmdVelTest(Node):

    def __init__(self):
        super().__init__("cmd_vel_test_node")
        self.cmd_publisher_ = self.create_publisher(Twist, "/cmd_vel", 10)
        self.scan_subscription = self.create_subscription(
            LaserScan, "/scan", self.listener_callback, 10
        )

        timer_period = 0.5  # seconds
        self.timer = self.create_timer(timer_period, self.timer_callback)

        self.i = 1
        self.obstale_detect_flag = False

    def listener_callback(self, msg):
        # len(msg.ranges)
        self.get_logger().info(f"msg.ranges[100] : {msg.ranges[100]}")
        if msg.ranges[100] <= 0.2:
            self.get_logger().info(f"obstale_detect_flag : True")
            self.obstale_detect_flag = True
        else:
            self.get_logger().info(f"obstale_detect_flag : False")
            self.obstale_detect_flag = False

    def timer_callback(self):
        cmd_vel_msg = Twist()

        cmd_vel_msg.linear.x = 0.1 * self.i
        cmd_vel_msg.angular.z = 0.017  # 1도

        self.get_logger().info(f"전진속도 : {cmd_vel_msg.linear.x}")
        self.get_logger().info(f"각속도 : {cmd_vel_msg.angular.z}")

        if self.obstale_detect_flag == True:
            cmd_vel_msg.linear.x = 0.0
            cmd_vel_msg.angular.z = 0.0

        self.cmd_publisher_.publish(cmd_vel_msg)

        self.i *= -1


def main(args=None):
    try:
        rclpy.init(args=args)
        cmd_vel_test = CmdVelTest()

        rclpy.spin(cmd_vel_test)
    except (KeyboardInterrupt, ExternalShutdownException):
        pass


if __name__ == "__main__":
    main()

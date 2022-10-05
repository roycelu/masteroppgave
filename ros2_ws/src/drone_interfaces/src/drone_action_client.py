import random
from unittest import result

import rclpy
from rclpy.action import ActionClient
from rclpy.node import Node

from drone_interfaces.action import Drone


class DroneActionClient(Node):
    def __init__(self):
        super().__init__('drone_action_client')
        self._action_client = ActionClient(self, Drone, 'drone')

    def send_goal(self, pos):
        goal_msg = Drone.Goal()
        goal_msg.pos = pos

        self._action_client.wait_for_server()
        self._send_goal_future = self._action_client.send_goal_async(goal_msg)
        self._send_goal_future.add_done_callback(self.goal_response_callback)

    def goal_response_callback(self, future):
        goal_handle = future.result()

        if not goal_handle.accepted:
            self.get_logger().info('Goal rejected...')
            return
        self.get_logger().info('Goal accepted!')

        self._get_result_future = goal_handle.get_result_async()
        self._get_result_future.add_done_callback(self.get_result_callback)

    def get_result_callback(self, future):
        result = future.result().result
        self.get_logger().info('Result: {0}'.format(result.final_pos))
        rclpy.shutdown()    # Shutdown after receiving a result


def main(args=None):
    pos_x = random.random()*100
    pos_y = random.random()*100
    print("Position:", pos_x, pos_y)

    rclpy.init(args=args)
    action_client = DroneActionClient()
    action_client.send_goal([pos_x, pos_y])
    rclpy.spin(action_client)


if __name__ == '__main__':
    main()

import time

import rclpy
from rclpy.action import ActionServer
from rclpy.node import Node

from drone_interfaces.action import Drone


class DroneActionServer(Node):

    def __init__(self):
        super().__init__('drone_action_server')
        self._action_server = ActionServer(
            self,
            Drone,
            'drone',
            self.execute_callback)

    def execute_callback(self, goal_handle):
        self.get_logger().info('Executing goal...')

        feedback_msg = Drone.Feedback()
        feedback_msg.current_pos = [0.0, 1.0]   # Tentativ start posisjon

        n = 10  # Tentativ stegtall
        pos = goal_handle.request.pos

        for i in range(n):
            # Øker current_pos lineært med konstant speed
            feedback_msg.current_pos[0] += pos[0]/10
            feedback_msg.current_pos[1] += pos[1]/10
            self.get_logger().info('Feedback: {0}'.format(
                feedback_msg.current_pos))
            goal_handle.publish_feedback(feedback_msg)

        # final_position = [0.0, 0.0]
        # self.get_logger().info('Updating final position')   # Foreløpig kommentar
        # final_position = goal_handle.request.position

        goal_handle.succeed()
        result = Drone.Result()
        result.final_pos = feedback_msg.current_pos  # final_pos
        return result


def main(args=None):
    rclpy.init(args=args)
    drone_action_server = DroneActionServer()
    rclpy.spin(drone_action_server)


if __name__ == '__main__':
    main()

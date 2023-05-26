import pygame
import numpy as np
from constants import *

AWAY_TARGET_ACTION = 2000

class OurDroneCom:
    def __init__(self, id, initial_position):
        self.id = id
        self.figure = pygame.Rect(0, 0, SIZE, SIZE)
        self.position = initial_position
        self.velocity = pygame.Vector2(0, 0)
        
        self.steering_point_v = pygame.Vector2(0, 0)
        self.direction = 'right'
        self.current_position = 'left'
        self.collides_with_point = False
        self.theta = 0 # angle in degrees

        self.direction_index = 0  # 0:clockwise (right), 1:counterclockwise (left)
        self.right_pass = 0  # 0: otherwise, 1: pass z=0 by right flying to z=j
        self.left_pass = 0  # =. otherwise, 1: pass z=0 by left flying to z=j
        self.travel_path = []  # The path from start to steering point
        self.possible_allocations = []  # All possible steering points allocations
        self.edge_point = pygame.Vector2(0, 0)  # The first point on the edge
        self.steering_point = pygame.Vector2(0, 0)  # The final point to fly to
        self.steering_drive = 0

        self.dist1 = 0
        self.dist2 = 0
        self.dist3 = 0

        self.P_leftie = pygame.Vector2(0, 0)
        self.P_centerie = pygame.Vector2(0, 0)
        self.P_rightie = pygame.Vector2(0, 0)

    def draw(self, canvas, font):
        self.figure.center = self.position
        pygame.draw.rect(canvas, pygame.Color("black"), self.figure)

    def update(self, sheep, dt, target_fps):
        # Drone should not move faster than max speed
        if np.linalg.norm(self.velocity) > MAX_SPEED:
            self.velocity = self.velocity / np.linalg.norm(self.velocity) * MAX_SPEED

        # Move
        self.position += self.velocity * dt * target_fps

        # Reset velocity vector
        self.velocity = pygame.Vector2(0, 0)

    def fly_to_position(self, position):
        self.velocity = (position - self.position)

    def find_steering_point(self, sheep, goal, com, theta, canvas, dt, target_fps):
        goal = goal.position
        self.theta = theta

        # Radius from com to sheep furthest away
        d_furthest = 0
        for s in sheep:
            distance = np.linalg.norm(s.position-com)
            if distance > d_furthest:
                d_furthest = distance

        d_over = DESIRED_SEPARATION_SHEEP
        distance_from_com = d_furthest + d_over
    
        com_to_goal = pygame.Vector2(com - goal) 
        point = com + distance_from_com * (com_to_goal/com_to_goal.length())

        P_left = pygame.Vector2(0, 0)
        P_center = pygame.Vector2(0, 0)
        P_right = pygame.Vector2(0, 0)

        # Find correct points for this specific drone
        if self.id == 0:
            P_left = com + (point - com).rotate(theta)
            P_center = point
            P_right = com + (point - com).rotate(-theta)

        if self.id == 1:
            P_right = com + (point - com).rotate(theta)
            P_center = com + (point - com).rotate(2 * theta) 
            P_left = com + (point - com).rotate(3 * theta)

        if self.id == 2:
            P_left = com + (point - com).rotate(-theta)
            P_center = com + (point - com).rotate(2 * -theta) 
            P_right = com + (point - com).rotate(3 * -theta)

        pygame.draw.circle(canvas, color='orange', center=P_center, radius=2)
        pygame.draw.circle(canvas, color='purple', center=P_left, radius=2)
        pygame.draw.circle(canvas, color='blue', center=P_right, radius=2)
        
        # Fly between P_left -> P_center -> P_right -> ...
        if self.current_position == 'left' and self.figure.collidepoint(P_left):
            self.current_position = 'center'
            self.direction = 'right'
            self.steering_point_v = P_center
        if self.current_position == 'right' and self.figure.collidepoint(P_right):
            self.current_position = 'center'
            self.direction = 'left'
            self.steering_point_v = P_center
        if self.current_position == 'center' and self.figure.collidepoint(P_center) and self.direction == 'right':
            self.current_position = 'right'
            self.steering_point_v = P_right
        if self.current_position == 'center' and self.figure.collidepoint(P_center) and self.direction == 'left':
            self.current_position = 'left'
            self.steering_point_v = P_left
        if self.current_position == 'left' and not self.figure.collidepoint(P_left):
            self.steering_point_v = P_left
        if self.current_position == 'right' and not self.figure.collidepoint(P_right):
            self.steering_point_v = P_right
        if self.current_position == 'center' and not self.figure.collidepoint(P_center):
            self.steering_point_v = P_center

        # Update velocity
        self.velocity = self.steering_point_v - self.position
        self.update(sheep, dt, target_fps)



    def find_steering_point_gather_sheep(self, sheep_pos, com, theta, screen, sheep, dt, target_fps, shortest_points = []):
        d_over = DESIRED_SEPARATION_SHEEP
        self.theta = theta # angle set by test.py
        sheeppos_to_com = pygame.Vector2(sheep_pos - com) 

        if sheeppos_to_com.length() != 0:
            point = sheep_pos + d_over * (sheeppos_to_com/sheeppos_to_com.length())
        else:
            point = com + d_over

        P_left = pygame.Vector2(0, 0)
        P_center = pygame.Vector2(0, 0)
        P_right = pygame.Vector2(0, 0)

        # Find correct points for this specific drone
        if len(shortest_points) > 0:
            for drone_id in shortest_points:
                if drone_id == self.id:
                    side = shortest_points.index(drone_id)
                    if side == 0:
                        P_left = point
                        P_center = com + (point - com).rotate(theta)
                        P_right = com + (point - com).rotate(2 * theta)

                    if side == 1:
                        P_right = point
                        P_center = com + (point - com).rotate(-theta)
                        P_left = com + (point - com).rotate(2 * -theta)
        else:
            P_left = sheep_pos + (point - sheep_pos).rotate(theta)
            P_center = point
            P_right = sheep_pos + (point - sheep_pos).rotate(-theta)

        # Fly between P_left -> P_center -> P_right -> ...
        if self.current_position == 'left' and self.figure.collidepoint(P_left):
            self.current_position = 'center'
            self.direction = 'right'
            self.steering_point_v = P_center
        if self.current_position == 'right' and self.figure.collidepoint(P_right):
            self.current_position = 'center'
            self.direction = 'left'
            self.steering_point_v = P_center
        if self.current_position == 'center' and self.figure.collidepoint(P_center) and self.direction == 'right':
            self.current_position = 'right'
            self.steering_point_v = P_right
        if self.current_position == 'center' and self.figure.collidepoint(P_center) and self.direction == 'left':
            self.current_position = 'left'
            self.steering_point_v = P_left
        if self.current_position == 'left' and not self.figure.collidepoint(P_left):
            self.steering_point_v = P_left
        if self.current_position == 'right' and not self.figure.collidepoint(P_right):
            self.steering_point_v = P_right
        if self.current_position == 'center' and not self.figure.collidepoint(P_center):
            self.steering_point_v = P_center

        # Update velocity
        self.velocity = self.steering_point_v - self.position
        self.update(sheep, dt, target_fps)

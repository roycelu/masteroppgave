import pygame
import numpy as np
from constants import *


# SIZE = 10
# MAX_SPEED = 19
# MAX_SPEED_SHEEP = 0.003
# PERCEPTION = 100
# DESIRED_SEPARATION = 20


class PolygonDrone:
    def __init__(self, id, initial_position):
        self.id = id
        self.figure = pygame.Rect(0, 0, SIZE, SIZE)
        self.position = initial_position
        self.velocity = pygame.Vector2(0, 0)

        self.direction_index = 0  # 0:clockwise (right), 1:counterclockwise (left)
        self.right_pass = 0  # 0: otherwise, 1: pass z=0 by right flying to z=j
        self.left_pass = 0  # =. otherwise, 1: pass z=0 by left flying to z=j
        self.travel_path = []  # The path from start to steering point
        self.possible_allocations = []  # All possible steering points allocations
        self.edge_point = pygame.Vector2(0, 0)  # The first point on the edge
        self.steering_point = pygame.Vector2(0, 0)  # The final point to fly to
        self.steering_drive = 0
        
    def draw(self, canvas, font):
        self.figure.center = self.position
        pygame.draw.rect(canvas, pygame.Color("black"), self.figure)

    def update(self, sheep, dt, target_fps):    
        # Drone should not move faster than max speed
        if np.linalg.norm(self.velocity) > MAX_SPEED:
            self.velocity = self.velocity / np.linalg.norm(self.velocity) * MAX_SPEED

        # If the drone is close to the sheep, make sure the drone does not move faster than the sheep
        # for s in sheep:
        #     if (self.position-s.position).magnitude() <= (DESIRED_SEPARATION_SHEEP) and np.linalg.norm(self.velocity) != 0:
        #         self.velocity = self.velocity / np.linalg.norm(self.velocity) * MAX_SPEED_SHEEP
        
        # Move
        self.position += self.velocity * dt * target_fps

        # Reset velocity vector
        self.velocity = pygame.Vector2(0, 0)

    def move(self, goal, drones, sheep, canvas, dt, target_fps):
        self.update(sheep, dt, target_fps)

    def fly_to_position(self, position, sheep, dt, target_fps):
        self.velocity = (position - self.position)
        self.update(sheep, dt, target_fps)

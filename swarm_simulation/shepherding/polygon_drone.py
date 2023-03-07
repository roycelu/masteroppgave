import pygame
import numpy as np


SIZE = 8
STEP_SIZE = 500
PERCEPTION = 100
DESIRED_SEPARATION = 20
S_WEIGHT = 10


class PolygonDrone:
    def __init__(self, id, initial_position):
        self.id = id
        self.max_speed = 2
        self.figure = pygame.Rect(0, 0, SIZE, SIZE)
        self.position = initial_position
        self.goal_position = pygame.Vector2(0, 0)
        self.velocity = pygame.Vector2(0.5, 0.5)
        self.acceleration = pygame.Vector2(0, 0)

        # 0: clockwise (right), 1: counterclockwise (left)
        self.direction_index = 0  # 0:clockwise, 1:counterclockwise
        self.right_pass = 0  # 0: otherwise, 1: pass z=0 by right flying to z=j
        self.left_pass = 0  # =. otherwise, 1: pass z=0 by left flying to z=j
        self.travel_path = []  # The path from start to steering point
        self.possible_allocations = []  # All possible steering points allocations
        self.edge_point = pygame.Vector2(0, 0)  # The first point on the edge
        self.steering_point = pygame.Vector2(0, 0)  # The final point to fly to

    def draw(self, canvas, font):
        self.figure.center = self.position
        pygame.draw.rect(canvas, pygame.Color("black"), self.figure)

        label = font.render(str(self.id), True, pygame.Color("white"))
        label_rect = label.get_rect()
        label_rect.center = self.position
        canvas.blit(label, label_rect)

    def update(self):
        self.position += self.velocity
        self.velocity += self.acceleration
        if self.velocity.magnitude() > self.max_speed:
            self.velocity = self.velocity / self.velocity.magnitude() * self.max_speed
        self.acceleration = pygame.Vector2(0, 0)

    def move(self, goal, drones, sheep):
        if self.figure.colliderect(goal.figure):
            print("{id} is within the goal".format(id="drone" + str(self.id)))

        separation = self.separation(drones)
        self.acceleration += separation * S_WEIGHT

        self.update()

    def separation(self, drones):
        """The drone avoid colliding with each other"""
        steering = pygame.Vector2(0, 0)
        for drone in drones:
            distance = drone.position - self.position
            if self != drone and distance.magnitude() < DESIRED_SEPARATION:
                steering -= distance
        return steering

    def fly_to_position(self, position):
        self.goal_position = position
        self.acceleration = (position - self.position) * (STEP_SIZE / 100)

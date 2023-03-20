import pygame
import numpy as np


SIZE = 8
STEP_SIZE = 200
PERCEPTION = 100
DESIRED_SEPARATION = 20
S_WEIGHT = 10



class PolygonDrone:
    def __init__(self, id, initial_position):
        self.id = id
        self.max_speed = 19 # Endrer hastigheten når dronene skal støte sauene
        self.figure = pygame.Rect(0, 0, SIZE, SIZE)
        self.position = initial_position
        self.velocity = pygame.Vector2(0.5, 0.5)
        self.acceleration = pygame.Vector2(0, 0)

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

        label = font.render(str(self.id), True, pygame.Color("white"))
        label_rect = label.get_rect()
        label_rect.center = self.position
        canvas.blit(label, label_rect)

    def update(self, dt, target_fps):
        acceleration_distance = np.linalg.norm(self.acceleration)
        if acceleration_distance > self.max_speed:
            self.acceleration = self.acceleration / acceleration_distance * self.max_speed
        #if (self.position-com).magnitude() <= (flock_radius + DESIRED_SEPARATION_SHEEP):
        #    self.acceleration = self.acceleration / acceleration_distance * MAX_SPEED_SHEEP # Mindre enn hastigheten til sauene (enn så lenge bare makshastigheten til sauene)
        print(self.acceleration)
        self.position += self.acceleration * dt * target_fps
        # self.position += self.velocity
        # self.velocity += self.acceleration
        # if self.velocity.magnitude() > self.max_speed:
        #     self.velocity = self.velocity / self.velocity.magnitude() * self.max_speed
        # self.acceleration = pygame.Vector2(0, 0)

    def move(self, goal, drones, sheep, goal_vector, canvas, dt, target_fps):
        separation = self.separation(drones)
        self.acceleration += separation * S_WEIGHT

        self.update(dt, target_fps)

    def separation(self, drones):
        """The drone avoid colliding with each other"""
        steering = pygame.Vector2(0, 0)
        for drone in drones:
            distance = drone.position - self.position
            if self != drone and distance.magnitude() < DESIRED_SEPARATION:
                steering -= distance
        return steering

    def fly_to_position(self, position):
        self.acceleration = (position - self.position) #* (STEP_SIZE / 100)

    # def fly(self, speed, point):
    #     # TODO: implementere som en del av dronen? Formel (18) og (19)
    #     speed = speed.normalize()
    #     F = pygame.Vector2(0, 0)
    #     g = 1
    #     f = point - (speed.dot(point)) * speed

    #     if f != 0:
    #         F = pygame.Vector2(f / f.length())
    #     if speed.dot(point) <= 0:
    #         g = -1
        
    #     self.acceleration = MAX_ACCELERATION * g * F
    #     self.velocity = pygame.Vector2(self.max_speed * g)

    #     print(self.acceleration)

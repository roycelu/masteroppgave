import pygame
import numpy as np


SIZE = 8
MAX_SPEED = 19 # m/s
MAX_SPEED_SHEEP = 0.003 # m/s
STEP_SIZE = 200
PERCEPTION = 100
DESIRED_SEPARATION = 20


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

        label = font.render(str(self.id), True, pygame.Color("white"))
        label_rect = label.get_rect()
        label_rect.center = self.position
        canvas.blit(label, label_rect)

    def update(self, sheep, dt, target_fps):
        velocity_distance = np.linalg.norm(self.velocity)
        if velocity_distance > MAX_SPEED:
            self.velocity = self.velocity / velocity_distance * MAX_SPEED

        # for s in sheep:
        #     if (self.position-s.position).magnitude() <= (DESIRED_SEPARATION):
        #         self.velocity = self.velocity / velocity_distance * MAX_SPEED_SHEEP
        
        self.position += self.velocity * dt * target_fps
        self.velocity = pygame.Vector2(0, 0)

    def move(self, goal, drones, sheep, canvas, dt, target_fps):
        # self.fly_to_position(self.steering_point)
        self.update(sheep, dt, target_fps)

    def fly_to_position(self, position):
        # self.steering_point = position
        self.velocity = (position - self.position) * (STEP_SIZE / 100)


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
        
    #     self.velocity = MAX_ACCELERATION * g * F
    #     self.velocity = pygame.Vector2(MAX_SPEED * g)

    #     print(self.velocity)

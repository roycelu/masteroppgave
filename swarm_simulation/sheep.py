import math
import random
import pygame
from sklearn.neighbors import NearestNeighbors


""" Logic for the sheep - algorithm? flocking behaviour """


def points2vector(pos, tar):
    print("VECTOR--------------")
    return pygame.Vector2(pos)-pygame.Vector2(tar)


def distance(tar, pos):
    dx = tar[0]-pos[0]
    dy = tar[1]-pos[1]
    return (dx**2+dy**2)**0.5


class Sheep:
    def __init__(self, id):
        # Colour, size, speed, direction, position etc.
        self.id = id
        self.x = random.randint(0, 50)
        self.y = random.randint(0, 50)
        self.size = 10
        self.target = pygame.Vector2(self.x+5, self.y+5)
        self.position = pygame.Vector2(self.x, self.y)
        self.grazingVector = pygame.Vector2()

    def graze(self, dt):
        # Separation
        if distance(self.target, self.position) < 10:
            MOVEMENT_DISTANCE = random.randint(0, 1)
            MOVEMENT_DIRECTION = random.randint(0, 360)
            self.target = (self.x + MOVEMENT_DISTANCE * math.cos(MOVEMENT_DIRECTION),
                           self.y + MOVEMENT_DISTANCE * math.sin(MOVEMENT_DIRECTION))
            self.grazingVector = points2vector(self.position, self.target)
            # self.grazingVector = pygame.Vector2(self.position, self.target)
            if self.grazingVector.magnitude() > 0:
                self.grazingVector.scale_to_length(1)
        self.direction = math.atan2(self.grazingVector.y, self.grazingVector.x)
        self.speed = self.grazingVector.magnitude()

        self.x += math.cos(self.direction) * self.speed * dt
        self.y += math.sin(self.direction) * self.speed * dt
        self.position = (self.x, self.y)

        print(self.id, self.position)

    # def move(self, shepered, dt):

    def move(self, dt):
        # Movement for the sheep, flocking behaviour
        self.graze(dt)

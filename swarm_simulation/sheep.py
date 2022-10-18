import math
import pygame
import random


class sheep:
    def __init__(self, id):
        pass

    def graze(self, dt):
        if distance(self.target, self.position) < 10:
            MOVEMENT_DISTANCE = random.randint(0, 50)
            MOVEMENT_DIRECTION = random.randint(0, 360)
            self.target = (self.x + MOVEMENT_DISTANCE * math.cos(MOVEMENT_DIRECTION),
                           self.y + MOVEMENT_DISTANCE * math.sin(MOVEMENT_DIRECTION))
            self.grazingVector = points2vector(self.position, self.target)

            if self.grazingVector.magnitude() > 0:
                self.grazingVector.scale_to_length(1)

        self.direction = math.atan2(self.grazingVector.y, self.grazingVector.x)
        self.speed = self.grazingVector.magnitude()

        self.x += math.cos(self.direction) * self.speed * dt
        self.y += math.sin(self.direction) * self.speed * dt
        self.position = (self.x, self.y)

    def move(self, shepered, dt):
        self.graze(dt)

    # Vector: v = pygame.Vector2()

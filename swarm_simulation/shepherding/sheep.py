import pygame
import math
import numpy as np

"""
Code inspired by https://betterprogramming.pub/boids-simulating-birds-flock-behavior-in-python-9fff99375118
"""

radius = 10
a_weight = 5
c_weight = 30
s_weight = 50


class Sheep:
    def __init__(self, id, initial_position):
        self.id = id
        self.position = initial_position
        self.velocity = pygame.Vector2(
            (np.random.random(1) - 0.5) * 10, (np.random.random(1) - 0.5) * 10
        )
        self.acceleration = pygame.Vector2(
            (np.random.random(1) - 0.5) / 2, (np.random.random(1) - 0.5) / 2
        )
        self.max_speed = 2
        self.max_force = 0.1
        self.horizon = 100
        self.desired_separation = 10

    def draw(self, canvas, font):
        pygame.draw.circle(canvas, pygame.Color("white"), self.position, radius)
        label = font.render(str(self.id), True, pygame.Color("black"))
        rect = label.get_rect()
        rect.center = self.position
        canvas.blit(label, rect)

    def update(self):
        self.position += self.velocity
        self.velocity += self.acceleration
        if self.velocity.magnitude() > self.max_speed:
            self.velocity = self.velocity / self.velocity.magnitude() * self.max_speed
        self.acceleration = pygame.Vector2(0, 0)

    def move(self, sheeps):
        alignment = self.alignment(sheeps)
        cohesion = self.cohesion(sheeps)
        separation = self.separation(sheeps)

        self.acceleration += alignment * a_weight
        self.acceleration += cohesion * c_weight
        self.acceleration += separation * s_weight

        self.update()

    def alignment(self, sheeps):
        total = 0
        steering = pygame.Vector2(0, 0)
        average = pygame.Vector2(0, 0)
        for sheep in sheeps:
            if (sheep.position - self.position).magnitude() < self.horizon:
                average += sheep.velocity
                total += 1
        if total > 0:
            average /= total
            average = (average / average.magnitude()) * self.max_speed
            steering = average - self.velocity
        return steering

    def cohesion(self, sheeps):
        total = 0
        steering = pygame.Vector2(0, 0)
        center_of_mass = pygame.Vector2(0, 0)
        for sheep in sheeps:
            if (sheep.position - self.position).magnitude() < self.horizon:
                center_of_mass += sheep.position
                total += 1
        if total > 0:
            center_of_mass /= total
            vector = center_of_mass - self.position
            if vector.magnitude() > 0:
                vector = (vector / vector.magnitude()) * self.max_speed
            steering = vector - self.velocity
            if steering.magnitude() > self.max_force:
                steering = (steering / steering.magnitude()) * self.max_force
        return steering

    def separation(self, sheeps):
        total = 0
        steering = pygame.Vector2(0, 0)
        average = pygame.Vector2(0, 0)
        for sheep in sheeps:
            distance = (sheep.position - self.position).magnitude()
            if self != sheep and distance < self.horizon:
                average += (self.position - sheep.position) / distance
                total += 1
        if total > 0:
            average /= total
            if steering.magnitude() > 0:
                average = (average / steering.magnitude()) * self.max_speed
            steering = average - self.velocity
            if steering.magnitude() > self.max_force:
                steering = (steering / steering.magnitude()) * self.max_force
        return steering

import pygame
import numpy as np

"""
Code based on Kubo et al. A-sheep from "Herd guidance by multiple sheepdog agents with repulsive force".
"""

SIZE = 3
MAX_SPEED = 1
GRAZE_SPEED = 0.2
PERCEPTION = 30
GRAZE_PERCEPTION = 50
A_WEIGHT = 0.5
C_WEIGHT = 2
S_WEIGHT = 10
DRONE_SEPARATION = 5000


class Sheep:
    def __init__(self, id, initial_position):
        self.id = id
        self.figure = pygame.Rect(0, 0, SIZE * 2, SIZE * 2)
        self.position = initial_position
        self.acceleration = pygame.Vector2(
            (np.random.random(1) - 0.5) / 2, (np.random.random(1) - 0.5) / 2
        )

    def draw(self, canvas, font):
        self.figure.center = self.position
        pygame.draw.rect(
            canvas,
            pygame.Color("white"),
            self.figure,
            border_radius=int(SIZE),
        )

        label = font.render(str(self.id), True, pygame.Color("black"))
        rect = label.get_rect()
        rect.center = self.position
        canvas.blit(label, rect)

    def update(self, drones, dt, target_fps):
        acceleration_distance = np.linalg.norm(self.acceleration)
        if (self.position-drones[0].position).magnitude() <= GRAZE_PERCEPTION or (self.position-drones[1].position).magnitude() <= GRAZE_PERCEPTION or (self.position-drones[2].position).magnitude() <= GRAZE_PERCEPTION:
            self.acceleration = self.acceleration / acceleration_distance * MAX_SPEED
        else:
            self.acceleration = self.acceleration / acceleration_distance * GRAZE_SPEED

        self.position += self.acceleration * dt * target_fps

    def move(self, goal, sheep, drones, dt, target_fps):
        alignment = self.alignment(sheep)
        cohesion = self.cohesion(sheep)
        separation = self.separation(sheep)
        escape = self.escape(drones)  # Move away from predators

        self.acceleration += alignment * A_WEIGHT
        self.acceleration += cohesion * C_WEIGHT
        self.acceleration += separation * S_WEIGHT
        self.acceleration += escape * DRONE_SEPARATION

        self.update(drones, dt, target_fps)

        if self.figure.colliderect(goal.figure):
            #print("{id} reached the goal".format(id="sheep" + str(self.id)))
            return True
            


    def separation(self, sheep):
        total = pygame.Vector2(0, 0)
        for s in sheep:
            distance = self.position-s.position
            if self != s and distance.magnitude() < PERCEPTION and (np.linalg.norm(distance) != 0):
                separation = distance / (np.linalg.norm(self.position-s.position))**2
                total += separation
        total /= len(sheep)
        return total
    
    def alignment(self, sheep):
        total = pygame.Vector2(0, 0)
        for s in sheep:
            distance = self.position-s.position
            if self != s and distance.magnitude() < PERCEPTION:
                alignment = s.acceleration / np.linalg.norm(s.acceleration)
                total += alignment
        total /= len(sheep)
        return total

    def cohesion(self, sheep):
        total = pygame.Vector2(0, 0)
        for s in sheep:
            distance = self.position-s.position
            if self != s and distance.magnitude() < PERCEPTION and (np.linalg.norm(distance) != 0):
                cohesion = distance / np.linalg.norm(self.position-s.position)
                total += cohesion
        total /= len(sheep)
        total *= (-1)
        return total
    
    def escape(self, drones):
        total = pygame.Vector2(0, 0)
        for drone in drones:
            distance = self.position-drone.position
            if distance.magnitude() < PERCEPTION:
                separation = distance / (np.linalg.norm(self.position-drone.position))**3
                total += separation
        total /= len(drones)
        return total


import pygame
import numpy as np

"""
Code based on Kubo et al. A-sheep from "Herd guidance by multiple sheepdog agents with repulsive force".
"""

SIZE = 3
MAX_SPEED = 0.277
GRAZE_SPEED = 0.013
GRAZE_PERCEPTION = 30
A_WEIGHT = 0.5
C_WEIGHT = 2
S_WEIGHT = 10
DRONE_SEPARATION = 5000


class Sheep:
    def __init__(self, id, initial_position, perception):
        self.id = id
        self.figure = pygame.Rect(0, 0, SIZE * 2, SIZE * 2)
        self.perception = perception
        self.position = initial_position
        self.velocity = pygame.Vector2(0.1,0.1)
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

    def update(self, drones, dt, target_fps):
        self.velocity += self.acceleration * dt * target_fps

        # Make sure sheep doesn't move faster than max speed
        velocity_distance = np.linalg.norm(self.velocity)
        if (self.position-drones[0].position).magnitude() <= GRAZE_PERCEPTION or (self.position-drones[1].position).magnitude() <= GRAZE_PERCEPTION or (self.position-drones[2].position).magnitude() <= GRAZE_PERCEPTION:
            self.velocity = self.velocity / velocity_distance * MAX_SPEED
        else:
            self.velocity = self.velocity / velocity_distance * GRAZE_SPEED

        self.position += self.velocity * dt * target_fps
        self.acceleration = pygame.Vector2(0,0)

    def move(self, goal, sheep, drones, dt, target_fps):
        # Find forces acting on sheep
        alignment = self.alignment(sheep)
        cohesion = self.cohesion(sheep)
        separation = self.separation(sheep)
        escape = self.escape(drones)  # Move away from predators

        # Update acceleration
        self.acceleration += alignment * A_WEIGHT
        self.acceleration += cohesion * C_WEIGHT
        self.acceleration += separation * S_WEIGHT
        self.acceleration += escape * DRONE_SEPARATION

        self.update(drones, dt, target_fps)

        if self.figure.colliderect(goal.figure):
            return True
            
    def separation(self, sheep):
        # Sheep should move away from other sheep to avoid collisions
        total = pygame.Vector2(0, 0)
        for s in sheep:
            distance = self.position-s.position
            if self != s and distance.magnitude() < self.perception and (np.linalg.norm(distance) != 0):
                separation = distance / (np.linalg.norm(self.position-s.position))**2
                total += separation
        total /= len(sheep)
        return total
    
    def alignment(self, sheep):
        # Sheep should move in same direction as other sheep in close proximity
        total = pygame.Vector2(0, 0)
        for s in sheep:
            distance = self.position-s.position
            if self != s and distance.magnitude() < self.perception and s.velocity != 0 and np.linalg.norm(distance) != 0:
                alignment = s.velocity / np.linalg.norm(s.velocity)
                total += alignment
        total /= len(sheep)
        return total

    def cohesion(self, sheep):
        # Sheep should move together with the flock
        total = pygame.Vector2(0, 0)
        for s in sheep:
            distance = self.position-s.position
            if self != s and distance.magnitude() < self.perception and (np.linalg.norm(distance) != 0):
                cohesion = distance / np.linalg.norm(self.position-s.position)
                total += cohesion
        total /= len(sheep)
        total *= (-1)
        return total
    
    def escape(self, drones):
        # Sheep should move away from drones
        total = pygame.Vector2(0, 0)
        for drone in drones:
            distance = self.position-drone.position
            if distance.magnitude() < GRAZE_PERCEPTION and np.linalg.norm(distance) != 0:
                separation = distance / (np.linalg.norm(self.position-drone.position))**3
                total += separation
        total /= len(drones)
        return total


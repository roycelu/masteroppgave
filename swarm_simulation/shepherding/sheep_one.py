import pygame
import numpy as np

"""
Code based on Kubo et al. A-sheep from "Herd guidance by multiple sheepdog agents with repulsive force".
"""

SIZE = 3
MAX_SPEED = 2.77
GRAZE_SPEED = 0.13 # m/s 
PERCEPTION = 40
GRAZE_PERCEPTION = 50
A_WEIGHT = 0.5
C_WEIGHT = 2
S_WEIGHT = 10
DRONE_SEPARATION = 5000


class SheepOne:
    def __init__(self, id, initial_position):
        self.id = id
        self.figure = pygame.Rect(0, 0, SIZE * 2, SIZE * 2)
        self.position = initial_position
        self.velocity = pygame.Vector2(
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
        velocity_distance = np.linalg.norm(self.velocity)
        if (self.position-drones[0].position).magnitude() <= GRAZE_PERCEPTION or (self.position-drones[1].position).magnitude() <= GRAZE_PERCEPTION or (self.position-drones[2].position).magnitude() <= GRAZE_PERCEPTION:
            self.velocity = self.velocity / velocity_distance * MAX_SPEED
        else:
            self.velocity = self.velocity / velocity_distance * GRAZE_SPEED

        self.position += self.velocity * dt * target_fps

    def move(self, goal, sheep, drones, dt, target_fps):
        closest_sheep_distance = np.inf
        closest_sheep = None
        for s in sheep:
            distance = np.linalg.norm(s.position - self.position)
            if s != self and distance != 0 and distance < closest_sheep_distance:
                closest_sheep_distance = distance
                closest_sheep = s

        alignment = self.alignment(closest_sheep)
        cohesion = self.cohesion(closest_sheep)
        separation = self.separation(closest_sheep)
        escape = self.escape(drones)  # Move away from predators

        self.velocity += alignment * A_WEIGHT
        self.velocity += cohesion * C_WEIGHT
        self.velocity += separation * S_WEIGHT
        self.velocity += escape * DRONE_SEPARATION

        self.update(drones, dt, target_fps)

        if self.figure.colliderect(goal.figure):
            #print("{id} reached the goal".format(id="sheep" + str(self.id)))
            return True
            


    def separation(self, sheep):

        distance = self.position-sheep.position
        if distance.magnitude() < PERCEPTION:
            separation = distance / (np.linalg.norm(distance))**2
            return separation
        else:
            return pygame.Vector2(0,0)
       
    
    def alignment(self, sheep):
        distance = self.position-sheep.position
        if distance.magnitude() < PERCEPTION:
            alignment = sheep.velocity / np.linalg.norm(sheep.velocity)
            alignment *= (-1)
            return alignment
        else:
            return pygame.Vector2(0,0)


    def cohesion(self, sheep):
        distance = self.position-sheep.position
        if distance.magnitude() < PERCEPTION:
            cohesion = distance / np.linalg.norm(distance)
            return cohesion
        else:
            return pygame.Vector2(0,0)

    
    def escape(self, drones):
        total = pygame.Vector2(0, 0)
        for drone in drones:
            distance = self.position-drone.position
            if distance.magnitude() < PERCEPTION:
                separation = distance / (np.linalg.norm(self.position-drone.position))**3
                total += separation
        total /= len(drones)
        return total


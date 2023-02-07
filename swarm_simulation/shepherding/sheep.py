import pygame
import numpy as np

"""
Code inspired by https://betterprogramming.pub/boids-simulating-birds-flock-behavior-in-python-9fff99375118
"""

SIZE = 1
MAX_SPEED = 1.5
MAX_FORCE = 0.2
PERCEPTION = 20
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

    def update(self):
        acceleration_distance = np.linalg.norm(self.acceleration)
        if acceleration_distance > MAX_SPEED:
            self.acceleration = self.acceleration / acceleration_distance * MAX_SPEED
        self.position += self.acceleration

    def move(self, goal, sheep, drones):
        alignment = self.alignment(sheep)
        cohesion = self.cohesion(sheep)
        separation = self.separation(sheep)
        escape = self.escape(drones)  # Move away from predators

        self.acceleration += alignment * A_WEIGHT
        self.acceleration += cohesion * C_WEIGHT
        self.acceleration += separation * S_WEIGHT
        self.acceleration += escape * DRONE_SEPARATION

        self.update()

        if self.figure.colliderect(goal.figure):
            # print("{id} reached the goal".format(id="sheep" + str(self.id)))
            pass


    def separation(self, sheep):
        total = pygame.Vector2(0, 0)
        for s in sheep:
            distance = self.position-s.position
            if self != s and distance.magnitude() < PERCEPTION:
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
            if self != s and distance.magnitude() < PERCEPTION:
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

    """
    def cohesion(self, sheeps):
            #The sheep move together as a flock
            total = 0
            steering = pygame.Vector2(0, 0)
            center_of_mass = pygame.Vector2(0, 0)
            for sheep in sheeps:
                if (sheep.position - self.position).magnitude() < PERCEPTION:
                    center_of_mass += sheep.position
                    total += 1
            if total > 0:
                center_of_mass /= total
                vector = center_of_mass - self.position
                if vector.magnitude() > 0:
                    vector = (vector / vector.magnitude()) * MAX_SPEED
                steering = vector - self.velocity
                if steering.magnitude() > MAX_FORCE:
                    steering = (steering / steering.magnitude()) * MAX_FORCE
            return steering

    def alignment(self, sheeps):
        #The sheep orient themselves toward each other
        total = 0
        steering = pygame.Vector2(0, 0)
        average = pygame.Vector2(0, 0)
        for sheep in sheeps:
            if (sheep.position - self.position).magnitude() < PERCEPTION:
                average += sheep.velocity
                total += 1
        if total > 0:
            average /= total
            average = (average / average.magnitude()) * MAX_SPEED
            steering = average - self.velocity
        return steering

    def separation(self, sheeps):
            #The sheep avoid colliding with each other
            total = 0
            steering = pygame.Vector2(0, 0)
            average = pygame.Vector2(0, 0)
            for sheep in sheeps:
                distance = sheep.position - self.position
                if self != sheep and distance.magnitude() < PERCEPTION:
                    average += (self.position - sheep.position) / distance.magnitude()
                    total += 1
            if total > 0:
                average /= total
                if steering.magnitude() > 0:
                    average = (average / steering.magnitude()) * MAX_SPEED
                steering = average - self.velocity
                if steering.magnitude() > MAX_FORCE:
                    steering = (steering / steering.magnitude()) * MAX_FORCE
            return steering

    

    def escape(self, drones):
        #The sheep flee from the predators (custom)
        steering = pygame.Vector2(0, 0)
        for drone in drones:
            distance = drone.position - self.position
            if distance.magnitude() < DRONE_SEPARATION:
                # steering -= distance
                steering = distance / distance.magnitude()
        return steering
    """
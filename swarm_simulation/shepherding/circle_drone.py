import pygame
import numpy as np
from utils import Calculate


SIZE = 10
MAX_SPEED = 19 #m/s
MAX_SPEED_SHEEP = 0.003 #  m/s
DESIRED_SEPARATION_SHEEP = 20
PERCEPTION = 100

CHASE_ACTION = 10
AWAY_TARGET_ACTION = 200
AWAY_GOAL = 8
REPULSION = 3000


class CircleDrone:
    def __init__(self, id, initial_position):
        self.id = id
        self.figure = pygame.Rect(0, 0, SIZE, SIZE)
        self.position = initial_position
        self.velocity = pygame.Vector2(0, 0)

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
           
        for s in sheep:
            if (self.position-s.position).magnitude() <= (DESIRED_SEPARATION_SHEEP):
                self.velocity = self.velocity / velocity_distance * MAX_SPEED_SHEEP

        self.position += self.velocity * dt * target_fps

        self.velocity = pygame.Vector2(0, 0)


    def move(self, goal, drones, sheep, canvas, dt, target_fps):
        com = Calculate.center_of_mass(sheep)

        flock_radius = 0
        furthest_from_goal = 0 
        target = 0
        for s in sheep:
            distance = np.linalg.norm(s.position-com)
            if distance > flock_radius:
                flock_radius = distance
            distance_goal = np.linalg.norm(s.position-goal.position)
            if distance_goal > furthest_from_goal:
                furthest_from_goal = distance_goal
                target = s
   
        chase_action = self.chase(target)
        stay_away_action = self.stay_away_target(target)
        stay_away_goal = self.move_to_goal(goal.position)
        repulsion = self.separation(drones, target)
        
        self.velocity += chase_action * CHASE_ACTION
        self.velocity += stay_away_action * AWAY_TARGET_ACTION
        self.velocity += stay_away_goal * AWAY_GOAL
        self.velocity += repulsion * REPULSION

        self.update(sheep, dt, target_fps)


    def chase(self, target):
        return -((self.position-target.position) / np.linalg.norm(self.position - target.position))
    
    def stay_away_target(self, target):
        return (self.position-target.position) / (np.linalg.norm(self.position - target.position))**3

    def move_to_goal(self, goal):
        return ((self.position - goal) / np.linalg.norm(self.position - goal))
    
    def separation(self, drones, target):
        repulsion = pygame.Vector2(0, 0)
        for drone in drones:
            distance = np.linalg.norm(self.position - drone.position)
            if drone != self and distance < PERCEPTION and distance != 0:
                repulsion += ((self.position - drone.position) / (np.linalg.norm(self.position - drone.position))**3)
        repulsion /= len(drones)
        return repulsion

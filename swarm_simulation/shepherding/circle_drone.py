import pygame
import numpy as np
from sympy import *

SIZE = 10
MAX_SPEED = 3
MAX_SPEED_SHEEP = 1.5
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
        self.acceleration = pygame.Vector2(0, 0)

    def draw(self, canvas, font):
        self.figure.center = self.position
        pygame.draw.rect(canvas, pygame.Color("black"), self.figure)

        label = font.render(str(self.id), True, pygame.Color("white"))
        label_rect = label.get_rect()
        label_rect.center = self.position
        canvas.blit(label, label_rect)

    def update(self, sheep):

        acceleration_distance = np.linalg.norm(self.acceleration)
        if acceleration_distance > MAX_SPEED:
            self.acceleration = self.acceleration / acceleration_distance * MAX_SPEED
           
        for s in sheep:
            if (self.position-s.position).magnitude() <= (DESIRED_SEPARATION_SHEEP):
                self.acceleration = self.acceleration / acceleration_distance * MAX_SPEED_SHEEP

        self.position += self.acceleration

        

    def move(self, goal, drones, sheep, goal_vector, canvas):
        if self.figure.colliderect(goal.figure):
            self.goal_status = True

        com = pygame.Vector2(0, 0)
        for s in sheep:
            com += s.position
        com /= len(sheep)
        flock_radius = 0
        furthest_from_goal = 0 
        target = 0
        for s in sheep:
            distance = np.linalg.norm(s.position-com)
            if distance > flock_radius:
                flock_radius = distance
            distance_goal = np.linalg.norm(s.position-goal_vector)
            if distance_goal > furthest_from_goal:
                furthest_from_goal = distance_goal
                target = s

        
   
        chase_action = self.chase(target)
        stay_away_action = self.stay_away_target(target)
        stay_away_goal = self.move_to_goal(goal_vector)
        repulsion = self.separation(drones, target)
        
        self.acceleration += chase_action * CHASE_ACTION
        self.acceleration += stay_away_action * AWAY_TARGET_ACTION
        self.acceleration += stay_away_goal * AWAY_GOAL
        self.acceleration += repulsion * REPULSION
        

        self.update(sheep)

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

 
import pygame
import numpy as np
from utils import Calculate
from constants import *

CHASE_ACTION = 10
AWAY_TARGET_ACTION = 200
AWAY_GOAL = 8
REPULSION = 6000


class CircleDrone:
    def __init__(self, id, initial_position):
        self.id = id
        self.figure = pygame.Rect(0, 0, SIZE, SIZE)
        self.position = initial_position
        self.velocity = pygame.Vector2(0.1, 0.1)
        self.acceleration = pygame.Vector2(0, 0)

    def draw(self, canvas, font):
        self.figure.center = self.position
        pygame.draw.rect(canvas, pygame.Color("black"), self.figure)

    def update(self, sheep, dt, target_fps):
        self.velocity += self.acceleration * dt * target_fps

        # Make sure drones do not move faster than max speed
        if np.linalg.norm(self.velocity) > MAX_SPEED:
            self.velocity = self.velocity / np.linalg.norm(self.velocity) * MAX_SPEED
        
        # If the drones are in close proximity to sheep they should not move faster than the sheep
        for s in sheep:
            if (self.position-s.position).magnitude() <= (DESIRED_SEPARATION_SHEEP):
                self.velocity = self.velocity / np.linalg.norm(self.velocity) * MAX_SPEED_SHEEP

        # Move
        self.position += self.velocity * dt * target_fps

        # Reset velocity and acceleration
        self.velocity = pygame.Vector2(0, 0)
        self.acceleration = pygame.Vector2(0, 0)


    def move(self, goal, drones, sheep, canvas, dt, target_fps):
        com = Calculate.center_of_mass(sheep)

        # Find the sheep furthest from the center of mass
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

        # Find forces acting on the drone
        chase_action = self.chase(target)
        stay_away_action = self.stay_away_target(target)
        stay_away_goal = self.move_to_goal(goal.position)
        repulsion = self.separation(drones, target)
        
        # Update acceleration
        self.acceleration += chase_action * CHASE_ACTION
        self.acceleration += stay_away_action * AWAY_TARGET_ACTION
        self.acceleration += stay_away_goal * AWAY_GOAL
        self.acceleration += repulsion * REPULSION

        self.update(sheep, dt, target_fps)


    def chase(self, target):
        # Chase the sheep
        return -((self.position-target.position) / np.linalg.norm(self.position - target.position))
    
    def stay_away_target(self, target):
        # Don't crash into sheep
        return (self.position-target.position) / (np.linalg.norm(self.position - target.position))**3

    def move_to_goal(self, goal):
        # Herd sheep towards goal
        return ((self.position - goal) / np.linalg.norm(self.position - goal))
    
    def separation(self, drones, target):
        # Stay away from other drones to avoid crashing with them
        repulsion = pygame.Vector2(0, 0)
        for drone in drones:
            distance = np.linalg.norm(self.position - drone.position)
            if drone != self and distance < PERCEPTION and distance != 0:
                repulsion += ((self.position - drone.position) / (np.linalg.norm(self.position - drone.position))**3)
        repulsion /= len(drones)
        return repulsion

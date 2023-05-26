import pygame
import numpy as np
from utils import Calculate
from constants import *


class VDrone:
    def __init__(self, id, initial_position):
        self.id = id
        self.figure = pygame.Rect(0, 0, SIZE, SIZE)
        self.position = initial_position
        self.velocity = pygame.Vector2(0, 0)
        
        self.steering_point = pygame.Vector2(0, 0)
        self.direction = 'right'
        self.current_position = 'left'

    def draw(self, canvas, font):
        self.figure.center = self.position
        pygame.draw.rect(canvas, pygame.Color("black"), self.figure)

    def update(self, sheep, dt, target_fps):
        # Drone should not move faster than max speed
        if np.linalg.norm(self.velocity) > MAX_SPEED:
            self.velocity = self.velocity / np.linalg.norm(self.velocity) * MAX_SPEED

        # Move
        self.position += self.velocity * dt * target_fps

        # Update velocity vector
        self.velocity = pygame.Vector2(0, 0)


    def move(self, goal, drones, sheep, canvas, dt, target_fps):
        com = Calculate.center_of_mass(sheep)

        # Radius from com to sheep furthest away
        d_furthest = 0
        for s in sheep:
            distance = np.linalg.norm(s.position-com)
            if distance > d_furthest:
                d_furthest = distance

        d_over = DESIRED_SEPARATION_SHEEP
        distance_from_com = d_furthest + d_over
        
        self.find_steering_point(com, distance_from_com, drones, goal.position, canvas)
        self.velocity = self.steering_point - self.position
        self.update(sheep, dt, target_fps)


    def find_steering_point(self, com, distance_from_com, drones, goal, canvas):
        theta = 35 # angle with highest success rate from the studies
        
        com_to_goal = pygame.Vector2(com - goal) 
        point = com + distance_from_com * (com_to_goal/com_to_goal.length())

        P_left = pygame.Vector2(0, 0)
        P_center = pygame.Vector2(0, 0)
        P_right = pygame.Vector2(0, 0)

        # Find correct points for this specific drone
        if self.id == 0:
            P_left = point
            P_center = com + (point - com).rotate(theta)
            P_right = com + (point - com).rotate(2 * theta)

        if self.id == 1:
            P_right = point
            P_center = com + (point - com).rotate(-theta)
            P_left = com + (point - com).rotate(2 * -theta)


        # Fly between P_left -> P_center -> P_right -> ...
        if self.current_position == 'left' and self.figure.collidepoint(P_left):
            self.current_position = 'center'
            self.direction = 'right'
            self.steering_point = P_center
        if self.current_position == 'right' and self.figure.collidepoint(P_right):
            self.current_position = 'center'
            self.direction = 'left'
            self.steering_point = P_center
        if self.current_position == 'center' and self.figure.collidepoint(P_center) and self.direction == 'right':
            self.current_position = 'right'
            self.steering_point = P_right
        if self.current_position == 'center' and self.figure.collidepoint(P_center) and self.direction == 'left':
            self.current_position = 'left'
            self.steering_point = P_left
        if self.current_position == 'left' and not self.figure.collidepoint(P_left):
            self.steering_point = P_left
        if self.current_position == 'right' and not self.figure.collidepoint(P_right):
            self.steering_point = P_right
        if self.current_position == 'center' and not self.figure.collidepoint(P_center):
            self.steering_point = P_center
        
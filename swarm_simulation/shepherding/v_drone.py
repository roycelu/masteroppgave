import pygame
import numpy as np
from utils import Calculate


SIZE = 10
MAX_SPEED = 19 #m/s
MAX_SPEED_SHEEP = 0.003 #  m/s
DESIRED_SEPARATION_SHEEP = 15
PERCEPTION = 100


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

        # label = font.render(str(self.id), True, pygame.Color("white"))
        # label_rect = label.get_rect()
        # label_rect.center = self.position
        # canvas.blit(label, label_rect)

    def update(self, sheep, dt, target_fps):
        velocity_distance = np.linalg.norm(self.velocity)
        # Drone should not move faster than max speed
        if velocity_distance > MAX_SPEED:
            self.velocity = self.velocity / velocity_distance * MAX_SPEED
        # If drone is in close proximity to sheep they should not move faster than sheep
        for s in sheep:
            if (self.position-s.position).magnitude() <= (DESIRED_SEPARATION_SHEEP):
                self.velocity = self.velocity / velocity_distance * MAX_SPEED_SHEEP

        self.position += self.velocity * dt * target_fps
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
        theta = np.pi/6 # = 30, angle is fixed
        
        com_to_goal = pygame.Vector2(com - goal) 
        point = com + distance_from_com * (com_to_goal/com_to_goal.length())
        # pygame.draw.circle(canvas, pygame.Color("brown"), point, 2)

        P_left = pygame.Vector2(0, 0)
        P_center = pygame.Vector2(0, 0)
        P_right = pygame.Vector2(0, 0)

        if self.id == 0:
            P_left = point
            P_center = com + (point - com).rotate_rad(theta)
            P_right = com + (point - com).rotate_rad(2 * theta)

            # pygame.draw.circle(canvas, pygame.Color("blue"), P_center, 5)
            # pygame.draw.circle(canvas, pygame.Color("blue"), P_left, 3)
            # pygame.draw.circle(canvas, pygame.Color("blue"), P_right, 3)

        if self.id == 1:
            P_right = point
            P_center = com + (point - com).rotate_rad(-theta)
            P_left = com + (point - com).rotate_rad(2 * -theta)

            # pygame.draw.circle(canvas, pygame.Color("yellow"), P_center, 5)
            # pygame.draw.circle(canvas, pygame.Color("yellow"), P_left, 3)
            # pygame.draw.circle(canvas, pygame.Color("yellow"), P_right, 3)

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
        
import pygame
import numpy as np
from utils import Calculate
from itertools import permutations


SIZE = 10
MAX_SPEED = 19 #m/s
MAX_SPEED_SHEEP = 0.3 #  m/s
DESIRED_SEPARATION_SHEEP = 25
PERCEPTION = 100

STEP_SIZE = 200

AWAY_TARGET_ACTION = 2000

class OurDroneFurthest:
    def __init__(self, id, initial_position):
        self.id = id
        self.figure = pygame.Rect(0, 0, SIZE, SIZE)
        self.position = initial_position
        self.velocity = pygame.Vector2(0, 0)
        # self.acceleration = pygame.Vector2(0, 0)
        
        self.steering_point_v = pygame.Vector2(0, 0)
        self.direction = 'right'
        self.current_position = 'left'
        self.collides_with_point = False
        self.theta = 0 # vinkel i grader

        self.direction_index = 0  # 0:clockwise (right), 1:counterclockwise (left)
        self.right_pass = 0  # 0: otherwise, 1: pass z=0 by right flying to z=j
        self.left_pass = 0  # =. otherwise, 1: pass z=0 by left flying to z=j
        self.travel_path = []  # The path from start to steering point
        self.possible_allocations = []  # All possible steering points allocations
        self.edge_point = pygame.Vector2(0, 0)  # The first point on the edge
        self.steering_point = pygame.Vector2(0, 0)  # The final point to fly to
        self.steering_drive = 0

        self.dist1 = 0
        self.dist2 = 0
        self.dist3 = 0

        self.P_leftie = pygame.Vector2(0, 0)
        self.P_centerie = pygame.Vector2(0, 0)
        self.P_rightie = pygame.Vector2(0, 0)

    def draw(self, canvas, font):
        self.figure.center = self.position
        pygame.draw.rect(canvas, pygame.Color("black"), self.figure)

        # label = font.render(str(self.id), True, pygame.Color("white"))
        # label_rect = label.get_rect()
        # label_rect.center = self.position
        # canvas.blit(label, label_rect)


    def update(self, sheep, dt, target_fps):
        velocity_distance = np.linalg.norm(self.velocity)
        
        velocity_distance_sheep = 0
        for s in sheep:
            velocity_distance_sheep += np.linalg.norm(s.velocity)
        velocity_distance_sheep /= len(sheep)

        k = np.abs(np.linalg.norm(self.velocity)-velocity_distance_sheep)
        self.velocity *= k
        k=0

        # Update velocity to avoid running into sheep
        # self.velocity += self.acceleration * dt * target_fps

        # Drone should not move faster than max speed
        if np.linalg.norm(self.velocity) > MAX_SPEED:
            self.velocity = self.velocity / np.linalg.norm(self.velocity) * MAX_SPEED

        # If drone is in close proximity to sheep they should not move faster than sheep
        for s in sheep:
            if (self.position-s.position).magnitude() <= (DESIRED_SEPARATION_SHEEP) and velocity_distance != 0:
                self.velocity = self.velocity / np.linalg.norm(self.velocity) * MAX_SPEED_SHEEP
        
        self.position += self.velocity * dt * target_fps
        self.velocity = pygame.Vector2(0, 0)
        self.acceleration = pygame.Vector2(0,0)

    def fly_to_position(self, position):
        self.velocity = (position - self.position)

    def move(self, goal, drones, sheep, canvas, dt, target_fps):
        # stay_away_action = self.stay_away_target(sheep)
        # self.acceleration += stay_away_action * AWAY_TARGET_ACTION
        self.update(sheep, dt, target_fps)

    # def stay_away_target(self, sheep):
    #     # Don't crash into sheep
    #     acc = pygame.Vector2(0,0)
    #     for s in sheep:
    #         if np.linalg.norm(self.position-s.position) < 30:
    #             acc += (self.position-s.position) / (np.linalg.norm(self.position - s.position))**3
    #     acc /= len(sheep)
    #     return acc

    def find_steering_point(self, sheep, goal, com, theta):
        goal = goal.position
        self.theta = theta

        # Radius from com to sheep furthest away
        d_furthest = 0
        for s in sheep:
            distance = np.linalg.norm(s.position-com)
            if distance > d_furthest:
                d_furthest = distance

        d_over = DESIRED_SEPARATION_SHEEP
        distance_from_com = d_furthest + d_over
    
        com_to_goal = pygame.Vector2(com - goal) 
        point = com + distance_from_com * (com_to_goal/com_to_goal.length())

        P_left = pygame.Vector2(0, 0)
        P_center = pygame.Vector2(0, 0)
        P_right = pygame.Vector2(0, 0)

        if self.id == 0:
            P_left = com + (point - com).rotate(theta)
            P_center = point
            P_right = com + (point - com).rotate(-theta)

        if self.id == 1:
            P_right = com + (point - com).rotate(theta)
            P_center = com + (point - com).rotate(2 * theta) 
            P_left = com + (point - com).rotate(3 * theta)

        if self.id == 2:
            P_left = com + (point - com).rotate(-theta)
            P_center = com + (point - com).rotate(2 * -theta) 
            P_right = com + (point - com).rotate(3 * -theta)
            
        
        # Fly between P_left -> P_center -> P_right -> ...
        if self.current_position == 'left' and self.figure.collidepoint(P_left):
            self.current_position = 'center'
            self.direction = 'right'
            self.steering_point_v = P_center
        if self.current_position == 'right' and self.figure.collidepoint(P_right):
            self.current_position = 'center'
            self.direction = 'left'
            self.steering_point_v = P_center
        if self.current_position == 'center' and self.figure.collidepoint(P_center) and self.direction == 'right':
            self.current_position = 'right'
            self.steering_point_v = P_right
        if self.current_position == 'center' and self.figure.collidepoint(P_center) and self.direction == 'left':
            self.current_position = 'left'
            self.steering_point_v = P_left
        if self.current_position == 'left' and not self.figure.collidepoint(P_left):
            self.steering_point_v = P_left
        if self.current_position == 'right' and not self.figure.collidepoint(P_right):
            self.steering_point_v = P_right
        if self.current_position == 'center' and not self.figure.collidepoint(P_center):
            self.steering_point_v = P_center

        self.velocity = self.steering_point_v - self.position


    def find_steering_point_gather_sheep(self, sheep_pos, com, theta, screen, shortest_points = []):
        d_over = DESIRED_SEPARATION_SHEEP
        self.theta = theta # angle set by test.py
        sheeppos_to_com = pygame.Vector2(sheep_pos - com) 
        point = sheep_pos + d_over * (sheeppos_to_com/sheeppos_to_com.length())

        P_left = pygame.Vector2(0, 0)
        P_center = pygame.Vector2(0, 0)
        P_right = pygame.Vector2(0, 0)

        if len(shortest_points) > 0:
            for drone_id in shortest_points:
                if drone_id == self.id:
                    side = shortest_points.index(drone_id)
                    if side == 0:
                        P_left = point
                        P_center = com + (point - com).rotate(theta)
                        P_right = com + (point - com).rotate(2 * theta)

                    if side == 1:
                        P_right = point
                        P_center = com + (point - com).rotate(-theta)
                        P_left = com + (point - com).rotate(2 * -theta)
        else:
            P_left = sheep_pos + (point - sheep_pos).rotate(theta)
            P_center = point
            P_right = sheep_pos + (point - sheep_pos).rotate(-theta)

        # pygame.draw.circle(screen, pygame.Color("yellow"), P_left, 5)
        # pygame.draw.circle(screen, pygame.Color("brown"), P_center, 2)
        # pygame.draw.circle(screen, pygame.Color("yellow"), P_right, 5)

        # Fly between P_left -> P_center -> P_right -> ...
        if self.current_position == 'left' and self.figure.collidepoint(P_left):
            self.current_position = 'center'
            self.direction = 'right'
            self.steering_point_v = P_center
        if self.current_position == 'right' and self.figure.collidepoint(P_right):
            self.current_position = 'center'
            self.direction = 'left'
            self.steering_point_v = P_center
        if self.current_position == 'center' and self.figure.collidepoint(P_center) and self.direction == 'right':
            self.current_position = 'right'
            self.steering_point_v = P_right
        if self.current_position == 'center' and self.figure.collidepoint(P_center) and self.direction == 'left':
            self.current_position = 'left'
            self.steering_point_v = P_left
        if self.current_position == 'left' and not self.figure.collidepoint(P_left):
            self.steering_point_v = P_left
        if self.current_position == 'right' and not self.figure.collidepoint(P_right):
            self.steering_point_v = P_right
        if self.current_position == 'center' and not self.figure.collidepoint(P_center):
            self.steering_point_v = P_center

        self.velocity = self.steering_point_v - self.position
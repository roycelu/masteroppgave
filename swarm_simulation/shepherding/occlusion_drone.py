import pygame
import numpy as np
from sympy import *

SIZE = 10
STEP_SIZE = 500
MAX_SPEED = 3
MAX_SPEED_SHEEP = 1.1
PERCEPTION = 100
VIEW_DISTANCE_SHEEP = 20
DESIRED_SEPARATION = 10
DESIRED_SEPARATION_SHEEP = 15

S_WEIGHT = 200
R_WEIGHT = 500000



class OcclusionDrone:
    def __init__(self, id, initial_position, FPS):
        self.id = id
        self.figure = pygame.Rect(0, 0, SIZE, SIZE)
        self.position = initial_position
        self.velocity = pygame.Vector2(0.5, 0.5)
        self.acceleration = pygame.Vector2(0, 0)
        self.c_t = 1
        self.FPS = FPS
        self.time = 1
        self.prev_coupling_weight = 0

    def draw(self, canvas, font):
        self.figure.center = self.position
        pygame.draw.rect(canvas, pygame.Color("black"), self.figure)

        label = font.render(str(self.id), True, pygame.Color("white"))
        label_rect = label.get_rect()
        label_rect.center = self.position
        canvas.blit(label, label_rect)

    def update(self, com, flock_radius, dt, target_fps):
        
        acceleration_distance = np.linalg.norm(self.acceleration)
        if acceleration_distance > MAX_SPEED:
            self.acceleration = self.acceleration / acceleration_distance * MAX_SPEED
            
        if (self.position-com).magnitude() <= (flock_radius + DESIRED_SEPARATION_SHEEP):
            self.acceleration = self.acceleration / acceleration_distance * MAX_SPEED_SHEEP # Mindre enn hastigheten til sauene (enn så lenge bare makshastigheten til sauene)
        print('acceleration after', self.acceleration)
        self.position += self.acceleration * dt * target_fps

    def move(self, goal, drones, sheep, goal_vector, canvas, dt, target_fps):
        if self.figure.colliderect(goal.figure):
            self.goal_status = True

        com = pygame.Vector2(0, 0)
        for s in sheep:
            com += s.position
        com /= len(sheep)
        flock_radius = 0
        for s in sheep:
            distance = np.linalg.norm(s.position-com)
            if distance > flock_radius:
                flock_radius = distance
        #print('goal_vector', goal_vector)
        repulsive_field = self.repulsion(com, flock_radius, goal_vector)
        attractive_force = self.alignment(com, self.FPS, canvas, goal_vector)
        separation = self.separation(drones)
        
        self.acceleration += repulsive_field
        self.acceleration += attractive_force
        self.acceleration += separation
        print('acceleration before', self.acceleration)
        

        self.update(com, flock_radius, dt, target_fps)

    def repulsion(self, com, flock_radius, goal):
        """ Avoid pushing the flock in the wrong direction """
        repulsion = pygame.Vector2(0, 0)
        distancecom = np.linalg.norm(self.position-com)
        n = 0
        a = np.array([goal-self.position, com-self.position])
        if (distancecom <= (flock_radius + VIEW_DISTANCE_SHEEP)) and ((((np.linalg.norm(np.linalg.det(a))) / np.linalg.norm(goal-self.position)) >= flock_radius) or (np.linalg.norm(self.position-goal) <= np.linalg.norm(com-goal))):
            repulsion += R_WEIGHT*((1/distancecom)-(1/(flock_radius+VIEW_DISTANCE_SHEEP)))*((self.position-com)/(distancecom)**2)
        print('repulsion', repulsion)
        return repulsion
    
    def alignment(self, com, FPS, canvas, goal):
        # Det må være noe feil med denne, verdiene blir helt wack store. Tror det er c greia, alt annet ser riktig ut fra formlene

        """ Make the drones fly toward the occlusion area and push the sheep towards the goal """
        print('id, goal', self.id, goal)
        
        
        w = 0.0001 # Tuning parameter, denne justeres for riktig oppførsel
        e = self.position-com
        p = (1 + np.transpose(e) * np.sqrt(w) * e)**3


        self.c_t = np.transpose(e) * w * e  # Dette er en diskretisering, newtons metode
        x = self.prev_coupling_weight + (self.c_t - self.prev_coupling_weight)/2
        self.prev_coupling_weight = self.c_t
        self.c_t += x

        print('coupling_weight', self.c_t)
        
        c = self.c_t * (1000/FPS)
        print('c', c)

        
        
        
        pygame.draw.circle(canvas, pygame.Color("pink"), com, 4)
        pygame.draw.line(canvas, pygame.Color('orange'), com, self.position)
        pygame.draw.circle(canvas, pygame.Color('orange'), goal, 5)
        pygame.draw.line(canvas, pygame.Color('pink'), self.position, goal)

        u = -c * p * (np.transpose(e) * np.sqrt(w) * e) * np.sqrt(w) * e
        print('alignment', u)
        return u
        

    def separation(self, drones):
        """ The drones avoid colliding with each other """
        separation = pygame.Vector2(0, 0)
        for drone in drones:
            distance = np.linalg.norm(self.position - drone.position)
            if drone != self and distance < PERCEPTION:
                if distance <= DESIRED_SEPARATION and distance != 0:
                    separation += S_WEIGHT*((1/distance)-(1/DESIRED_SEPARATION))*((self.position-drone.position)/(distance**2))
        print('separation', separation)
        return separation

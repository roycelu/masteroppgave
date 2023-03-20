import pygame
import numpy as np
from sympy import *

SIZE = 10
MAX_SPEED = 3
MAX_SPEED_SHEEP = 1.5
DESIRED_SEPARATION_SHEEP = 20
PERCEPTION = 1000

CHASE_ACTION = 10
AWAY_TARGET_ACTION = 200
AWAY_GOAL = 8
REPULSION = 3000

C_r = 3
C_s = 1  # 0 < C_r < C_s such that the robots pay more attention to the distribution of the flock than that of themselves.
density_0 = 20 # Reference density that control s the expected distance between the robot and the flock
k_o = 1 # > 0  weight exploration
k_f = 2 # > 0 weight exploitation
h = 100 # > 0 parameter that controls the shrink rate
q = 0.2 # >= 0 relaxation factor


class CagingDrone:
    def __init__(self, id, initial_position):
        self.id = id
        self.figure = pygame.Rect(0, 0, SIZE, SIZE)
        self.position = initial_position
        self.velocity = pygame.Vector2(0, 0)
        self.t_0 = 0

    def draw(self, canvas, font):
        self.figure.center = self.position
        pygame.draw.rect(canvas, pygame.Color("black"), self.figure)

        label = font.render(str(self.id), True, pygame.Color("white"))
        label_rect = label.get_rect()
        label_rect.center = self.position
        canvas.blit(label, label_rect)

    def update(self, dt, target_fps):
        velocity_distance = np.linalg.norm(self.velocity)
        if velocity_distance > MAX_SPEED:
            self.velocity = self.velocity / velocity_distance * MAX_SPEED

        self.position += self.velocity * dt * target_fps

        self.velocity = pygame.Vector2(0, 0)

    def move(self, goal, drones, sheep, goal_vector, canvas, dt, target_fps):
        if self.figure.colliderect(goal.figure):
            self.goal_status = True

        if self.shrink_condition(drones):
            self.velocity += self.shrink_mechanism(sheep)
            print('SHRINK CONDITION')
        else:
            O_i = self.edge_mechanism_O(drones)
            F_i = self.edge_mechanism_F(drones, sheep)
            self.velocity = k_o*O_i + k_f*F_i
            print('EDGE MECHANISM')
        self.update(dt, target_fps)

    def weight_function(self, agent): # Ser fin ut :)
        k = 0.375 # Chosen such that an agent 20 body length away has 11.76% as much influence in the direction of the focal agent i as one right next to the agent i.
        distance = self.position - agent.position
        agent_density = 0
        if np.linalg.norm(distance) <= PERCEPTION and self != agent and distance != 0:
            agent_density = (1/(1+k*np.linalg.norm(distance))*(distance/np.linalg.norm(distance)))
        return agent_density
                
    def density(self, drones, sheep): # Ser fint ut
        drone_density = 0
        sheep_density = 0
        for drone in drones:
            drone_density += self.weight_function(drone)
        for s in sheep:
            sheep_density += self.weight_function(s)
        density = C_r*drone_density + C_s*sheep_density
        return density


    def edge_mechanism_O(self, drones): # Ser riktig ut
        """Movement of drones is guided by the overlap avoidance force"""
        neighbouring_drones = 0
        O_sum = 0
        for drone in drones:
            distance = self.position-drone.position
            if np.linalg.norm(distance) < PERCEPTION and drone != self and distance != 0:
                neighbouring_drones += 1
                O_sum += (1/(np.linalg.norm(distance))*(distance/np.linalg.norm(distance)))

        O_i = (1/neighbouring_drones)*O_sum # Overlap avoidance force
        return O_i
    

    def edge_mechanism_F(self, drones, sheep):
        """Movement of drones is guided by the density-force"""
        F_i = 0 # Density-based force
        # drone_array = []
        # sheep_array = []
        # for s in sheep:
        #     print('weight', self.weight_function(s))
        #     print('gradient', np.gradient(self.weight_function(s)))
        #     sheep_array.append(np.gradient(self.weight_function(s)))
        # for drone in drones:
        #     if drone != self:
        #         drone_array.append(np.gradient(self.weight_function(drone)))
        
        # drone_gradient = drone_array
        # sheep_gradient = sheep_array
        # print('dronearray', drone_array)
        # print('sheeparray', sheep_array)

        # density = self.density(drones, sheep)
        # m = len(drones)+len(sheep)
        # for i in range(m):
        #     print('i', i)
        #     print('len drones', len(drones))
        #     print('len sheep', len(sheep))
        #     if i < len(drones)-2 and i < len(sheep)-1:
        #         F_i += 1/density*np.dot(((density/density_0)**7 - 1),(C_r*drone_gradient[i]+C_s*sheep_gradient[i]))
        #     elif i < len(drones)-2:
        #         F_i += 1/density*((density/density_0)**7 - 1)*(C_s*drone_gradient[i])
        #     elif i < len(sheep)-1:
        #         F_i += 1/density*((density/density_0)**7 - 1)*(C_r*sheep_gradient[i])

        sheep_force = 0
        drones_force = 0
        density = (1/self.density(drones, sheep))*((self.density(drones, sheep)/density_0)**7 - 1)
        for d in drones:
            drones_force += C_r * np.gradient(self.weight_function(d))
        for s in sheep:
            sheep_force += C_s * np.gradient(self.weight_function(s))
        F_i = density * (drones_force + sheep_force)
        return F_i


    def shrink_condition(self, drones):
        s_squared = 0
        for drone in drones:
            nearest_distance = np.Inf
            distance_mean = 0

            n_dist = np.Inf
            for d in drones:
                distance = np.linalg.norm(drone.position-d.position)
                if drone != d and distance < n_dist:
                    n_dist = distance
            distance_mean += n_dist


            for d in drones:
                if drone != d:
                    distance = np.linalg.norm(d.position-drone.position)
                    if distance < nearest_distance:
                        nearest_distance = distance

            distance_mean /= len(drones)
            s_squared += (nearest_distance-distance_mean)**2/len(drones)

        if s_squared < q:
            self.t_0 = pygame.time.get_ticks()
            return True
        else:
            return False
      
        

    def shrink_mechanism(self, sheep):
        t = pygame.time.get_ticks()

        if t < self.t_0:
            p = density_0*(1/len(sheep)**2)
        else:
            p = (density_0 + h*(t-self.t_0))*(1/len(sheep)**2)

        return p

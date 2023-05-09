import pygame
import numpy as np
import pandas as pd
from goal import Goal
from itertools import permutations


DISTANCE = 20 #30  # drone-to-animal distance (predefined)
TURNING_RADIUS = 5  # minimum turning radius of the drone (predefined?)
SHEEP_RADIUS = 20 # 60  # the sheep's smallest circle during driving (predefined)


class OurMainDroneFurthest:
    def __init__(self, canvas, goal, drones, sheeps, theta):
        self.canvas = canvas

        self.main_goal = goal
        self.goal = Goal(goal.position)
        self.drones = drones
        self.sheeps = sheeps

        self.centre_of_mass = pygame.Vector2(0, 0)

        self.on_edge = False
        self.toward_goal = False

        self.theta = theta

        self.current_point = 'left'
        self.direction = 'right'


    def allocate_steering_points(self, drones, sheep, com, goal):
        # Find sheep behind center of mass relative to the goal
        com_goal = com - goal.position
        steering_points = []
        flocks = []
        for s in sheep:
            s_com = com - s.position
            angle = com_goal.angle_to(s_com)
            #pygame.draw.circle(self.canvas, pygame.Color('blue'), s.position, 5)
            if abs(angle) > 45:
                steering_points.append(s.position)
                flocks.append([s])
                #pygame.draw.circle(self.canvas, pygame.Color('pink'), s.position, 8)
        # Group sheep so as to consider them as one if they are within 5 px of each other
        i = 0
        for list_f in flocks:
            com_new = pygame.Vector2(0,0)
            for sheep in list_f:
                com_new += sheep.position
            com_new /= len(list_f)
            
            for element in flocks[flocks.index(list_f)+1:]:
                for sheep in element:
                    if sheep.position.distance_to(com_new) < 20:
                        list_f.append(sheep)

        com_list = []
        for list_f in flocks:
            com_p = pygame.Vector2(0,0)
            for sheep in list_f:
                com_p += sheep.position
            com_p /= len(list_f)
            com_list.append(com_p)        
        
        # Find the N sheep furthest away from the center of mass (the steering points)
        # (Bubble) sorting based on the distance from the centre of mass
        steering_sheep = []
        if len(com_list) > 1:
            for m in range(len(com_list)):
                for n in range(len(com_list) - m - 1):
                    d = com.distance_to(com_list[n])
                    d2 = com.distance_to(com_list[n + 1])
                    if d < d2:
                        com_list[n], com_list[n + 1] = com_list[n + 1], com_list[n]
            steering_sheep = com_list[:3]
        else:
            steering_sheep = com_list[:3]

        # Find shortest total travel distance for all drones to the different variations of steeringpoints
        shortest_total = np.inf
        shortest_points = [2,0,1]
        perm = permutations([0,1,2],2)
        perm2 = permutations([0,1,2])

        # If there is only one group of sheep, herd them in a V-formation with all three drones
        if len(steering_sheep) == 0 or len(steering_sheep) == 1:
            for dro in drones:
                dro.find_steering_point(self.sheeps, goal, com, self.theta)

        # If there are two groups, send two drones to the group with the most sheep and one to the other
        elif len(steering_sheep) == 2:
            # for point in steering_sheep:
            #     pygame.draw.circle(self.canvas, pygame.Color("lightblue"), point, 5)
            flock1len = len(flocks[0])
            flock2len = len(flocks[1])
            
            for i in list(perm):
                dist0 = drones[i[0]].position.distance_to(steering_sheep[0])
                dist1 = drones[i[1]].position.distance_to(steering_sheep[1])
                total = dist0+dist1
                if total < shortest_total:
                    shortest_total = total
                    shortest_points = list(i)
            
            shortest_dist = np.inf
            for drone in drones:
                if drone.id not in shortest_points:
                    shortest_points.append(drone.id)
                    if flock1len > flock2len:
                        steering_sheep.append(steering_sheep[0])
                    elif flock2len > flock1len:
                        steering_sheep.append(steering_sheep[1])
                    else:
                        steering = steering_sheep[0]
                        for point in steering_sheep:
                            if drone.position.distance_to(point) < shortest_dist:
                                shortest_dist = drone.position.distance_to(point)
                                steering = point
                        steering_sheep.append(steering)
            
            duplicate_index = np.where(pd.Series(steering_sheep).duplicated(keep=False))[0] # Duplikater [første_index, ..., siste_index]
            for j in range(len(shortest_points)):
                drones[shortest_points[j]].find_steering_point_gather_sheep(steering_sheep[j], com, self.theta, self.canvas, [duplicate_index[0], duplicate_index[-1]])

        # If there are three groups, each drone moves to the one that makes for the shortest total travel distance
        elif len(steering_sheep) == 3:
            # for point in steering_sheep:
            #     pygame.draw.circle(self.canvas, pygame.Color("lightblue"), point, 5)
            for i in list(perm2):
                dist0 = drones[i[0]].position.distance_to(steering_sheep[0])
                dist1 = drones[i[1]].position.distance_to(steering_sheep[1])
                dist2 = drones[i[2]].position.distance_to(steering_sheep[2])
                total = dist0+dist1+dist2
                if total < shortest_total:
                    shortest_total = total
                    shortest_points = i
            j = 0
            for i in shortest_points:
                drones[shortest_points[j]].find_steering_point_gather_sheep(steering_sheep[j], com, self.theta, self.canvas)
                j += 1
    

    def run(self, drones, sheeps, goal, centre_of_mass):
        #self.centre_of_mass = centre_of_mass

        # The minimum distance of gathering, before the animals need to be driven to a designated location
        gather_radius = pygame.draw.circle(self.canvas, pygame.Color("palegreen3"), centre_of_mass, SHEEP_RADIUS, 1)
        sheep_list = []
        for s in sheeps:
            if not gather_radius.contains(s.figure):
                sheep_list.append(s)
        if len(sheep_list) > 0:
            self.allocate_steering_points(drones, sheeps, centre_of_mass, goal)

        else:
            for dro in drones:
                dro.find_steering_point(sheeps, goal, centre_of_mass, self.theta)

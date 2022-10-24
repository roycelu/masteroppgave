import math
from re import S
#from p5 import circle, stroke, fill
import pygame
import random
import tkinter
from geometry_msgs.msg import Twist, PoseStamped, Pose
from util import Vector2
import numpy as np


class Sheep:
    def __init__(self, initial_position, id):
        
        self.id = id
        self.position = initial_position
        self.max_speed = 2
        
        #Set initial velocity
        #initial_random_velocity = (np.random.rand(2)-0.5) * self.max_speed * 2
        self.velocity = 0
        self.horizon = 100
        self.cohesion_weight = 1
        self.separation_weight = 30
        self.separation_weight_drones = 10
        self.alignment_weight = 5

        self.desired_separation = 15
        self.desired_separation_drones = 30

    def draw_sheep(self, canvas):
        size = 10
        x1 = self.position[0] + size 
        x2 = self.position[1] + size
        canvas.create_oval(self.position[0], self.position[1], x1, x2, fill='white', tags=self.id)
    
    def update_sheep(self):
        # Limiting the speed
        if np.linalg.norm(self.velocity) > self.max_speed:
            self.velocity = (self.velocity/np.linalg.norm(self.velocity)) * self.max_speed
        # Then update the position
        self.position = np.add(self.position, self.velocity)
    
    def main_sheep(self, list_of_sheep, canvas, list_of_drones):
        step_size = 5
        desired_position = np.zeros(2, dtype=np.int32)
        desired_position[0] = 250
        desired_position[1] = 250
        for drone in list_of_drones:
            if np.linalg.norm(drone.position - self.position) < self.desired_separation_drones:
                self.velocity = drone.velocity
            else:
                self.velocity = (desired_position - self.position) * (step_size / 100)
                
        v1 = self.cohesion(list_of_sheep)
        v2 = self.separation(list_of_sheep)
        v2_2 = self.drone_separation(list_of_drones)
        v3 = self.alignment(list_of_sheep)
        self.velocity += v1 + v2 + v2_2 + v3

        canvas.delete(self.id)
        self.draw_sheep(canvas)
        self.update_sheep()
        
    
    def cohesion(self, nearest_sheep):
        # move together - cohesion
        center_of_mass = np.zeros(2)
        N = 0 #Total sheep number
        #com_direction = Vector2()

        # Find mean position of neighbouring sheep
        for sheep in nearest_sheep:
            if (np.linalg.norm(sheep.position - self.position) < self.horizon) & (sheep != self):
                center_of_mass += sheep.position
            N += 1
        
        center_of_mass = center_of_mass / (N-1)
        target_position = (center_of_mass * self.cohesion_weight) / 100

        """
        # Magnitude of force is proportional to agents' distance from the center of mass
        # Force should be applied in the direction of the com
        if nearest_agents:
            #print(sheep_position)
            #print(len(nearest_agents))
            com_direction.x = center_of_mass.x / len(nearest_agents)
            com_direction.y = center_of_mass.y / len(nearest_agents)
            #print(com_direction)
            d = com_direction.norm()
            #print(com_direction)
            com_direction.set_mag((self.max_force))
            #print(com_direction)
   
        return com_direction
        """
        return target_position
        
        
    def separation(self, nearest_sheep):
        # move away from nearest - separation
        c = np.zeros(2)
        
        for sheep in nearest_sheep:
            if ((np.linalg.norm(sheep.position - self.position) < self.horizon)
                    & (np.linalg.norm(sheep.position - self.position) < self.desired_separation)
                    & (sheep != self)):
                c -= (sheep.position - self.position)*(self.separation_weight/100)
        """
        N = 0 # Total boid number

        for b in nearest_agents:
            boid_position = get_agent_position(b)
            d = boid_position.norm()
            if d < self.desired_separation:
                N += 1
                boid_position *= -1 # Force towards outside
                boid_position.normalize() # Normalize to get only direction
                # Magnitude is proportional to inverse square of d, where d is the distance between agents
                boid_position = boid_position / (d**2)
                c += boid_position
        
        if N:
            c /= N #average
            c.limit(2 * self.max_force) # 2 * max_force gives this rule a slight priority
        """
        return c
              

    def drone_separation(self, nearest_drone):
        # move away from nearest - separation
        c = np.zeros(2)
        
        for drone in nearest_drone:
            if ((np.linalg.norm(drone.position - self.position) < self.horizon)
                    & (np.linalg.norm(drone.position - self.position) < self.desired_separation_drones)
                    & (drone != self)):
                c -= (drone.position - self.position)*(self.separation_weight_drones/100)
                self.velocity = -drone.velocity
        return c

    def alignment(self, nearest_sheep):
        # orient towards the neighbours - alignment
        perceived_velocity = np.zeros(2)
        N = 0 #Total sheep number

        # Find mean direction of the neighbouring agents
        for sheep in nearest_sheep:
            if (np.linalg.norm(sheep.position - self.position) < self.horizon) & (sheep != self):
                perceived_velocity += sheep.velocity
            N += 1
        
        # Steer toward calculated mean direction with maximum velocity
        perceived_velocity =  perceived_velocity / (N-1)
        pv = (perceived_velocity * self.alignment_weight / 100)
        """
        # Steer toward calculated mean direction with maximum velocity
        if nearest_agents:
            perceived_velocity.set_mag(self.max_speed)
            pv = perceived_velocity - self.velocity
        """
        return pv


def get_agent_velocity(agent):
    vel = Vector2()
    vel.x = agent.velocity.x
    vel.y = agent.velocity.y
    return vel

def get_agent_position(agent):
    pos = Vector2() 
    pos.x = agent.position.x
    pos.y = agent.position.y
    return pos


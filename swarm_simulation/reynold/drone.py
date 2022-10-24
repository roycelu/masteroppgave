import math
from re import S
#from p5 import circle, stroke, fill
import pygame
import random
import tkinter
from geometry_msgs.msg import Twist, PoseStamped, Pose
from util import Vector2
import numpy as np


class Drone:
    def __init__(self, initial_position, id):
        
        self.id = id
        self.position = initial_position
        self.max_speed = 2
        
        #Set initial velocity
        initial_random_velocity = (np.random.rand(2)-0.5) * self.max_speed * 2
        self.velocity = initial_random_velocity
        self.horizon = 100
        self.cohesion_weight = 1
        self.separation_weight = 10
        self.separation_weight_sheep = 10
        
        self.alignment_weight = 5

        self.desired_separation = 30
        self.desired_separation_sheep = 30
        
        
        #self.max_force = 50
        #self.separation_weight = 1.0
        #self.cohesion_weight = 1.0
        #self.alignment_weight = 1.0
        # This dictionary holds values of each flocking component and is used
        # to pass them to the visualization markers publisher.
        #self.viz_components = {}

    def draw_drone(self, canvas):
        size = 10
        x1 = self.position[0] + size 
        x2 = self.position[1] + size
        canvas.create_oval(self.position[0], self.position[1], x1, x2, fill='green', tags=self.id)
        canvas.create_text(self.position[0], self.position[1], text=self.id, tags=self.id)
    def update_drone(self):
        # Limiting the speed
        if np.linalg.norm(self.velocity) > self.max_speed:
            self.velocity = (self.velocity/np.linalg.norm(self.velocity)) * self.max_speed
        # Then update the position
        self.position = np.add(self.position, self.velocity)
    
    def main_drone(self, drones, canvas, list_of_sheep):
        v1 = self.cohesion(drones)
        v2 = self.separation(drones)
        v2_2 = self.sheep_separation(list_of_sheep)
        v3 = self.alignment(drones)
        
        canvas.delete(self.id)
        self.draw_drone(canvas)
        self.velocity += v1*self.cohesion_weight + v2*self.separation_weight + v2_2*self.separation_weight_sheep + v3*self.alignment_weight
        self.update_drone()
        
        
    def tend_to_place(self, desired_position, step_size):
        self.velocity = (desired_position - self.position) * (step_size / 100)

    def cohesion(self, nearest_drone):
        # move together - cohesion
        center_of_mass = np.zeros(2)
        N = 0 #Total drone number
        #com_direction = Vector2()

        # Find mean position of neighbouring drone
        for drone in nearest_drone:
            if (np.linalg.norm(drone.position - self.position) < self.horizon) & (drone != self):
                center_of_mass += drone.position
            N += 1
        
        center_of_mass = center_of_mass / (N-1)
        target_position = (center_of_mass * self.cohesion_weight) / 100

        return target_position
        
        

    def separation(self, nearest_drone):
        # move away from nearest - separation
        c = np.zeros(2)
        
        for drone in nearest_drone:
            if ((np.linalg.norm(drone.position - self.position) < self.horizon)
                    & (np.linalg.norm(drone.position - self.position) < self.desired_separation)
                    & (drone != self)):
                c -= (drone.position - self.position)*(self.separation_weight/100)
        return c

    def sheep_separation(self, nearest_sheep):
        # move away from nearest - separation
        c = np.zeros(2)
        
        for drone in nearest_sheep:
            if ((np.linalg.norm(drone.position - self.position) < self.horizon)
                    & (np.linalg.norm(drone.position - self.position) < self.desired_separation_sheep)
                    & (drone != self)):
                c -= (drone.position - self.position)*(self.separation_weight_sheep/100)
        
        return c
        
    def alignment(self, nearest_drone):
        # orient towards the neighbours - alignment
        perceived_velocity = np.zeros(2)
        N = 0 #Total drone number

        for drone in nearest_drone:
            if (np.linalg.norm(drone.position - self.position) < self.horizon) & (drone != self):
                perceived_velocity += drone.velocity
            N += 1
        
        perceived_velocity =  perceived_velocity / (N-1)
        pv = (perceived_velocity * self.alignment_weight / 100)
        return pv










    def compute_leader_following(self, rel2leader):
        for agent in rel2leader:
            rel2leader_position = get_leader_position(agent)
            # Force in the direction that minimizes rel_position to leader,
            # i.e. it should be in the direction of the rel2leader
            direction = Vector2() #initializes (0,0)
            direction = rel2leader_position # *0.01
            # d = direction.norm()
            # direction.set_mag((self.max_force * d))
        return direction

    def euclidean_distance(self, neighbour_drone):
        return math.sqrt((self.position.x - neighbour_drone.position.x) * (self.position.x - neighbour_drone.position.x) + \
                         (self.position.y - neighbour_drone.position.y) * (self.position.y - neighbour_drone.position.y))

    def compute_velocity(self, nearest_agents):
        # While waiting to start, send zero velocity and decrease counter.
        if self.wait_count > 0:
            self.wait_count -= 1
            #rospy.logdebug("wait " + ’{}’.format(self.wait_count))
            #rospy.logdebug("velocity:\n%s", Twist().linear)
            return Twist(), None

        # Send initial velocity and decrease counter.
        elif self.start_count > 0:
            self.start_count -= 1
            #rospy.logdebug("start " + ’{}’.format(self.start_count))
            #rospy.logdebug("velocity:\n%s", self.initial_velocity.linear)
            return self.initial_velocity, None

        # Normal operation, velocity is determined using Reynolds' rules
        else:
            self.velocity = get_agent_velocity(self)
            self.old_heading = self.velocity.arg()
            self.old_velocity = Vector2(self.velocity.x, self.velocity.y)
            #rospy.logdebug("old_velocity: %s", self.velocity)
            
            # Compute all the components.
            v1 = self.cohesion(nearest_agents) #cohesion
            v2 = self.separation(nearest_agents) #seperation
            v3 = self.alignment(nearest_agents) #alignment
            #leader = self.compute_leader_following(rel2leader)

            # Add components together and limit the output.
            force = Vector2()
            force += v1 * self.cohesion_weight
            force += v2 * self.separation_weight
            force += v3 * self.alignment_weight
            #force += leader * self.leader_weight
            force.limit(self.max_force)

            self.velocity.limit(self.max_speed)

            # Return the velocity as Twist message
            #vel = Twist()
            #vel.linear.x = self.velocity.x
            #vel.linear.y = self.velocity.y

            # Pack all components for Rviz visualization
            # Make sure these keys are the same as the ones in 'util.py'
            #self.viz_components['cohesion'] = v1 * self.cohesion_weight
            #self.viz_components['separation'] = v2 * self.separation_weight
            #self.viz_components['alignment'] = v3 * self.alignment_weight
            #self.viz_components['leader'] = leader * self.leader_weight
            #return self.velocity #, self.viz_components

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

def get_leader_position(leader):
    pos = Vector2()
    pos.x = leader.position.x
    pos.y = leader.position.y
    return pos



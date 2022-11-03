import math
import numpy as np
from geometry_msgs.msg import Twist
from util import Vector2


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

        self.desired_separation = 10
        self.desired_separation_sheep = 5
        
        self.desired_position = initial_position

        self.goal = False
        self.count_right = 0
        self.count_left = 10

        self.u_max = 200

    def draw_drone(self, canvas):
        size = 10
        # Draw the circle around the position (centre)
        x0 = self.position[0] - size/2
        y0 = self.position[1] - size/2
        x1 = self.position[0] + size/2
        y1 = self.position[1] + size/2
        canvas.create_oval(x0, y0, x1, y1, fill='green', outline='green', tags=self.id)
        canvas.create_text(self.position[0], self.position[1], text=self.id, tags=self.id)

    def update_drone(self):
        # Limiting the speed
        if np.linalg.norm(self.velocity) > self.max_speed:
            self.velocity = (self.velocity/np.linalg.norm(self.velocity)) * self.max_speed
        # Then update the position
        moving = True
        max_left = self.position - 10
        max_right = self.position + 10
        
        if self.count_right == 10:
            vector = (self.velocity[0]-self.position[0], self.velocity[1]-self.position[1])
            print(vector)

            vector[0] *= math.pi/4
            #self.velocity[0] /= math.cos(30)
            #self.velocity[1] /= math.cos(30)
            self.position = np.add(self.position, vector)
            self.count_left += 1
            if self.count_left == 10:
                self.count_right == 0

        if self.count_left == 10:
            vector = (self.velocity[0]-self.position[0], self.velocity[1]-self.position[1])
            print(vector)
            vector[0] *= (-math.pi/4)
            #self.velocity[0] /= math.cos(-30)
            #self.velocity[1] /= math.cos(-30)
            self.position = np.add(self.position, vector)
            self.count_right += 1
            if self.count_right == 10:
                self.count_left == 0

    def main_drone(self, drones, canvas, list_of_sheep):
        v1 = self.cohesion(drones)
        v2 = self.separation(drones)
        v2_2 = self.sheep_separation(list_of_sheep)
        v3 = self.alignment(drones)
        
        canvas.delete(self.id)
        self.draw_drone(canvas)
        self.velocity += v1*self.cohesion_weight + v2*self.separation_weight + v2_2*self.separation_weight_sheep + v3*self.alignment_weight
        self.update_drone()
        
    def fly_to_position(self, pos, step_size):
        self.desired_position = pos
        self.velocity = (pos - self.position) * (step_size / 100)
        #print("Goal", self.position, self.desired_position)
        if (self.desired_position[0] -5 <= self.position[0] <= self.desired_position[0] + 5) and (self.desired_position[1] - 5 <= self.position[1] <= self.desired_position[1] + 5):
            self.goal = True

    def fly_to_edge_guidance_law(self, drone, list_of_corners):
        E_j = list_of_corners[0]
        E_j_p = list_of_corners[1]
        
        q_t = E_j_p - E_j
        p_t = E_j_p - drone.position
        o_t = (0, 0) # O is closest point from drone to edge
        b_t = drone.position - o_t

        if np.dot(p_t, q_t) < 0:
            o_t = E_j_p
            b_t = -p_t
        elif (np.dot(p_t, q_t) > 0) and (np.linalg.norm(p_t) > np.linalg.norm(q_t)):
            o_t = np.linalg.norm(q_t)^(-1) * np.dot(p_t, q_t) * np.linalg.norm(q_t)^(-1) * q_t
            b_t = o_t - p_t
        else:
            o_t = E_j
            b_t = q_t - p_t

        a_t = 2
        u_t = self.u_max * self.g(a_t, b_t) * self.F(a_t, b_t)
        v_t = self.max_speed * self.g(a_t, b_t)

        return u_t, v_t

    def F(self, w_1, w_2):
        f = w_2 - np.dot(w_2, w_1) * w_1
        if f == 0:
            F = 0
        elif f != 0:
            F = np.linalg.norm(f)^(-1) * f
        return F
    
    def g(self, w_1, w_2):
        if np.dot(w_1, w_2) > 0:
            g = 1
        elif np.dot(w_1, w_2) <= 0:
            g = -1
        return g

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



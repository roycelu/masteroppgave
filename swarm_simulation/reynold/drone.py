import math
import numpy as np


class Drone:
    def __init__(self, initial_position, id):
        
        self.id = id
        self.position = initial_position
        self.angle = 45

        self.max_speed = 2
        
        #Set initial velocity
        #initial_random_velocity = (np.random.rand(2)-0.5) * self.max_speed * 2
        self.velocity = 0
        self.rotation_velocity = 5
        self.max_rot_vel = 5
        self.acceleration = 0.1

        self.horizon = 100
        self.cohesion_weight = 1
        self.separation_weight = 10
        self.separation_weight_sheep = 10
        self.alignment_weight = 5
        self.desired_separation = 10
        self.desired_separation_sheep = 5
        
        self.desired_position = initial_position
        
        self.extended_hull_goal = False
        self.hull_position_goal = False
        self.path_goal = False
        self.count_right = 0
        self.count_left = 10

        self.u_max = 200
        self.b_t = (math.inf, math.inf)

    def draw_drone(self, canvas):
        size = 10
        # Draw the circle around the position (centre)
        x0 = self.position[0] - size/2
        y0 = self.position[1] - size/2
        x1 = self.position[0] + size/2
        y1 = self.position[1] + size/2
        #canvas.create_oval(x0, y0, x1, y1, fill='green', outline='green', tags=self.id)
        canvas.create_text(self.position[0], self.position[1], text=self.id, tags=self.id)
        if self.id == 'drone0':
            canvas.create_oval(self.desired_position[0]-size/2, self.desired_position[1]-size/2, self.desired_position[0]+size/2, self.desired_position[1]+size/2, fill='black', outline='pink', tags=self.id)
        if self.id == 'drone1':
            canvas.create_oval(self.desired_position[0]-size/2, self.desired_position[1]-size/2, self.desired_position[0]+size/2, self.desired_position[1]+size/2, fill='yellow', outline='pink', tags=self.id)
        if self.id == 'drone2':
            canvas.create_oval(self.desired_position[0]-size/2, self.desired_position[1]-size/2, self.desired_position[0]+size/2, self.desired_position[1]+size/2, fill='red', outline='pink', tags=self.id)

        x1 = self.position[0] + size * math.cos(self.angle)
        x2 = self.position[1] + size * math.sin(self.angle)
        canvas.create_line(self.position[0], self.position[1], x1, x2, fill='black', arrow='last', arrowshape=(12.8,16,4.8), width=2, tags=self.id)

    """def drone_motion_dynamics(self):
        d_t = self.position
        d_t = v_t * a_t
        a_t = u_t 
        np.linalg.norm(a_t) = 1 # for every t
        np.linalg.norm(u_t) <= u_max
        0 <= v_t <= self.max_speed
        np.dot(a_t, u_t) = 0"""


    def calculate_angle(self):
        target_x, target_y =  self.desired_position
        x_diff = target_x - self.position[0]
        y_diff = target_y - self.position[1]

        if y_diff == 0:
            desired_radian_angle = math.pi/2
        else:
            desired_radian_angle = math.atan(x_diff/y_diff)
        
        if target_y > self.position[1]:
            desired_radian_angle += math.pi
        
        difference_in_angle = self.angle - math.degrees(desired_radian_angle)
        if difference_in_angle >= 180:
            difference_in_angle -= 360
        # print("diff_angle", difference_in_angle)
        
        if difference_in_angle > 0:
            self.angle -= min(self.rotation_velocity, abs(difference_in_angle))
        else:
            self.angle += min(self.rotation_velocity, abs(difference_in_angle))


    def update_drone(self):
        # Limiting the speed
        if np.linalg.norm(self.velocity) > self.max_speed:
            self.velocity = (self.velocity/np.linalg.norm(self.velocity)) * self.max_speed
        # Then update the position        
        self.position = np.add(self.position, self.velocity)
        
        """self.calculate_angle()
        #self.velocity = min(self.velocity - self.acceleration, -self.max_speed/2)
        #self.position = np.add(self.position, (self.velocity * math.cos(self.angle), self.velocity * math.sin(self.angle)) 
        radians = math.radians(self.angle)
        vertical = math.cos(radians) * self.velocity
        horizontal = math.sin(radians) * self.velocity
        print(horizontal)
        self.position = np.subtract(self.position, (horizontal, vertical))
        #self.position[0] -= horizontal
        #self.position[1] -= vertical"""
        
        """if self.count_right == 10:
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
                self.count_left == 0"""

    def main_drone(self, drones, canvas, list_of_sheep):
        v1 = self.cohesion(drones)
        v2 = self.separation(drones)
        v2_2 = self.sheep_separation(list_of_sheep)
        v3 = self.alignment(drones)
        
        canvas.delete(self.id)
        self.draw_drone(canvas)
        self.velocity += v1*self.cohesion_weight + v2*self.separation_weight + v2_2*self.separation_weight_sheep + v3*self.alignment_weight
        self.update_drone()
        

    def fly_to_position(self, pos):
        step_size = 200
        self.desired_position = pos
        self.velocity = (pos - self.position) * (step_size / 100)

        if (self.desired_position[0] -15 <= self.position[0] <= self.desired_position[0] + 15) and (self.desired_position[1] - 15 <= self.position[1] <= self.desired_position[1] + 15):
            self.path_goal = True


    def fly_to_edge_guidance_law(self, extended_hull):
        shortest_b = (math.inf, math.inf)   # Korteste distansen mellom drone og (saue)kant
        i = 0
        bt_list = []
        des_pos = []
        # print(extended_hull)
        if len(extended_hull) != 0:
            for corner in extended_hull:
                E_j = corner
                if i == len(extended_hull)-1:
                    E_j_p = extended_hull[0]
                else:
                    E_j_p = extended_hull[i+1]
                
                q_t = (E_j_p[0] - E_j[0], E_j_p[1] - E_j[1])
                p_t = (E_j_p[0] - self.position[0], E_j_p[1] - self.position[1])

                if np.dot(p_t, q_t) < 0:
                    b_t = (-p_t[0], -p_t[1])
                    des_pos.append(E_j_p)
                    bt_list.append(b_t)
                elif (np.dot(p_t, q_t) > 0) and (np.linalg.norm(q_t) >= np.linalg.norm(p_t)):
                    o_t = ((np.linalg.norm(q_t)**(-1) * np.dot(p_t, q_t)) * np.linalg.norm(q_t)**(-1) * (q_t[0]), (np.linalg.norm(q_t)**(-1) * np.dot(p_t, q_t)) * np.linalg.norm(q_t)**(-1) * (q_t[1]))
                    des_pos.append(np.subtract(E_j_p, o_t))
                    b_t = (o_t[0] - p_t[0], o_t[1] - p_t[1])
                    bt_list.append(b_t)
                else:
                    b_t = (q_t[0] - p_t[0], q_t[1] - p_t[1])
                    des_pos.append(E_j)
                    bt_list.append(b_t)
                i += 1
                if np.linalg.norm(shortest_b) > np.linalg.norm(b_t):
                    shortest_b = b_t

            self.desired_position = des_pos[bt_list.index(shortest_b)]

        a_t = [-2,-2]
        self.b_t = shortest_b
        self.rotation_velocity = self.max_rot_vel * self.g(a_t, self.b_t) * self.F(a_t, self.b_t)
        self.velocity = self.max_speed * self.g(a_t, self.b_t)

        if -5 <= self.b_t[0] <= 5 and -5 <= self.b_t[1] <= 5:
            self.extended_hull_goal = True


    def fly_on_edge_guidance_law(self, extended_hull, desired_position):
        desired_position_to_vertex = math.inf   # distance
        drone_to_vertex = math.inf
        closest_desired_position_index = 0
        closest_drone_index = 0

        i = 0
        for vertex in extended_hull:
            des_pos_vertex = np.linalg.norm(desired_position-vertex)
            if des_pos_vertex < desired_position_to_vertex:
                desired_position_to_vertex = des_pos_vertex
                closest_desired_position_index = i

            drone_vertex = np.linalg.norm(self.position-vertex)
            if drone_vertex < drone_to_vertex:
                drone_to_vertex = drone_vertex
                closest_drone_index = i

            i += 1

        path_1 = []
        path_2 = []
        path_1_length = 0
        path_2_length = 0

        if closest_desired_position_index < closest_drone_index:
            path_1 = extended_hull[closest_desired_position_index:closest_drone_index]
            np.append(path_1, desired_position)
            path_2 = extended_hull[closest_drone_index:]
            np.append(path_2, extended_hull[:closest_desired_position_index])
            np.append(path_2, desired_position)
        else:
            path_1 = extended_hull[closest_drone_index:closest_desired_position_index]
            np.append(path_1, desired_position)
            path_2 = extended_hull[closest_desired_position_index:]
            np.append(path_2, extended_hull[:closest_drone_index])
            np.append(path_2, desired_position)
            
        j = 0
        for vertex in path_1:
            if j == len(path_1)-1:
                path_1_length += np.linalg.norm(vertex-path_1[0])
            else: 
                path_1_length += np.linalg.norm(vertex-path_1[j+1])
            j += 1
        
        k = 0
        for vertex in path_2:
            if k == len(path_2)-1:
                path_2_length += np.linalg.norm(vertex-path_2[0])
            else: path_2_length += np.linalg.norm(vertex-path_2[k+1])
            k += 1
        
        if path_1_length < path_2_length:
            for point in path_1:
                self.fly_to_position(point)
        else:
            for point in path_2:
                self.fly_to_position(point)

        if (self.desired_position[0] -5 <= self.position[0] <= self.desired_position[0] + 5) and (self.desired_position[1] - 5 <= self.position[1] <= self.desired_position[1] + 5):
            self.hull_position_goal = True
        """
        # Dronene beveger seg fra kant til kant. Finne raskeste vei rundt til neste desired_position.

        distance_left_drone = math.inf
        distance_right_drone = math.inf
        distance_left_desired_pos = math.inf
        distance_right_desired_pos = math.inf
        closest_vertice_drone = (0,0)
        closest_vertice_desired_pos = (0, 0)
        
        # Distance from drone/ desired position to a vertice
        for i in range(len(extended_hull)):
            if i == len(extended_hull)-1:
                distance_left_drone_new = np.linalg.norm((extended_hull[i][0]-self.position[0], extended_hull[i][1]-self.position[1]))
                distance_right_drone_new = np.linalg.norm((extended_hull[0][0]-self.position[0], extended_hull[0][1] - self.position[1]))
                distance_left_desired_pos_new = np.linalg.norm((extended_hull[i][0]-desired_position[0], extended_hull[i][1]-desired_position[1]))
                distance_right_desired_pos_new = np.linalg.norm((extended_hull[0][0]-desired_position[0], extended_hull[0][1]-desired_position[1]))
                
            else:
                distance_left_drone_new = np.linalg.norm((extended_hull[i][0]-self.position[0], extended_hull[i][1]-self.position[1]))
                distance_right_drone_new = np.linalg.norm((extended_hull[i+1][0]-self.position[0], extended_hull[i+1][1] - self.position[1]))
                distance_left_desired_pos_new = np.linalg.norm((extended_hull[i][0]-desired_position[0], extended_hull[i][1]-desired_position[1]))
                distance_right_desired_pos_new = np.linalg.norm((extended_hull[i+1][0]-desired_position[0], extended_hull[i+1][1]-desired_position[1]))
            
            # Finding the shortest distance between vertice and drone's position
            if distance_left_drone > distance_left_drone_new:
                distance_left_drone = distance_left_drone_new
            if distance_right_drone > distance_right_drone_new:
                distance_right_drone = distance_right_drone_new
            
            # Finding the shortest distance between vertice and desired position
            if distance_left_desired_pos > distance_left_desired_pos_new:
                distance_left_desired_pos = distance_left_desired_pos_new
            if distance_right_desired_pos > distance_right_desired_pos_new:
                distance_right_desired_pos = distance_right_desired_pos_new
            
            #Getting the closest vertice to the drone
            if distance_left_drone < distance_right_drone:
                closest_vertice_drone = extended_hull[i]
            else:
                if i == len(extended_hull)-1:
                    closest_vertice_drone = extended_hull[0]
                else: 
                    closest_vertice_drone = extended_hull[i+1]
            # Getting the closest vertice to the desired position
            if distance_left_desired_pos < distance_right_desired_pos:
                closest_vertice_desired_pos = extended_hull[i]
            else:
                if i == len(extended_hull)-1:
                    closest_vertice_desired_pos = extended_hull[0]
                else:
                    closest_vertice_desired_pos = extended_hull[i+1]

        # Fly drone to the closest vertice
        self.fly_to_position(closest_vertice_drone)   
        
        # Fly from vertice to vertice until drone reaches desired position
        for vertice in extended_hull:
            if vertice[0] != closest_vertice_drone[0] and vertice[1] != closest_vertice_drone[1]:
                break
            elif vertice[0] != closest_vertice_desired_pos[0] and vertice[1] != closest_vertice_desired_pos[1]:
                self.fly_to_position(vertice)
            else:
                print("Arrived desired position on convex hull")
                break
        """    


    def F(self, w_1, w_2):
        f = self.g(w_1, w_2)
        if f == 0:
            F = 0
        elif f != 0:
            F = np.linalg.norm(f)**(-1) * f
        """    
        f = w_2 - np.multiply(np.dot(w_2, w_1), w_1)
        if f[0] == 0 and f[1] == 0:
            F = 0
        elif f[0] != 0 and f[1] != 0:
            F = np.linalg.norm(f)**(-1) * f"""
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
        N = 0   # Total drone number

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

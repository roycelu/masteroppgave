import math
import numpy as np


class Drone:
    def __init__(self, initial_position, id):
        
        self.id = id
        self.position = initial_position
        self.angle = 45

        self.max_speed = 3
        
        #Set initial velocity
        #initial_random_velocity = (np.random.rand(2)-0.5) * self.max_speed * 2
        self.velocity = 0
        self.rotation_velocity = 5
        self.max_rot_vel = 5
        self.acceleration = 0.1

        self.horizon = 100
        self.separation_weight = 10
        self.desired_separation = 30
        
        self.desired_position = initial_position
        
        self.extended_hull_goal = False
        self.hull_position_goal = False
        self.path_goal = False


        self.u_max = 200
        self.b_t = (math.inf, math.inf)

    def draw_drone(self, canvas):
        size = 10
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


    def update_drone(self):
        # Limiting the speed
        if np.linalg.norm(self.velocity) > self.max_speed:
            self.velocity = (self.velocity/np.linalg.norm(self.velocity)) * self.max_speed
        # Then update the position        
        self.position = np.add(self.position, self.velocity)
          

    def main_drone(self, drones, canvas, list_of_sheep):
        v2 = self.separation(drones)
        
        canvas.delete(self.id)
        self.draw_drone(canvas)
        self.velocity += v2*self.separation_weight
        self.update_drone()
        

    def fly_to_position(self, pos):
        step_size = 200
        self.desired_position = pos
        self.velocity = (pos - self.position) * (step_size / 100)

        if (self.desired_position[0] -10 <= self.position[0] <= self.desired_position[0] + 10) and (self.desired_position[1] - 10 <= self.position[1] <= self.desired_position[1] + 10):
            self.path_goal = True


    def fly_to_edge_guidance_law(self, extended_hull):
        shortest_distance = math.inf
        closest_vertex = (math.inf, math.inf)
        if len(extended_hull) != 0: # Sørger for at extended_hull eksisterer
            for vertex in extended_hull:
                if np.linalg.norm(vertex-self.position) < shortest_distance:
                    shortest_distance = np.linalg.norm(vertex-self.position)
                    closest_vertex = vertex
            self.desired_position = closest_vertex
        self.fly_to_position(self.desired_position)
                
        if self.position[0]-5 <= self.desired_position[0] <= self.position[0]+5 and self.position[1]-5 <= self.desired_position[1] <= self.position[1]+5:
            self.extended_hull_goal = True


    def fly_on_edge_guidance_law(self, extended_hull, desired_position):
        desired_position_to_vertex = math.inf   # distance
        drone_to_vertex = math.inf # distance
        closest_desired_position_index = 0
        closest_drone_index = 0

        i = 0
        # Finding the closes vertex to the desired position and the drone's own position
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

        # Creating two paths of vertices, one clockwise, the other counterclockwise
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

        # Finding the length of the two paths    
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
        
        # If the drone is already on the desired position, stay there, else, fly along the shortest path
        if (self.desired_position[0] -10 <= self.position[0] <= self.desired_position[0] + 10) and (self.desired_position[1] - 10 <= self.position[1] <= self.desired_position[1] + 10):
            self.fly_to_position(desired_position)
        else:
            if path_1_length < path_2_length:
                for point in path_1:
                    self.fly_to_position(point)
            else:
                for point in path_2:
                    self.fly_to_position(point)

        if (self.desired_position[0] -5 <= self.position[0] <= self.desired_position[0] + 5) and (self.desired_position[1] - 5 <= self.position[1] <= self.desired_position[1] + 5):
            self.hull_position_goal = True


    def F(self, w_1, w_2):
        f = self.g(w_1, w_2)
        if f == 0:
            F = 0
        elif f != 0:
            F = np.linalg.norm(f)**(-1) * f
        return F
    
    def g(self, w_1, w_2):
        if np.dot(w_1, w_2) > 0:
            g = 1
        elif np.dot(w_1, w_2) <= 0:
            g = -1
        return g
   
        
    def separation(self, nearest_drone):
        # move away from nearest - separation
        c = np.zeros(2)
        
        for drone in nearest_drone:
            if ((np.linalg.norm(drone.position - self.position) < self.horizon)
                    & (np.linalg.norm(drone.position - self.position) < self.desired_separation)
                    & (drone != self)):
                c -= (drone.position - self.position)*(self.separation_weight/100)
        return c

        
import numpy as np


class Sheep:
    def __init__(self, initial_position, id):
        
        self.id = id
        self.position = initial_position
        self.velocity = (np.random.rand(2) - 0.5)*10

        self.acceleration = (np.random.rand(2) - 0.5)/2

        self.max_force = 0.3
        self.max_speed = 0.5
        self.horizon = 100
        
        #Set initial velocity
        #initial_random_velocity = (np.random.rand(2)-0.5) * self.max_speed * 2
        
        self.cohesion_weight = 1
        self.separation_weight = 40
        self.separation_weight_drones = 20
        self.alignment_weight = 20

        self.desired_separation = 10
        self.desired_separation_drones = 45 # Samme avstand som extended_hull og sauene?


    def draw_sheep(self, canvas):
        size = 10
        # Draw the circle around the position (centre)
        x0 = self.position[0] - size/2
        y0 = self.position[1] - size/2
        x1 = self.position[0] + size/2 
        y1 = self.position[1] + size/2
        canvas.create_oval(x0, y0, x1, y1, fill='white', tags=self.id)
        canvas.create_text(self.position[0], self.position[1], text=self.id[-1], tags=self.id)
    
    def update_sheep(self):
        #self.position = np.add(self.position, self.velocity)
        #self.velocity = np.add(self.velocity, self.acceleration)
        # Limiting the speed
        if np.linalg.norm(self.velocity) > self.max_speed:
            self.velocity = (self.velocity/np.linalg.norm(self.velocity)) * self.max_speed # Her er det noe rart kanskje
            #self.velocity = self.max_speed
        # Then update the position
        self.position = np.add(self.position, self.velocity)
        #self.acceleration = np.zeros(2)
        #print('velocity',self.velocity)
    

    def main_sheep(self, list_of_sheep, canvas, list_of_drones):
        for drone in list_of_drones:
            if np.linalg.norm(drone.position - self.position) < self.desired_separation_drones:
                self.max_speed = 1.7
                self.velocity = drone.velocity * self.max_speed # Føler det er noe rart her og
            else:
                self.max_speed = 0.5
                # self.velocity = (desired_position - self.position) # Trenger kanskje ikke denne?
                
        v1 = self.cohesion(list_of_sheep)
        v2 = self.separation(list_of_sheep)
        v2_2 = self.drone_separation(list_of_drones)
        v3 = self.alignment(list_of_sheep)

        self.acceleration = np.add(self.acceleration, v1, v2)
        self.acceleration = np.add(self.acceleration, v2_2, v3)

        canvas.delete(self.id)
        self.draw_sheep(canvas)
        self.update_sheep()
        
    
    def cohesion(self, nearest_sheep):
        steering = np.zeros(2)
        total = 0
        center_of_mass = np.zeros(2)
        for boid in nearest_sheep:
            # Because all boids are the same mass, the center of mass is equal to the average position of them
            if np.linalg.norm(boid.position - self.position) < self.horizon:
                center_of_mass = np.add(center_of_mass, boid.position)
                total += 1
        if total > 0:
            center_of_mass /= total
            # Vector to center of mass
            vec_to_com = center_of_mass - self.position
            # Normalize the vector towards the center of mass, because we want
            if np.linalg.norm(vec_to_com) > 0:
                vec_to_com = (vec_to_com / np.linalg.norm(vec_to_com)) * self.max_speed
            steering = np.subtract(vec_to_com, self.velocity)
            if np.linalg.norm(steering)> self.max_force:
                steering = (steering /np.linalg.norm(steering)) * self.max_force

        return steering
        
        
    def separation(self, nearest_sheep):
        steering = np.zeros(2)
        total = 0
        avg_vector = np.zeros(2)
        for boid in nearest_sheep:
            # Find distance between self and another sheep
            distance = np.linalg.norm(boid.position - self.position)
            # If the two sheep are not in the same spot, find the vector between them divided by the distance between them
            if ((boid.position[0] -5 <= self.position[0] <= boid.position[0] + 5) and (boid.position[1] -5 <= self.position[1] <= boid.position[1] + 5)) and distance < self.horizon:
                diff = self.position - boid.position
                diff = (diff[0]/distance, diff[1]/distance)
                avg_vector = np.add(avg_vector, diff)
                total += 1
        # If there are other sheep close to the sheep
        if total > 0:
            avg_vector /= total
            if np.linalg.norm(steering) > 0:
                avg_vector = (avg_vector / np.linalg.norm(steering)) * self.max_speed
            steering = avg_vector - self.velocity
            if np.linalg.norm(steering) > self.max_force:
                steering = (steering /np.linalg.norm(steering)) * self.max_force

        return steering
              

    def drone_separation(self, nearest_drone):
        # move away from nearest - separation
        steering = np.zeros(2)
        total = 0
        avg_vector = np.zeros(2)
        for drone in nearest_drone:
            if np.linalg.norm(drone.position - self.position) < self.desired_separation_drones:
                diff = self.position - drone.position
                diff /= np.linalg.norm(drone.position - self.position)
                avg_vector = np.add(avg_vector, diff)
                total += 1
        if total > 0:
            avg_vector /= total
            if np.linalg.norm(steering) > 0:
                avg_vector = (avg_vector / np.linalg.norm(steering)) * self.max_speed
            steering = np.subtract(avg_vector, self.velocity)
            if np.linalg.norm(steering) > self.max_force:
                steering = (steering /np.linalg.norm(steering)) * self.max_force

        return steering

    
    def alignment(self, nearest_sheep):
        # orient towards the neighbours - alignment
        steering = np.zeros(2)
        N = 0
        avg_vector = np.zeros(2)
        for sheep in nearest_sheep:
            if np.linalg.norm(sheep.position - self.position) < self.horizon:
                avg_vector = np.add(avg_vector, sheep.velocity)
                N += 1
        # Make sure there are other sheep around
        if N > 0:
            avg_vector /= N
            # Normalize the vector as we only want the direction, and multiply it by the max speed
            avg_vector = (avg_vector / np.linalg.norm(avg_vector)) * self.max_speed
            steering = np.subtract(avg_vector, self.velocity)

        return steering

import numpy as np


class Sheep:
    def __init__(self, initial_position, id):
        
        self.id = id
        self.position = initial_position

        
        self.force = 0
        self.max_force = 5

        self.horizon = 100
        
        #Set initial velocity
        #initial_random_velocity = (np.random.rand(2)-0.5) * self.max_speed * 2
        
        
        self.separation_weight = 40
        self.cohesion_weight = 30
        self.separation_weight_drones = 20
        self.previous_step_weight = 10
        self.alignment_weight = 5
        
        self.random_movement_weight = 2

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
        # Limiting the speed
        if np.linalg.norm(self.force) > self.max_force:
            self.force = (self.force/np.linalg.norm(self.force)) * self.max_speed # Her er det noe rart kanskje
        # Then update the position
        self.position = np.add(self.position, (self.max_speed*self.force))
    

    def main_sheep(self, list_of_sheep, canvas, list_of_drones):
        for drone in list_of_drones:
            if np.linalg.norm(drone.position - self.position) < self.desired_separation_drones:
                self.max_speed = 1.7
                self.velocity = drone.velocity * self.max_speed # Føler det er noe rart her og
            else:
                self.max_speed = 0.5
                # self.velocity = (desired_position - self.position) # Trenger kanskje ikke denne?

                
        v1 = self.cohesion(list_of_sheep)*self.cohesion_weight
        v2 = self.separation(list_of_sheep)*self.separation_weight
        v2_2 = self.drone_separation(list_of_drones)*self.separation_weight_drones
        v3 = self.alignment(list_of_sheep)*self.alignment_weight
        v4 = self.force*self.previous_step_weight
        v5 = (np.random.rand(2) - 0.5)*10*self.random_movement_weight

        self.force = np.add(self.force, v1, v2)
        self.force = np.add(self.force, v2_2, v3) # , v3
        self.force = np.add(self.force, v4, v5)

        canvas.delete(self.id)
        self.draw_sheep(canvas)
        self.update_sheep()
        
    
    def cohesion(self, nearest_sheep):
        steering = np.zeros(2)
        center_of_mass = np.zeros(2)
        
        for sheep in nearest_sheep:
            # Because all boids are the same mass, the center of mass is equal to the average position of them
            if sheep != self:
                if np.linalg.norm(sheep.position - self.position) < self.horizon:
                    center_of_mass = np.add(center_of_mass, sheep.position)
        
        steering = (center_of_mass-self.position) / (np.linalg.norm(center_of_mass-self.position))
        
        return steering
        
        
    def separation(self, nearest_sheep):
        avg_vector = np.zeros(2)
        for sheep in nearest_sheep:
            if self != sheep: # Trenger ikke å separere seg fra seg selv
                distance = np.linalg.norm(self.position - sheep.position)
                if distance <= self.desired_separation:
                    diff = self.position - sheep.position
                    diff = (diff[0]/distance, diff[1]/distance)
                    avg_vector = np.add(avg_vector, diff)

        return avg_vector
              

    def drone_separation(self, nearest_drone):
        # move away from nearest - separation
        avg_vector = np.zeros(2)
        for drone in nearest_drone:
            distance = np.linalg.norm(self.position - drone.position)
            if distance <= self.desired_separation_drones:
                diff = self.position - drone.position
                diff = (diff[0]/distance, diff[1]/distance)
                avg_vector = np.subtract(avg_vector, diff)

        return avg_vector

    
    def alignment(self, nearest_sheep):
        # orient towards the neighbours - alignment
        avg_vector = np.zeros(2)
        for sheep in nearest_sheep:
            distance = np.linalg.norm(self.position - sheep.position)
            if distance <= self.desired_separation:
                diff = self.position - sheep.position
                diff = (diff[0]/distance, diff[1]/distance)
                avg_vector = np.add(avg_vector, diff)

        return avg_vector
       

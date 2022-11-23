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
    
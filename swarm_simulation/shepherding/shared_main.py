import sys
import pygame, time
import numpy as np
from scipy.spatial.transform import Rotation as R
from sheep import Sheep
from circle_drone import CircleDrone
from occlusion_drone import OcclusionDrone
from caging_drone import CagingDrone
from polygon_main_drone import PolygonMainDrone
from polygon_drone import PolygonDrone
from goal import Goal
from utils import Calculate


class SharedMain:

    def __init__(self, id, sheep_positions, no_drones, FPS, dronetype, testtype, initial_goal_vector, initial_goal):
        self.id = id
        self.sheep_positions = sheep_positions
        self.no_drones = no_drones
        self.FPS = FPS
        self.dronetype = dronetype
        self.testtype = testtype
        self.goal_vector = initial_goal_vector
        self.goal = initial_goal


    def draw_center_of_mass(self, canvas, font, sheep):
            center_of_mass = Calculate.center_of_mass(sheep)
            pygame.draw.circle(canvas, pygame.Color("gray"), center_of_mass, 1, 2)

            label = font.render("GCM", True, pygame.Color("black"))
            rect = label.get_rect()
            rect.center = center_of_mass
            canvas.blit(label, rect)

            flock_radius = 0
            for s in sheep:
                distance = np.linalg.norm(s.position-center_of_mass)
                if distance > flock_radius:
                    flock_radius = distance
            
            pygame.draw.circle(canvas, pygame.Color("purple"), center_of_mass, flock_radius, 1)

            potential_field = flock_radius + 50
            pygame.draw.circle(canvas, pygame.Color("pink"), center_of_mass, potential_field, 1)

            return center_of_mass


    def sheep_behaviour(self, sheep_positions):
        sheep_list = []
        i = 0
        for position in sheep_positions:
            sheep_list.append(Sheep(i, position))
            i += 1
        return sheep_list


    def drone_behaviour(self, n):
        drone_list = [x for x in range(n)]
        for i in drone_list:
            x = np.random.randint(200, 220)
            y = np.random.randint(200, 220)
            position = pygame.Vector2(x, y)
            if self.dronetype == "circle":
                drone_list[i] = CircleDrone(i, position)
            if self.dronetype == "occlusion":
                drone_list[i] = OcclusionDrone(i, position, self.FPS)
            if self.dronetype == 'caging':
                drone_list[i] = CagingDrone(i, position)
            if self.dronetype == "polygon":
                drone_list[i] = PolygonDrone(i, position)
        return drone_list


    def main(self):
        pygame.init()
        pygame.display.set_caption("The shepherding problem")

        screen = pygame.display.set_mode((1000, 1000))
        label_font = pygame.font.SysFont("Times New Roman", 12)

        sheep = self.sheep_behaviour(self.sheep_positions)
        drones = self.drone_behaviour(self.no_drones)
        main_drone = None

        if self.dronetype == 'polygon':
            main_drone = PolygonMainDrone(screen, label_font, self.goal, drones, sheep)

        running = True
        goals_reached = 0
        while running:
            

            goal_count = np.zeros(len(sheep))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()
                    sys.exit()

            screen.fill(pygame.Color("darkgreen"))
            self.goal.draw(screen, label_font)

            centre_of_mass = self.draw_center_of_mass(screen, label_font, sheep)

            if main_drone != None:
                main_drone.run(drones, sheep, self.goal, centre_of_mass)


            for s in sheep:
                s.draw(screen, label_font)
                sheep_id_goal_reached = s.move(self.goal, sheep, drones)
                if sheep_id_goal_reached:
                    goal_count[s.id] = 1
                else:
                    goal_count[s.id] = 0
                    
            for drone in drones:
                drone.draw(screen, label_font)
                drone.move(self.goal, drones, sheep, self.goal_vector, screen)
        

            pygame.display.update()
            pygame.time.Clock().tick_busy_loop(self.FPS)

            count = 0
            for value in goal_count:
                if value == 1:
                    count += 1
                else:
                    break
            
            
            sek = 1/self.FPS
            if count == len(self.sheep_positions):
                
                if goals_reached == 1 and self.testtype == "right_angle":
                    print('ja')
                    successrate = (count / len(self.sheep_positions)) * 100
                    herdtime = pygame.time.get_ticks() / (sek * 1000)
                    pygame.quit()
                    return successrate, herdtime
                
                elif self.testtype == "right_angle":
                    sheep_alignment_vector = pygame.Vector2(0, 0)
                    for s in sheep:
                        sheep_alignment_vector += s.acceleration / np.linalg.norm(s.acceleration)
                    sheep_alignment_vector /= len(sheep)
                    rotation_radians = np.radians(90)
                    newX = sheep_alignment_vector.x * np.cos(rotation_radians) - sheep_alignment_vector.y * np.sin(rotation_radians)
                    newY = sheep_alignment_vector.x * np.sin(rotation_radians) + sheep_alignment_vector.y * np.cos(rotation_radians)
                    vector = pygame.Vector2(newX, newY)
                    self.goal_vector += vector*200
                    self.goal = Goal(self.goal_vector)
                    goals_reached += 1    
                
                else:
                    successrate = (count / len(self.sheep_positions)) * 100
                    herdtime = pygame.time.get_ticks() / (sek * 1000)
                    pygame.quit()
                    return successrate, herdtime

            if pygame.time.get_ticks() > 50000:   
                successrate = (count / len(self.sheep_positions)) * 100
                herdtime = pygame.time.get_ticks() / (sek * 1000)
                pygame.quit()     
                return successrate, herdtime  
                    




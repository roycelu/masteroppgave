from datetime import datetime
import os
import sys
import pygame, time
import numpy as np
from sheep import Sheep
from circle_drone import CircleDrone
from polygon_main_drone import PolygonMainDrone
from polygon_drone import PolygonDrone
from v_drone import VDrone
from our_drone_polygon import OurDronePolygon
from our_main_drone_polygon import OurMainDronePolygon
from goal import Goal
from utils import Calculate


class SharedMain:
    def __init__(self, id, sheep_positions, no_drones, FPS, dronetype, testtype, perception, results_path):
        self.id = id
        self.sheep_positions = sheep_positions
        self.no_drones = no_drones
        self.FPS = FPS
        self.dronetype = dronetype
        self.testtype = testtype
        self.goal_vector = pygame.Vector2(500, 600)
        self.goal = Goal(self.goal_vector)
        self.sheep_away = False
        self.perception = perception
        self.results_path = results_path

    
    def draw_center_of_mass(self, canvas, font, sheep):
        center_of_mass = Calculate.center_of_mass(sheep)
        pygame.draw.circle(canvas, pygame.Color("black"), center_of_mass, 2)

        # label = font.render("COM", True, pygame.Color("black"))
        # rect = label.get_rect()
        # rect.center = center_of_mass
        # canvas.blit(label, rect)

        flock_radius = 0
        for s in sheep:
            distance = np.linalg.norm(s.position-center_of_mass)
            if distance > flock_radius:
                flock_radius = distance
        
        pygame.draw.circle(canvas, pygame.Color("purple"), center_of_mass, flock_radius, 1)

        return center_of_mass


    def sheep_behaviour(self, sheep_positions):
        # Create sheep
        sheep_list = []
        i = 0
        for position in sheep_positions:
            sheep_list.append(Sheep(i, position, self.perception))
            i += 1

        return sheep_list


    def drone_behaviour(self, n):
        # Create drones
        drone_list = [x for x in range(n)]
        for i in drone_list:
            x = np.random.randint(200, 220)
            y = np.random.randint(200, 220)
            position = pygame.Vector2(x, y)
            if self.dronetype == "circle":
                drone_list[i] = CircleDrone(i, position)
            if self.dronetype == 'v':
                drone_list[i] = VDrone(i, position)
            if self.dronetype == "polygon":
                drone_list[i] = PolygonDrone(i, position)
            if self.dronetype == "our":
                drone_list[i] = OurDronePolygon(i, position)
        return drone_list


    def capture_screenshot(self, clock_time, screen, capture_times):
        time = int(round(clock_time, -1)) # Runder av tiden til nærmste 10'er
        # Take the screenshot every 10 simulation
        if self.id % 10 == 0 and time in capture_times: # Listen med 'tidspunkter' fastsettes i testen

            # Creates a directory to save the screenshots, if it not already exists
            path = '{}/screenshots/{}_{}'.format(self.results_path, self.id, self.dronetype)
            if not os.path.exists(path):
                os.makedirs(path)
            
            # print("klikk klikk", clock_time, time)
            text = pygame.font.SysFont("Times New Roman", 25)
            text = text.render('Testscenario: {}  |  Synsrekkevidde: {}'.format(self.testtype, self.perception), True, pygame.Color("black"), pygame.Color("white"))
            rect = text.get_rect()
            rect.left, rect.bottom = 10, screen.get_height()-10
            screen.blit(text, rect)

            text2 = pygame.font.SysFont("Times New Roman", 25)
            text2 = text2.render('TestID: {}  |  Tid: {} | Dronemetode: {}'.format(self.id, time, self.dronetype), True, pygame.Color("black"), pygame.Color("white"))
            rect = text2.get_rect()
            rect.left, rect.bottom = 10, screen.get_height()-15-rect.height
            screen.blit(text2, rect)
            
            image = screen.copy()
            pygame.image.save(image, '{path}/{time}_{t}{p}.png'.format(path=path, time=time, t=self.testtype, p=self.perception))        


    def main(self, time_limit, target_fps, capture_times):
        pygame.init()
        pygame.display.set_caption("The shepherding problem - existing methods")

        screen = pygame.display.set_mode((1000, 1000))
        label_font = pygame.font.SysFont("Times New Roman", 12)

        sheep = self.sheep_behaviour(self.sheep_positions)
        drones = self.drone_behaviour(self.no_drones)
        
        main_drone = None
        if self.dronetype == 'polygon':
            main_drone = PolygonMainDrone(screen, self.goal, drones, sheep)
        if self.dronetype == 'our':
            main_drone = OurMainDronePolygon(screen, self.goal, drones, sheep)

        clock = pygame.time.Clock()
        prev_time = time.time()
        dt = 0

        prev_time_herding = 0
        herd_time = 0
        collect_time = 0
        running = True

        goals_reached = 0
        while running:
            # Limit framerate
            clock.tick(target_fps)
            # Compute delta time
            now = time.time()
            dt = now - prev_time
            prev_time = now


            goal_count = np.zeros(len(sheep))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()
                    sys.exit()

            screen.fill(pygame.Color("palegreen3"))
            self.goal.draw(screen, label_font)

            centre_of_mass = self.draw_center_of_mass(screen, label_font, sheep)

            if main_drone != None:
                main_drone.run(drones, sheep, self.goal, centre_of_mass)


            sek = 1/self.FPS

            reached_goal_time_list = []
            reached_goal_number = []
            sheep_count = 0
            all_sheep = False

            # Make sheep move
            for s in sheep:
                s.draw(screen, label_font)
                sheep_id_goal_reached = s.move(self.goal, sheep, drones, dt, target_fps)
                # Keep track of whether sheep have reached the goal or not
                if sheep_id_goal_reached:
                    goal_count[s.id] = 1
                    reached_goal_time_list.append(pygame.time.get_ticks()/1000)
                    sheep_count += 1
                    reached_goal_number.append(sheep_count)
                else:
                    goal_count[s.id] = 0
                
                if np.linalg.norm(s.position - centre_of_mass) < 20:
                    if self.sheep_away == False:
                        self.sheep_away = True
                        curr_time = pygame.time.get_ticks()
                        collect_time += (curr_time - prev_time_herding)
                        prev_time_herding = curr_time
                    all_sheep = True
            
            if all_sheep == False and self.sheep_away == True:
                self.sheep_away = False
                curr_time = pygame.time.get_ticks() 
                herd_time += (curr_time - prev_time_herding)
                prev_time_herding = curr_time
     
            # Make drones move
            for drone in drones:
                drone.draw(screen, label_font)
                drone.move(self.goal, drones, sheep, screen, dt, target_fps)
        

            count = 0
            for value in goal_count:
                if value == 1:
                    count += 1
                else:
                    break

            
            # Øyeblikksbilder av simuleringen på gitte tidspunkt
            self.capture_screenshot(pygame.time.get_ticks() / (sek * 1000), screen, capture_times)


            # If the test i "right angle", make new goal when first goal is reached
            if count == len(self.sheep_positions):
                if goals_reached == 1 and self.testtype == "right_angle":
                    successrate = (count / len(self.sheep_positions)) * 100
                    herdtime = pygame.time.get_ticks() / (sek * 1000)
                    herd_time += (pygame.time.get_ticks() - prev_time_herding)
                    herd_time /= (sek * 1000)
                    collect_time /= (sek * 1000)
                    pygame.quit()
                    return successrate, herdtime, reached_goal_time_list, reached_goal_number, collect_time, herd_time
                
                elif self.testtype == "right_angle":
                    sheep_alignment_vector = pygame.Vector2(0, 0)
                    for s in sheep:
                        if np.linalg.norm(s.velocity) != 0:
                            sheep_alignment_vector += s.velocity / np.linalg.norm(s.velocity)
                    sheep_alignment_vector /= len(sheep)
                    rotation_radians = np.radians(90)
                    newX = sheep_alignment_vector.x * np.cos(rotation_radians) - sheep_alignment_vector.y * np.sin(rotation_radians)
                    newY = sheep_alignment_vector.x * np.sin(rotation_radians) + sheep_alignment_vector.y * np.cos(rotation_radians)
                    vector = pygame.Vector2(newX, newY)
                    vector.scale_to_length(200) # Sørger for lik avstand hver gang
                    self.goal_vector += vector
                    self.goal = Goal(self.goal_vector)
                    goals_reached += 1    
                
                else:
                    successrate = (count / len(self.sheep_positions)) * 100
                    herdtime = pygame.time.get_ticks() / (sek * 1000)
                    herd_time += (pygame.time.get_ticks() - prev_time_herding)
                    herd_time /= (sek * 1000)
                    collect_time /= (sek * 1000)
                    pygame.quit()
                    return successrate, herdtime, reached_goal_time_list, reached_goal_number, collect_time, herd_time

            if pygame.time.get_ticks() > time_limit:   
                successrate = (count / len(self.sheep_positions)) * 100
                herdtime = pygame.time.get_ticks() / (sek * 1000)
                herd_time += (pygame.time.get_ticks() - prev_time_herding)
                herd_time /= (sek * 1000)
                collect_time /= (sek * 1000)
                pygame.quit()     
                return successrate, herdtime, reached_goal_time_list, reached_goal_number, collect_time, herd_time

            pygame.display.update()
            pygame.time.Clock().tick_busy_loop(self.FPS)
            
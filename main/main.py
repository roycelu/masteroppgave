import os
import sys
import pygame, time
import numpy as np
from models.sheep import Sheep
from models.our_drone_vpolygon import OurDroneVPolygon
from models.our_drone_com import OurDroneCom
from models.our_main_drone_com import OurMainDroneCom
from models.our_main_drone_vpolygon import OurMainDroneVPolygon
from models.goal import Goal
from utils import Calculate


class Main:
    def __init__(self, id, sheep_positions, no_drones, FPS, collect_type, testtype, theta, results_path):
        self.id = id
        self.sheep_positions = sheep_positions
        self.no_drones = no_drones
        self.FPS = FPS
        self.collect_type = collect_type
        self.testtype = testtype
        self.goal_vector = pygame.Vector2(500, 600)
        self.goal = Goal(self.goal_vector)
        self.sheep_away = False
        self.theta = theta
        self.perception = 40
        self.results_path = results_path

    
    def draw_center_of_mass(self, canvas, font, sheep):
        center_of_mass = Calculate.center_of_mass(sheep)
        pygame.draw.circle(canvas, pygame.Color("black"), center_of_mass, 2)

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
            if self.collect_type == "v_polygon":
                drone_list[i] = OurDroneVPolygon(i, position)
            if self.collect_type == "com":
                drone_list[i] = OurDroneCom(i, position)
        return drone_list
    

    def capture_screenshot(self, clock_time, screen, capture_times):
        time = int(round(clock_time)) 
        # Take the screenshot every 20 simulation
        if self.id % 20 == 0 and time in capture_times: # List of times is s in the test

            # Creates a directory to save the screenshots, if it not already exists
            path = '{}/screenshots/{}_{}'.format(self.results_path, self.id, self.collect_type)
            if not os.path.exists(path):
                os.makedirs(path)
            
            text = pygame.font.SysFont("Times New Roman", 25)
            text = text.render('Testscenario: {}  |  Vinkel: {}'.format(self.testtype, self.theta), True, pygame.Color("black"), pygame.Color("white"))
            rect = text.get_rect()
            rect.left, rect.bottom = 10, screen.get_height()-10
            screen.blit(text, rect)

            text2 = pygame.font.SysFont("Times New Roman", 25)
            text2 = text2.render('TestID: {}  |  Tid: {} | Dronemetode: {}'.format(self.id, time, self.collect_type), True, pygame.Color("black"), pygame.Color("white"))
            rect = text2.get_rect()
            rect.left, rect.bottom = 10, screen.get_height()-15-rect.height
            screen.blit(text2, rect)
            
            image = screen.copy()
            pygame.image.save(image, '{path}/{time}_{t}{a}.png'.format(path=path, time=time, t=self.testtype, a=self.theta))        


    def main(self, time_limit, target_fps, capture_times):
        pygame.init()
        pygame.display.set_caption("The shepherding problem - our method")

        screen = pygame.display.set_mode((1000, 1000))
        label_font = pygame.font.SysFont("Times New Roman", 12)

        sheep = self.sheep_behaviour(self.sheep_positions)
        drones = self.drone_behaviour(self.no_drones)
        
        our_main_drone = None
        if self.collect_type == 'v_polygon':
            our_main_drone = OurMainDroneVPolygon(screen, self.goal, drones, sheep, self.theta)
        if self.collect_type == 'com':
            our_main_drone = OurMainDroneCom(screen, self.goal, drones, sheep, self.theta)


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

            if our_main_drone != None:
                our_main_drone.run(drones, sheep, self.goal, centre_of_mass, dt, target_fps)


            seconds = pygame.time.get_ticks() / (1000)

            sheep_count = 0
            all_sheep = False

            # Make sheep move
            for s in sheep:
                s.draw(screen, label_font)
                sheep_id_goal_reached = s.move(self.goal, sheep, drones, dt, target_fps)
                # Keep track of whether sheep have reached the goal or not
                if sheep_id_goal_reached:
                    goal_count[s.id] = 1
                    sheep_count += 1
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
                #if our_main_drone_name != 'our':
                #    drone.move(self.goal, drones, sheep, screen, dt, target_fps)
        

            count = 0
            for value in goal_count:
                if value == 1:
                    count += 1
                else:
                    break


            # Screenshots at a given time
            self.capture_screenshot(seconds, screen, capture_times)

            
            # If the test i "right angle", make new goal when first goal is reached
            # If the time limit is reached, stop the simulation
            if count == len(self.sheep_positions):
                if goals_reached == 1 and self.testtype == "right_angle":
                    successrate = (count / len(self.sheep_positions)) * 100
                    herdtime = seconds
                    herd_time += (pygame.time.get_ticks() - prev_time_herding)
                    herd_time /= (1000)
                    collect_time /= (1000)
                    pygame.quit()
                    return successrate, herdtime, collect_time, herd_time
                
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
                    self.goal_vector += vector*200
                    self.goal = Goal(self.goal_vector)
                    goals_reached += 1    
                
                else:
                    successrate = (count / len(self.sheep_positions)) * 100
                    herdtime = seconds
                    herd_time += (pygame.time.get_ticks() - prev_time_herding)
                    herd_time /= (1000)
                    collect_time /= (1000)
                    pygame.quit()
                    return successrate, herdtime, collect_time, herd_time

            if seconds > time_limit:   
                successrate = (count / len(self.sheep_positions)) * 100
                herdtime = seconds
                herd_time += (pygame.time.get_ticks() - prev_time_herding)
                herd_time /= (1000)
                collect_time /= (1000)
                pygame.quit()     
                return successrate, herdtime, collect_time, herd_time 


            pygame.display.update()
            pygame.time.Clock().tick_busy_loop(self.FPS)

import sys
import pygame, time
import numpy as np
from sheep import Sheep
from circle_drone import CircleDrone
from polygon_main_drone import PolygonMainDrone
from polygon_drone import PolygonDrone
from v_drone import VDrone
from goal import Goal
from utils import Calculate


class SharedMain:
    def __init__(self, id, sheep_positions, no_drones, FPS, dronetype, testtype):
        self.id = id
        self.sheep_positions = sheep_positions
        self.no_drones = no_drones
        self.FPS = FPS
        self.dronetype = dronetype
        self.testtype = testtype
        self.goal_vector = pygame.Vector2(500, 600)
        self.goal = Goal(self.goal_vector)
        self.sheep_away = False

    
    def draw_center_of_mass(self, canvas, font, sheep):
        center_of_mass = Calculate.center_of_mass(sheep)
        pygame.draw.circle(canvas, pygame.Color("gray"), center_of_mass, 1, 2)

        label = font.render("COM", True, pygame.Color("black"))
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
            if self.dronetype == 'v':
                drone_list[i] = VDrone(i, position)
            if self.dronetype == "polygon":
                drone_list[i] = PolygonDrone(i, position)
        return drone_list


    def main(self, time_limit, target_fps):
        pygame.init()
        pygame.display.set_caption("The shepherding problem")

        screen = pygame.display.set_mode((1000, 1000))
        label_font = pygame.font.SysFont("Times New Roman", 12)

        sheep = self.sheep_behaviour(self.sheep_positions)
        drones = self.drone_behaviour(self.no_drones)
        main_drone = None

        if self.dronetype == 'polygon':
            main_drone = PolygonMainDrone(screen, self.goal, drones, sheep)

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

            screen.fill(pygame.Color("darkgreen"))
            self.goal.draw(screen, label_font)

            centre_of_mass = self.draw_center_of_mass(screen, label_font, sheep)

            if main_drone != None:
                main_drone.run(drones, sheep, self.goal, centre_of_mass)

            sek = 1/self.FPS

            reached_goal_time_list = []
            reached_goal_number = []
            sheep_count = 0
            all_sheep = False
            for s in sheep:
                s.draw(screen, label_font)
                sheep_id_goal_reached = s.move(self.goal, sheep, drones, dt, target_fps)
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
     

            for drone in drones:
                drone.draw(screen, label_font)
                drone.move(self.goal, drones, sheep, screen, dt, target_fps)
        
 

            count = 0
            for value in goal_count:
                if value == 1:
                    count += 1
                else:
                    break

            
            if count == len(self.sheep_positions):
                if goals_reached == 1 and self.testtype == "right_angle":
                    successrate = (count / len(self.sheep_positions)) * 100
                    herdtime = pygame.time.get_ticks() / (sek * 1000)
                    # print('herdtime 1', herdtime)
                    # print('prev_time herding 1', prev_time_herding)
                    herd_time += (pygame.time.get_ticks() - prev_time_herding)
                    # print('collect time 1', collect_time)
                    # print('herd time 1', herd_time)
                    herd_time /= (sek * 1000)
                    collect_time /= (sek * 1000)
                    # print('collect time 1 after', collect_time)
                    # print('herd time 1 after', herd_time)
                    pygame.quit()
                    return successrate, herdtime, reached_goal_time_list, reached_goal_number, collect_time, herd_time
                
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
                    # print('herdtime 2', herdtime)
                    # print('prev_time herding 2', prev_time_herding)
                    herd_time += (pygame.time.get_ticks() - prev_time_herding)
                    # print('collect time 2', collect_time)
                    # print('herd time 2', herd_time)
                    herd_time /= (sek * 1000)
                    collect_time /= (sek * 1000)
                    # print('collect time 2 after', collect_time)
                    # print('herd time 2 after', herd_time)
                    pygame.quit()
                    return successrate, herdtime, reached_goal_time_list, reached_goal_number, collect_time, herd_time

            if pygame.time.get_ticks() > time_limit:   
                successrate = (count / len(self.sheep_positions)) * 100
                herdtime = pygame.time.get_ticks() / (sek * 1000)
                # print('herdtime 3', herdtime)
                # print('prev_time herding 3', prev_time_herding)
                herd_time += (pygame.time.get_ticks() - prev_time_herding)
                # print('collect time 3', collect_time)
                # print('herd time 3', herd_time)
                herd_time /= (sek * 1000)
                collect_time /= (sek * 1000)
                # print('collect time 3 after', collect_time)
                # print('herd time 3 after', herd_time)
                pygame.quit()     
                return successrate, herdtime, reached_goal_time_list, reached_goal_number, collect_time, herd_time 


            pygame.display.update()
            pygame.time.Clock().tick_busy_loop(self.FPS)
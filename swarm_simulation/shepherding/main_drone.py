import pygame
import numpy as np
from utils import Calculate
from royce_moira_method import RoyceMoiraMethod

SIZE = 5


class MainDrone:
    def __init__(self, canvas, font, drones, sheeps, goal):
        self.canvas = canvas
        self.font = font
        self.drones = drones
        self.sheeps = sheeps
        self.goal = goal
        self.figure = pygame.Rect(0, 0, SIZE * 2, SIZE * 2)

    def draw_center_of_mass(self, canvas, font, sheeps):
        center_of_mass = Calculate.center_of_mass(sheeps)
        self.figure.center = center_of_mass
        pygame.draw.rect(
            canvas,
            pygame.Color("gray"),
            self.figure,
            border_radius=int(SIZE),
        )

        label = font.render("GCM", True, pygame.Color("black"))
        rect = label.get_rect()
        rect.center = center_of_mass
        canvas.blit(label, rect)

    # def update_goal(self, drone, new_position):
    #     self.goal.position = new_position
    #     drone.fly_to_position(new_position)
    #     drone.goal_status = False
    #     return new_position

    def main(self):
        new_goal_position = pygame.Vector2(
            np.random.randint(100, 900),
            np.random.randint(100, 900),
        )

        for sheep in self.sheeps:
            sheep.move(self.goal, self.sheeps, self.drones)

        for drone in self.drones:
            drone.move(self.goal, self.drones, self.sheeps)
            drone.fly_to_position(self.goal.position)

            # if drone.goal_status == True:
            #     print("{id} has reached the goal".format(id="drone" + str(drone.id)))
            #     self.update_goal(drone, new_goal_position)

        # self.draw_center_of_mass(self.canvas, self.font, self.sheeps)

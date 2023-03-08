import pygame
import numpy as np
from utils import Calculate
from royce_moira_method import RoyceMoiraMethod
from polygon_method import PolygonMethod

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

    # TODO: Sender ny målposisjon når målet er nådd
    # def update_goal(self, drone, new_position):
    #     self.goal.position = new_position
    #     drone.fly_to_position(new_position)
    #     drone.goal_status = False
    #     return new_position

    # TODO: Ikke testet ennå, men tanken er at metoden skal telle antall sauer i mål
    def amount_sheeps_in_goal(self, sheeps):
        amount = []
        for sheep in sheeps:
            if sheep.id not in amount:
                amount.append(sheep.id)
        if len(amount) == len(sheeps):
            print("Shepherding accomplished")
        return len(amount)

    def main(self):
        new_goal_position = pygame.Vector2(
            np.random.randint(100, 900),
            np.random.randint(100, 900),
        )

        # TODO: Unngår at sauene beveger seg, lettere å teste metode
        # for sheep in self.sheeps:
        #     sheep.move(self.goal, self.sheeps, self.drones)

        for drone in self.drones:
            drone.move(self.goal, self.drones, self.sheeps)
            # drone.fly_to_position(self.goal.position)

            # if drone.goal_status == True:
            #     print("{id} has reached the goal".format(id="drone" + str(drone.id)))
            #     self.update_goal(drone, new_goal_position)

        method1 = RoyceMoiraMethod(
            self.canvas, self.font, self.goal, self.drones, self.sheeps
        )

        method2 = PolygonMethod(
            self.canvas, self.font, self.goal, self.drones, self.sheeps
        )
        method2.main(self.drones, self.sheeps, self.goal)

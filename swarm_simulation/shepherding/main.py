import sys
import pygame
import numpy as np
from sheep import Sheep
from drone import Drone
from goal import Goal
from main_drone import MainDrone
from polygon_method import PolygonMethod

FPS = 50  # Hastigheten på simuleringen
NO_OF_SHEEP = 5
NO_OF_DRONES = 3


def sheep_behaviour(n):
    sheep_list = [x for x in range(n)]
    for i in sheep_list:
        x = np.random.randint(400, 500)
        y = np.random.randint(400, 500)
        position = pygame.Vector2(x, y)
        sheep_list[i] = Sheep(i, position)
    return sheep_list


def drone_behaviour(n):
    drone_list = [x for x in range(n)]
    for i in drone_list:
        x = np.random.randint(800, 820)
        y = np.random.randint(60, 82)
        position = pygame.Vector2(x, y)
        drone_list[i] = Drone(i, position)
    return drone_list


def main():
    pygame.init()
    pygame.display.set_caption("The shepherding problem")

    screen = pygame.display.set_mode((1000, 1000))
    label_font = pygame.font.SysFont("Times New Roman", 12)

    goal = Goal(pygame.Vector2(850, 50))
    sheeps = sheep_behaviour(NO_OF_SHEEP)
    drones = drone_behaviour(NO_OF_DRONES)
    main_drone = MainDrone(screen, label_font, drones, sheeps, goal)

    polygon_method = PolygonMethod(screen, label_font, goal, drones, sheeps)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()

        screen.fill(pygame.Color("darkgreen"))
        goal.draw(screen, label_font)

        main_drone.draw_center_of_mass(screen, label_font, sheeps)
        # main_drone.main()  # Run the methods determined by the main drone (the brain)
        polygon_method.main(drones, sheeps, goal)

        for sheep in sheeps:
            sheep.draw(screen, label_font)
            sheep.move(goal, sheeps, drones)

        for drone in drones:
            drone.draw(screen, label_font)
            drone.move(goal, drones, sheeps)

        pygame.display.update()
        pygame.time.Clock().tick(FPS)


if __name__ == "__main__":
    main()

import sys
import pygame
import numpy as np
from sheep import Sheep

FPS = 500  # Hastigheten på simuleringen?
no_of_sheep = 5
no_of_drones = 3


def sheep_behaviour(n):
    sheep_list = [x for x in range(n)]
    for i in sheep_list:
        x = np.random.randint(300, 400)
        y = np.random.randint(300, 400)
        position = pygame.Vector2(x, y)
        sheep_list[i] = Sheep(i, position)
    return sheep_list


def main():
    pygame.init()
    pygame.display.set_caption("The shepherding problem")

    screen = pygame.display.set_mode((1000, 1000))
    label_font = pygame.font.SysFont("Times New Roman", 15)

    sheeps = sheep_behaviour(no_of_sheep)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()

        screen.fill(pygame.Color("darkgreen"))

        for sheep in sheeps:
            sheep.draw(screen, label_font)
            # sheep.update()
            sheep.move(sheeps)

        pygame.display.update()
        pygame.time.Clock().tick(FPS)


if __name__ == "__main__":
    main()

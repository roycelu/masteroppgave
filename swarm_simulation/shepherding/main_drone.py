import pygame
import numpy as np

SIZE = 5


class MainDrone:
    def __init__(self, canvas, drones, sheeps, goal):
        self.canvas = canvas
        self.drones = drones
        self.sheeps = sheeps
        self.goal = goal
        self.figure = pygame.Rect(0, 0, SIZE * 2, SIZE * 2)

    def calculate_center_of_mass(self, sheeps):
        center_of_mass = pygame.Vector2(0, 0)
        if len(sheeps) > 0:
            for sheep in sheeps:
                center_of_mass += sheep.position
            center_of_mass /= len(sheeps)
        return center_of_mass

    def draw_center_of_mass(self, canvas, font, sheeps):
        center_of_mass = self.calculate_center_of_mass(sheeps)
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

    def drive():
        pass

    def gather():
        pass

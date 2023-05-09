import pygame
import numpy as np


class Goal:
    def __init__(self, initial_position):
        self.position = initial_position
        self.vertices = []  # På sikt holde på alle punktene langs path
        self.figure = pygame.Rect(0, 0, 25, 25)

    def draw(self, canvas, font):
        self.figure.center = self.position
        pygame.draw.rect(canvas, pygame.Color("red"), self.figure)

        # label = font.render("GOAL", True, pygame.Color("black"))
        # rect = label.get_rect()
        # rect.center = self.position
        # canvas.blit(label, rect)

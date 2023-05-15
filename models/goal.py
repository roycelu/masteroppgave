import pygame


class Goal:
    def __init__(self, initial_position):
        self.position = initial_position
        self.figure = pygame.Rect(0, 0, 25, 25)

    def draw(self, canvas, font):
        self.figure.center = self.position
        pygame.draw.rect(canvas, pygame.Color("red"), self.figure)


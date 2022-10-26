from turtle import position
import pygame
import random

from sheep import Sheep
from shepherd import Shepherd

""" draw the object """

FPS = 60  # Unsure if it has an impact on the code

GREEN = pygame.Color('green')
RED = pygame.Color('red')


class Environment:

    def __init__(self, dimentions, goal):
        self.mapW, self.mapH = dimentions   # Width and height of the map
        self.goal = goal    # x- and y-coords of the goal region

        pygame.init()
        self.name = 'Royce'
        pygame.display.set_caption(self.name)
        self.canvas = pygame.display.set_mode((self.mapW, self.mapH))
        self.shepherds = [Shepherd(1, (0, 0)), Shepherd(2, (0, 150))]

    def draw(self, i):
        # for sheep in HERD:
        #     sheep.move(FPS)
        #     pygame.draw.circle(self.canvas, RED, sheep.position, sheep.size)

        sheep = {}
        sheep["size"] = 10
        #sheep["position"] = pygame.Vector2(pygame.mouse.get_pos())
        sheep["position"] = pygame.Vector2(i, 100)
        sheep["velocity"] = pygame.Vector2(50, 50)
        pygame.draw.circle(self.canvas, RED, sheep["position"], sheep["size"])

        for shepherd in self.shepherds:
            shepherd.move(FPS, sheep["position"], sheep["velocity"])
            pygame.draw.circle(self.canvas, GREEN,
                               shepherd.position, shepherd.size)

import random
import pygame
import math
import time
import sys
from sklearn.neighbors import NearestNeighbors
import warnings

NAME = 'Royce'
DIMENTIONS = (1000, 600)
WHITE = (255, 255, 255)

pygame.init()
canvas = pygame.display.set_mode(DIMENTIONS)
pygame.mouse.set_visible(False)

RUNNING = True

while RUNNING:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            RUNNING = False
            pygame.quit()
    # BUTTER_FACE.position = pygame.mouse.get_pos()   # "Hunden"
    # map.canvas.fill(WHITE)
    canvas.fill(WHITE)  # An empty window with a white background
    pygame.display.update()

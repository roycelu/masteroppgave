import pygame
import numpy as np
import scipy
import shapely.geometry as shp
from utils import Calculate


class RoyceMoiraMethod:
    def __init__(self, goal, drones, sheeps):
        self.goal = goal
        self.drones = drones
        self.sheeps = sheeps

    def create_convex_hull(self, sheeps):
        center_of_mass = Calculate.center_of_mass(sheeps)
        print(center_of_mass)

    def draw_convex_hull(self, canvas, sheeps):
        pass

    def create_extended_hull(self, sheeps):
        pass

    def draw_extended_hull(self, canvas, sheeps):
        pass

    def main(self, drones, sheeps):
        self.create_convex_hull(sheeps)

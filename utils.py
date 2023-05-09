import pygame


class Calculate:
    def center_of_mass(sheeps):
        center_of_mass = pygame.Vector2(0, 0)
        if len(sheeps) > 0:
            for sheep in sheeps:
                center_of_mass += sheep.position
            center_of_mass /= len(sheeps)
        return center_of_mass


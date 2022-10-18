import pygame


class environment:
    def __init__(self, dimentions, goal):
        self.SHEPHERED_IMAGE = pygame.image.load(r"")
        self.mapW, self.mapH = dimentions   # Width and height of the map
        self.goal = goal    # x- and y-coords of the goal region

        pygame.init()
        self.name = 'Royce'
        pygame.display.set_caption(self.name)
        self.canvas = pygame.display.set_mode((self.mapW, self.mapH))

    def draw(self):
        for sheep in HERD:
            pygame.draw.circle(map.canvas, GREEN, sheep.position, sheep.size)
        pygame.draw.circle(map.canvas, SHEPHERD_COLOR,
                           BUTTER_FACE.position, BUTTER_FACE.size)

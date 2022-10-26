import pygame


from environment import Environment

FPS = 10
FramePerSec = pygame.time.Clock()

NAME = 'Royce'
DIMENTIONS = (1000, 600)
WHITE = (255, 255, 255)

pygame.init()
canvas = pygame.display.set_mode(DIMENTIONS)
# pygame.mouse.set_visible(False)


RUNNING = True
COUNTER = 0

while RUNNING:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            RUNNING = False
            pygame.quit()
    canvas.fill(WHITE)  # An empty window with a white background

    e = Environment(DIMENTIONS, (10, 20))
    e.draw(COUNTER)
    COUNTER += 10

    pygame.display.update()
    FramePerSec.tick(FPS)

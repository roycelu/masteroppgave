import pygame


class Calculate:
    def center_of_mass(sheeps):
        center_of_mass = pygame.Vector2(0, 0)
        if len(sheeps) > 0:
            for sheep in sheeps:
                center_of_mass += sheep.position
            center_of_mass /= len(sheeps)
        return center_of_mass


# class Draw:
#     def __init__(self, canvas, font, drones, sheeps):
#         self.canvas = canvas
#         self.font = font
#         self.drones = drones
#         self.sheeps = sheeps

#     def circle(self, position, color, size=0, text="", text_color="black"):
#         figure = pygame.Rect(0, 0, size * 2, size * 2)
#         figure.center = position
#         pygame.draw.rect(
#             self.canvas,
#             pygame.Color(color),
#             figure,
#             border_radius=int(size),
#         )

#         label = self.font.render(text, True, pygame.Color(text_color))
#         rect = label.get_rect()
#         rect.center = position
#         self.canvas.blit(label, rect)

#     def rectangle(self, position, color, size=0, text="", text_color="black"):
#         figure = pygame.Rect(0, 0, size, size)
#         figure.center = position
#         pygame.draw.rect(self.canvas, pygame.Color(color), figure)

#         label = self.font.render(text, True, pygame.Color(text_color))
#         rect = label.get_rect()
#         rect.center = position
#         self.canvas.blit(label, rect)

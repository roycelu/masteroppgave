import math
import pygame


class Shepherd:
    def __init__(self, id, pos):
        self.id = id
        self.size = 10
        self.position = pygame.Vector2(pos[0], pos[1])
        #self.position = pygame.Vector2(0, 0)
        self.velocity = pygame.Vector2(0, 0)

        self.MAX_DISTANCE_FROM_SHEEP = 50

    def move(self, dt, sheep_pos, sheep_vel):
        dx = sheep_pos.x - self.position.x
        dy = sheep_pos.y - self.position.y
        self.velocity = pygame.Vector2(dx, dy)

        distance = self.velocity.magnitude()
        direction = pygame.Vector2(0, 0)
        if distance > 0:
            self.velocity.scale_to_length(-1)
            direction = (sheep_pos-self.position)/distance

        angle = math.atan2(self.velocity.y, self.velocity.x)
        self.position.x += direction.x * distance * 1.1
        self.position.y += direction.y * distance * 1.1

        # self.position.x += self.velocity.x*0.1  # distance * math.cos(angle)
        # self.position.y += self.velocity.y*0.1  # distance * math.sin(angle)
        print(self.id)
        print("POS", self.position)
        print("vel", self.velocity)
        print("sheep", sheep_pos)
        print(math.degrees(angle), math.cos(angle), math.sin(angle))
        # print(distance)
        print("-----------")

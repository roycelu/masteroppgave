import pygame
import numpy as np
import shapely as shp
from scipy.spatial import ConvexHull
from goal import Goal
from utils import Calculate


DISTANCE = 10  # predefined drone-to-animal distance


class PolygonMethod:
    def __init__(self, canvas, font, goal, drones, sheeps):
        self.canvas = canvas
        self.font = font

        self.main_goal = goal
        self.goal = Goal(goal.position)
        self.drones = drones
        self.sheeps = sheeps

        self.centre_of_mass = Calculate.center_of_mass(sheeps)

    def convex_hull(self, sheeps):
        points = []
        positions = []

        for sheep in sheeps:
            positions.append(sheep.position)

        hull = ConvexHull(positions)
        for i in hull.vertices:
            points.append(positions[i])

            pygame.draw.circle(self.canvas, pygame.Color("green"), positions[i], 8)
            self.__add_label(str(i), positions[i])

        pygame.draw.polygon(self.canvas, pygame.Color("black"), points, 2)
        return points

    def extended_hull(self, vertices):
        extended_hull = []
        # points = self.convex_hull(sheeps)

        for i in range(len(vertices)):
            P = pygame.Vector2(vertices[i])
            if i == 0:
                P1 = pygame.Vector2(vertices[-1])
                P2 = pygame.Vector2(vertices[i + 1])
            if i == len(vertices) - 1:
                P1 = pygame.Vector2(vertices[i - 1])
                P2 = pygame.Vector2(vertices[0])
            else:
                P1 = pygame.Vector2(vertices[i - 1])
                P2 = pygame.Vector2(vertices[i + 1])

            PP1 = P1 - P
            PP2 = P2 - P
            P1P = P - P1
            P2P = P - P2

            cos_alpha = PP1.dot(PP2) / (PP1.length() * PP2.length())
            PL1 = (DISTANCE / abs(cos_alpha)) * (P1P / P1P.length())
            PL2 = (DISTANCE / abs(cos_alpha)) * (P2P / P2P.length())
            E = P + PL1 + PL2

            extended_hull.append(E)

            pygame.draw.circle(self.canvas, pygame.Color("pink"), E, 8).normalize()
            self.__add_label(str(i), E)

        figure = pygame.draw.polygon(
            self.canvas,
            pygame.Color("gray"),
            extended_hull,
            1,
        )
        return extended_hull, figure

    def fly_to_egde(self, drone, vertices, extended_hull):
        # Fly to the extended hull
        closest_point = pygame.Vector2(0, 0)
        closest_vertex = pygame.Vector2(0, 0)
        shortest_distance = np.inf

        for j in range(len(vertices) - 1):
            O = pygame.Vector2(0, 0)  # TODO: Tentativ løsning
            q = pygame.Vector2(vertices[j]) - pygame.Vector2(vertices[j + 1])
            p = drone.position - pygame.Vector2(vertices[j + 1])
            b = pygame.Vector2(0, 0)  # Drone to O

            o = ((1 / q.length()) * p.dot(q)) * (1 / q.length()) * q

            if p.dot(q) < 0:
                b = -p
                O = pygame.Vector2(vertices[j + 1])
            elif p.dot(q) > 0 and q.length() >= p.length():
                b = o - p
                # https://math.stackexchange.com/a/1630886
                distance = o.length() / q.length()
                O = pygame.Vector2(
                    (1 - distance) * vertices[j + 1].x + distance * vertices[j].x,
                    (1 - distance) * vertices[j + 1].y + distance * vertices[j].y,
                )
            else:
                b = q - p
                O = pygame.Vector2(vertices[j])

            # Find the closest point on extended hull edge
            if drone.position.distance_to(O) < shortest_distance:
                shortest_distance = drone.position.distance_to(O)
                closest_point = O

        # TODO: Usikker på hvordan implementere formel (18) & (19)
        # a = drone.velocity
        # F = pygame.Vector2(0, 0)
        # g = 1
        # f = b - (a.dot(b)) * a

        # if f != 0:
        #     F = pygame.Vector2(f / f.length())
        # if a.dot(b) <= 0:
        #     g = -1

        # drone.acceleration = drone.max_speed * g * F

        pygame.draw.circle(self.canvas, pygame.Color("purple"), closest_point, 5)
        drone.fly_to_position(closest_point)

        # The drone is on the extended hull edge
        if drone.figure.colliderect(extended_hull):
            # self.fly_on_edge(drone, vertices)
            b_star = b + o  # Edge sliding
            direction_index = 0  # 0: clockwise, 1:counterclockwise
            self.fly_on_edge(drone, vertices, direction_index)
        else:
            print("Flying to edge")

    def fly_on_edge(self, drone, vertices, direction):
        # Fly to the steering points along the extended hull
        print("Time to fly along the edge")

    def calculate_optimal_steering_points(self, drones, sheeps, points):
        # Find the optimal steering points and their collision-free allocation
        pass

    def __add_label(self, text, position, color="black"):
        label = self.font.render(text, True, pygame.Color(color))
        rect = label.get_rect()
        rect.center = position
        self.canvas.blit(label, rect)

    def main(self, drones, sheeps, goal):
        convex_hull = self.convex_hull(sheeps)
        extended_hull_vertices, extended_hull = self.extended_hull(convex_hull)
        # Styrer tentativ bare én drone
        # for drone in drones:
        self.fly_to_egde(drones[0], extended_hull_vertices, extended_hull)

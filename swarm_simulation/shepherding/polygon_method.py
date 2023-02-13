import pygame
import numpy as np
import shapely as shp
from scipy.spatial import ConvexHull
from goal import Goal
from utils import Calculate


DISTANCE = 10  # predefined drone-to-animal distance
TURNING_RADIUS = 15  # minimum turning radius of the drone (predefined?)


class PolygonMethod:
    def __init__(self, canvas, font, goal, drones, sheeps):
        self.canvas = canvas
        self.font = font

        self.main_goal = goal
        self.goal = Goal(goal.position)
        self.drones = drones
        self.sheeps = sheeps

        self.centre_of_mass = Calculate.center_of_mass(sheeps)
        self.next_vertex = False

    def convex_hull(self, sheeps):
        points = []
        positions = []

        for sheep in sheeps:
            positions.append(sheep.position)

        hull = ConvexHull(positions)
        for i in hull.vertices:
            points.append(positions[i])

            pygame.draw.circle(self.canvas, pygame.Color("black"), positions[i], 4)
            self.__add_label(str(i), positions[i])

        figure = pygame.draw.polygon(self.canvas, pygame.Color("black"), points, 1)
        return points, figure

    def extended_hull(self, vertices):
        extended_hull = []
        # points = self.convex_hull(sheeps)

        for i in range(len(vertices)):
            prev, current, next = self.__get_indices(i, len(vertices))
            P = pygame.Vector2(vertices[current])
            P1 = pygame.Vector2(vertices[prev])
            P2 = pygame.Vector2(vertices[next])

            PP1 = P1 - P
            PP2 = P2 - P
            P1P = P - P1
            P2P = P - P2

            cos_alpha = PP1.dot(PP2) / (PP1.length() * PP2.length())
            PL1 = (DISTANCE / abs(cos_alpha)) * (P1P / P1P.length())
            PL2 = (DISTANCE / abs(cos_alpha)) * (P2P / P2P.length())
            E = P + PL1 + PL2

            extended_hull.append(E)

            pygame.draw.circle(self.canvas, pygame.Color("gray"), E, 8).normalize()
            self.__add_label(str(i), E)

        figure = pygame.draw.polygon(
            self.canvas, pygame.Color("gray"), extended_hull, 1
        )
        return extended_hull, figure

    def closest_vertex_to_goal(self, vertices, goal):
        shortest_distance = np.inf
        closest_vertex = pygame.Vector2(0, 0)
        for j in range(len(vertices)):
            if vertices[j].distance_to(goal.position) < shortest_distance:
                shortest_distance = vertices[j].distance_to(goal.position)
                closest_vertex = vertices[j]
        pygame.draw.circle(self.canvas, pygame.Color("yellow"), closest_vertex, 3)
        return closest_vertex

    def fly_to_egde(self, drone, vertices):
        # Fly to the extended hull
        closest_point = pygame.Vector2(0, 0)
        shortest_distance = np.inf
        edge_vertices = [pygame.Vector2(0, 0), pygame.Vector2(0, 0)]

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
                edge_vertices[0] = pygame.Vector2(vertices[j])
                edge_vertices[1] = pygame.Vector2(vertices[j + 1])

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

        edge = pygame.draw.line(
            self.canvas, pygame.Color("purple"), edge_vertices[0], edge_vertices[1]
        )

        if drone.goal_status == False:
            pygame.draw.circle(self.canvas, pygame.Color("purple"), closest_point, 5)
            drone.fly_to_position(closest_point)
            print("Flying to closest point")
        return edge

    def fly_on_edge(self, drone, goal, extended_vertices, convex_vertices):
        # Fly to the steering points along the extended hull
        direction_index = 0  # 0: clockwise, 1:counterclockwise

        closest_vertex = pygame.Vector2(0, 0)
        # Find the closest extended vertex to drone position on the edge
        shortest_distance = np.inf
        for j in range(len(extended_vertices)):
            if drone.position.distance_to(extended_vertices[j]) < shortest_distance:
                shortest_distance = drone.position.distance_to(extended_vertices[j])
                closest_vertex = extended_vertices[j]

        closest_convex_vertex = pygame.Vector2(0, 0)
        # Find the correspondng the convex vertex to the closest extended vertex
        shortest_distance = np.inf
        for i in range(len(convex_vertices)):
            if closest_vertex.distance_to(convex_vertices[i]) < shortest_distance:
                shortest_distance = closest_vertex.distance_to(convex_vertices[i])
                closest_convex_vertex = convex_vertices[i]

        # The angle between the edges
        j = extended_vertices.index(closest_vertex)  # Extended vertex index
        i = convex_vertices.index(closest_convex_vertex)  # Convex vertex index

        prev, curr, next = self.__get_indices(j, len(extended_vertices))
        edge1 = pygame.Vector2(extended_vertices[prev] - extended_vertices[curr])
        edge2 = pygame.Vector2(extended_vertices[next] - extended_vertices[curr])

        angle = np.arccos(edge1.dot(edge2) / (edge1.length() * edge2.length()))
        # print(angle * 180 / np.pi)

        # Turning trajectory
        F_1 = extended_vertices[j] + (edge1 / edge1.length()) * (
            TURNING_RADIUS / np.tan(angle / 2)
        )
        EP = pygame.Vector2(convex_vertices[i] - extended_vertices[j])
        C_t = convex_vertices[i] + (EP / EP.length()) * (
            (TURNING_RADIUS - DISTANCE) / np.sin(angle / 2)
        )

        # if DISTANCE <= TURNING_RADIUS:
        B = self.closest_vertex_to_goal(extended_vertices, goal)
        Eb = extended_vertices[extended_vertices.index(B) - 1]

        edgeEbB = pygame.draw.line(self.canvas, pygame.Color("blue"), Eb, B)

        # Vertices between O and B along the given direction
        vertices = []
        if curr < B:
            vertices1 = extended_vertices[curr:B]

        
        if not drone.figure.colliderect(edgeEbB):
            # if not angle > 2 * np.arcsin(1 - DISTANCE / TURNING_RADIUS):
            #     print("Directly")
            #     drone.fly_to_position(extended_vertices[curr])
            #     if drone.figure.collidepoint(extended_vertices[curr]):
            #         print("Moving to next")
            #         drone.fly_to_position(extended_vertices[next])
            # else:
            #     print("Turning")
            #     drone.fly_to_position(extended_vertices[next])
            pass
        else:
            # Brake - stop the drone when it arrives at the final vertex
            

        if drone.figure.collidepoint(extended_vertices[curr]):
            print("Colliding")
            self.next_vertex = True
        print(self.next_vertex)
        if self.next_vertex == True:
            print("Flying to next vertex")
            drone.fly_to_position(extended_vertices[next])
        if self.next_vertex == False:
            print("Hallo..?")
            drone.fly_to_position(extended_vertices[curr])  # Fly to the closest vertex

        pygame.draw.circle(self.canvas, pygame.Color("blue"), drone.goal_position, 10)

    def calculate_optimal_steering_points(self, drones, sheeps, points):
        # Find the optimal steering points and their collision-free allocation
        pass

    def __add_label(self, text, position, color="black"):
        label = self.font.render(text, True, pygame.Color(color))
        rect = label.get_rect()
        rect.center = position
        self.canvas.blit(label, rect)

    def __get_indices(self, current, max_length):
        if current == 0:
            prev = -1
            next = current + 1
        if current == max_length - 1:
            prev = current - 1
            next = 0
        else:
            prev = current - 1
            next = current + 1
        return prev, current, next

    def main(self, drones, sheeps, goal):
        convex_vertices, convex_hull = self.convex_hull(sheeps)
        extended_vertices, extended_hull = self.extended_hull(convex_vertices)
        # Styrer tentativ bare én drone
        # for drone in drones:

        edge = self.fly_to_egde(drones[0], extended_vertices)

        # The drone is on the extended hull edge
        if drones[0].figure.colliderect(edge) and drones[0].goal_status == False:
            # TODO: "Kolliderer" for tidlig, må finne alternativ løsning..
            drones[0].goal_status = True  # Drone arrived edge
            # b_star = b + o  # Edge sliding
            pygame.draw.circle(
                self.canvas, pygame.Color("brown"), drones[0].position, 10
            )
        # The drone will fly along the edge
        if drones[0].goal_status == True:
            self.fly_on_edge(drones[0], goal, extended_vertices, convex_vertices)

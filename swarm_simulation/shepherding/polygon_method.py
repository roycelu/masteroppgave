import pygame
import numpy as np
import shapely as shp
from scipy.spatial import ConvexHull
from goal import Goal
from utils import Calculate


DISTANCE = 10  # predefined drone-to-animal distance
TURNING_RADIUS = 5  # minimum turning radius of the drone (predefined?)


class PolygonMethod:
    def __init__(self, canvas, font, goal, drones, sheeps):
        self.canvas = canvas
        self.font = font

        self.main_goal = goal
        self.goal = Goal(goal.position)
        self.drones = drones
        self.sheeps = sheeps

        self.centre_of_mass = Calculate.center_of_mass(sheeps)

        self.on_edge = False
        self.next_vertex = True
        self.toward_goal = False

        self.path = []
        self.direction_index = 0  # 0: clockwise, 1: counterclockwise
        self.fly_to_vertex = pygame.Vector2(0, 0)

    def convex_hull(self, sheeps):
        points = []
        positions = []

        for sheep in sheeps:
            positions.append(sheep.position)

        hull = ConvexHull(positions)
        for i in hull.vertices:
            points.append(positions[i])

            pygame.draw.circle(self.canvas, pygame.Color("black"), positions[i], 4)
            self.add_label(str(i), positions[i])

        figure = pygame.draw.polygon(self.canvas, pygame.Color("black"), points, 1)
        return points, figure

    def extended_hull(self, vertices):
        extended_hull = []

        for i in range(len(vertices)):
            prev, current, next = self.get_indices(i, len(vertices))
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
            self.add_label(str(i), E)

        figure = pygame.draw.polygon(
            self.canvas, pygame.Color("gray"), extended_hull, 1
        )
        return extended_hull, figure

    def fly_to_egde(self, drone, vertices):
        # FLY TO EXTENDED HULL
        closest_point = pygame.Vector2(0, 0)
        shortest_distance = np.inf
        edge_vertices = [pygame.Vector2(0, 0), pygame.Vector2(0, 0)]

        for j in range(len(vertices) - 1):
            O = pygame.Vector2(0, 0)
            q = pygame.Vector2(vertices[j]) - pygame.Vector2(vertices[j + 1])
            p = drone.position - pygame.Vector2(vertices[j + 1])
            b = pygame.Vector2(0, 0)  # Drone to O

            o = ((1 / q.length()) * p.dot(q)) * (1 / q.length()) * q  # (16)

            if p.dot(q) < 0:
                b = -p
                O = pygame.Vector2(vertices[j + 1])
            elif p.dot(q) > 0 and q.length() >= p.length():
                b = o - p
                # Find point along a line - https://math.stackexchange.com/a/1630886
                distance = o.length() / q.length()
                O = pygame.Vector2(
                    (1 - distance) * vertices[j + 1].x + distance * vertices[j].x,
                    (1 - distance) * vertices[j + 1].y + distance * vertices[j].y,
                )
            else:
                b = q - p
                O = pygame.Vector2(vertices[j])
            # (17)

            # FIND THE CLOSEST POINT ON THE EXTENDED HULL EDGE
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

        pygame.draw.line(
            self.canvas, pygame.Color("purple"), edge_vertices[0], edge_vertices[1]
        )

        pygame.draw.circle(self.canvas, pygame.Color("purple"), closest_point, 5)
        drone.fly_to_edge_point = closest_point
        drone.fly_to_position(closest_point)

    def fly_on_edge(self, drone, goal, extended_vertices, convex_vertices):
        # FLY TO THE STEERING POINTS ALONG THE EXTENDED HULL
        initial_point = self.first_edge_vertex
        # closest_vertex = self.closest_vertex(drone.position, extended_vertices)
        closest_initial_vertex = self.closest_vertex(initial_point, extended_vertices)
        closest_convex_vertex = self.closest_vertex(
            closest_initial_vertex, convex_vertices
        )

        j = extended_vertices.index(closest_initial_vertex)  # Extended vertex index
        i = convex_vertices.index(closest_convex_vertex)  # Convex vertex index
        prev, curr, next = self.get_indices(j, len(extended_vertices))

        # FIND THE VECTOR BETWEEN COM AND GOAL
        com_to_goal = -pygame.Vector2(goal.position - self.centre_of_mass)
        goal_vertex = pygame.Vector2(0, 0)  # Closest vertex to B
        goal_vertex2 = pygame.Vector2(0, 0)  # Closest vertex to B - opposite
        smallest_angle = np.inf

        # Visual line between COM and goal
        pygame.draw.line(
            self.canvas,
            pygame.Color("yellow"),
            self.centre_of_mass + 5 * com_to_goal,
            goal.position,
        )

        # FIND THE VERTEX CLOSEST TO POINT B
        for v in range(len(extended_vertices)):
            # Find angle between two vectors - https://mathsathome.com/angle-between-two-vectors/
            com_to_vertex = pygame.Vector2(extended_vertices[v] - self.centre_of_mass)
            angle = np.arccos(
                (com_to_goal.dot(com_to_vertex))
                / (com_to_goal.length() * com_to_vertex.length())
            )
            if angle < smallest_angle:
                smallest_angle = angle
                goal_vertex = extended_vertices[v]

        # FIND THE OPPOSITE VERTEX CLOSEST TO POINT B
        # Check which side of line is the vertex - https://math.stackexchange.com/a/274728
        side = (goal_vertex.x - self.centre_of_mass.x) * (
            goal.position.y - self.centre_of_mass.y
        ) - (goal_vertex.y - self.centre_of_mass.y) * (
            goal.position.x - self.centre_of_mass.x
        )
        goal_vertex_p, goal_vertex_c, goal_vertex_n = self.get_indices(
            extended_vertices.index(goal_vertex), len(extended_vertices)
        )

        if side > 0:  # closest goal_vertex to the right of line
            goal_vertex = extended_vertices[goal_vertex_c]  # left
            goal_vertex2 = extended_vertices[goal_vertex_p]  # right
        else:
            goal_vertex = extended_vertices[goal_vertex_n]  # left
            goal_vertex2 = extended_vertices[goal_vertex_c]  # right

        # FIND POINT B
        # Calculate the intersection point where point B lies - https://stackoverflow.com/a/56312654
        goal_point = pygame.Vector2(0, 0)
        goal_vertices_edge = pygame.Vector2(goal_vertex - goal_vertex2)
        d = com_to_goal.dot((goal_vertices_edge.y, -goal_vertices_edge.x))
        t = (goal_vertex - self.centre_of_mass).dot(
            (goal_vertices_edge.y, -goal_vertices_edge.x)
        ) / d
        goal_point = self.centre_of_mass + com_to_goal * t

        pygame.draw.circle(self.canvas, pygame.Color("yellow"), goal_point, 5)
        self.add_label("B", goal_point)

        # VERTICES BETWEEN O AND B ALONG THE GIVEN DIRECTION
        path1 = []  # Clockwise
        path2 = []  # Counterclockwise
        b_left = extended_vertices.index(goal_vertex)
        b_right = extended_vertices.index(goal_vertex2)

        if b_right < curr:
            path1.extend(extended_vertices[b_right:next])
            path1.append(extended_vertices[b_right])
            path2.extend(extended_vertices[prev:])
            path2.extend(extended_vertices[:b_left])
        else:
            path1.extend(extended_vertices[next:b_right])
            path1.append(extended_vertices[b_right])
            path2.extend(extended_vertices[b_left:])
            path2.extend(extended_vertices[:prev])
            path2.append(extended_vertices[prev])

        # DECIDE ON WHICH PATH THE DRONE SHALL FOLLOW - EITHER CLOKWISE OR COUNTERCLOCKWISE
        path1_length = 0
        for p in range(len(path1) - 1):
            path1_length += path1[p].distance_to(path1[p + 1])
        path2_length = 0
        for p in range(len(path2) - 1):
            path2_length += path2[p].distance_to(path2[p + 1])

        if path1_length <= path2_length:
            self.direction_index = 0
            self.path = path1
        else:
            self.direction_index = 1
            self.path = path2

        # THE ANGLE BETWEEN THE EDGES
        closest_vertex = self.closest_vertex(drone.position, extended_vertices)
        j = extended_vertices.index(closest_vertex)
        i = convex_vertices.index(self.closest_vertex(closest_vertex, convex_vertices))
        prev, curr, next = self.get_indices(j, len(extended_vertices))

        edge1 = pygame.Vector2(extended_vertices[prev] - extended_vertices[curr])
        edge2 = pygame.Vector2(extended_vertices[next] - extended_vertices[curr])

        smallest_angle = np.arccos(
            edge1.dot(edge2) / (edge1.length() * edge2.length())
        )  # (9)
        # print(angle * 180 / np.pi)  # (0,pi)

        # CALCULATE THE TURNING TRAJECTORY
        F_1 = extended_vertices[j] + (edge1 / edge1.length()) * (
            TURNING_RADIUS / np.tan(smallest_angle / 2)
        )  # (26)
        F_2 = extended_vertices[j] + (edge2 / edge2.length()) * (
            TURNING_RADIUS / np.tan(smallest_angle / 2)
        )
        EP = pygame.Vector2(convex_vertices[i] - extended_vertices[j])
        C_t = convex_vertices[i] + (EP / EP.length()) * (
            (TURNING_RADIUS - DISTANCE) / np.sin(smallest_angle / 2)
        )  # (27)

        # FIND THE GOAL "AREA" ON THE EDGE
        B = goal_point
        if self.direction_index == 0:  # clockwise
            Eb = extended_vertices[b_right]
        if self.direction_index == 1:  # counterclockwise
            Eb = extended_vertices[b_left]
        edgeEbB = pygame.draw.line(self.canvas, pygame.Color("blue"), Eb, B)

        new = self.path.pop(0)
        if len(self.path) == 0 and drone.figure.colliderect(edgeEbB):
            # BRAKE - stop the drone when it arrives at the final vertex
            drone.fly_to_position(B)
            if drone.figure.collidepoint(B):
                self.toward_goal = True  # TODO: Tentativ løsning
        else:
            # TRANSFER - arc trajectory TODO
            if DISTANCE <= TURNING_RADIUS:
                if not (convex_vertices[i] - C_t).length() < TURNING_RADIUS:
                    if not np.sin(angle / 2) > 1 - (DISTANCE / TURNING_RADIUS):
                        if not angle > 2 * np.arcsin(
                            1 - DISTANCE / TURNING_RADIUS
                        ):  # (28)
                            drone.fly_to_position(new)
            else:
                # print("Turning")
                if self.direction_index == 0:
                    if drone.figure.collidepoint(F_1):
                        drone.fly_to_position(F_2)
                else:
                    if drone.figure.collidepoint(F_2):
                        drone.fly_to_position(F_1)

                # if drone.figure.collidepoint(new):
                #     print("Stuck")
                #     drone.fly_to_position(self.path[0])

                drone.fly_to_position(new)
            # print("--", self.path)
            # print(drone.position, new)

        pygame.draw.circle(self.canvas, pygame.Color("blue"), drone.goal_position, 5)
        pygame.draw.circle(self.canvas, pygame.Color("orange"), F_1, 5)
        pygame.draw.circle(self.canvas, pygame.Color("yellow"), C_t, 5)
        pygame.draw.circle(self.canvas, pygame.Color("red"), F_2, 5)

    def selection_of_steering_points(self, drones, convex_vertices, vertices):
        # FIND THE OPTIMAL STEERING POINTS FOR THE DRONES ALONG EXTENDED HULL
        # Input: number of drones (n_d), extended hull (E), drones (D)

        drone = drones[0]  # Tentativ løsning for én drone
        largest_distance = -np.inf
        furthest_convex_vertices = [pygame.Vector2(0, 0) for i in drones]

        # Find the sheep furthest away from the centre of mass
        left = 0  # 1: drone pass z=0 by left, 0: otherwise
        right = 0  # 1: drone pass z=0 by right, 0: otherwise
        direction = 0  # 0: flying left, 1: flying right

        # FIND STEERING POINTS
        furtest_convex_vertex = pygame.Vector2(0, 0)
        for vertex in convex_vertices:
            if self.centre_of_mass.distance_to(vertex) > largest_distance:
                largest_distance = self.centre_of_mass.distance_to(vertex)
                furtest_convex_vertex = vertex
        furthest_vertex = self.closest_vertex(furtest_convex_vertex)

        initial = self.closest_vertex(drone.fly_to_edge_point, vertices)
        line_segment = []  # line segment: [0,M]
        line_segment2 = []
        for i in range(len(vertices)):
            if i >= vertices.index(initial):
                line_segment.append(vertices[i])
            else:
                line_segment2.append(vertices[i])
        line_segment.extend(line_segment2)

        for z in range(len(line_segment)):
            prev, curr, next = self.get_indices(z, line_segment)
            #

        print(line_segment2)
        print("--", vertices)

        # if len(vertices) >= len(drones):

    def add_label(self, text, position, color="black"):
        label = self.font.render(text, True, pygame.Color(color))
        rect = label.get_rect()
        rect.center = position
        self.canvas.blit(label, rect)

    def get_indices(self, current, max_length):
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

    def closest_vertex(self, point, vertices):
        shortest_distance = np.inf
        closest_vertex = pygame.Vector2(0, 0)
        for i in range(len(vertices)):
            if point.distance_to(vertices[i]) < shortest_distance:
                shortest_distance = point.distance_to(vertices[i])
                closest_vertex = vertices[i]
        return closest_vertex

    def main(self, drones, sheeps, goal):
        convex_vertices, convex_hull = self.convex_hull(sheeps)
        extended_vertices, extended_hull = self.extended_hull(convex_vertices)
        # Styrer tentativ bare én drone
        # for drone in drones:

        self.selection_of_steering_points(drones, convex_vertices, extended_vertices)

        # The drone is on the extended hull edge
        if drones[0].figure.colliderect(extended_hull) and self.on_edge == False:
            # TODO: "Kolliderer" for tidlig, må finne alternativ løsning..
            self.on_edge = True  # Drone arrived edge

            pygame.draw.circle(
                self.canvas, pygame.Color("brown"), drones[0].position, 10
            )

        # The drone will either fly TO the edge or along (ON) the edge
        if self.on_edge == False and self.toward_goal == False:
            self.fly_to_egde(drones[0], extended_vertices)
            # print("Flying to the edge")
        if self.toward_goal == True:
            drones[0].fly_to_position(goal.position)
            # print("Goaaaal")
        if self.on_edge == True and self.toward_goal == False:
            self.fly_on_edge(drones[0], goal, extended_vertices, convex_vertices)
            # print("Around the edge")

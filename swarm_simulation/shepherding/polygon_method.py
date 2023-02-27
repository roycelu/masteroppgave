import pygame
import numpy as np
import shapely as shp
from scipy.spatial import ConvexHull
from goal import Goal
from utils import Calculate


DISTANCE = 10  # drone-to-animal distance (predefined)
TURNING_RADIUS = 5  # minimum turning radius of the drone (predefined?)
SHEEP_RADIUS = 60  # the sheep's smallest circle during driving (predefined)
DRIVING_SPEED = 38  # driving speed (predefined)


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

    def convex_hull(self, sheeps):
        points = []
        positions = []

        for sheep in sheeps:
            positions.append(sheep.position)

        hull = ConvexHull(positions)
        for i in hull.vertices:
            points.append(positions[i])

            pygame.draw.circle(self.canvas, pygame.Color(
                "black"), positions[i], 4)
            self.add_label(str(i), positions[i])

        figure = pygame.draw.polygon(
            self.canvas, pygame.Color("black"), points, 1)
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

            pygame.draw.circle(self.canvas, pygame.Color(
                "gray"), E, 8).normalize()
            self.add_label(str(i), E)

        figure = pygame.draw.polygon(
            self.canvas, pygame.Color("gray"), extended_hull, 1
        )
        return extended_hull, figure

    def fly_to_egde(self, drone, vertices):
        # THE DRONE FLIES TO EXTENDED HULL
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
                    (1 - distance) * vertices[j +
                                              1].x + distance * vertices[j].x,
                    (1 - distance) * vertices[j +
                                              1].y + distance * vertices[j].y,
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
            self.canvas, pygame.Color(
                "purple"), edge_vertices[0], edge_vertices[1]
        )

        pygame.draw.circle(self.canvas, pygame.Color(
            "purple"), closest_point, 5)
        drone.fly_to_edge_point = closest_point
        drone.fly_to_position(closest_point)

    def fly_on_edge(self, drone, extended_vertices, convex_vertices):
        # THE DRONE FLIES TO THE STEERING POINTS ALONG THE EXTENDED HULL
        initial_point = drone.fly_to_edge_point
        # closest_vertex = self.closest_vertex(drone.position, extended_vertices)
        closest_initial_vertex = self.closest_vertex(
            initial_point, extended_vertices)
        closest_convex_vertex = self.closest_vertex(
            closest_initial_vertex, convex_vertices
        )

        j = extended_vertices.index(
            closest_initial_vertex)  # Extended vertex index
        i = convex_vertices.index(closest_convex_vertex)  # Convex vertex index
        prev, curr, next = self.get_indices(j, len(extended_vertices))

        # VERTICES BETWEEN O AND B ALONG THE GIVEN DIRECTION
        path1 = []  # Clockwise
        path2 = []  # Counterclockwise
        # b = extended_vertices.index(drone.steering_point)
        b = 2

        if b < curr:
            path1.extend(extended_vertices[b:next])
            path1.append(extended_vertices[b])
            path2.extend(extended_vertices[prev:])
            path2.extend(extended_vertices[:b])
        else:
            path1.extend(extended_vertices[next:b])
            path1.append(extended_vertices[b])
            path2.extend(extended_vertices[b:])
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
        i = convex_vertices.index(self.closest_vertex(
            closest_vertex, convex_vertices))
        prev, curr, next = self.get_indices(j, len(extended_vertices))

        edge1 = pygame.Vector2(
            extended_vertices[prev] - extended_vertices[curr])
        edge2 = pygame.Vector2(
            extended_vertices[next] - extended_vertices[curr])

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
        B = extended_vertices[2]  # drone.steering_point
        if self.direction_index == 0:  # clockwise
            Eb = extended_vertices[b]
        if self.direction_index == 1:  # counterclockwise
            Eb = extended_vertices[b]
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

        pygame.draw.circle(self.canvas, pygame.Color(
            "blue"), drone.goal_position, 5)
        pygame.draw.circle(self.canvas, pygame.Color("orange"), F_1, 5)
        pygame.draw.circle(self.canvas, pygame.Color("yellow"), C_t, 5)
        pygame.draw.circle(self.canvas, pygame.Color("red"), F_2, 5)

    def selection_of_steering_points(self, drones, convex_vertices, vertices):
        # FIND THE OPTIMAL STEERING POINTS FOR THE DRONES ALONG EXTENDED HULL
        line_segment = []   # vertices = line segment: [0,M]
        steering_points = []    # Possible steering points on the extended hull
        travel_distances = []   # Γ: distances to reach allocated steering point

        # FIND THE N SHEEP FURTHEST AWAY FROM THE CENTRE OF MASS (the steering points)
        # (Bubble) sorting the convex vertices based on the distance from the centre of mass
        furthest_convex_vertices = []
        copy_list = convex_vertices
        for m in range(len(convex_vertices)):
            for n in range(len(convex_vertices)-1):
                d = self.centre_of_mass.distance_to(copy_list[n])
                d2 = self.centre_of_mass.distance_to(
                    copy_list[n+1])
                if d > d2:
                    copy_list[n], copy_list[n+1] = copy_list[n+1], copy_list[n]
        furthest_convex_vertices = copy_list[::-1]  # From furthest to closest

        # The steering points on the extended vertices, later to be allocated
        for vertex in furthest_convex_vertices[:len(drones)]:
            closest = self.closest_vertex(vertex, vertices)
            steering_points.append(closest)

            pygame.draw.circle(
                self.canvas, pygame.Color("yellow"), closest, 10)
        print(steering_points)

        # The disconnected extended hull from the first drone's position (z-axis)
        initial = self.closest_vertex(
            drones[0].fly_to_edge_point, vertices)
        temp = []
        for i in range(len(vertices)):
            if i >= vertices.index(initial):
                line_segment.append(vertices[i])
            else:
                temp.append(vertices[i])
        line_segment.extend(temp)

        # Set the direction indices for the drones, TODO
        for i in range(len(drones)):
            closest_vertex = self.closest_vertex(drones[i].position, vertices)
            drones[i].direction_index = 1  # fly right

        # Temporarily allocating the steering points to the drones
        for drone in drones:
            x = steering_points.pop(0)

        # Compute which direction the drones are moving
        for drone in drones:
            z_ = line_segment.index(drone.steering_point)
            z = line_segment.index(self.closest_vertex(
                drone.position, line_segment))
            # Formula (29)
            if z_ > z and drone.direction_index == 0:
                drone.left_pass = 1
            else:
                drone.left_pass = 0
            # Formula (30)
            if z_ < z and drone.direction_index == 1:
                drone.right_pass = 1
            else:
                drone.right_pass = 0

        # Extended z-axis: z*=[M,2M], formula (31)
        extended_points = []    # [x, x, ...]
        for drone in drones:
            z_ = line_segment.index(drone.steering_point)
            if drone.direction_index == 0:
                extended_points.append(z_ - drone.left_pass*len(line_segment))
            if drone.direction_index == 1:
                extended_points.append(z_ - drone.right_pass*len(line_segment))

        # Travel distances for the drones
        for drone in drones:
            j = 0
            z = line_segment.index(self.closest_vertex(
                drone.position, line_segment))
            z_star = extended_points[j]
            if drone.direction_index == 0:
                drone.travel_distance = z - z_star
            if drone.direction_index == 1:
                drone.travel_distance = z_star - z
            travel_distances.append(drone.travel_distance)
            j += 1

        # Updating the steering points, so the sheep furthest away will always be steered closer to the centre of mass
        allocated_steering_points = []
        for drone in drones:
            allocated_steering_points.append(drone.steering_point)
        return allocated_steering_points

        # if len(vertices) >= len(drones):
        #    Set steering points
        # else:
        #    n_d - n_e barking drones (far away from the steering points) quit gathering task
        #    stand by until n_e increases

    def drive_to_goal(self, drones, goal, vertices):
        # FIND THE POINT BEHIND THE EXTENDED HULL, BETWEEN THE CENTROID AND THE GOAL
        goal_point = pygame.Vector2(0, 0)  # A point between centroid and goal
        # FIND THE VECTOR BETWEEN COM AND GOAL
        com_to_goal = -pygame.Vector2(goal.position - self.centre_of_mass)
        goal_vertex = pygame.Vector2(0, 0)  # Closest vertex to B
        goal_vertex2 = pygame.Vector2(0, 0)  # Closest vertex to B - opposite
        smallest_angle = np.inf

        # Visual line between the goal and the centre of mass
        pygame.draw.line(
            self.canvas,
            pygame.Color("yellow"),
            self.centre_of_mass + 5 * com_to_goal,
            goal.position,
        )

        # FIND THE VERTEX CLOSEST TO POINT B
        for v in range(len(vertices)):
            # Find angle between two vectors - https://mathsathome.com/angle-between-two-vectors/
            com_to_vertex = pygame.Vector2(
                vertices[v] - self.centre_of_mass)
            angle = np.arccos(
                (com_to_goal.dot(com_to_vertex))
                / (com_to_goal.length() * com_to_vertex.length())
            )
            if angle < smallest_angle:
                smallest_angle = angle
                goal_vertex = vertices[v]

        # FIND THE OPPOSITE VERTEX CLOSEST TO POINT B
        # Check which side of line is the vertex - https://math.stackexchange.com/a/274728
        side = (goal_vertex.x - self.centre_of_mass.x) * (
            goal.position.y - self.centre_of_mass.y
        ) - (goal_vertex.y - self.centre_of_mass.y) * (
            goal.position.x - self.centre_of_mass.x
        )
        goal_vertex_p, goal_vertex_c, goal_vertex_n = self.get_indices(
            vertices.index(goal_vertex), len(vertices)
        )

        if side > 0:  # closest goal_vertex to the right of line
            goal_vertex = vertices[goal_vertex_c]  # left
            goal_vertex2 = vertices[goal_vertex_p]  # right
        else:
            goal_vertex = vertices[goal_vertex_n]  # left
            goal_vertex2 = vertices[goal_vertex_c]  # right

        # FIND POINT B
        # Calculate the intersection point where point B lies - https://stackoverflow.com/a/56312654
        goal_point = pygame.Vector2(0, 0)
        goal_vertices_edge = pygame.Vector2(goal_vertex - goal_vertex2)
        d = com_to_goal.dot((goal_vertices_edge.y, -goal_vertices_edge.x))
        t = (goal_vertex - self.centre_of_mass).dot(
            (goal_vertices_edge.y, -goal_vertices_edge.x)
        ) / d
        goal_point = self.centre_of_mass + com_to_goal * t

        pygame.draw.circle(self.canvas, pygame.Color(
            "yellow"), self.centre_of_mass, SHEEP_RADIUS, draw_bottom_left=True, draw_bottom_right=True)

        # # Compute the point moving from centroid and the goal, formula (43)
        # goal_point = self.centre_of_mass + DRIVING_SPEED * \
        #     (com_to_goal/com_to_goal.length())

        # Visually display the goal_point
        pygame.draw.circle(self.canvas, pygame.Color("yellow"), goal_point, 5)
        self.add_label("B", goal_point)

        # The perpendicular line to com_to_goal line
        vector_g = com_to_goal.rotate_rad(np.pi/2)
        pygame.draw.line(self.canvas, pygame.Color(
            "orange"), self.centre_of_mass, goal.position + 5*vector_g)
        pygame.draw.line(self.canvas, pygame.Color(
            "orange"), self.centre_of_mass, goal.position - 5*vector_g)

        return goal_point

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

        # The minimum distance of gathering, before the animals need to be driven to a designated location
        gather_radius = pygame.draw.circle(self.canvas, pygame.Color(
            "orange"), self.centre_of_mass, SHEEP_RADIUS, 1)

        # Tentativ plassering for testing av metode
        # self.selection_of_steering_points(
        #     drones, convex_vertices, extended_vertices)

        # The drone is on the extended hull edge
        if drones[0].figure.colliderect(extended_hull) and self.on_edge == False:
            # TODO: "Kolliderer" for tidlig, må finne alternativ løsning..
            self.on_edge = True  # Drone arrived edge

            pygame.draw.circle(
                self.canvas, pygame.Color("brown"), drones[0].position, 10
            )

        # for drone in drones:
        # Styrer tentativ bare én drone

        # The drone will either fly TO the edge or along (ON) the edge
        if self.on_edge == False and self.toward_goal == False:
            self.fly_to_egde(drones[0], extended_vertices)
            # print("Flying to the edge")
        if gather_radius.contains(convex_hull) and self.toward_goal == False:
            self.toward_goal = True
        # if self.toward_goal == True:
        goal_point = self.drive_to_goal(drones, goal, extended_vertices)
        drones[0].fly_to_position(goal_point)
        # print("Goaaaal")
        if self.on_edge == True and self.toward_goal == False:
            # steering_points = self.selection_of_steering_points(
            #     drones, convex_vertices, extended_vertices)
            self.fly_on_edge(
                drones[0], extended_vertices, convex_vertices)
            # print("Around the edge")

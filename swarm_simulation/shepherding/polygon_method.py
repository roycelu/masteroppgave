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
        drone.edge_point = closest_point
        drone.fly_to_position(closest_point)

    def fly_on_edge(self, drone, extended_vertices, convex_vertices):
        # Steering point, direction index, edge_point
        travel_path = []
        start_point = drone.edge_point
        end_point = drone.steering_point

    def allocate_steering_points(self, drones, convex_vertices, vertices):
        # FIND THE OPTIMAL STEERING POINTS FOR THE DRONES ALONG EXTENDED HULL
        allocated_steering_points = [pygame.Vector2(0, 0) for d in drones]

        # FIND THE N SHEEP FURTHEST AWAY FROM THE CENTRE OF MASS (the steering points)
        # (Bubble) sorting the convex vertices based on the distance from the centre of mass
        furthest_convex_vertices = []
        copy_list = convex_vertices
        for m in range(len(convex_vertices)):
            for n in range(len(convex_vertices) - 1):
                distance = self.centre_of_mass.distance_to(copy_list[n])
                d2 = self.centre_of_mass.distance_to(copy_list[n + 1])
                if distance > d2:
                    copy_list[n], copy_list[n + 1] = copy_list[n + 1], copy_list[n]
        furthest_convex_vertices = copy_list[::-1]  # From furthest to closest

        # The steering points on the extended vertices, later to be allocated
        steering_points = []  # Possible steering points on the extended hull
        for vertex in furthest_convex_vertices:
            closest = self.closest_vertex(vertex, vertices)
            if vertex not in steering_points:  # TODO: Slipper inn uavhengig
                steering_points.append(closest)
        # pygame.draw.circle(self.canvas, pygame.Color("yellow"), closest, 10)

        # CALCULATE THE DRONES' POSITION ON THE DISCONNECTED EXTENDED HULL (z-axis)
        # The disconnected extended hull from the first drone's position [0, M]
        initial = self.closest_vertex(drones[0].edge_point, vertices)
        line_segment = []  # line segment (z-axis): [0,M]
        for drone in drones:
            x = vertices.index(self.closest_vertex(drone.edge_point, vertices))
            if drones.index(drone) < x:
                initial = self.closest_vertex(drone.edge_point, vertices)
        temp = []
        for i in range(len(vertices)):
            if i >= vertices.index(initial):
                line_segment.append(vertices[i])
            else:
                temp.append(vertices[i])
        line_segment.extend(temp)

        # Convert the drones' extended hull positions to correspond to the disconnected extended hull (z-axis)
        drone_positions = [0 for d in drones]
        for drone in drones:
            i = drones.index(drone)
            vertex = self.closest_vertex(drone.edge_point, vertices)
            drone_positions[i] = line_segment.index(vertex)

        # Extend the disconnected extended hull [-M, 2M]
        ext_line_segment = []
        temp_segment = line_segment[-1:0:-1]  # [-M,0]
        ext_line_segment.extend(temp_segment)  # [0,M]
        ext_line_segment.extend(2 * line_segment)  # [M, 2M]

        # GENERATE POSSIBLE ALLOCATIONS FOR EACH DRONE
        for drone in drones:
            drone.possible_allocations = []
            for point in steering_points:
                drone.possible_allocations.append([0, point])
                drone.possible_allocations.append([1, point])
                # i=0: direction index, i=1: possible steering point

        # CALCLULATE THE OPTIMAL STEERING POINTS FOR THE DRONES BASED ON THE TRAVEL DISTANCES
        for drone in drones:
            i = drones.index(drone)
            for el in drone.possible_allocations:
                # Calculate the position on the disconnected extended hull and the travel distance
                direction = el[0]  # direction index (z)
                point = el[1]  # possible steering point (s')
                s = line_segment.index(point)  # index of the point on the z-axis (z')
                # Compute and find how the drone moves along the z-axis
                if s > drone_positions[i] and direction == 0:  # (29)
                    drone.left_pass = 1
                else:
                    drone.left_pass = 0
                if s < drone_positions[i] and direction == 1:  # (30)
                    drone.right_pass = 1
                else:
                    drone.right_pass = 0
                # Find the drone's position on the extended z-axis, formula (31)
                if direction == 0:
                    z_star = s - drone.left_pass * len(line_segment)
                if direction == 1:
                    z_star = s + drone.right_pass * len(line_segment)
                # Compute the travel distance from the drone to the possible steering point, formula (32)
                if direction == 0:
                    distance = drone_positions[i] - z_star
                if direction == 1:
                    distance = z_star - drone_positions[i]
                # Adds the travel distance to the list of possible steering point allocations
                el.extend([distance])

        # STEERING POINTS ALLOCATION OPTIMISATION
        # Sort the list of possible allocations based on the furthest travel distance
        for drone in drones:
            temp_list = drone.possible_allocations
            for n in range(len(drone.possible_allocations) - 1):
                distance = drone.possible_allocations[n][2]
                d2 = drone.possible_allocations[n + 1][2]
                if distance > d2:
                    temp_list[n], temp_list[n + 1] = temp_list[n + 1], temp_list[n]
            drone.possible_allocations = temp_list[::-1]  # From furthest to closest

        # Remark 5: Each drone is allocated to each steering point, if there is enough of steering points to be allocated, or else the drone stand by
        x = 0
        if len(steering_points) < len(drones):
            x = len(steering_points) - len(drones)

        # Allocation of the optimal steering point for each drone
        for i in range(len(drones) - x):
            drone = drones[i]
            for el in drone.possible_allocations:
                direction = el[0]
                point = el[1]
                distance = el[2]
                # TODO: Legger til i listen uavhengig (v)
                if point not in allocated_steering_points:
                    drone.steering_point = point
                    drone.direction_index = direction
                    # Avoid duplicate of the steering points, so two or more drones do not fly to the same steering point
                    allocated_steering_points[i] = point

        # FIND THE FLYING PATH FOR THE DRONE TO THE ALLOCATED STEERING POINT
        for i in range(len(drones) - x):
            drone = drones[i]
            drone.travel_path = []

            # Check if the drone is allocated a steering point
            if drone.steering_point == pygame.Vector2(0, 0):
                print("No steering point set")
                continue

            # Calculte the drone's path
            path = ext_line_segment
            start_index = drone_positions[i]
            end_index = path.index(drone.steering_point)

            for n in range(start_index, end_index + 1):
                index = 0
                if drone.direction_index == 0:
                    if n > start_index:  # (29)
                        drone.left_pass = 1
                    else:
                        drone.left_pass = 0
                    index = n + drone.left_pass * len(line_segment)  # (31)
                if drone.direction_index == 1:
                    if n < start_index:  # (30)
                        drone.right_pass = 1
                    else:
                        drone.right_pass = 0
                    index = n + drone.right_pass * len(line_segment)  # (31)
                drone.travel_path.append(path[index])

            drone.fly_to_position(path[end_index])

        # The optimal steering points are allocated to the drones
        # return allocated_steering_points

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
            com_to_vertex = pygame.Vector2(vertices[v] - self.centre_of_mass)
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

        # # Compute the point moving from centroid and the goal, formula (43)
        # goal_point = self.centre_of_mass + DRIVING_SPEED * \
        #     (com_to_goal/com_to_goal.length())

        # Visually display the goal_point
        pygame.draw.circle(self.canvas, pygame.Color("yellow"), goal_point, 5)
        self.add_label("B", goal_point)

        goal_point_left = pygame.Vector2(0, 0)
        goal_point_right = pygame.Vector2(0, 0)

        goal_point_left = (self.centre_of_mass - goal_point).rotate_rad(np.pi / 2)
        goal_point_left.scale_to_length((self.centre_of_mass - goal_point).length())
        goal_point_right = (self.centre_of_mass - goal_point).rotate_rad(-np.pi / 2)

        pygame.draw.circle(self.canvas, pygame.Color("orange"), goal_point_left, 10)
        pygame.draw.circle(self.canvas, pygame.Color("orange"), goal_point_right, 10)

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
        gather_radius = pygame.draw.circle(
            self.canvas, pygame.Color("orange"), self.centre_of_mass, SHEEP_RADIUS, 1
        )

        # The drone is on the extended hull edge
        if drones[0].figure.colliderect(extended_hull) and self.on_edge == False:
            # TODO: "Kolliderer" for tidlig, må finne alternativ løsning..
            self.on_edge = True  # Drone arrived edge

            pygame.draw.circle(
                self.canvas, pygame.Color("brown"), drones[0].position, 10
            )

        # The drone will either fly TO the edge or along (ON) the edge
        if self.on_edge == False and self.toward_goal == False:
            for drone in drones:
                self.fly_to_egde(drone, extended_vertices)
                # Wait until all the drones have arrived to the extended hull, before flying to their allocated steering points
                if drone.figure.colliderect(extended_hull):
                    self.on_edge = True
                else:
                    self.on_edge = False

        # Check if the sheep flock is gathered enough, if so, push them toward the goal
        if gather_radius.contains(convex_hull) and self.toward_goal == False:
            self.toward_goal = True

        if self.toward_goal == True:
            goal_point = self.drive_to_goal(drones, goal, extended_vertices)
            drones[0].fly_to_position(goal_point)  # TODO

        # When the drones arrive at the edge of the sheep flock, begin to gather them more closer to each other
        if self.on_edge == True and self.toward_goal == False:
            self.allocate_steering_points(drones, convex_vertices, extended_vertices)

            # for drone in drones:
            #     self.fly_on_edge(drone, extended_vertices)

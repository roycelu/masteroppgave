import pygame
import numpy as np
import shapely.geometry as shp
from scipy.spatial import ConvexHull
from goal import Goal


DISTANCE = 20 #30  # drone-to-animal distance (predefined)
TURNING_RADIUS = 5  # minimum turning radius of the drone (predefined?)
SHEEP_RADIUS = 20 # 60  # the sheep's smallest circle during driving (predefined)


class OurMainDronePolygon:
    def __init__(self, canvas, goal, drones, sheeps, theta, drive_type):
        self.canvas = canvas

        self.main_goal = goal
        self.goal = Goal(goal.position)
        self.drones = drones
        self.sheeps = sheeps

        self.centre_of_mass = pygame.Vector2(0, 0)

        self.on_edge = False
        self.toward_goal = False

        self.theta = theta
        self.drive_type = drive_type


    def convex_hull(self, sheeps):
        # Creates a convex hull from the sheep's positions
        points = []
        positions = []

        for sheep in sheeps:
            positions.append(sheep.position)

        hull = ConvexHull(positions)
        for i in hull.vertices:
            points.append(positions[i])

        figure = pygame.draw.polygon(self.canvas, pygame.Color("black"), points, 1)
        return points, figure


    def extended_hull(self, vertices):
        # Create an extended hull from the convex hull where the drones will fly
        extended_hull = []

        polygon = shp.Polygon([[v.x, v.y] for v in vertices]).buffer(DISTANCE, join_style=2, mitre_limit=1)
        polygon_list = polygon.exterior.coords
        for i in range(len(polygon_list) - 1):
            point = pygame.Vector2(polygon_list[i][0], polygon_list[i][1])
            extended_hull.append(point)
            pygame.draw.circle(self.canvas, pygame.Color("gray"), point, 5)

        figure = pygame.draw.polygon(self.canvas, pygame.Color("gray"), extended_hull, 2)
        return extended_hull, figure


    def fly_to_egde(self, drone, vertices):
        # Make the drone fly to the extended hull
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

            # Find the closest point on the extended hull
            if drone.position.distance_to(O) < shortest_distance:
                shortest_distance = drone.position.distance_to(O)
                closest_point = O
                edge_vertices[0] = pygame.Vector2(vertices[j])
                edge_vertices[1] = pygame.Vector2(vertices[j + 1])

        pygame.draw.circle(self.canvas, pygame.Color("purple"), closest_point, 3)

        drone.edge_point = closest_point
        drone.fly_to_position(closest_point)


    def fly_on_edge(self, drone, vertices, convex_vertices):
        # Make the drone fly along the extended hull
        if len(drone.travel_path) == 0:
            # BRAKE - stop the drone when it arrives at the final vertex
            drone.fly_to_position(drone.steering_point)
        else:
            # TRANSFER - arc trajectory to the steering point
            new = drone.travel_path.pop(0)
            drone.edge_point = new

            # Find the next point on the list when arrived the first one
            prev, curr, next = self.get_indices(vertices.index(new), len(vertices))

            current_point = vertices[curr]
            edge1 = pygame.Vector2(vertices[prev] - current_point)
            edge2 = pygame.Vector2(vertices[next] - current_point)

            # Calculate the angle between two edges, (0,pi) , formula (9)
            angle = np.arccos(edge1.dot(edge2) / (edge1.length() * edge2.length()))

            # Calculate the turning trajectory, formula (26)
            F_1 = current_point + (edge1 / edge1.length()) * (
                TURNING_RADIUS / np.tan(angle / 2)
            )
            F_2 = current_point + (edge2 / edge2.length()) * (
                TURNING_RADIUS / np.tan(angle / 2)
            )

            convex_vertex = self.closest_vertex(current_point, convex_vertices)
            EP = pygame.Vector2(convex_vertex - current_point)
            C_t = convex_vertex + (EP / EP.length()) * (
                (TURNING_RADIUS - DISTANCE) / np.sin(angle / 2)
            )  # (27)

            # To avoid dispersing the sheep, therefore ensure that the turning trajectory do not touch the convex hull
            if DISTANCE <= TURNING_RADIUS:
                # If the inequalities does not hold, the drone flies directly to the point instead of along the arc trajectory, formula (28)
                if not (convex_vertex - C_t).length() < TURNING_RADIUS:
                    if not np.sin(angle / 2) > 1 - (DISTANCE / TURNING_RADIUS):
                        if not angle > 2 * np.arcsin(1 - (DISTANCE / TURNING_RADIUS)):
                            drone.fly_to_position(current_point)
            else:
                drone.fly_to_position(new)
                if drone.direction_index == 0:
                    if drone.figure.collidepoint(F_1):
                        drone.fly_to_position(F_2)
                if drone.direction_index == 1:
                    if drone.figure.collidepoint(F_2):
                        drone.fly_to_position(F_1)                      


    def allocate_steering_points(self, drones, vertices):
        # Find the optimal steering points for the drones on the extended hull
        allocated_steering_points = [pygame.Vector2(0, 0) for d in drones]

        # Find the N sheep furthest away from the center of mass (the steering points)
        # (Bubble) sorting the extended vertices based on the distance from the centre of mass
        steering_points = []
        copy_list = vertices
        for m in range(len(vertices)):
            for n in range(len(vertices) - m - 1):
                d = self.centre_of_mass.distance_to(copy_list[n])
                d2 = self.centre_of_mass.distance_to(copy_list[n + 1])
                if d > d2:
                    copy_list[n], copy_list[n + 1] = copy_list[n + 1], copy_list[n]
        steering_points = copy_list[:len(drones):-1]

        # Calculate the drones' positions on the disconnected extended hull (z-axis)
        # The disconnected extended hull from the first drone's position [0, M]
        initial = self.closest_vertex(drones[0].edge_point, vertices)
        line_segment = []  # line segment (z-axis): [0,M]
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
            vertex = self.closest_vertex(drone.position, vertices)  # TODO?
            drone_positions[i] = line_segment.index(vertex)

        # Generate possible allocations for each drone
        for drone in drones:
            drone.possible_allocations = []
            for point in steering_points:
                drone.possible_allocations.append([0, point])  # clockwise
                drone.possible_allocations.append([1, point])  # counterclcokwise

        # Calculate the optimal steering points for the drones based on the travel distance
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

        # Steering points allocation optimisation
        # Sort the list of possible allocations of the steering points based on the closest travel distance from each drone
        for drone in drones:
            temp_list = drone.possible_allocations
            for m in range(len(drone.possible_allocations)):
                for n in range(len(drone.possible_allocations) - m - 1):
                    d = drone.possible_allocations[n][2]
                    d2 = drone.possible_allocations[n + 1][2]
                    if d > d2:
                        temp_list[n], temp_list[n + 1] = temp_list[n + 1], temp_list[n]
            drone.possible_allocations = temp_list

        # Remark 5: Each drone is allocated to each steering point, if there is enough of steering points to be allocated, or else the drone stand by
        x = 0
        if len(steering_points) <= len(drones):
            x = len(steering_points) - len(drones)
            if x < 0:
                x = 0

        # Allocation of the optimal steering point for each drone
        for i in range(len(drones) - x):
            drone = drones[i]
            for el in drone.possible_allocations:
                direction = el[0]
                point = el[1]
                distance = el[2]
                if allocated_steering_points[i] != pygame.Vector2(0, 0):
                    break
                if point not in allocated_steering_points:
                    drone.steering_point = point
                    drone.direction_index = direction
                    # Avoid duplicate of the steering points, so two or more drones do not fly to the same steering point
                    allocated_steering_points[i] = point

        # Find the flying path for the drone to the allocated steering point
        for i in range(len(drones)):
            drone = drones[i]
            drone.travel_path = []

            # Check if the drone is allocated a steering point
            if allocated_steering_points[i] == pygame.Vector2(0, 0):
                # print(drone.id, "No steering point set")
                continue

            # Calculte the drone's path
            start_index = drone_positions[i]
            end_index = line_segment.index(drone.steering_point)

            for n in range(len(line_segment)):
                if drone.direction_index == 0:
                    if end_index > start_index:  # (29)
                        drone.left_pass = 1
                    else:
                        drone.left_pass = 0
                    index = n - drone.left_pass * len(line_segment)  # (31)
                if drone.direction_index == 1:
                    if end_index < start_index:  # (30)
                        drone.right_pass = 1
                    else:
                        drone.right_pass = 0
                    index = n + drone.right_pass * len(line_segment)  # (31)
                # Only append the vertices that are between the starting position and the steering point
                if start_index <= n <= end_index:
                    drone.travel_path.append(line_segment[index])



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


    def run(self, drones, sheeps, goal, centre_of_mass):
        #self.centre_of_mass = centre_of_mass

        convex_vertices, convex_hull = self.convex_hull(sheeps)
        extended_vertices, extended_hull = self.extended_hull(convex_vertices)

        # The minimum distance of gathering, before the animals need to be driven to a designated location
        gather_radius = pygame.draw.circle(self.canvas, pygame.Color("orange"), centre_of_mass, SHEEP_RADIUS, 1)

        # Wait until all the drones have arrived to the extended hull, before flying to their allocated steering points
        for drone in drones:
            if drone.figure.colliderect(extended_hull):
                self.on_edge = True

        # The drone will either fly TO the edge or along (ON) the edge
        if self.on_edge == False and self.toward_goal == False:
            for drone in drones:
                self.fly_to_egde(drone, extended_vertices)

        # When the drones arrive at the edge of the sheep flock, begin to gather them more closer to each other
        if self.on_edge == True and self.toward_goal == False and not gather_radius.contains(convex_hull):
            self.allocate_steering_points(drones, extended_vertices)
            for drone in drones:
                self.fly_on_edge(drone, extended_vertices, convex_vertices)
                
        # Check if the sheep flock is gathered enough, if so, push them toward the goal
        if gather_radius.contains(convex_hull) and self.toward_goal == False and self.on_edge == True:
            self.toward_goal = True
        else:
            self.toward_goal = False

        if self.toward_goal == True and gather_radius.contains(convex_hull):
            steering = False
            if drones[0].collides_with_point and drones[1].collides_with_point and drones[2].collides_with_point:
                steering = True
            else:
                steering = False
        
            for drone in drones:
                if self.drive_type == 'async':
                    drone.find_steering_point_async(sheeps, goal, centre_of_mass, steering, self.theta)
                if self.drive_type == 'sync':
                    drone.find_steering_point_sync(sheeps, goal, centre_of_mass, self.theta)
        

        
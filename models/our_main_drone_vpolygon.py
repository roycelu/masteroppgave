import pygame
import numpy as np
import shapely.geometry as shp
from scipy.spatial import ConvexHull
from models.goal import Goal


DISTANCE = 20 # drone-to-animal distance (predefined)
TURNING_RADIUS = 5  # minimum turning radius of the drone (predefined?)
SHEEP_RADIUS = 20 # the sheep's smallest circle during driving (predefined)


class OurMainDroneVPolygon:
    def __init__(self, canvas, goal, theta):
        self.canvas = canvas

        self.main_goal = goal
        self.goal = Goal(goal.position)

        self.on_edge = False
        self.toward_goal = False

        self.theta = theta


    def convex_hull(self, sheeps):
        # Creates a convex hull from the sheep's positions
        points = []
        positions = []

        for sheep in sheeps:
            positions.append(sheep.position)

        hull = ConvexHull(positions)
        for i in hull.vertices:
            points.append(positions[i])

        figure = pygame.draw.polygon(self.canvas, pygame.Color("palegreen3"), points, 1)
        return points, figure


    def extended_hull(self, vertices):
        # Create an extended hull from the convex hull where the drones will fly
        extended_hull = []

        polygon = shp.Polygon([[v.x, v.y] for v in vertices]).buffer(DISTANCE, join_style=2, mitre_limit=1)
        polygon_list = polygon.exterior.coords
        for i in range(len(polygon_list) - 1):
            point = pygame.Vector2(polygon_list[i][0], polygon_list[i][1])
            extended_hull.append(point)
            pygame.draw.circle(self.canvas, pygame.Color("red4"), point, 2)

        figure = pygame.draw.polygon(self.canvas, pygame.Color("red4"), extended_hull, 2)
        return extended_hull, figure


    def fly_to_egde(self, drone, vertices, sheep, dt, target_fps):
        # Make the drone fly to the extended hull
        closest_point = pygame.Vector2(0, 0)
        shortest_distance = np.inf
        edge_vertices = [pygame.Vector2(0, 0), pygame.Vector2(0, 0)]

        for j in range(len(vertices) - 1):
            O = pygame.Vector2(0, 0)
            q = pygame.Vector2(vertices[j]) - pygame.Vector2(vertices[j + 1])
            p = drone.position - pygame.Vector2(vertices[j + 1])
            b = pygame.Vector2(0, 0)  # Drone to O

            o = ((1 / q.length()) * p.dot(q)) * (1 / q.length()) * q 

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

            # Find the closest point on the extended hull
            if drone.position.distance_to(O) < shortest_distance:
                shortest_distance = drone.position.distance_to(O)
                closest_point = O
                edge_vertices[0] = pygame.Vector2(vertices[j])
                edge_vertices[1] = pygame.Vector2(vertices[j + 1])

        drone.edge_point = closest_point
        drone.fly_to_position(closest_point, sheep, dt, target_fps)


    def fly_on_edge(self, drone, vertices, convex_vertices, sheep, dt, target_fps):
        # Make the drone fly along the extended hull
        if len(drone.travel_path) == 0:
            # BRAKE - stop the drone when it arrives at the final vertex
            drone.fly_to_position(drone.steering_point, sheep, dt, target_fps)
        else:
            # TRANSFER - arc trajectory to the steering point
            new = drone.travel_path.pop(0)
            drone.edge_point = new

            # Find the next point on the list when arrived the first one
            prev, curr, next = self.get_indices(vertices.index(new), len(vertices))

            current_point = vertices[curr]
            edge1 = pygame.Vector2(vertices[prev] - current_point)
            edge2 = pygame.Vector2(vertices[next] - current_point)

            # Calculate the angle between two edges, (0,pi) 
            angle = np.arccos(edge1.dot(edge2) / (edge1.length() * edge2.length()))

            # Calculate the turning trajectory
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
            )  

            # To avoid dispersing the sheep, therefore ensure that the turning trajectory do not touch the convex hull
            if DISTANCE <= TURNING_RADIUS:
                # If the inequalities does not hold, the drone flies directly to the point instead of along the arc trajectory
                if not (convex_vertex - C_t).length() < TURNING_RADIUS:
                    if not np.sin(angle / 2) > 1 - (DISTANCE / TURNING_RADIUS):
                        if not angle > 2 * np.arcsin(1 - (DISTANCE / TURNING_RADIUS)):
                            drone.fly_to_position(current_point, sheep, dt, target_fps)
            else:
                drone.fly_to_position(new, sheep, dt, target_fps)
                if drone.direction_index == 0:
                    if drone.figure.collidepoint(F_1):
                        drone.fly_to_position(F_2, sheep, dt, target_fps)
                if drone.direction_index == 1:
                    if drone.figure.collidepoint(F_2):
                        drone.fly_to_position(F_1, sheep, dt, target_fps)                      


    def allocate_steering_points(self, drones, vertices, centre_of_mass):
        # Find the optimal steering points for the drones on the extended hull
        allocated_steering_points = [pygame.Vector2(0, 0) for d in drones]

        # Find the N sheep furthest away from the center of mass (the steering points)
        # (Bubble) sorting the extended vertices based on the distance from the centre of mass
        steering_points = []
        copy_list = vertices
        for m in range(len(vertices)):
            for n in range(len(vertices) - m - 1):
                d = centre_of_mass.distance_to(copy_list[n])
                d2 = centre_of_mass.distance_to(copy_list[n + 1])
                if d > d2:
                    copy_list[n], copy_list[n + 1] = copy_list[n + 1], copy_list[n]
        #steering_points = copy_list[:len(drones):-1]
        steering_points = copy_list[len(copy_list)-len(drones):]
        steering_points.reverse()

        # Calculate the drones' positions on the disconnected extended hull (z-axis)
        # The disconnected extended hull from the first drone's position [0, M]
        initial_drone = None
        for drone in drones:
            if drone.id == 0:
                initial_drone = drone
        initial = self.closest_vertex(initial_drone.position, vertices)
        line_segment = []  # line segment (z-axis): [0,M]
        temp = []
        for i in range(len(vertices)):
            if i >= vertices.index(initial):
                line_segment.append(vertices[i])
            else:
                temp.append(vertices[i])
        line_segment.extend(temp)

      # Relabel the drone ids counterclockwise, so they won't collide. Returns the drones' closest point on the disconnected extended hull (z-axis)
        corners = self.closest_vertex2(line_segment, drones)
        drone_positions = [0 for d in drones]
        for i in range(len(drones)):
            drone_positions[i] = line_segment.index(corners[i])

        # Generate possible allocations for each drone
        for drone in drones:
            drone.possible_allocations = []
            for point in steering_points:
                drone.possible_allocations.append([0, point])  # clockwise
                drone.possible_allocations.append([1, point])  # counterclcokwise

        # Calculate the optimal steering points for the drones based on the travel distance
        for drone in drones:
            #i = drones.index(drone)
            i = drone.id
            for el in drone.possible_allocations:
                # Calculate the position on the disconnected extended hull and the travel distance
                direction = el[0]  # direction index (z)
                point = el[1]  # possible steering point (s')
                s = line_segment.index(point)  # index of the point on the z-axis (z')
                # Compute and find how the drone moves along the z-axis
                if s > drone_positions[i] and direction == 0:  
                    drone.left_pass = 1
                else:
                    drone.left_pass = 0
                if s < drone_positions[i] and direction == 1: 
                    drone.right_pass = 1
                else:
                    drone.right_pass = 0
                # Find the drone's position on the extended z-axis
                if direction == 0:
                    z_star = s - drone.left_pass * len(line_segment)
                if direction == 1:
                    z_star = s + drone.right_pass * len(line_segment)
                # Compute the travel distance from the drone to the possible steering point
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
            x = len(drones) - len(steering_points)
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
            end_index = line_segment.index(allocated_steering_points[i])

            for n in range(len(line_segment)):
                if drone.direction_index == 0:
                    if end_index > start_index:  
                        drone.left_pass = 1
                    else:
                        drone.left_pass = 0
                    index = n - drone.left_pass * len(line_segment)  
                if drone.direction_index == 1:
                    if end_index < start_index: 
                        drone.right_pass = 1
                    else:
                        drone.right_pass = 0
                    index = n + drone.right_pass * len(line_segment)  
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
        """Find the closest corner"""
        shortest_distance = np.inf
        corners = []
        for i in range(len(vertices)-1):
            q = pygame.Vector2(0, 0)
            if i == len(vertices):
                q = vertices[i] - vertices[0]
                p = point - vertices[0]
                o = ((1 / q.length()) * p.dot(q)) * (1 / q.length()) * q 
                b = o - p
                distance = np.linalg.norm(b)
                if distance < shortest_distance:
                    shortest_distance = distance
                    corners = [vertices[i], vertices[0]]
            else:
                q = vertices[i] - vertices[i+1]
                p = point - vertices[i+1]
                o = ((1 / q.length()) * p.dot(q)) * (1 / q.length()) * q 
                b = o - p
                distance = np.linalg.norm(b)

                if distance < shortest_distance:
                    shortest_distance = distance
                    corners = [vertices[i], vertices[i+1]]
        
        if corners[0].distance_to(point) < corners[1].distance_to(point):
            return corners[0]
        else:
            return corners[1]
        

    def closest_vertex2(self, line_segment, drones):
        """Find the closest corners for all the drones, and their position on the straight line segment"""
        shortest_distance0 = np.inf
        shortest_distance1 = np.inf
        shortest_distance2 = np.inf
        corners0 = []
        corners1 = []
        corners2 = []
        drone0_edge = 0
        drone1_edge = 0
        drone2_edge = 0
        # Find the distance to the corners connected to the edge every drone is on
        for i in range(len(line_segment)-1):
            for drone in drones:
                q = pygame.Vector2(0, 0)
                if i == len(line_segment):
                    q = line_segment[i] - line_segment[0]
                    p = drone.position - line_segment[0]
                    o = ((1 / q.length()) * p.dot(q)) * (1 / q.length()) * q 
                    b = o - p
                    distance = np.linalg.norm(b)

                    if drone.id == 0:
                        if distance < shortest_distance0:
                            drone0_edge = i
                            shortest_distance0 = distance
                            corners0 = [line_segment[i], line_segment[0]]
                    if drone.id == 1:
                        if distance < shortest_distance1:
                            drone1_edge = i
                            shortest_distance1 = distance
                            corners1 = [line_segment[i], line_segment[0]]
                    if drone.id == 2:
                        if distance < shortest_distance2:
                            drone2_edge = i
                            shortest_distance2 = distance
                            corners2 = [line_segment[i], line_segment[0]]
                else:
                    q = line_segment[i] - line_segment[i+1]
                    p = drone.position - line_segment[i+1]
                    o = ((1 / q.length()) * p.dot(q)) * (1 / q.length()) * q 
                    b = o - p
                    distance = np.linalg.norm(b)
                    
                    if drone.id == 0:
                        if distance < shortest_distance0:
                            drone0_edge = i
                            shortest_distance0 = distance
                            corners0 = [line_segment[i], line_segment[i+1]]
                    if drone.id == 1:
                        if distance < shortest_distance1:
                            drone1_edge = i
                            shortest_distance1 = distance
                            corners1 = [line_segment[i], line_segment[i+1]]
                    if drone.id == 2:
                        if distance < shortest_distance2:
                            drone2_edge = i
                            shortest_distance2 = distance
                            corners2 = [line_segment[i], line_segment[i+1]]
    
        edge_list = [drone0_edge, drone1_edge, drone2_edge]
        if edge_list[0] == edge_list[1] == edge_list[2]: # Check if all drones are on the same edge and update their id accordingly
            drone0_dist = [drones[0].position.distance_to(line_segment[0]), 0]
            drone1_dist = [drones[1].position.distance_to(line_segment[0]), 1]
            drone2_dist = [drones[2].position.distance_to(line_segment[0]), 2]
            dist_list = [drone0_dist, drone1_dist, drone2_dist]
            dist_list.sort(key=lambda x:x[0], reverse=True) 
            i = 0
            for i in range(len(dist_list)):
                drone_number = dist_list[i][1]
                drones[drone_number].id = i
                i += 1

        elif edge_list[0] == edge_list[1]: # Check if drone 0 and 1 are on the same edge and update their id accordingly
            drone0_dist = [drones[0].position.distance_to(line_segment[0]), 0]
            drone1_dist = [drones[1].position.distance_to(line_segment[0]), 1]
            dist_list = [drone0_dist, drone1_dist]
            dist_list.sort(key=lambda x:x[0], reverse=True) 
            drones_list = [0, 1]
            i = 0
            for drone_id in drones_list:
                drone_number = dist_list[i][1]
                drones[drone_number].id = drone_id
                i += 1
            drones[2].id = 2

        elif edge_list[0] == edge_list[2]: # Check if drone 0 and 2 are on the same edge and update their id accordingly
            drone0_dist = [drones[0].position.distance_to(line_segment[0]), 0]
            drone2_dist = [drones[2].position.distance_to(line_segment[0]), 2]
            dist_list = [drone0_dist, drone2_dist]
            dist_list.sort(key=lambda x:x[0], reverse=True)

            drones_list = [0, 1]
            i = 0
            for drone_id in drones_list:
                drone_number = dist_list[i][1]
                drones[drone_number].id = drone_id
                i+= 1
            drones[1].id = 2

        elif edge_list[1] == edge_list[2]: # Check if drone 1 and 2 are on the same edge and update their id accordingly
            drone1_dist = [drones[1].position.distance_to(line_segment[drone1_edge]), 1]
            drone2_dist = [drones[2].position.distance_to(line_segment[drone2_edge]), 2]
            dist_list = [drone1_dist, drone2_dist]
            dist_list.sort(key=lambda x:x[0], reverse=True) 

            drones_list = [1, 2]
            i = 0
            for drone_id in drones_list:
                drone_number = dist_list[i][1]
                drones[drone_number].id = drone_id
                i += 1
            drones[0].id = 0

        else:
            drones[0].id = 0
            if drone1_edge > drone2_edge:
                drones[1].id = 2
                drones[2].id = 1
            if drone1_edge < drone2_edge:
                drones[1].id = 1
                drones[2].id = 2
        
        # Set the closest corners
        corners = [0 for d in drones]
        if corners0[0].distance_to(drones[0].position) < corners0[1].distance_to(drones[0].position):
            corners[0] = corners0[0]
        else:
            corners[0] = corners0[1]

        if corners1[0].distance_to(drones[1].position) < corners1[1].distance_to(drones[1].position):
            corners[1] = corners1[0]
        else:
            corners[1] = corners1[1]
            
        if corners2[0].distance_to(drones[2].position) < corners2[1].distance_to(drones[2].position):
            corners[2] = corners2[0]
        else:
            corners[2] = corners2[1]
        return corners


    def run(self, drones, sheeps, goal, centre_of_mass, dt, target_fps):
        convex_vertices, convex_hull = self.convex_hull(sheeps)
        extended_vertices, extended_hull = self.extended_hull(convex_vertices)

        # The minimum distance of gathering, before the animals need to be driven to a designated location
        gather_radius = pygame.draw.circle(self.canvas, pygame.Color("palegreen3"), centre_of_mass, SHEEP_RADIUS, 1)

        # Wait until all the drones have arrived to the extended hull, before flying to their allocated steering points
        for drone in drones:
            if drone.figure.colliderect(extended_hull):
                self.on_edge = True

        # The drone will either fly TO the edge or along (ON) the edge
        if self.on_edge == False and self.toward_goal == False:
            for drone in drones:
                self.fly_to_egde(drone, extended_vertices, sheeps, dt, target_fps)

        # When the drones arrive at the edge of the sheep flock, begin to gather them more closer to each other
        if self.on_edge == True and self.toward_goal == False and not gather_radius.contains(convex_hull):
            self.allocate_steering_points(drones, extended_vertices, centre_of_mass)
            for drone in drones:
                self.fly_on_edge(drone, extended_vertices, convex_vertices, sheeps, dt, target_fps)
                
        # Check if the sheep flock is gathered enough, if so, push them toward the goal
        if not gather_radius.contains(convex_hull):
            self.toward_goal = False
        else:
            self.toward_goal = True

        if self.toward_goal == True and gather_radius.contains(convex_hull):
            steering = False
            if drones[0].collides_with_point and drones[1].collides_with_point and drones[2].collides_with_point:
                steering = True
            else:
                steering = False
        
            for drone in drones:
                drone.find_steering_point(sheeps, goal, centre_of_mass, steering, self.theta, dt, target_fps, self.canvas)

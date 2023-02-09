import pygame
import numpy as np
import shapely.geometry as shp
from scipy.spatial import ConvexHull
from utils import Calculate

"""[UFERDIG] Revidert kode fra https://github.com/roycelu/prosjektoppgave/tree/main/swarm_simulation/reynold"""


class RoyceMoiraMethod:
    def __init__(self, canvas, font, goal, drones, sheeps):
        self.canvas = canvas
        self.font = font
        self.goal = goal
        self.drones = drones
        self.sheeps = sheeps

        self.extended_hull_goal = False
        self.hull_position_goal = False
        self.path_goal = False

        self.zigzag_index = -1
        self.prev_zigzag_index = -1

    def create_convex_hull(self, sheeps):
        center_of_mass = Calculate.center_of_mass(sheeps)
        points = []
        positions = []
        for sheep in sheeps:
            positions.append(sheep.position)
        hull = ConvexHull(positions)

        for index in hull.vertices:
            points.append(sheeps[index].position)

        pygame.draw.polygon(self.canvas, pygame.Color("black"), points, 2)
        return points

    def create_extended_hull(self, sheeps):
        convex_hull = self.create_convex_hull(sheeps)
        extended_hull = []
        # Create shapely polygon from the convex hull points
        poly = shp.Polygon([[p.x, p.y] for p in convex_hull])
        simple_poly = poly.simplify(0.0001)
        # Make two buffered polygons
        extended_outer_poly = simple_poly.buffer(50, 4)
        extended_inner_poly = simple_poly.buffer(30, 4)
        # Find the vertices of these polygons
        extended_outer_array = np.array(extended_outer_poly.exterior)
        extended_inner_array = np.array(extended_inner_poly.exterior)

        size = 4
        center = pygame.Vector2(size, size) / 4
        # The outer extended hull
        buffered_hull_outer = []
        for i in range(len(extended_outer_array) - 1):
            buffered_hull_outer.append(
                pygame.Vector2(extended_outer_array[i][0], extended_outer_array[i][1])
            )
        # Drawing the outer hull
        for point in buffered_hull_outer:
            pygame.draw.circle(self.canvas, pygame.Color("gray"), point + center, size)
        pygame.draw.polygon(self.canvas, pygame.Color("gray"), buffered_hull_outer, 2)

        buffered_hull_inner = []
        for i in range(len(extended_inner_array) - 1):
            buffered_hull_inner.append(
                pygame.Vector2(extended_inner_array[i][0], extended_inner_array[i][1])
            )
        # Drawing the inner hull
        for point in buffered_hull_inner:
            pygame.draw.circle(self.canvas, pygame.Color("gray"), point + center, size)
        pygame.draw.polygon(self.canvas, pygame.Color("gray"), buffered_hull_inner, 1)

        return buffered_hull_outer, buffered_hull_inner

    def calculate_positions_toward_next_point(
        self, sheeps, goal_position, extended_hull_poly
    ):
        # Calculates and returns the five positions of the drones on the extended hull
        center_of_mass = Calculate.center_of_mass(sheeps)
        vector = pygame.Vector2(goal_position - center_of_mass)
        back_vector = -vector * 100  # Times 100 in case the path is very close
        line_back = shp.LineString([center_of_mass, center_of_mass + back_vector])

        point_back = pygame.Vector2(0, 0)
        point_left1 = pygame.Vector2(0, 0)
        point_left2 = pygame.Vector2(0, 0)
        point_right1 = pygame.Vector2(0, 0)
        point_right2 = pygame.Vector2(0, 0)

        # Points at xx degree away from point a
        # vector_left1 = (back_vector[0] * np.cos(np.pi / 6) - back_vector[1] * np.sin(np.pi / 6), back_vector[0] * np.sin(np.pi / 6) + back_vector[1] * np.cos(np.pi / 6))
        vector_left1 = back_vector.rotate_rad(np.pi / 6)
        vector_right1 = back_vector.rotate_rad(-np.pi / 6)
        vector_left2 = back_vector.rotate_rad(np.pi / 2)
        vector_right2 = back_vector.rotate_rad(-np.pi / 2)

        distance = 45
        alpha_left = distance / vector_left2.magnitude()
        alpha_right = distance / vector_right2.magnitude()

        vector_left2_test = vector_left2 * alpha_left
        vector_right2_test = vector_right2 * alpha_right
        point_left2_test = center_of_mass + vector_left2_test
        point_right2_test = center_of_mass + vector_right2_test

        line_left1 = shp.LineString([center_of_mass, center_of_mass + vector_left1])
        line_left2 = shp.LineString([center_of_mass, center_of_mass + vector_left2])
        line_right1 = shp.LineString([center_of_mass, center_of_mass + vector_right1])
        line_right2 = shp.LineString([center_of_mass, center_of_mass + vector_right2])

        i = 0
        for vertex in extended_hull_poly:
            if i == len(extended_hull_poly) - 1:
                line_polygon = shp.LineString([vertex, extended_hull_poly[0]])
            else:
                line_polygon = shp.LineString([vertex, extended_hull_poly[i + 1]])

            int_pt_back = line_back.intersection(line_polygon)
            int_pt_left1 = line_left1.intersection(line_polygon)
            int_pt_left2 = line_left2.intersection(line_polygon)
            int_pt_right1 = line_right1.intersection(line_polygon)
            int_pt_right2 = line_right2.intersection(line_polygon)

            if not int_pt_back.is_empty:
                point_back = pygame.Vector2(int_pt_back.x, int_pt_back.y)
            if not int_pt_left1.is_empty:
                point_left1 = pygame.Vector2(int_pt_left1.x, int_pt_left1.y)
            if not int_pt_left2.is_empty:
                point_left2 = pygame.Vector2(int_pt_left2.x, int_pt_left2.y)
            if not int_pt_right1.is_empty:
                point_right1 = pygame.Vector2(int_pt_right1.x, int_pt_right1.y)
            if not int_pt_right2.is_empty:
                point_right2 = pygame.Vector2(int_pt_right2.x, int_pt_right2.y)

            i += 1

            size = 10
            center = pygame.Vector2(size, size) / 4
            color = pygame.Color("pink")
            pygame.draw.circle(self.canvas, color, point_left1 + center, size)
            self.__add_label("L1", point_left1 + center)
            pygame.draw.circle(self.canvas, color, point_right1 + center, size)
            self.__add_label("R1", point_right1 + center)
            pygame.draw.circle(self.canvas, color, point_left2 + center, size)
            self.__add_label("L2", point_left2 + center)
            pygame.draw.circle(self.canvas, color, point_right2 + center, size)
            self.__add_label("R2", point_right2 + center)

            pygame.draw.circle(self.canvas, color, point_back + center, size)
            self.__add_label("B", point_back + center)
            pygame.draw.line(self.canvas, color, center_of_mass, goal_position)

            return (
                point_left2_test,
                point_left1,
                point_back,
                point_right1,
                point_right2_test,
            )

    def fly_to_edge_convex_hull(self, drones, goal, extended_hull_poly):
        # For every drone, fly to the edge of the convex hull that is closest
        shortest_distance = np.inf
        closest_vertex = pygame.Vector2(np.inf, np.inf)
        for drone in drones:
            for vertex in extended_hull_poly:
                distance = vertex - drone.position
                if distance.magnitude() < shortest_distance:
                    shortest_distance = distance.magnitude()
                    closest_vertex = vertex
            drone.goal_position = closest_vertex
            drone.fly_to_position(drone.goal_position)

            if drone.figure.colliderect(goal.figure):
                drone.goal_status = True

        if drones[0].goal_status and drones[1].goal_status and drones[2].goal_status:
            self.extended_hull_goal = True
            drones[0].goal_status, drones[1].goal_status, drones[2].goal_status = False

    def fly_on_edge_convex_hull(self, extended_hull_poly, drones, left, back, right):
        drones[0].goal_status, drones[1].goal_status, drones[2].goal_status = False
        for drone in drones:
            if drone.id == 0:
                self.fly_on_edge_guidance_law(drone, extended_hull_poly, left)
            if drone.id == 1:
                self.fly_on_edge_guidance_law(drone, extended_hull_poly, back)
            if drone.id == 2:
                self.fly_on_edge_guidance_law(drone, extended_hull_poly, right)
        if drones[0].goal_status and drones[1].goal_status and drones[2].goal_status:
            self.hull_position_goal = True

    def fly_on_edge_guidance_law(drone, extended_hull, goal):
        position_to_vertex = np.inf
        drone_to_vertex = np.inf
        closest_position_index = 0
        closest_drone_index = 0

        i = 0
        for vertex in extended_hull:
            pos_vertex = (goal.position - vertex).magnitude()
            if pos_vertex < position_to_vertex:
                position_to_vertex = pos_vertex
                closest_position_index = i
            drone_vertex = (drone.position - vertex).magnitude()
            if drone_vertex < drone_to_vertex:
                drone_to_vertex = drone_vertex
                closest_drone_index = i
            i += 1

        path_1 = []
        path_2 = []
        path_1_length = 0
        path_2_length = 0
        # Creating two paths of vertices, one clockwise, the other counterclockwise
        if closest_position_index < closest_drone_index:
            path_1 = extended_hull[closest_position_index:closest_drone_index]
            np.append(path_1, goal.position)
            path_2 = extended_hull[closest_drone_index:]
            np.append(path_2, extended_hull[:closest_position_index])
            np.append(path_2, goal.position)
        else:
            path_1 = extended_hull[closest_drone_index:closest_position_index]
            np.append(path_1, goal.position)
            path_2 = extended_hull[closest_position_index:]
            np.append(path_2, extended_hull[:closest_drone_index])
            np.append(path_2, goal.position)

        # Finding the length of the two paths
        j = 0
        for vertex in path_1:
            if j == len(path_1) - 1:
                path_1_length += np.linalg.norm(vertex - path_1[0])
            else:
                path_1_length += np.linalg.norm(vertex - path_1[j + 1])
            j += 1
        k = 0
        for vertex in path_2:
            if k == len(path_2) - 1:
                path_2_length += np.linalg.norm(vertex - path_2[0])
            else:
                path_2_length += np.linalg.norm(vertex - path_2[k + 1])
            k += 1

        # If the drone is already on the desired position, stay there, else, fly along the shortest path
        if drone.figure.colliderect(goal.figure):
            drone.fly_to_position(goal.position)
        else:
            if path_1_length < path_2_length:
                for point in path_1:
                    drone.fly_to_position(point)
            else:
                for point in path_2:
                    drone.fly_to_position(point)

        if drone.figure.colliderect(goal.figure):
            drone.goal_status = True

    def fly_on_buffered_hull(
        self,
        drones,
        extended_inner_poly,
        extended_outer_poly,
        left2,
        back2,
        right2,
        mass_center,
        back,
        left,
        right,
        back_left,
        back_right,
    ):
        drone = drones[1]
        if drone.id == 1:
            point = shp.Point(drone.position)
            # "KRANGLER" LITT OM HVOR DRONEN SKAL.
            if shp.Polygon(extended_inner_poly).contains(
                point
            ):  # Sjekker om dronen er innenfor det indre hullet
                self.fly_on_edge_guidance_law(drone, extended_inner_poly, back)
            else:
                self.zigzag_movement(
                    drone, extended_inner_poly, [back_left, back2, back_right]
                )

        # If the drones are too far from the mass center, fly closer to avoid the spreading of sheep
        drone0_masscenter = np.linalg.norm(drones[0].position - mass_center)
        drone2_masscenter = np.linalg.norm(drones[2].position - mass_center)

        if drone0_masscenter > 25:
            self.fly_on_edge_guidance_law(drones[0], extended_inner_poly, left2)
        else:
            self.fly_on_edge_guidance_law(drone[0], extended_inner_poly, left)

        if drone2_masscenter > 25:
            self.fly_on_edge_guidance_law(drones[2], extended_inner_poly, right2)
        else:
            self.fly_on_edge_guidance_law(drones[2], extended_inner_poly, right)

    def zigzag_movement(self, drone, poly, movement):
        # drone.id = drone1 | poly = np.array(poly.exterior) | movement = [outer_left, centre, outer_right]
        if (
            self.zigzag_index == -1
        ):  # Sørger for at zigzag_index settes, default i midten
            self.zigzag_index = 1

        if (movement[1][0] - 1 <= drone.position[0] <= movement[1][0] + 1) and (
            movement[1][1] - 1 <= drone.position[1] <= movement[1][1] + 1
        ):
            # Centre. Zigzag to left.
            if self.prev_zigzag_index > self.zigzag_index:
                self.zigzag_index = 0
                self.prev_zigzag_index = 1
            # Centre. Zigag to right.
            else:
                self.zigzag_index = 2
                self.prev_zigzag_index = 1
        # Left. Zigzag to centre.
        if (movement[0][0] - 1 <= drone.position[0] <= movement[0][0] + 1) and (
            movement[0][1] - 1 <= drone.position[1] <= movement[0][1] + 1
        ):
            self.zigzag_index = 1
            self.prev_zigzag_index = 0
        # Right. Zigzag to centre.
        if (movement[2][0] - 1 <= drone.position[0] <= movement[2][0] + 1) and (
            movement[2][1] - 1 <= drone.position[1] <= movement[2][1] + 1
        ):
            self.zigzag_index = 1
            self.prev_zigzag_index = 2

        # drone.max_speed = 5
        self.fly_on_edge_guidance_law(drone, poly, movement[self.zigzag_index])

    def __add_label(self, text, position):
        label = self.font.render(text, True, pygame.Color("black"))
        rect = label.get_rect()
        rect.center = position
        self.canvas.blit(label, rect)

    def main(self, drones, sheeps, goal):
        centre_of_mass = Calculate.center_of_mass(sheeps)
        convex_hull = self.create_convex_hull(sheeps)
        extended_hull_outer, extended_hull_inner = self.create_extended_hull(sheeps)

        # Fly to the extended hull if this has not been reached
        if self.extended_hull_goal == False:
            # print("Flying to edge")
            self.fly_to_edge_convex_hull(drones, goal, extended_hull_outer)

        # If the drones are at the extended hull, fly along it to position themselves towards the first point on the path
        elif (self.extended_hull_goal) and (self.hull_position_goal == False):
            # print("Positioning around hull")
            (
                left2,
                left1,
                back,
                right1,
                right2,
            ) = self.calculate_positions_toward_next_point(
                extended_hull_outer, sheeps, self.canvas
            )
            self.fly_on_edge_convex_hull(
                extended_hull_outer, drones, left2, back, right2
            )

        # If the drones are correctly positioned, fly closer to the sheep so as to make them move
        elif self.extended_hull_goal and self.hull_position_goal:
            # print("Drive the sheep to path")
            (
                left2,
                left1,
                back,
                right1,
                right2,
            ) = self.calculate_positions_toward_next_point(
                extended_hull_outer, sheeps, self.canvas
            )
            (
                left2_2,
                left1_2,
                back_2,
                right1_2,
                right2_2,
            ) = self.calculate_positions_toward_next_point(
                extended_hull_inner, sheeps, self.canvas
            )
            self.fly_on_buffered_hull(
                drones,
                extended_hull_inner,
                extended_hull_outer,
                left2_2,
                back_2,
                right2_2,
                centre_of_mass,
                back,
                left2,
                right2,
                left1_2,
                right1_2,
            )

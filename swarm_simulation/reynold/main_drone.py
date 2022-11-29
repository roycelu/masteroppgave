import time
from scipy.spatial import ConvexHull
import numpy as np
import shapely.geometry as shp
from p5 import Vector


class MainDrone:
    def __init__(self, id, drone_path, polygon, point):
        self.id = id
        self.path = drone_path
        self.point = point
        self.polygon = polygon
        
        self.drone0_point = (70, 70)
        self.drone1_point = (50, 50)
        self.drone2_point = (30, 30)
        
        self.extended_hull_goal = False
        self.hull_position_goal = False
        self.path_goal = False

        self.zigzag_index = -1
        self.prev_zigzag_index = -1


    # Vises som massesenteret til sauene
    def draw_sheep_mass_centre(self, canvas, list_of_sheep):
        size = 3
        c = calculate_center_of_mass(list_of_sheep)
        # Draw the circle around the position (centre)
        x0 = c[0] - size/2
        y0 = c[1] - size/2
        x1 = c[0] + size/2
        y1 = c[1] + size/2
        canvas.create_oval(x0, y0, x1, y1, fill='red', tags=self.id)

    
    def draw_convex_and_extended_hull(self, canvas, list_of_sheep):
        # Returns array containing the vertices of the extended hull
        
        points = []
        positions = []
        new_positions = []
        for sheep in list_of_sheep:
            positions.append(sheep.position)
        hull = ConvexHull(positions)
       
        for index in hull.vertices:
            points.append(list_of_sheep[index].position[0])
            points.append(list_of_sheep[index].position[1])
            new_positions.append(list_of_sheep[index].position)
        
        canvas.create_polygon(points, fill='', outline='green', tags=self.id)

        buffered_hull = []
        buffered_hull2 = []
        # Create shaply polygon from the convex hull points
        poly = shp.Polygon([[p[0], p[1]] for p in new_positions])
        simple_poly = poly.simplify(0.0001)
        # Make two buffered polygons
        extended_outer_poly = simple_poly.buffer(50, 4)
        extended_inner_poly = simple_poly.buffer(30, 4)
        # Find the vertices of these polygons
        extended_outer_array = np.array(extended_outer_poly.exterior)
        extended_inner_array = np.array(extended_inner_poly.exterior)
        
        size = 4
        for l in range(0, len(extended_outer_array)-1):
            buffered_hull.append(extended_outer_array[l][0])
            buffered_hull.append(extended_outer_array[l][1])
            canvas.create_oval(extended_outer_array[l][0]-size/2, extended_outer_array[l][1]-size/2, extended_outer_array[l][0]+size/2, extended_outer_array[l][1]+size/2, fill='cyan', outline='black', tags=self.id)
        canvas.create_polygon(buffered_hull, fill='', outline='blue', tags=self.id)

        for l in range(0, len(extended_inner_array)-1):
            buffered_hull2.append(extended_inner_array[l][0])
            buffered_hull2.append(extended_inner_array[l][1])
            canvas.create_oval(extended_inner_array[l][0]-size/2, extended_inner_array[l][1]-size/2, extended_inner_array[l][0]+size/2, extended_inner_array[l][1]+size/2, fill='cyan', outline='black', tags=self.id)
        canvas.create_polygon(buffered_hull2, fill='', outline='blue', tags=self.id)

        return extended_outer_poly, extended_inner_poly

    def calculate_positions_toward_next_point(self, extended_hull_poly, list_of_sheep, canvas):

        # Calculates and returns the 5 positions for the drones on the extended hull
        mass_center = calculate_center_of_mass(list_of_sheep)
        vector = (self.point[0] - mass_center[0], self.point[1] - mass_center[1])
        back_vector = (-vector[0]*100, -vector[1]*100) # Times 100 in case the path is very close, making the vector very small
        line_back = shp.LineString([mass_center, np.add(mass_center, back_vector)])
        
        point_back = (0,0)
        point_left1 = (0,0)
        point_right1 = (0,0)
        point_left2 = (0,0)
        point_right2 = (0,0)

        # Points at pi/4 degree away from point a
        vector_left1 = (back_vector[0]*np.cos(np.pi/6)-back_vector[1]*np.sin(np.pi/6), back_vector[0]*np.sin(np.pi/6)+back_vector[1]*np.cos(np.pi/6))
        vector_right1 = (back_vector[0]*np.cos(-np.pi/6)-back_vector[1]*np.sin(-np.pi/6), back_vector[0]*np.sin(-np.pi/6)+back_vector[1]*np.cos(-np.pi/6))
        # Points at pi/3 degree away from point a
        vector_left2 = (back_vector[0]*np.cos(np.pi/2)-back_vector[1]*np.sin(np.pi/2), back_vector[0]*np.sin(np.pi/2)+back_vector[1]*np.cos(np.pi/2))
        vector_right2 = (back_vector[0]*np.cos(-np.pi/2)-back_vector[1]*np.sin(-np.pi/2), back_vector[0]*np.sin(-np.pi/2)+back_vector[1]*np.cos(-np.pi/2))

        line_left1 = shp.LineString([mass_center, np.add(mass_center, vector_left1)])
        line_left2 = shp.LineString([mass_center, np.add(mass_center, vector_left2)])
        line_right1 = shp.LineString([mass_center, np.add(mass_center, vector_right1)])
        line_right2 = shp.LineString([mass_center, np.add(mass_center, vector_right2)])

        poly_array = np.array(extended_hull_poly.exterior)
        # Create line between two vertices to check if any of the vectors/lines intersects
        i = 0
        for vertex in poly_array:
            if i == len(poly_array)-1:
                line_polygon = shp.LineString([vertex, poly_array[0]])
            else:
                line_polygon = shp.LineString([vertex, poly_array[i+1]])

            int_pt_back = line_back.intersection(line_polygon)
            int_pt_left1 = line_left1.intersection(line_polygon)
            int_pt_left2 = line_left2.intersection(line_polygon)
            int_pt_right1 = line_right1.intersection(line_polygon)
            int_pt_right2 = line_right2.intersection(line_polygon)

            if not int_pt_back.is_empty:
                point_back = int_pt_back.x, int_pt_back.y
            if not int_pt_left1.is_empty:
                point_left1 = int_pt_left1.x, int_pt_left1.y
            if not int_pt_left2.is_empty:
                point_left2 = int_pt_left2.x, int_pt_left2.y
            if not int_pt_right1.is_empty:
                point_right1 = int_pt_right1.x, int_pt_right1.y
            if not int_pt_right2.is_empty:
                point_right2 = int_pt_right2.x, int_pt_right2.y

            i += 1 
      
        # Draw the positions they should end up at
        size = 12
        canvas.create_oval(point_left1[0]-size/2, point_left1[1]-size/2, point_left1[0]+size/2, point_left1[1]+size/2, fill='brown', outline='cyan', tags=self.id)
        canvas.create_oval(point_right1[0]-size/2, point_right1[1]-size/2, point_right1[0]+size/2, point_right1[1]+size/2, fill='pink', outline='cyan', tags=self.id)
        canvas.create_oval(point_left2[0]-size/2, point_left2[1]-size/2, point_left2[0]+size/2, point_left2[1]+size/2, fill='green', outline='pink', tags=self.id)
        canvas.create_oval(point_right2[0]-size/2, point_right2[1]-size/2, point_right2[0]+size/2, point_right2[1]+size/2, fill='green', outline='pink', tags=self.id)

        canvas.create_oval(point_back[0]-size/2, point_back[1]-size/2, point_back[0]+size/2, point_back[1]+size/2, fill='purple', outline='pink', tags=self.id)
        canvas.create_line(mass_center[0], mass_center[1], self.point[0], self.point[1], fill='yellow', tags=self.id)

        return point_left2, point_left1, point_back, point_right1, point_right2


    def fly_to_edge_convex_hull(self, extended_hull_poly, list_of_drones):
        # For every drone, fly to the edge of the convex hull that is closest
        for drone in list_of_drones:
            drone.fly_to_edge_guidance_law(np.array(extended_hull_poly.exterior))
            if list_of_drones[0].extended_hull_goal and list_of_drones[1].extended_hull_goal and list_of_drones[2].extended_hull_goal:
                self.extended_hull_goal = True

            
    def fly_on_edge_convex_hull(self, extended_hull_poly, list_of_drones, left, back, right):
        if len(self.path) > 0:  # Sørger for at det eksisterer en path
            if self.point == (0,0):
                self.point = self.path[0]

            list_of_drones[0].hull_position_goal = False
            list_of_drones[1].hull_position_goal = False
            list_of_drones[2].hull_position_goal = False
             
            extended_hull = np.array(extended_hull_poly.exterior)
            for drone in list_of_drones:
                if drone.id == 'drone0':
                    drone.max_speed = 3.5
                    drone.fly_on_edge_guidance_law(extended_hull, left)
                if drone.id == 'drone1':
                    drone.fly_on_edge_guidance_law(extended_hull, back)
                if drone.id == 'drone2':
                    drone.fly_on_edge_guidance_law(extended_hull, right)

                if list_of_drones[0].hull_position_goal and list_of_drones[1].hull_position_goal and list_of_drones[2].hull_position_goal:
                    self.hull_position_goal = True

    
    def fly_on_buffered_hull(self, list_of_drones, extended_inner_poly, extended_outer_poly, left2, back2, right2, mass_center, back, left, right, back_left, back_right):
        if len(self.path) > 0:  # Sørger for at det eksisterer en path
            if self.point == (0,0):
                self.point = self.path[0]

            # list = [back2, right2, back2, left2]
            # if element in list:
            drone = list_of_drones[1]

            if drone.id == 'drone1':
                point = shp.Point(drone.position)
                # "KRANGLER" LITT OM HVOR DRONEN SKAL, DERFOR FORELØPIG KOMMENTERT UT.
                # if extended_inner_poly.contains(point):
                #     drone.fly_on_edge_guidance_law(np.array(extended_inner_poly.exterior), back)
                #     print("Within the poly")
                # else:
                #     # drone.fly_on_edge_guidance_law(np.array(extended_inner_poly.exterior), back2)
                #     self.zigzag_movement(drone, np.array(extended_inner_poly.exterior), [back_left, back2, back_right])
                self.zigzag_movement(drone, np.array(extended_inner_poly.exterior), [back_left, back2, back_right])

            # If the drones are too far from the mass center, fly closer to avoid the spreading of sheep
            drone0_masscenter = np.linalg.norm(list_of_drones[0].position - mass_center)
            drone2_masscenter = np.linalg.norm(list_of_drones[2].position - mass_center)

            if drone0_masscenter > 25:
                list_of_drones[0].fly_on_edge_guidance_law(np.array(extended_inner_poly.exterior), left2)
            else:
                list_of_drones[0].fly_on_edge_guidance_law(np.array(extended_inner_poly.exterior), left)

            if drone2_masscenter > 25:
                list_of_drones[2].fly_on_edge_guidance_law(np.array(extended_inner_poly.exterior), right2)
            else:
                list_of_drones[2].fly_on_edge_guidance_law(np.array(extended_inner_poly.exterior), right)
            # distance = np.linalg.norm(list_of_drones[0].position - list_of_drones[2].position)
            # if distance > 50:
            #     print("Drones far from each other")
            #     list_of_drones[0].fly_on_edge_guidance_law(np.array(extended_inner_poly.exterior), left2)
            #     list_of_drones[2].fly_on_edge_guidance_law(np.array(extended_inner_poly.exterior), right2)
            # else:
            #     print("Drones' position ok")
            #     list_of_drones[0].fly_on_edge_guidance_law(np.array(extended_inner_poly.exterior), left)
            #     list_of_drones[2].fly_on_edge_guidance_law(np.array(extended_inner_poly.exterior), right)
                
                if (mass_center[0] -10 <= self.point[0] <= mass_center[0] + 10) and (mass_center[1] - 10 <= self.point[1] <= mass_center[1] + 10):
                    if self.point == self.path[-1]:
                        #print("Fly to point", self.path_goal)
                        self.path_goal = True
                    else:    
                        self.point = self.path[self.path.index(self.point)+1]
                        #print("New point recieved", self.point, self.path)
                        self.hull_position_goal = False
    
    def zigzag_movement(self, drone, poly, movement):
        # drone.id = drone1 | poly = np.array(poly.exterior) | movement = [outer_left, centre, outer_right]
        if self.zigzag_index == -1:  # Sørger for at zigzag_index settes, default i midten
            self.zigzag_index = 1
        
        if (movement[1][0]-1 <= drone.position[0] <= movement[1][0]+1) and (movement[1][1]-1 <= drone.position[1] <= movement[1][1]+1):
            # Centre. Zigzag to left.
            if self.prev_zigzag_index > self.zigzag_index:
                self.zigzag_index = 0
                self.prev_zigzag_index = 1
            # Centre. Zigag to right.
            else:
                self.zigzag_index = 2
                self.prev_zigzag_index = 1
        # Left. Zigzag to centre.
        if (movement[0][0]-1 <= drone.position[0] <= movement[0][0]+1) and (movement[0][1]-1 <= drone.position[1] <= movement[0][1]+1):
            self.zigzag_index = 1
            self.prev_zigzag_index = 0
        # Right. Zigzag to centre.
        if (movement[2][0]-1 <= drone.position[0] <= movement[2][0]+1) and (movement[2][1]-1 <= drone.position[1] <= movement[2][1]+1):
            self.zigzag_index = 1
            self.prev_zigzag_index = 2
    
        drone.max_speed = 5
        drone.fly_on_edge_guidance_law(poly, movement[self.zigzag_index])   # FORTSATT LITT USTABIL
        # drone.fly_to_position(movement[self.zigzag_index])
        # drone.max_speed = 3 # Set back to default max speed?


    def main(self, list_of_sheep, canvas, list_of_drones):
        canvas.delete(self.id)
        self.draw_sheep_mass_centre(canvas, list_of_sheep)
        mass_center = calculate_center_of_mass(list_of_sheep)
        extended_outer_poly, extended_inner_poly = self.draw_convex_and_extended_hull(canvas, list_of_sheep)

        # Fly to the extended hull if this has not been reached
        if self.extended_hull_goal == False:
            #print("Flying to edge")
            self.fly_to_edge_convex_hull(extended_outer_poly, list_of_drones)
            
        # If the drones are at the extended hull, fly along it to position themselves towards the first point on the path
        elif (self.extended_hull_goal) and (self.hull_position_goal==False):
            #print("Positioning around hull")
            left2, left1, back, right1, right2 = self.calculate_positions_toward_next_point(extended_outer_poly, list_of_sheep, canvas)
            self.fly_on_edge_convex_hull(extended_outer_poly, list_of_drones, left2, back, right2)
        
        # If the drones are correctly positioned, fly closer to the sheep so as to make them move
        elif self.extended_hull_goal and self.hull_position_goal:
            #print("Drive the sheep to path")
            left2, left1, back, right1, right2 = self.calculate_positions_toward_next_point(extended_outer_poly, list_of_sheep, canvas)
            left2_2, left1_2, back_2, right1_2, right2_2 = self.calculate_positions_toward_next_point(extended_inner_poly, list_of_sheep, canvas)
            self.fly_on_buffered_hull(list_of_drones, extended_inner_poly, extended_outer_poly, left2_2, back_2, right2_2, mass_center, back, left2, right2, left1_2, right1_2)
                
        # Fly to the path and along the path 
        # PS:må endre position per nye punkt den har kommet til, altså se på neste punk og rotere basert på det, 
        # evt at dte blir mer krumninger. Dronene må hvertfall alltid være bak sauene.
        #if self.extended_hull_goal:
        #    self.calculate_center_back(poly_array, list_of_sheep, canvas)
        #    self.fly_along_path(list_of_drones)

        # else
        #
    


def calculate_center_of_mass(list_of_sheep):
    total = 0
    center_of_mass = np.zeros(2)
    for boid in list_of_sheep:
        center_of_mass += boid.position
        total += 1
    if total > 0:
        center_of_mass /= total
    
    # N = 0 # Number of sheep
    # center_of_mass = (0,0)
    
    # for sheep in list_of_sheep:
    #     position = sheep.get_position()
    #     print(position)
    #     center_of_mass += position
    #     N += 1
        
    # center_of_mass = (center_of_mass[0]/(N), center_of_mass[1]/(N))
    return center_of_mass
    
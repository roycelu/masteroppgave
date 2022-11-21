import time
from scipy.spatial import ConvexHull
import numpy as np
import shapely.geometry as shp


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
        poly = shp.Polygon([[p[0], p[1]] for p in new_positions])
        simple_poly = poly.simplify(0.0001)
        buf_poly = simple_poly.buffer(50, 4)
        buf_poly2 = simple_poly.buffer(30, 4)
        poly_array = np.array(buf_poly.exterior)
        poly_array2 = np.array(buf_poly2.exterior)
        
        size = 4
        for l in range(0, len(poly_array)-1):
            buffered_hull.append(poly_array[l][0])
            buffered_hull.append(poly_array[l][1])
            canvas.create_oval(poly_array[l][0]-size/2, poly_array[l][1]-size/2, poly_array[l][0]+size/2, poly_array[l][1]+size/2, fill='cyan', outline='black', tags=self.id)
        canvas.create_polygon(buffered_hull, fill='', outline='blue', tags=self.id)

        for l in range(0, len(poly_array2)-1):
            buffered_hull2.append(poly_array2[l][0])
            buffered_hull2.append(poly_array2[l][1])
            canvas.create_oval(poly_array2[l][0]-size/2, poly_array2[l][1]-size/2, poly_array2[l][0]+size/2, poly_array2[l][1]+size/2, fill='cyan', outline='black', tags=self.id)
        canvas.create_polygon(buffered_hull2, fill='', outline='blue', tags=self.id)

        return poly_array, buf_poly2

    def calculate_positions_toward_next_point(self, poly_array, list_of_sheep, canvas):
        # Calculates and returns the three positions for the drones on the extended hull
        mass_center = calculate_center_of_mass(list_of_sheep)
        vector = (self.point[0] - mass_center[0], self.point[1] - mass_center[1])
        opp_vector = (-vector[0], -vector[1])
        point_behind = np.add(mass_center, opp_vector)
        line1 = shp.LineString([mass_center, point_behind])
        size = 12
        i = 0
        point_of_intersection = (0, 0)
        point_orthogonal_1 = (0, 0)
        point_orthogonal_2 = (0, 0)

        # calculate perpendicular points
        v_1 = 100
        v_2 = -100
        v_3 = 0
        v_4 = 0
        if (vector[0] < 0 and vector[1] < 0) or (vector[0] > 0 and vector[1] > 0):
            v_3 = -(vector[0]/vector[1])*v_1
        if (vector[0] < 0 and vector[1] > 0) or (vector[0] < 0 and vector[1] > 0):
            v_3 = (vector[0]/vector[1])*v_1
        if (vector[0] < 0 and vector[1] < 0) or (vector[0] > 0 and vector[1] > 0):
            v_4 = -(vector[0]/vector[1])*v_2
        if (vector[0] < 0 and vector[1] > 0) or (vector[0] < 0 and vector[1] > 0):
            v_4 = (vector[0]/vector[1])*v_2
        orthogonal_1 = (v_1, v_3)
        orthogonal_2 = (v_2, v_4)
        line3 = shp.LineString([mass_center, (mass_center + orthogonal_1)])
        line4 = shp.LineString([mass_center, (mass_center + orthogonal_2)])

        for vertex in poly_array:
            if i == len(poly_array)-1:
                line2 = shp.LineString([vertex, poly_array[0]])
            else:
                line2 = shp.LineString([vertex, poly_array[i+1]])

            int_pt = line1.intersection(line2)
            int_pt_3 = line3.intersection(line2)
            int_pt_4 = line4.intersection(line2)

            if not int_pt.is_empty:
                point_of_intersection = int_pt.x, int_pt.y
            if not int_pt_3.is_empty:
                point_orthogonal_1 = int_pt_3.x, int_pt_3.y
            if not int_pt_4.is_empty:
                point_orthogonal_2 = int_pt_4.x, int_pt_4.y
                
            i += 1 

        a = (point_of_intersection[0]-mass_center[0], point_of_intersection[1]-mass_center[1])
        hyp_a1 = (a[0]*np.cos(np.pi/8)-a[1]*np.sin(np.pi/8), a[0]*np.sin(np.pi/8)+a[1]*np.cos(np.pi/8))
        point_a1 = (mass_center[0]+hyp_a1[0], mass_center[1]+hyp_a1[1])
        hyp_a2 = (a[0]*np.cos(-np.pi/8)-a[1]*np.sin(-np.pi/8), a[0]*np.sin(-np.pi/8)+a[1]*np.cos(-np.pi/8))
        point_a2 = (mass_center[0]+hyp_a2[0], mass_center[1]+hyp_a2[1])

        ort_a1 = (a[0]*np.cos(np.pi/2)-a[1]*np.sin(np.pi/2), a[0]*np.sin(np.pi/2)+a[1]*np.cos(np.pi/2))
        pointort_a1 = (mass_center[0]+ort_a1[0], mass_center[1]+ort_a1[1])
        ort_a2 = (a[0]*np.cos(-np.pi/2)-a[1]*np.sin(-np.pi/2), a[0]*np.sin(-np.pi/2)+a[1]*np.cos(-np.pi/2))
        pointort_a2 = (mass_center[0]+ort_a2[0], mass_center[1]+ort_a2[1])


      
        canvas.create_oval(point_a1[0]-size/2, point_a1[1]-size/2, point_a1[0]+size/2, point_a1[1]+size/2, fill='brown', outline='cyan', tags=self.id)
        canvas.create_oval(point_a2[0]-size/2, point_a2[1]-size/2, point_a2[0]+size/2, point_a2[1]+size/2, fill='pink', outline='cyan', tags=self.id)
        canvas.create_oval(pointort_a1[0]-size/2, pointort_a1[1]-size/2, pointort_a1[0]+size/2, pointort_a1[1]+size/2, fill='green', outline='pink', tags=self.id)
        canvas.create_oval(pointort_a2[0]-size/2, pointort_a2[1]-size/2, pointort_a2[0]+size/2, pointort_a2[1]+size/2, fill='green', outline='pink', tags=self.id)


        canvas.create_oval(point_orthogonal_1[0]-size/2, point_orthogonal_1[1]-size/2, point_orthogonal_1[0]+size/2, point_orthogonal_1[1]+size/2, fill='purple', outline='yellow', tags=self.id)
        canvas.create_oval(point_orthogonal_2[0]-size/2, point_orthogonal_2[1]-size/2, point_orthogonal_2[0]+size/2, point_orthogonal_2[1]+size/2, fill='purple', outline='green', tags=self.id)
        canvas.create_oval(point_of_intersection[0]-size/2, point_of_intersection[1]-size/2, point_of_intersection[0]+size/2, point_of_intersection[1]+size/2, fill='purple', outline='pink', tags=self.id)
        canvas.create_line(mass_center[0], mass_center[1], self.point[0], self.point[1], fill='yellow', tags=self.id)

        return pointort_a1, point_of_intersection, pointort_a2, point_a1, point_a2


    def fly_to_edge_convex_hull(self, extended_hull, list_of_drones):
        # For every drone, fly to the edge of the convex hull that is closest
        for drone in list_of_drones:
            drone.fly_to_edge_guidance_law(extended_hull)
            if list_of_drones[0].extended_hull_goal and list_of_drones[1].extended_hull_goal and list_of_drones[2].extended_hull_goal:
                self.extended_hull_goal = True

            
    def fly_on_edge_convex_hull(self, extended_hull, list_of_drones, left, back, right):
        if len(self.path) > 0:  # Sørger for at det eksisterer en path
            if self.point == (0,0):
                self.point = self.path[0]

            list_of_drones[0].hull_position_goal = False
            list_of_drones[1].hull_position_goal = False
            list_of_drones[2].hull_position_goal = False
        #Must calculate how far it is to move either clockwise or counterclockwise, choose shortest path 
            for drone in list_of_drones:
                if drone.id == 'drone0':
                    drone.fly_on_edge_guidance_law(extended_hull, left)
                if drone.id == 'drone1':
                    drone.fly_on_edge_guidance_law(extended_hull, back)
                if drone.id == 'drone2':
                    drone.fly_on_edge_guidance_law(extended_hull, right)
                #drone.fly_on_edge_guidance_law(extended_hull, desired_position)

                if list_of_drones[0].hull_position_goal and list_of_drones[1].hull_position_goal and list_of_drones[2].hull_position_goal:
                    self.hull_position_goal = True

    
    def fly_on_buffered_hull(self, list_of_drones, poly, left2, back2, right2, mass_center, back, left, right):
        if len(self.path) > 0:  # Sørger for at det eksisterer en path
            if self.point == (0,0):
                self.point = self.path[0]

            list = [back2, right2, back2, left2]
            for element in list:
                drone = list_of_drones[1]
        
                distance = np.linalg.norm(list_of_drones[0].position - list_of_drones[2].position)
                if distance > 40:
                    list_of_drones[0].fly_on_edge_guidance_law(np.array(poly.exterior), left2)
                    list_of_drones[2].fly_on_edge_guidance_law(np.array(poly.exterior), right2)
                else:
                    list_of_drones[0].fly_on_edge_guidance_law(np.array(poly.exterior), left)
                    list_of_drones[2].fly_on_edge_guidance_law(np.array(poly.exterior), right)

                if drone.id == 'drone1':
                    point = shp.Point(drone.position)
                    if poly.contains(point):
                        drone.fly_on_edge_guidance_law(np.array(poly.exterior), back)
                        print(drone.id, "inside of buffered hull")
                    else:
                        drone.fly_on_edge_guidance_law(np.array(poly.exterior), element)
                        print(drone.id, "outside of buffered hull")
                   
                
                if (mass_center[0] -5 <= self.point[0] <= mass_center[0] + 5) and (mass_center[1] - 5 <= self.point[1] <= mass_center[1] + 5):
                    if self.point == self.path[-1]:
                        print("Fly to point", self.path_goal)
                        self.path_goal = True
                    else:    
                        self.point = self.path[self.path.index(self.point)+1]
    
        
    def main(self, list_of_sheep, canvas, list_of_drones):
        canvas.delete(self.id)
        self.draw_sheep_mass_centre(canvas, list_of_sheep)
        mass_center = calculate_center_of_mass(list_of_sheep)
        poly_array, poly = self.draw_convex_and_extended_hull(canvas, list_of_sheep)
        # if droner posisjoner korrekt rundt sauer mtp retning de skal bevege seg i mot pathen
        # Fly to the extended hull if this has not been reached
        if self.extended_hull_goal == False:

            self.fly_to_edge_convex_hull(poly_array, list_of_drones)
            
        
        # If the drones are at the extended hull, fly along it to position themselves towards the first point on the path
        if self.extended_hull_goal:
            left, back, right, left_middle, right_middle = self.calculate_positions_toward_next_point(poly_array, list_of_sheep, canvas)
            self.fly_on_edge_convex_hull(poly_array, list_of_drones, left, back, right)
            if self.hull_position_goal:
                left2, back2, right2, left_middle, right_middle = self.calculate_positions_toward_next_point(np.array(poly.exterior), list_of_sheep, canvas)
                self.fly_on_buffered_hull(list_of_drones, poly, left_middle, back2, right_middle, mass_center, back, left2, right2)
                
        # Fly to the path and along the path 
        # PS:må endre position per nye punkt den har kommet til, altså se på neste punk og rotere basert på det, 
        # evt at dte blir mer krumninger. Dronene må hvertfall alltid være bak sauene.
        #if self.extended_hull_goal:
        #    self.calculate_center_back(poly_array, list_of_sheep, canvas)
        #    self.fly_along_path(list_of_drones)

        # else
        #
    


def calculate_center_of_mass(list_of_sheep):
    N = 0 # Number of sheep
    center_of_mass = 0
    
    for sheep in list_of_sheep:
        center_of_mass += sheep.position
        N += 1
        
    center_of_mass = center_of_mass / (N)
    return center_of_mass
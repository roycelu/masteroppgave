from scipy.spatial import ConvexHull
import numpy as np
from drones_path import DronesPath

class MainDrone:
    def __init__(self, id, drone_path):
        self.id = id
        self.path = drone_path

    
    def draw_main_drone(self, canvas, list_of_sheep):
        size = 3
        c = calculate_center_of_mass(list_of_sheep)
        # Draw the circle around the position (centre)
        x0 = c[0] - size/2
        y0 = c[1] - size/2
        x1 = c[0] + size/2
        y1 = c[1] + size/2
        canvas.create_oval(x0, y0, x1, y1, fill='red', tags=self.id)
    
    def draw_sheep_border(self, canvas, list_of_sheep, list_of_drones):
        points = []
        positions = []
        centre = calculate_center_of_mass(list_of_sheep)
        for sheep in list_of_sheep:
            positions.append(sheep.position)
        hull = ConvexHull(positions)
        neighbours = hull.neighbors # [ [1,3], [x,y] ]
       
        for index in hull.vertices:
            points.append(list_of_sheep[index].position[0])
            points.append(list_of_sheep[index].position[1])
            """P_iP_i_n = (list_of_sheep[index].position[0]-list_of_sheep[neighbours[i][0]].position[0], list_of_sheep[index].position[1]-list_of_sheep[neighbours[i][0]].position[1])
            P_iP_i_p = (list_of_sheep[index].position[0]-list_of_sheep[neighbours[i][1]].position[0], list_of_sheep[index].position[1]-list_of_sheep[neighbours[i][1]].position[1])
            P_i_nP_i = (list_of_sheep[neighbours[i][0]].position[0]-list_of_sheep[index].position[0], list_of_sheep[neighbours[i][0]].position[1]-list_of_sheep[index].position[1])
            P_i_pP_i = (list_of_sheep[neighbours[i][1]].position[0]-list_of_sheep[index].position[0], list_of_sheep[neighbours[i][1]].position[1]-list_of_sheep[index].position[1])
            
            print(P_iP_i_n, P_iP_i_p, P_i_nP_i, P_i_pP_i)"""
        
        #print(points)
        # print("------")
        
        #print('points', points)
        canvas.create_polygon(points, fill='', outline='green', tags=self.id)
        self.draw_extended_hull(canvas, list_of_drones, list_of_sheep, hull)
        
       

    def draw_extended_hull(self, canvas, list_of_drones, list_of_sheep, hull):

        extended_distance = 10
        extended_hull = []
        extended_hull_separate = []
        i = 0

        # print("Sheeppos",list_of_sheep.position)
        #print("Index", positions)
        """

        """
        
        for index in hull.vertices:
            P_ix = list_of_sheep[index].position[0]
            P_iy = list_of_sheep[index].position[1]
            #print(P_ix, P_iy)
            #print(index)
            #print(positions)
            """
            if i == 0:
                P_iP_i_n = (positions[-1][0]-index[0], positions[-1][1]-index[1])
                P_iP_i_p = (positions[i+1][0]-index[0], positions[i+1][1]-index[1])
                P_i_nP_i = (index[0]-positions[-1][0], index[1]-positions[-1][1])
                P_i_pP_i = (index[0]-positions[i+1][0], index[1]-positions[i+1][1])
            elif i == len(positions)-1:
                P_iP_i_n = (positions[i-1][0]-index[0], positions[i-1][1]-index[1])
                P_iP_i_p = (positions[0][0]-index[0], positions[0][1]-index[1])
                P_i_nP_i = (index[0]-positions[i-1][0], index[0]-positions[i-1][1])
                P_i_pP_i = (index[0]-positions[0][0], index[0]-positions[0][1])
            else:
                P_iP_i_n = (positions[i-1][0]-index[0], positions[i-1][1]-index[1])
                P_iP_i_p = (positions[i+1][0]-index[0], positions[i+1][1]-index[1])
                P_i_nP_i = (index[0]-positions[i-1][0], index[0]-positions[i-1][1])
                P_i_pP_i = (index[0]-positions[i+1][0], index[0]-positions[i+1][1])
            """
            if i == 0:
                P_iP_i_n = (list_of_sheep[hull.vertices[-1]].position[0]-P_ix , list_of_sheep[hull.vertices[-1]].position[1]-P_iy)
                P_iP_i_p = (list_of_sheep[hull.vertices[i+1]].position[0]-P_ix, list_of_sheep[hull.vertices[i+1]].position[1]-P_iy)
                P_i_nP_i = (P_ix-list_of_sheep[hull.vertices[-1]].position[0], P_iy-list_of_sheep[hull.vertices[-1]].position[1])
                P_i_pP_i = (P_ix-list_of_sheep[hull.vertices[i+1]].position[0], P_iy-list_of_sheep[hull.vertices[i+1]].position[1])

                #print("P_i", P_ix, P_iy)
                #print("P_i+1", list_of_sheep[hull.vertices[i+1]].position[0], list_of_sheep[hull.vertices[i+1]].position[1])
                #print("P_i-1", list_of_sheep[hull.vertices[-1]].position[0], list_of_sheep[hull.vertices[-1]].position[1])
                
            
            elif i == len(hull.vertices)-1:
                P_iP_i_n = (list_of_sheep[hull.vertices[i-1]].position[0]-P_ix, P_iy-list_of_sheep[hull.vertices[i-1]].position[1])
                P_iP_i_p = (list_of_sheep[hull.vertices[0]].position[0]-P_ix, P_iy-list_of_sheep[hull.vertices[0]].position[1])
                P_i_nP_i = (P_ix-list_of_sheep[hull.vertices[i-1]].position[0], P_iy-list_of_sheep[hull.vertices[i-1]].position[1])
                P_i_pP_i = (P_ix-list_of_sheep[hull.vertices[0]].position[0], P_iy-list_of_sheep[hull.vertices[0]].position[1])

                #print("P_i", P_ix, P_iy)
                #print("P_i+1", list_of_sheep[hull.vertices[0]].position[0], list_of_sheep[hull.vertices[0]].position[1])
                #print("P_i-1", list_of_sheep[hull.vertices[i-1]].position[0], list_of_sheep[hull.vertices[i-1]].position[1])
            
            else:
                P_iP_i_n = (list_of_sheep[hull.vertices[i-1]].position[0]-P_ix, list_of_sheep[hull.vertices[i-1]].position[1]-P_iy)
                P_iP_i_p = (list_of_sheep[hull.vertices[i+1]].position[0]-P_ix, list_of_sheep[hull.vertices[i+1]].position[1]-P_iy)
                P_i_nP_i = (P_ix-list_of_sheep[hull.vertices[i-1]].position[0], P_iy-list_of_sheep[hull.vertices[i-1]].position[1])
                P_i_pP_i = (P_ix-list_of_sheep[hull.vertices[i+1]].position[0], P_iy-list_of_sheep[hull.vertices[i+1]].position[1])

            
            cos_alpha = (np.dot(P_iP_i_n, P_iP_i_p)) / (np.linalg.norm(P_iP_i_n)*np.linalg.norm(P_iP_i_p))
            # print('cos_alpha', cos_alpha)
            # print('linalg', np.linalg.norm(cos_alpha))
            # print('pinpi', P_i_nP_i)
            # print('linalg pinpi', np.linalg.norm(P_i_nP_i))
            # print('pippi', P_i_pP_i)
            # print('linalg pippi', np.linalg.norm(P_i_pP_i))

            P_iL_1 = (extended_distance/np.linalg.norm(cos_alpha)) * (P_i_nP_i/np.linalg.norm(P_i_nP_i))
            P_iL_2 = (extended_distance/np.linalg.norm(cos_alpha)) * (P_i_pP_i/np.linalg.norm(P_i_pP_i))
            # print('list of sheep index', list_of_sheep[index].position)
            # print('pil1', P_iL_1)
            # print('pil2', P_iL_2)
            # E_i = index + P_iL_1 + P_iL_2
            E_i = (P_ix, P_iy) + P_iL_1 + P_iL_2
            # print('e_i', E_i)
            # #print("EEE", E_i, P_iL_1, P_iL_2)
            extended_hull.append(E_i)
            
            i += 1
            
        
        """ext_hull = ConvexHull(extended_hull)
        for point in ext_hull.vertices:
            extended_hull_separate.append(extended_hull[point][0])
            extended_hull_separate.append(extended_hull[point][1])
            #ext_hull = ConvexHull(extended_hull)

        """
        for point in extended_hull:
            extended_hull_separate.append(point[0])
            extended_hull_separate.append(point[1])
            
        
        # print("--------")
        canvas.create_polygon(extended_hull_separate, fill='', outline='purple', tags=self.id)
        self.fly_to_edge_convex_hull(extended_hull, list_of_drones)
        

    
    def fly_to_edge_convex_hull(self, extended_hull, list_of_drones):
        # print(extended_hull)
        step_size = 5
        for drone in list_of_drones:
            pos = np.zeros(2, dtype=np.int32)
            if drone.id == 'drone0':
                pos = extended_hull[0]
            elif drone.id == 'drone1':
                pos = extended_hull[1]
            elif drone.id == 'drone2':
                pos = extended_hull[2]
            drone.fly_to_position(pos, step_size)
        # Må tenke på plasseringen til dronene i forhold til hverandre, de burde få tilsendt
        # forskjellige posisjoner som de skal dra til, dett vil ta kortest til, kan disse 
        # koordinatene være 45 grader i forhold til hverandre? også blir det sånn at dersom en drone
        # når convex hullet stopper den? Da burde man kanskje vite avstand mellom dronene, så dronene
        # må kunne gi beskjed til hoveddronen om hvor de befinner seg, da kan hoveddronen evt.
        # gi dem litt modifiserte nye koordinater å bevege seg til. 
        # Må kanskje begynne å tenke på hastighet de skal bevege seg i og etterhvert
        return "hei"

    def fly_on_edge_convex_hull(list_of_drones):
        #Must calculate how far it is to move either clockwise or counterclockwise, choose shortest path 
        return "navigate clockwise/counterclockwise based on what is quicker"

    def fly_along_path(self, list_of_drones):
        print('nei')
        index = 0
        print(self.path)
        for point in self.path:
            print('yo', point)
            for drone in list_of_drones:
                print('drone', drone.position)
                position, goal = drone.fly_to_position(point, 5)
                if goal:
                    drone.fly_to_position(self.path[index+1], 5)
            index += 1
        
    def main(self, list_of_sheep, canvas, list_of_drones):
        canvas.delete(self.id)
        self.draw_main_drone(canvas, list_of_sheep)
        #self.draw_sheep_border(canvas, list_of_sheep, list_of_drones)
        self.fly_along_path(list_of_drones)


def calculate_center_of_mass(list_of_sheep):
    N = 0 # Number of sheep
    center_of_mass = 0
    
    for sheep in list_of_sheep:
        center_of_mass += sheep.position
        N += 1
        
    center_of_mass = center_of_mass / (N)
    return center_of_mass
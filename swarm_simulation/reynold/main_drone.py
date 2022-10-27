from scipy.spatial import ConvexHull
import numpy as np

class MainDrone:
    def __init__(self, id):
        self.id = id

    
    def draw_main_drone(self, canvas, list_of_sheep):
        size = 3
        c = calculate_center_of_mass(list_of_sheep)
        # Draw the circle around the position (centre)
        x0 = c[0] - size/2
        y0 = c[1] - size/2
        x1 = c[0] + size/2
        y1 = c[1] + size/2
        canvas.create_oval(x0, y0, x1, y1, fill='red', tags=self.id)
    
    def draw_sheep_border(self, canvas, list_of_sheep):
        points = []
        positions = []
        extended_distance = 30
        extended_hull = []
        hjelp = []
        centre = calculate_center_of_mass(list_of_sheep)
        for sheep in list_of_sheep:
            positions.append(sheep.position)
        hull = ConvexHull(positions)
        neighbours = hull.neighbors # [ [1,3], [x,y] ]
        i = 0
        for index in hull.vertices:
            #hull.vertices[i]
            points.append(list_of_sheep[index].position[0])
            points.append(list_of_sheep[index].position[1])
            #husk å sjekke for første og siste element i lista
            #if index == 0:
            """P_iP_i_n = (list_of_sheep[index].position[0]-list_of_sheep[neighbours[i][0]].position[0], list_of_sheep[index].position[1]-list_of_sheep[neighbours[i][0]].position[1])
            P_iP_i_p = (list_of_sheep[index].position[0]-list_of_sheep[neighbours[i][1]].position[0], list_of_sheep[index].position[1]-list_of_sheep[neighbours[i][1]].position[1])
            P_i_nP_i = (list_of_sheep[neighbours[i][0]].position[0]-list_of_sheep[index].position[0], list_of_sheep[neighbours[i][0]].position[1]-list_of_sheep[index].position[1])
            P_i_pP_i = (list_of_sheep[neighbours[i][1]].position[0]-list_of_sheep[index].position[0], list_of_sheep[neighbours[i][1]].position[1]-list_of_sheep[index].position[1])
            
            print(P_iP_i_n, P_iP_i_p, P_i_nP_i, P_i_pP_i)"""
            # elif index == len(hull.vertices-1):
            #     P_iP_i_n = (list_of_sheep[index].position[0]-list_of_sheep[index-1].position[0], list_of_sheep[index].position[1]-list_of_sheep[index-1].position[1])
            #     P_iP_i_p = (list_of_sheep[index].position[0]-list_of_sheep[0].position[0], list_of_sheep[index].position[1]-list_of_sheep[0].position[1])
            #     P_i_nP_i = (list_of_sheep[index-1].position[0]-list_of_sheep[index].position[0], list_of_sheep[index-1].position[1]-list_of_sheep[index].position[1])
            #     P_i_pP_i = (list_of_sheep[0].position[0]-list_of_sheep[index].position[0], list_of_sheep[0].position[1]-list_of_sheep[index].position[1])
            
            # else:
            #     P_iP_i_n = (list_of_sheep[index].position[0]-list_of_sheep[index-1].position[0], list_of_sheep[index].position[1]-list_of_sheep[index-1].position[1])
            #     P_iP_i_p = (list_of_sheep[index].position[0]-list_of_sheep[index+1].position[0], list_of_sheep[index].position[1]-list_of_sheep[index+1].position[1])
            #     P_i_nP_i = (list_of_sheep[index-1].position[0]-list_of_sheep[index].position[0], list_of_sheep[index-1].position[1]-list_of_sheep[index].position[1])
            #     P_i_pP_i = (list_of_sheep[index+1].position[0]-list_of_sheep[index].position[0], list_of_sheep[index+1].position[1]-list_of_sheep[index].position[1])
            
            if index == 0:
                P_iP_i_n = (list_of_sheep[index].position[0]-list_of_sheep[hull.vertices[-1]].position[0], list_of_sheep[index].position[1]-list_of_sheep[hull.vertices[-1]].position[1])
                P_iP_i_p = (list_of_sheep[index].position[0]-list_of_sheep[hull.vertices[i+1]].position[0], list_of_sheep[index].position[1]-list_of_sheep[hull.vertices[i+1]].position[1])
                P_i_nP_i = (list_of_sheep[hull.vertices[-1]].position[0]-list_of_sheep[index].position[0], list_of_sheep[hull.vertices[-1]].position[1]-list_of_sheep[index].position[1])
                P_i_pP_i = (list_of_sheep[hull.vertices[i+1]].position[0]-list_of_sheep[index].position[0], list_of_sheep[hull.vertices[i+1]].position[1]-list_of_sheep[index].position[1])
            
            elif index == len(hull.vertices-1):
                P_iP_i_n = (list_of_sheep[index].position[0]-list_of_sheep[hull.vertices[i-1]].position[0], list_of_sheep[index].position[1]-list_of_sheep[hull.vertices[i-1]].position[1])
                P_iP_i_p = (list_of_sheep[index].position[0]-list_of_sheep[hull.vertices[0]].position[0], list_of_sheep[index].position[1]-list_of_sheep[hull.vertices[0]].position[1])
                P_i_nP_i = (list_of_sheep[hull.vertices[i-1]].position[0]-list_of_sheep[index].position[0], list_of_sheep[hull.vertices[i-1]].position[1]-list_of_sheep[index].position[1])
                P_i_pP_i = (list_of_sheep[hull.vertices[0]].position[0]-list_of_sheep[index].position[0], list_of_sheep[hull.vertices[0]].position[1]-list_of_sheep[index].position[1])
            
            else:
                P_iP_i_n = (list_of_sheep[index].position[0]-list_of_sheep[hull.vertices[i-1]].position[0], list_of_sheep[index].position[1]-list_of_sheep[hull.vertices[i-1]].position[1])
                P_iP_i_p = (list_of_sheep[index].position[0]-list_of_sheep[hull.vertices[i+1]].position[0], list_of_sheep[index].position[1]-list_of_sheep[hull.vertices[i+1]].position[1])
                P_i_nP_i = (list_of_sheep[hull.vertices[i-1]].position[0]-list_of_sheep[index].position[0], list_of_sheep[hull.vertices[i-1]].position[1]-list_of_sheep[index].position[1])
                P_i_pP_i = (list_of_sheep[hull.vertices[i+1]].position[0]-list_of_sheep[index].position[0], list_of_sheep[hull.vertices[i+1]].position[1]-list_of_sheep[index].position[1])
            
            
            cos_alpha = (np.dot(P_iP_i_n, P_iP_i_p) / (np.linalg.norm(P_iP_i_n)*np.linalg.norm(P_iP_i_p)))

            P_iL_1 = (extended_distance/np.linalg.norm(cos_alpha)) * (P_i_nP_i/np.linalg.norm(P_i_nP_i))
            P_iL_2 = (extended_distance/np.linalg.norm(cos_alpha)) * (P_i_pP_i/np.linalg.norm(P_i_pP_i))
            
            E_i = list_of_sheep[index].position + P_iL_1 + P_iL_2
            print("EEE", E_i, P_iL_1, P_iL_2)
            extended_hull.append(E_i)
            
            i += 1
        
        #print(points)
        print("------")
        ext_hull = ConvexHull(extended_hull)
        for index in ext_hull.vertices:
            hjelp.append(extended_hull[index][0])
            hjelp.append(extended_hull[index][1])
            
       
        canvas.create_polygon(points, fill='', outline='green', tags=self.id)
        canvas.create_polygon(hjelp, fill='', outline='purple', tags=self.id)

    def fly_to_edge_convex_hull(list_of_drones):
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
        
    def main(self, list_of_sheep, canvas):
        canvas.delete(self.id)
        self.draw_main_drone(canvas, list_of_sheep)
        self.draw_sheep_border(canvas, list_of_sheep)


def calculate_center_of_mass(list_of_sheep):
    N = 0 # Number of sheep
    center_of_mass = 0
    
    for sheep in list_of_sheep:
        center_of_mass += sheep.position
        N += 1
        
    center_of_mass = center_of_mass / (N)
    return center_of_mass
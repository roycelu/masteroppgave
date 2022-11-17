def draw_extended_hull(self, canvas, list_of_sheep, list_of_drones, hull):

        extended_distance = 40
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

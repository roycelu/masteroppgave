import os
import pygame
import pandas as pd
import numpy as np
from datetime import datetime
from constants import *
from main.main import Main


# NO_SHEEP = 5
# NO_DRONES = 3
# NO_SIMULATIONS = 100 # Number of simulations
# TIME_LIMIT = 70 # How long the simulation will run
# TARGET_FPS = 10 # Speed of the simulation
# FPS = 30
# TESTTYPES = ["cooperative_flock", "divided_flock", "lone_sheep", "right_angle"]
# OUR_DRONETYPES = ['com', 'v_polygon']
# ANGLES = [10, 15, 20, 25, 30]
# CAPTURE_TIMES = [x for x in range(0, TIME_LIMIT, 2)]

pd.set_option('display.precision', 2)  


def test(id, no_sheep, no_drones, FPS, collect_type, testtype, angle, dir_path):
    # Run the simulations
    sheep_positions = get_sheep_list(testtype, no_sheep)
    sim = Main(id, sheep_positions, no_drones, FPS, collect_type, testtype, angle, dir_path)
    successrate, herdtime, collect_time, herd_time = sim.main(TIME_LIMIT, TARGET_FPS, CAPTURE_TIMES)
    return round(successrate,2), round(herdtime,2), round(collect_time,2), round(herd_time,2)
    
def get_sheep_list(testtype, no_sheep):
    # Based on the testtype, the sheep are positioned different places
    position_list = [x for x in range(no_sheep)]
    
    if testtype == "cooperative_flock":
        for i in position_list:
            x = np.random.randint(400, 420)
            y = np.random.randint(200, 220)
            position_list[i] = pygame.Vector2(x, y) 
    
    if testtype == "lone_sheep":
        for i in range(len(position_list)):
            if i == len(position_list)-1:
                x = np.random.randint(200, 220)
                y = np.random.randint(400, 420)
            else:
                x = np.random.randint(400, 420)
                y = np.random.randint(200, 220)
            position_list[i] = pygame.Vector2(x, y)
    
    if testtype == "divided_flock":
        middle_index = len(position_list)//2
        for i in position_list[:middle_index]:
            x = np.random.randint(400, 420)
            y = np.random.randint(200, 220)
            position_list[i] = pygame.Vector2(x, y) 
        for i in position_list[middle_index:]:
            x = np.random.randint(200, 220)
            y = np.random.randint(400, 420)
            position_list[i] = pygame.Vector2(x, y)

    if testtype == "right_angle":
        for i in position_list:
            x = np.random.randint(400, 420)
            y = np.random.randint(200, 220)
            position_list[i] = pygame.Vector2(x, y) 

    return position_list


def main():    
    # Make a new directory to save the results
    dir_path = './our_sim_results/{}'.format(str(datetime.now()))
    if not os.path.exists(dir_path):
        os.mkdir(dir_path)

    # Run all the different variations of the simulations
    df_vpolygon = pd.DataFrame(columns = ['Testtype', 'Samletype', 'Vinkel', 'Gjetetid', 'Suksessrate', 'Oppsamlingstid', 'Drivetid'])
    df_com = pd.DataFrame(columns = ['Testtype', 'Samletype', 'Vinkel', 'Gjetetid', 'Suksessrate', 'Oppsamlingstid', 'Drivetid'])
        
    for test_type in TESTTYPES:
        for collect_type in OUR_DRONETYPES:
                for angle in ANGLES:
                    for id in range(NO_SIMULATIONS):
                        print(collect_type, angle, id)
                        successrate, herdtime, collect_time, actual_herd_time = test(id, NO_SHEEP, NO_DRONES, FPS*NO_DRONES, collect_type, test_type, angle, dir_path)
                        if collect_type == 'com':
                            df_com = df_com.append({'Testtype': test_type, 'Samletype': collect_type, 'Vinkel': angle, 'Gjetetid':herdtime, 'Suksessrate':successrate, 'Oppsamlingstid':collect_time, 'Drivetid':actual_herd_time}, ignore_index = True)
                        if collect_type == 'v_polygon':
                            df_vpolygon = df_vpolygon.append({'Testtype': test_type, 'Samletype': collect_type, 'Vinkel': angle, 'Gjetetid':herdtime, 'Suksessrate':successrate, 'Oppsamlingstid':collect_time, 'Drivetid':actual_herd_time}, ignore_index = True)

        
    df_vpolygon_original = df_vpolygon.copy()
    df_com_original = df_com.copy()

    # Make tables for all the data
    df_vpolygon_original = df_vpolygon_original.drop(columns=['Samletype'])
    df_vpolygon_original.to_csv('{path}/v_polygon.csv'.format(path=dir_path), index=False)

    df_com_original = df_com_original.drop(columns=['Samletype'])
    df_com_original.to_csv('{path}/com.csv'.format(path=dir_path), index=False)

if __name__ == "__main__":
    main()
    
import pygame
import pandas as pd
import numpy as np
import os
from datetime import datetime
from constants import *
from main.shared_main import SharedMain


# NO_SHEEP = 5
# NO_DRONES = 3
# NO_SIMULATIONS = 100 # Antall simuleringer per testtype per drone
# TIME_LIMIT = 70 # 50 sekunder for sauene å bevege seg maks 1000m
# TARGET_FPS = 10 # Hastigheten på simuleringen
# FPS = 30
# TESTTYPES = ["cooperative_flock", "divided_flock", "lone_sheep", "right_angle"]
# DRONETYPES = ['our', 'polygon', 'circle', 'v']
# PERCEPTIONS = [20, 30, 40]
# CAPTURE_TIMES = [x for x in range(0, TIME_LIMIT, 2)]
THETA = 15 # Vinkel i grader mellom dronene for our_drone

pd.set_option('display.precision', 2)   # Verdiene i tabellene runder av til to desimaler


def test(id, no_sheep, no_drones, FPS, dronetype, testtype, perception, dir_path):
    # Run the simulations
    sheep_positions = get_sheep_list(testtype, no_sheep)
    sim = SharedMain(id, sheep_positions, no_drones, FPS, dronetype, testtype, perception, dir_path, THETA)
    successrate, herdtime, reached_goal_times, reached_goal_number, collect_time, actual_herdtime = sim.main(TIME_LIMIT, TARGET_FPS, CAPTURE_TIMES)
    return round(successrate,2), round(herdtime,2), reached_goal_times, reached_goal_number, round(collect_time,2), round(actual_herdtime,2)
    
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
    dir_path = './sim_results/{}'.format(str(datetime.now()))
    if not os.path.exists(dir_path):
        os.mkdir(dir_path)

    # Run all the different variations of the simulations
    for perception in PERCEPTIONS:
        df_circle = pd.DataFrame(columns = ['Testtype', 'Dronetype', 'Gjetetid', 'Suksessrate'])
        df_v = pd.DataFrame(columns = ['Testtype', 'Dronetype', 'Gjetetid', 'Suksessrate'])
        df_polygon = pd.DataFrame(columns = ['Testtype', 'Dronetype', 'Gjetetid', 'Suksessrate'])
        df_our = pd.DataFrame(columns = ['Testtype', 'Dronetype', 'Gjetetid', 'Suksessrate'])

        for dronetype in DRONETYPES:
            for testtype in TESTTYPES:
                for id in range(NO_SIMULATIONS):
                    print(perception, dronetype, testtype, id)
                    successrate, herdtime, reached_goal_times, reached_goal_number, collect_time, actual_herd_time = test(id, NO_SHEEP, NO_DRONES, FPS*NO_DRONES, dronetype, testtype, perception, dir_path)
                    if dronetype == 'circle':
                        df_circle = df_circle.append({'Testtype': testtype, 'Dronetype': dronetype, 'Gjetetid':herdtime, 'Suksessrate':successrate, 'Oppsamlingstid':collect_time, 'Drivetid':actual_herd_time}, ignore_index = True)
                    if dronetype == 'v':
                        df_v = df_v.append({'Testtype': testtype, 'Dronetype': dronetype, 'Gjetetid':herdtime, 'Suksessrate':successrate, 'Oppsamlingstid':collect_time, 'Drivetid':actual_herd_time}, ignore_index = True)
                    if dronetype == 'polygon':
                        df_polygon = df_polygon.append({'Testtype': testtype, 'Dronetype': dronetype, 'Gjetetid':herdtime, 'Suksessrate':successrate, 'Oppsamlingstid':collect_time, 'Drivetid':actual_herd_time}, ignore_index = True)
                    if dronetype == 'our':
                        df_our = df_our.append({'Testtype': testtype, 'Dronetype': dronetype, 'Gjetetid':herdtime, 'Suksessrate':successrate, 'Oppsamlingstid':collect_time, 'Drivetid':actual_herd_time}, ignore_index = True)
                    
        df_circle_original = df_circle.copy()
        df_v_original = df_v.copy()
        df_polygon_original = df_polygon.copy()
        df_our_original = df_our.copy()

        # Make tables for all the data
        df_circle_original = df_circle_original.drop(columns=['Dronetype'])
        df_circle_original.to_csv('{path}/circle_{p}.csv'.format(path=dir_path, p=perception), index=False)

        df_v_original = df_v_original.drop(columns=['Dronetype'])
        df_v_original.to_csv('{path}/v_{p}.csv'.format(path=dir_path, p=perception), index=False)

        df_polygon_original = df_polygon_original.drop(columns=['Dronetype'])
        df_polygon_original.to_csv('{path}/polygon_{p}.csv'.format(path=dir_path, p=perception), index=False)

        df_our_original = df_our_original.drop(columns=['Dronetype'])
        df_our_original.to_csv('{path}/our_{p}.csv'.format(path=dir_path, p=perception), index=False)


if __name__ == "__main__":
    main()
    
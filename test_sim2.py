import pygame
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
from datetime import datetime
from shared_main import SharedMain


NO_SHEEP = 5
NO_DRONES = 3
NO_SIMULATIONS = 100 # Antall simuleringer per testtype per drone
TIME_LIMIT = 50000 # 50 sekunder for sauene å bevege seg maks 1000m
TARGET_FPS = 10 # Hastigheten på simuleringen
FPS = 30
TESTTYPES = ["cooperative_flock", "lone_sheep", "divided_flock", "right_angle"]
DRONETYPES = ['our', 'polygon', 'circle', 'v']
PERCEPTIONS = [30, 20, 40]
CAPTURE_TIMES = [x for x in range(50, 5000, 200)]
THETA = 10 # Vinkel i grader mellom dronene for our_drone

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
    dir_path = './results2/{}'.format(str(datetime.now()))
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

        """Bar chart for average herd time from successful herding for all algorithms per test"""
        
        # Circle
        df_circle_success = df_circle.loc[df_circle['Suksessrate'] == 100]
        df_avg_time_circle = df_circle_success.groupby(['Testtype', 'Dronetype'], as_index=False).aggregate({'Gjetetid':'mean', 'Oppsamlingstid':'mean', 'Drivetid':'mean'}).round(2) # Runder av til to desimaler
        df_avg_time_circle_index = df_avg_time_circle.copy()
        df_avg_time_circle_index.set_index('Testtype', inplace=True, drop=True)
        circle_time = []
        circle_collect_time = []
        circle_herd_time = []
        for testt in TESTTYPES:
            if (df_avg_time_circle['Testtype'] == testt).any():
                circle_row = df_avg_time_circle.loc[(df_avg_time_circle['Testtype'] == testt)]
                circle_time.append(circle_row['Gjetetid'].iloc[0])
                circle_collect_time.append(circle_row['Oppsamlingstid'].iloc[0])
                circle_herd_time.append(circle_row['Drivetid'].iloc[0])
            else:
                circle_time.append(0)
                circle_collect_time.append(0)
                circle_herd_time.append(0)
        
        # V
        df_v_success = df_v.loc[df_v['Suksessrate'] == 100]
        df_avg_time_v = df_v_success.groupby(['Testtype', 'Dronetype'], as_index=False).aggregate({'Gjetetid':'mean', 'Oppsamlingstid':'mean', 'Drivetid':'mean'}).round(2) # Runder av til to desimaler
        df_avg_time_v_index = df_avg_time_v.copy()
        df_avg_time_v_index.set_index('Testtype', inplace=True, drop=True)
        v_time = []
        v_collect_time = []
        v_herd_time = []
        # TODO Jeg er ikke sikker på om denne måten å gjøre det på faktisk blir riktig :/
        for testt in TESTTYPES:
            if (df_avg_time_v['Testtype'] == testt).any():
                v_row = df_avg_time_v.loc[(df_avg_time_v['Testtype'] == testt)]
                v_time.append(v_row['Gjetetid'].iloc[0])
                v_collect_time.append(v_row['Oppsamlingstid'].iloc[0])
                v_herd_time.append(v_row['Drivetid'].iloc[0])
            else:
                v_time.append(0)
                v_collect_time.append(0)
                v_herd_time.append(0)


        # Polygon
        df_polygon_success = df_polygon.loc[df_polygon['Suksessrate'] == 100]
        df_avg_time_polygon = df_polygon_success.groupby(['Testtype', 'Dronetype'], as_index=False).aggregate({'Gjetetid':'mean', 'Oppsamlingstid':'mean', 'Drivetid':'mean'}).round(2) # Runder av til to desimaler
        df_avg_time_polygon_index = df_avg_time_polygon.copy()
        df_avg_time_polygon_index.set_index('Testtype', inplace=True, drop=True)
        polygon_time = []
        polygon_collect_time = []
        polygon_herd_time = []
        for testt in TESTTYPES:
            if (df_avg_time_polygon['Testtype'] == testt).any():
                polygon_row = df_avg_time_polygon.loc[(df_avg_time_polygon['Testtype'] == testt)]
                polygon_time.append(polygon_row['Gjetetid'].iloc[0])
                polygon_collect_time.append(polygon_row['Oppsamlingstid'].iloc[0])
                polygon_herd_time.append(polygon_row['Drivetid'].iloc[0])
            else:
                polygon_time.append(0)
                polygon_collect_time.append(0)
                polygon_herd_time.append(0)

        # Our
        df_our_success = df_our.loc[df_our['Suksessrate'] == 100]
        df_avg_time_our = df_our_success.groupby(['Testtype', 'Dronetype'], as_index=False).aggregate({'Gjetetid':'mean', 'Oppsamlingstid':'mean', 'Drivetid':'mean'}).round(2) # Runder av til to desimaler
        df_avg_time_our_index = df_avg_time_our.copy()
        df_avg_time_our_index.set_index('Testtype', inplace=True, drop=True)
        our_time = []
        our_collect_time = []
        our_herd_time = []
        # TODO Jeg er ikke sikker på om denne måten å gjøre det på faktisk blir riktig :/
        for testt in TESTTYPES:
            if (df_avg_time_our['Testtype'] == testt).any():
                our_row = df_avg_time_our.loc[(df_avg_time_our['Testtype'] == testt)]
                our_time.append(our_row['Gjetetid'].iloc[0])
                our_collect_time.append(our_row['Oppsamlingstid'].iloc[0])
                our_herd_time.append(our_row['Drivetid'].iloc[0])
            else:
                our_time.append(0)
                our_collect_time.append(0)
                our_herd_time.append(0)
        
        # Make figure
        N = 4
        ind = np.arange(N) # the x locations for the groups
        width = 0.20

        # GJENNOMSNITTLIG GJETETID FOR SIMULERINGENE
        fig_time, ax_time = plt.subplots()

        circle_collect = ax_time.bar(ind-0.3, circle_collect_time, width, label='Sirkel: samletid = {}'.format(circle_collect_time), color='moccasin')
        circle_herd = ax_time.bar(ind-0.3, circle_herd_time, width, bottom=circle_collect_time, label='Sirkel: drivetid = {}'.format(circle_herd_time), color='orange')

        v_collect = ax_time.bar(ind-0.1, v_collect_time, width, label='V: samletid = {}'.format(v_collect_time), color='lightgreen')
        v_herd = ax_time.bar(ind-0.1, v_herd_time, width, bottom=v_collect_time, label='V: drivetid = {}'.format(v_herd_time), color='seagreen')

        polygon_collect = ax_time.bar(ind+0.1, polygon_collect_time, width, label='Polygon: samletid = {}'.format(polygon_collect_time), color='mediumpurple')
        polygon_herd = ax_time.bar(ind+0.1, polygon_herd_time, width, bottom=polygon_collect_time, label='Polygon: drivetid = {}'.format(polygon_herd_time), color='indigo')
        
        our_collect = ax_time.bar(ind+0.3, our_collect_time, width, label='Furthest: samletid = {}'.format(our_collect_time), color='lightcoral')
        our_herd = ax_time.bar(ind+0.3, our_herd_time, width, bottom=our_collect_time, label='Furthest: drivetid = {}'.format(our_herd_time), color='crimson')

        ax_time.bar_label(circle_herd, circle_time, rotation=90, padding=5)
        ax_time.bar_label(v_herd, v_time, rotation=90, padding=5)
        ax_time.bar_label(polygon_herd, polygon_time, rotation=90, padding=5)
        ax_time.bar_label(our_herd, our_time, rotation=90, padding=5)

        ax_time.margins(y=0.2)

        ax_time.set_xlabel('Testscenarioer')
        ax_time.set_ylabel('Gjennomsnittlig gjetetid')
        ax_time.set_xticks(ind)
        ax_time.set_xticklabels(["Cooperative flock", "Lone sheep", "Divided flock", "Right angle"])

        ax_time.set_title('Gjenomsnittlig total gjetetid, p={}'.format(perception))
        ax_time.legend(loc='center left', bbox_to_anchor=(1, 0.5))

        fig_time.savefig("{path}/gjetetid_{p}.png".format(path=dir_path, p=perception), bbox_inches='tight')
        plt.close(fig_time)


        """Bar chart for successful and unsuccessful herding for all drone algorithms and every testtype"""

        # Find successful and unsuccessful herding for circle algorithm per test
        df_circle['Suksess'] = np.where(df_circle['Suksessrate'] == 100, 1, 0)
        df_circle['Failure'] = np.where(df_circle['Suksessrate'] != 100, -1, 0)
        df_circle = df_circle.groupby(['Testtype', 'Dronetype'], as_index=False).aggregate({'Suksess': 'sum', 'Failure':'sum'})

        circle_success = df_circle['Suksess']
        circle_failure = df_circle['Failure']
        
        # Find successful and unsuccessful herding for v algorithm per test
        df_v['Suksess'] = np.where(df_v['Suksessrate'] == 100, 1, 0)
        df_v['Failure'] = np.where(df_v['Suksessrate'] != 100, -1, 0)
        df_v = df_v.groupby(['Testtype', 'Dronetype'], as_index=False).aggregate({'Suksess': 'sum', 'Failure':'sum'})

        v_success = df_v['Suksess']
        v_failure = df_v['Failure']
        
        # Find successful and unsuccessful herding for Polygon algorithm per test
        df_polygon['Suksess'] = np.where(df_polygon['Suksessrate'] == 100, 1, 0)
        df_polygon['Failure'] = np.where(df_polygon['Suksessrate'] != 100, -1, 0)
        df_polygon = df_polygon.groupby(['Testtype', 'Dronetype'], as_index=False).aggregate({'Suksess': 'sum', 'Failure':'sum'})

        polygon_success = df_polygon['Suksess']
        polygon_failure = df_polygon['Failure']
        
        # Find successful and unsuccessful herding for our algorithm per test
        df_our['Suksess'] = np.where(df_our['Suksessrate'] == 100, 1, 0)
        df_our['Failure'] = np.where(df_our['Suksessrate'] != 100, -1, 0)
        df_our = df_our.groupby(['Testtype', 'Dronetype'], as_index=False).aggregate({'Suksess': 'sum', 'Failure':'sum'})

        our_success = df_our['Suksess']
        our_failure = df_our['Failure']
        
        # SUKSESSRATEN FOR SIMULERINGENE
        fig, ax = plt.subplots()

        circle_1 = ax.bar(ind-0.3, circle_success, width, label='Sirkel: suksess', color='moccasin')
        circle_2 = ax.bar(ind-0.3, circle_failure, width, label='Sirkel: mislykket', color='orange')

        v_1 = ax.bar(ind-0.1, v_success, width, label='V: suksess', color='lightgreen')
        v_2 = ax.bar(ind-0.1, v_failure, width, label='V: mislykket', color='seagreen')

        polygon_1 = ax.bar(ind+0.1, polygon_success, width, label='Polygon: suksess', color='mediumpurple')
        polygon_2 = ax.bar(ind+0.1, polygon_failure, width, label='Polygon: mislykket', color='indigo')

        our_1 = ax.bar(ind+0.3, our_success, width, label='Furthest: suksess', color='lightcoral')
        our_2 = ax.bar(ind+0.3, our_failure, width, label='Furthest: mislykket', color='crimson')

        ax.bar_label(circle_1, padding=2)
        ax.bar_label(circle_2, padding=2)
        ax.bar_label(v_1, padding=2)
        ax.bar_label(v_2, padding=2)
        ax.bar_label(polygon_1, padding=2)
        ax.bar_label(polygon_2, padding=2)
        ax.bar_label(our_1, padding=2)
        ax.bar_label(our_2, padding=2)

        ax.margins(y=0.1)

        ax.axhline(0, color='grey', linewidth=0.8)
        ax.set_xlabel('Testscenarioer')
        ax.set_ylabel('Antall simuleringer')
        ax.set_xticks(ind)
        ax.set_xticklabels(["Cooperative flock", "Lone sheep", "Divided flock", "Right angle"])

        ax.set_title('Antall simuleringer som er suksess og mislykket, p={}'.format(perception))
        ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))

        fig.savefig("{path}/suksessrate_{p}.png".format(path=dir_path, p=perception), bbox_inches='tight')
        plt.close(fig)


if __name__ == "__main__":
    main()
    
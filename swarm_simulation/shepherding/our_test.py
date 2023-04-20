import pygame
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
from datetime import datetime
from main import Main


NO_SHEEP = 5
NO_DRONES = 3
NO_SIMULATIONS = 100 # Antall simuleringer per testtype per drone
TIME_LIMIT = 50000 # 50 sekunder for sauene å bevege seg maks 1000m
TARGET_FPS = 10 # Hastigheten på simuleringen
FPS = 30

TEST_TYPE = ["cooperative_flock", "lone_sheep", "divided_flock", "right_angle"]
COLLECT_TYPE = ['furthest', 'polygon']
DRIVE_TYPE = ['sync', 'sync']
ANGLE = [40, 30, 20]


def test(id, no_sheep, no_drones, FPS, collect_type, drive_type, testtype, angle):
    # Run the simulations
    sheep_positions = get_sheep_list(testtype, no_sheep)
    sim = Main(id, sheep_positions, no_drones, FPS, collect_type, drive_type, testtype, angle)
    successrate, herdtime, reached_goal_times, reached_goal_number, collect_time, herd_time = sim.main(TIME_LIMIT, TARGET_FPS)
    return successrate, herdtime, reached_goal_times, reached_goal_number, collect_time, herd_time
    
def get_sheep_list(testtype, no_sheep):
    # Based on the testtype, the sheep are positioned different places
    position_list = [x for x in range(no_sheep)]
    
    if testtype == "cooperative_flock":
        for i in position_list:
            x = np.random.randint(400, 420)
            y = np.random.randint(200, 220)
            position_list[i] = pygame.Vector2(x, y) 
    
    if testtype == "lone_sheep":
        for i in range(len(position_list)-1):
            x = np.random.randint(400, 420)
            y = np.random.randint(200, 220)
            position_list[i] = pygame.Vector2(x, y) 
        
        x = np.random.randint(300, 320)
        y = np.random.randint(800, 820)
        position_list[-1] = pygame.Vector2(x, y)
    
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
    dir_path = './results/{}'.format(str(datetime.now()))
    if not os.path.exists(dir_path):
        os.mkdir(dir_path)

    # Run all the different variations of the simulations
    for test_type in TEST_TYPE:
        for collect_type in COLLECT_TYPE:
            df_polygon = pd.DataFrame(columns = ['Testtype', 'Dronetype', 'Gjetetid', 'Suksessrate'])
            df_furthest = pd.DataFrame(columns = ['Testtype', 'Dronetype', 'Gjetetid', 'Suksessrate'])
            for drive_type in DRIVE_TYPE:
                for angle in ANGLE:
                    for id in range(NO_SIMULATIONS):
                        print(collect_type, drive_type, angle, id)
                        successrate, herdtime, collect_time, actual_herd_time = test(id, NO_SHEEP, NO_DRONES, FPS*NO_DRONES, collect_type, drive_type, test_type, angle)
                        if collect_type == 'furthest':
                            df_furthest = df_furthest.append({'Testtype': test_type, 'Dronetype': collect_type, 'Gjetetid':herdtime, 'Suksessrate':successrate, 'Oppsamlingstid':collect_time, 'Drivetid':actual_herd_time}, ignore_index = True)
                        if collect_type == 'polygon':
                            df_polygon = df_polygon.append({'Testtype': test_type, 'Dronetype': collect_type, 'Gjetetid':herdtime, 'Suksessrate':successrate, 'Oppsamlingstid':collect_time, 'Drivetid':actual_herd_time}, ignore_index = True)

        
        df_polygon_original = df_polygon.copy()
        df_furthest_original = df_furthest.copy()

        # Make tables for all the data
        # TODO: må dele opp i sync og async
        df_polygon_original = df_polygon_original.drop(columns=['Dronetype'])
        df_polygon_original.to_csv('{path}/polygon_{p}.csv'.format(path=dir_path, p=angle), index=False)

        df_furthest_original = df_furthest_original.drop(columns=['Dronetype'])
        df_furthest_original.to_csv('{path}/furthest_{p}.csv'.format(path=dir_path, p=angle), index=False)


        """Bar chart for average herd time from successful herding for all algorithms per test"""

        # Polygon
        df_polygon_success = df_polygon.loc[df_polygon['Suksessrate'] == 100]
        df_avg_time_polygon = df_polygon_success.groupby(['Testtype', 'Dronetype'], as_index=False).aggregate({'Gjetetid':'mean', 'Oppsamlingstid':'mean', 'Drivetid':'mean'})
        df_avg_time_polygon_index = df_avg_time_polygon.copy()
        df_avg_time_polygon_index.set_index('Testtype', inplace=True, drop=True)
        df_avg_time_polygon_index.style.set_precision(1)
        polygon_time = []
        polygon_collect_time = []
        polygon_herd_time = []
        if (df_avg_time_polygon['Testtype'].eq('cooperative_flock')).any():
            polygon_time.append(df_avg_time_polygon_index.loc['cooperative_flock', 'Gjetetid'])
            polygon_collect_time.append(df_avg_time_polygon_index.loc['cooperative_flock', 'Oppsamlingstid'])
            polygon_herd_time.append(df_avg_time_polygon_index.loc['cooperative_flock', 'Drivetid'])
        else:
            polygon_time.append(0)
            polygon_collect_time.append(0)
            polygon_herd_time.append(0)

        if (df_avg_time_polygon['Testtype'].eq('lone_sheep')).any():
            polygon_time.append(df_avg_time_polygon_index.loc['lone_sheep', 'Gjetetid'])
            polygon_collect_time.append(df_avg_time_polygon_index.loc['lone_sheep', 'Oppsamlingstid'])
            polygon_herd_time.append(df_avg_time_polygon_index.loc['lone_sheep', 'Drivetid'])
        else:
            polygon_time.append(0)
            polygon_collect_time.append(0)
            polygon_herd_time.append(0)

        if (df_avg_time_polygon['Testtype'].eq('divided_flock')).any():
            polygon_time.append(df_avg_time_polygon_index.loc['divided_flock', 'Gjetetid'])
            polygon_collect_time.append(df_avg_time_polygon_index.loc['divided_flock', 'Oppsamlingstid'])
            polygon_herd_time.append(df_avg_time_polygon_index.loc['divided_flock', 'Drivetid'])
        else:
            polygon_time.append(0)
            polygon_collect_time.append(0)
            polygon_herd_time.append(0)

        if (df_avg_time_polygon['Testtype'].eq('right_angle')).any():
            polygon_time.append(df_avg_time_polygon_index.loc['right_angle', 'Gjetetid'])
            polygon_collect_time.append(df_avg_time_polygon_index.loc['right_angle', 'Oppsamlingstid'])
            polygon_herd_time.append(df_avg_time_polygon_index.loc['right_angle', 'Drivetid'])
        else:
            polygon_time.append(0)
            polygon_collect_time.append(0)
            polygon_herd_time.append(0)

        # Furthest



        
        # Make figure
        N = 4
        ind = np.arange(N) # the x locations for the groups
        width = 0.20

        fig_time, ax_time = plt.subplots()

        furthest_collect = ax_time.bar(ind, furthest_collect_time, width, label='v collect', color='lightskyblue')
        furthest_herd = ax_time.bar(ind, furthest_herd_time, width, bottom=furthest_collect_time, label='v herd', color='dodgerblue')

        polygon_collect = ax_time.bar(ind+0.25, polygon_collect_time, width, label='Polygon collect', color='mediumpurple')
        polygon_herd = ax_time.bar(ind+0.25, polygon_herd_time, width, bottom=polygon_collect_time, label='Polygon herd', color='indigo')

        ax_time.bar_label(furthest_collect, label_type='center')
        ax_time.bar_label(furthest_herd, label_type='edge')
        ax_time.bar_label(polygon_collect, label_type='center')
        ax_time.bar_label(polygon_herd, label_type='edge')

        ax_time.set_xlabel('Testtypes')
        ax_time.set_ylabel('Gjetetid')
        ax_time.set_xticks(ind)
        ax_time.set_xticklabels(["Cooperative flock", "Lone sheep", "Divided flock", "Right angle"])

        ax_time.set_title('Gjenomsnittlig gjetetid for hver dronealgoritme per testtype, p={}'.format(test_type))
        ax_time.legend(loc='center left', bbox_to_anchor=(1, 0.5))

        fig_time.savefig("{path}/gjetetid_{p}.png".format(path=dir_path, p=test_type), bbox_inches='tight')
        plt.close(fig_time)


        """Bar chart for successful and unsuccessful herding for all drone algorithms and every testtype"""
        
        # Find successful and unsuccessful herding for v algorithm per test
        df_furthest['Suksess'] = np.where(df_furthest['Suksessrate'] == 100, 1, 0)
        df_furthest['Failure'] = np.where(df_furthest['Suksessrate'] != 100, -1, 0)
        df_furthest = df_furthest.groupby(['Testtype', 'Dronetype'], as_index=False).aggregate({'Suksess': 'sum', 'Failure':'sum'})

        v_success = df_furthest['Suksess']
        v_failure = df_furthest['Failure']
        
        # Find successful and unsuccessful herding for Polygon algorithm per test
        df_polygon['Suksess'] = np.where(df_polygon['Suksessrate'] == 100, 1, 0)
        df_polygon['Failure'] = np.where(df_polygon['Suksessrate'] != 100, -1, 0)
        df_polygon = df_polygon.groupby(['Testtype', 'Dronetype'], as_index=False).aggregate({'Suksess': 'sum', 'Failure':'sum'})

        polygon_success = df_polygon['Suksess']
        polygon_failure = df_polygon['Failure']
        
        
        # Make figure
        fig, ax = plt.subplots()

        furthest_1 = ax.bar(ind, v_success, width, label='V Successes', color='lightskyblue')
        furthest_2 = ax.bar(ind, v_failure, width, label='V Failures', color='dodgerblue')

        polygon_1 = ax.bar(ind+0.25, polygon_success, width, label='Polygon Successes', color='mediumpurple')
        polygon_2 = ax.bar(ind+0.25, polygon_failure, width, label='Polygon Failures', color='indigo')

        ax.bar_label(furthest_1, label_type='center')
        ax.bar_label(furthest_2, label_type='center')
        ax.bar_label(polygon_1, label_type='center')
        ax.bar_label(polygon_2, label_type='center')

        ax.axhline(0, color='grey', linewidth=0.8)
        ax.set_xlabel('Testtypes')
        ax.set_ylabel('Simuleringer')
        ax.set_xticks(ind)
        ax.set_xticklabels(["Cooperative flock", "Lone sheep", "Divided flock", "Right angle"])

        ax.set_title('Number of success and failure by testtype, p={}'.format(angle))
        ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))

        fig.savefig("{path}/suksessrate_{p}.png".format(path=dir_path, p=test_type), bbox_inches='tight')
        plt.close(fig)


if __name__ == "__main__":
    main()
    
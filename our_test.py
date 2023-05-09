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
TIME_LIMIT = 50000 # 50 sekunder for sauene å bevege seg maks 1000
TARGET_FPS = 10 # Hastigheten på simuleringen
FPS = 30
TEST_TYPE = ["cooperative_flock", "lone_sheep", "divided_flock", "right_angle"]
COLLECT_TYPE = ['polygon', 'furthest']
ANGLE = [10, 15, 20, 25, 30]
CAPTURE_TIMES = [x for x in range(50, 5000, 200)]

pd.set_option('display.precision', 2)   # Verdiene i tabellene runder av til to desimaler


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
    dir_path = './our_results/{}'.format(str(datetime.now()))
    if not os.path.exists(dir_path):
        os.mkdir(dir_path)

    # Run all the different variations of the simulations
    df_polygon = pd.DataFrame(columns = ['Testtype', 'Samletype', 'Vinkel', 'Gjetetid', 'Suksessrate', 'Oppsamlingstid', 'Drivetid'])
    df_furthest = pd.DataFrame(columns = ['Testtype', 'Samletype', 'Vinkel', 'Gjetetid', 'Suksessrate', 'Oppsamlingstid', 'Drivetid'])
        
    for test_type in TEST_TYPE:
        for collect_type in COLLECT_TYPE:
                for angle in ANGLE:
                    for id in range(NO_SIMULATIONS):
                        print(collect_type, angle, id)
                        successrate, herdtime, collect_time, actual_herd_time = test(id, NO_SHEEP, NO_DRONES, FPS*NO_DRONES, collect_type, test_type, angle, dir_path)
                        if collect_type == 'furthest':
                            df_furthest = df_furthest.append({'Testtype': test_type, 'Samletype': collect_type, 'Vinkel': angle, 'Gjetetid':herdtime, 'Suksessrate':successrate, 'Oppsamlingstid':collect_time, 'Drivetid':actual_herd_time}, ignore_index = True)
                        if collect_type == 'polygon':
                            df_polygon = df_polygon.append({'Testtype': test_type, 'Samletype': collect_type, 'Vinkel': angle, 'Gjetetid':herdtime, 'Suksessrate':successrate, 'Oppsamlingstid':collect_time, 'Drivetid':actual_herd_time}, ignore_index = True)

        
    df_polygon_original = df_polygon.copy()
    df_furthest_original = df_furthest.copy()

    # Make tables for all the data
    df_polygon_original = df_polygon_original.drop(columns=['Samletype'])
    df_polygon_original.to_csv('{path}/polygon.csv'.format(path=dir_path), index=False)

    df_furthest_original = df_furthest_original.drop(columns=['Samletype'])
    df_furthest_original.to_csv('{path}/furthest.csv'.format(path=dir_path), index=False)

    """Lineplot for average herd time from successful herding per test"""

    df_furthest_success = df_furthest.loc[df_furthest['Suksessrate'] == 100]
    df_avg_time_furthest = df_furthest_success.groupby(['Testtype', 'Samletype', 'Vinkel'], as_index=False).aggregate({'Gjetetid':'mean', 'Oppsamlingstid':'mean', 'Drivetid':'mean'}).round(2)
    df_avg_time_furthest_index = df_avg_time_furthest.copy()
    df_avg_time_furthest_index.set_index('Testtype', inplace=True, drop=True)

    df_polygon_success = df_polygon.loc[df_polygon['Suksessrate'] == 100]
    df_avg_time_polygon = df_polygon_success.groupby(['Testtype', 'Samletype', 'Vinkel'], as_index=False).aggregate({'Gjetetid':'mean', 'Oppsamlingstid':'mean', 'Drivetid':'mean'}).round(2)
    df_avg_time_polygon_index = df_avg_time_polygon.copy()
    df_avg_time_polygon_index.set_index('Testtype', inplace=True, drop=True)

    for type in TEST_TYPE:        
        polygon_time = []
        polygon_collect_time = []
        polygon_herd_time = [] 
        furthest_time = []
        furthest_collect_time = []
        furthest_herd_time = []

        for a in ANGLE:
            for drone in COLLECT_TYPE:   
                if drone == "polygon":
                    if ((df_avg_time_polygon['Testtype'] == type) & (df_avg_time_polygon['Samletype'] == drone)  & (df_avg_time_polygon['Vinkel'] == a)).any():
                        p_row = df_avg_time_polygon.loc[(df_avg_time_polygon['Testtype'] == type) & (df_avg_time_polygon['Samletype'] == drone) & (df_avg_time_polygon['Vinkel'] == a)]
                        polygon_time.append(p_row['Gjetetid'].iloc[0])
                        polygon_collect_time.append(p_row['Oppsamlingstid'].iloc[0])
                        polygon_herd_time.append(p_row['Drivetid'].iloc[0])
                    else:
                        polygon_time.append(0)
                        polygon_collect_time.append(0)
                        polygon_herd_time.append(0)
                    
                if drone == "furthest":
                    if ((df_avg_time_furthest['Testtype'] == type) & (df_avg_time_furthest['Samletype'] == drone) &  (df_avg_time_furthest['Vinkel'] == a)).any():
                        f_row = df_avg_time_furthest.loc[(df_avg_time_furthest['Testtype'] == type) & (df_avg_time_furthest['Samletype'] == drone) & (df_avg_time_furthest['Vinkel'] == a)]
                        furthest_time.append(f_row['Gjetetid'].iloc[0])
                        furthest_collect_time.append(f_row['Oppsamlingstid'].iloc[0])
                        furthest_herd_time.append(f_row['Drivetid'].iloc[0])
                    else:
                        furthest_time.append(0)
                        furthest_collect_time.append(0)
                        furthest_herd_time.append(0)


        plt.plot(ANGLE, furthest_collect_time, label='Furthest, samletid', color='lightcoral', marker='o')
        plt.plot(ANGLE, furthest_herd_time, label='Furthest, drivetid', color='crimson', marker='o')
        plt.plot(ANGLE, furthest_time, label='Furthest, totaltid', color='darkred', marker='o')

        plt.plot(ANGLE, polygon_collect_time, label='Polygon, samletid', color='skyblue', marker='o')
        plt.plot(ANGLE, polygon_herd_time, label='Polygon, drivetid', color='cornflowerblue', marker='o')
        plt.plot(ANGLE, polygon_time, label='Polygon, totaltid', color='mediumblue', marker='o')

        plt.xlabel('Vinkel i grader')
        plt.ylabel('Gjennomsnittlig total gjetetid')
        plt.xticks(ANGLE)
        plt.title("Gjennomsnittlig gjetetid basert på vinkler for '{}'".format(type))
        plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))
        plt.savefig('{path}/gjetetid_{t}.png'.format(path=dir_path, t=type), bbox_inches='tight')
        plt.close()

       
    for type in TEST_TYPE:
        fig_time, ax_time = plt.subplots()

        polygon_time = []
        polygon_collect_time = []
        polygon_herd_time = [] 
        furthest_time = []
        furthest_collect_time = []
        furthest_herd_time = []

        N = len(ANGLE)
        ind = np.arange(N)
        width = 0.20

        for a in ANGLE:
            for drone in COLLECT_TYPE:   
                if drone == "polygon":
                    if ((df_avg_time_polygon['Testtype'] == type) & (df_avg_time_polygon['Vinkel'] == a)).any():
                        p_row = df_avg_time_polygon.loc[(df_avg_time_polygon['Testtype'] == type) & (df_avg_time_polygon['Samletype'] == drone) & (df_avg_time_polygon['Vinkel'] == a)]
                        polygon_time.append(p_row['Gjetetid'].iloc[0])
                        polygon_collect_time.append(p_row['Oppsamlingstid'].iloc[0])
                        polygon_herd_time.append(p_row['Drivetid'].iloc[0])
                    else:
                        polygon_time.append(0)
                        polygon_collect_time.append(0)
                        polygon_herd_time.append(0)
                    
                if drone == "furthest":
                    if ((df_avg_time_furthest['Testtype'] == type) & (df_avg_time_furthest['Samletype'] == drone) & (df_avg_time_furthest['Vinkel'] == a)).any():
                        f_row = df_avg_time_furthest.loc[(df_avg_time_furthest['Testtype'] == type) & (df_avg_time_furthest['Samletype'] == drone) & (df_avg_time_furthest['Vinkel'] == a)]
                        furthest_time.append(f_row['Gjetetid'].iloc[0])
                        furthest_collect_time.append(f_row['Oppsamlingstid'].iloc[0])
                        furthest_herd_time.append(f_row['Drivetid'].iloc[0])
                    else:
                        furthest_time.append(0)
                        furthest_collect_time.append(0)
                        furthest_herd_time.append(0)

        furthest_collect = ax_time.bar(ind-0.1, furthest_collect_time, width, label='Furthest: samletid = {}'.format(furthest_collect_time), color='lightcoral')
        furthest_herd = ax_time.bar(ind-0.1, furthest_herd_time, width, bottom=furthest_collect_time, label='Furthest: drivetid = {}'.format(furthest_herd_time), color='crimson')

        polygon_collect = ax_time.bar(ind+0.1, polygon_collect_time, width, label='Polygon: samletid = {}'.format(polygon_collect_time), color='skyblue')
        polygon_herd = ax_time.bar(ind+0.1, polygon_herd_time, width, bottom=polygon_collect_time, label='Polygon: drivetid = {}'.format(polygon_herd_time), color='cornflowerblue')

        ax_time.bar_label(furthest_herd, furthest_time, rotation=90, padding=5)
        ax_time.bar_label(polygon_herd, polygon_time, rotation=90, padding=5)

        ax_time.margins(y=0.2)

        ax_time.set_xlabel('Vinkel i grader')
        ax_time.set_ylabel('Gjennomsnittlig gjetetid')
        ax_time.set_xticks(ind)
        ax_time.set_xticklabels(ANGLE)

        ax_time.set_title('Gjennomsnittlig gjetetid per vinkel per testtype')
        ax_time.legend(loc='center left', bbox_to_anchor=(1, 0.5))

        fig_time.savefig("{path}/gjetetid_{t}_vinkel.png".format(path=dir_path, t=type), bbox_inches='tight')
        plt.close(fig_time)


        """Bar chart for successful and unsuccessful herding for all drone algorithms and every testtype"""
        for type in TEST_TYPE:  
            f_success = 0
            f_failure = 0
            polygon_success = 0
            polygon_failure = 0

            N = len(ANGLE)
            ind = np.arange(N)
            width = 0.20      
                

            # Find successful and unsuccessful herding for furthest algorithm per test
            furthest_testtype = df_furthest.loc[(df_furthest['Testtype'] == type)]
            furthest_testtype['Suksess'] = np.where(furthest_testtype['Suksessrate'] == 100, 1, 0)
            furthest_testtype['Failure'] = np.where(furthest_testtype['Suksessrate'] != 100, -1, 0)
            furthest_testtype = furthest_testtype.groupby(['Testtype', 'Samletype', 'Vinkel'], as_index=False).aggregate({'Suksess': 'sum', 'Failure':'sum'})

            f_success = furthest_testtype['Suksess']
            f_failure = furthest_testtype['Failure']

            polygon_testtype = df_polygon.loc[(df_polygon['Testtype'] == type)]
            polygon_testtype['Suksess'] = np.where(polygon_testtype['Suksessrate'] == 100, 1, 0)
            polygon_testtype['Failure'] = np.where(polygon_testtype['Suksessrate'] != 100, -1, 0)
            polygon_testtype = polygon_testtype.groupby(['Testtype', 'Samletype', 'Vinkel'], as_index=False).aggregate({'Suksess': 'sum', 'Failure':'sum'})

            polygon_success = polygon_testtype['Suksess']
            polygon_failure = polygon_testtype['Failure']
                
                
            # Make figure
            fig, ax = plt.subplots()

            furthest_1 = ax.bar(ind-0.1, f_success, width, label='Furthest: suksess', color='lightcoral')
            furthest_2 = ax.bar(ind-0.1, f_failure, width, label='Furthest: mislykket', color='crimson')

            polygon_1 = ax.bar(ind+0.1, polygon_success, width, label='Polygon: suksess', color='skyblue')
            polygon_2 = ax.bar(ind+0.1, polygon_failure, width, label='Polygon: mislykket', color='cornflowerblue')

  
            ax.bar_label(furthest_1, padding=2)
            ax.bar_label(furthest_2, padding=2)
            ax.bar_label(polygon_1, padding=2)
            ax.bar_label(polygon_2, padding=2)

            ax.axhline(0, color='grey', linewidth=0.8)
            ax.set_xlabel('Vinkler')
            ax.set_ylabel('Antall Simuleringer')
            ax.set_xticks(ind)
            ax.set_xticklabels(ANGLE)

            ax.set_title('Antall simuleringer som er suksess og mislykket')
            ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))

            fig.savefig("{path}/suksessrate_{p}.png".format(path=dir_path, p=type), bbox_inches='tight')
            plt.close(fig)


if __name__ == "__main__":
    main()
    
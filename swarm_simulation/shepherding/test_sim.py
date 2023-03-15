import pandas as pd
import numpy as np
import pygame
from shared_main import SharedMain
from goal import Goal
import matplotlib.pyplot as plt


NO_SHEEP = 20
NO_DRONES = 3
NO_SIMULATIONS = 4 # Antall simuleringer per testtype per drone
TIME_LIMIT = 20000
FPS = 50
TESTTYPES = ["cooperative_flock", "lone_sheep", "divided_flock", "right_angle"]
DRONETYPES = ['circle', 'polygon'] # 'occlusion']
INITIAL_GOAL_VECTOR = pygame.Vector2(500, 600)
INITIAL_GOAL = Goal(INITIAL_GOAL_VECTOR)

def test(id, no_sheep, no_drones, FPS, dronetype, testtype, initial_goal_vector, initial_goal):
    sheep_positions = get_sheep_list(testtype, no_sheep)
    sim = SharedMain(id, sheep_positions, no_drones, FPS, dronetype, testtype, initial_goal_vector, initial_goal)
    successrate, herdtime, reached_goal_times, reached_goal_number = sim.main(TIME_LIMIT)
    return successrate, herdtime, reached_goal_times, reached_goal_number
    
def get_sheep_list(testtype, no_sheep):
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
        
        x = np.random.randint(100, 900)
        y = np.random.randint(100, 900)
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
    df_circle = pd.DataFrame(columns = ['Testtype', 'Dronetype', 'Gjetetid', 'Suksessrate'])
    # df_occlusion = pd.DataFrame(columns = ['Testtype', 'Dronetype', 'Gjetetid', 'Suksessrate'])
    df_polygon = pd.DataFrame(columns = ['Testtype', 'Dronetype', 'Gjetetid', 'Suksessrate'])

    
    for dronetype in DRONETYPES:
        for testtype in TESTTYPES:
            for id in range(NO_SIMULATIONS):
                print(dronetype, testtype, id)
                successrate, herdtime, reached_goal_times, reached_goal_number = test(id, NO_SHEEP, NO_DRONES, FPS*NO_DRONES, dronetype, testtype, INITIAL_GOAL_VECTOR, INITIAL_GOAL)
                if dronetype == 'circle':
                    df_circle = df_circle.append({'Testtype': testtype, 'Dronetype': dronetype, 'Gjetetid':herdtime, 'Suksessrate':successrate}, ignore_index = True)
                # if dronetype == 'occlusion':
                #     df_occlusion = df_occlusion.append({'Testtype': testtype, 'Dronetype': dronetype, 'Gjetetid':herdtime, 'Suksessrate':successrate}, ignore_index = True)
                if dronetype == 'polygon':
                    df_polygon = df_polygon.append({'Testtype': testtype, 'Dronetype': dronetype, 'Gjetetid':herdtime, 'Suksessrate':successrate}, ignore_index = True)

    df_circle_original = df_circle.copy()
    # df_occlusion_original = df_occlusion.copy()
    df_polygon_original = df_polygon.copy()

    """Make tables"""
    
    df_circle_original = df_circle_original.drop(columns=['Dronetype'])
    df_circle_original.to_csv('./results/circle.csv', index=False)

    # df_occlusion_original = df_occlusion_original.drop(columns=['Dronetype'])
    # df_occlusion_original.to_csv('./results/occlusion.csv', index=False)

    df_polygon_original = df_polygon_original.drop(columns=['Dronetype'])
    df_polygon_original.to_csv('./results/polygon.csv', index=False)

    """Bar chart for average herd time from successful herding for all algorithms per test"""
    
    # Circle
    df_circle_success = df_circle.loc[df_circle['Suksessrate'] == 100]
    df_avg_time_circle = df_circle_success.groupby(['Testtype', 'Dronetype'], as_index=False).aggregate({'Gjetetid':'mean'})
    df_avg_time_circle_index = df_avg_time_circle.copy()
    df_avg_time_circle_index.set_index('Testtype', inplace=True, drop=True)
    circle_time = []
    if (df_avg_time_circle['Testtype'].eq('cooperative_flock')).any():
        circle_time.append(df_avg_time_circle_index.loc['cooperative_flock', 'Gjetetid'])
    else:
        circle_time.append(0)
    if (df_avg_time_circle['Testtype'].eq('lone_sheep')).any():
        circle_time.append(df_avg_time_circle_index.loc['lone_sheep', 'Gjetetid'])
    else:
        circle_time.append(0)
    if (df_avg_time_circle['Testtype'].eq('divided_flock')).any():
        circle_time.append(df_avg_time_circle_index.loc['divided_flock', 'Gjetetid'])
    else:
        circle_time.append(0)
    if (df_avg_time_circle['Testtype'].eq('right_angle')).any():
        circle_time.append(df_avg_time_circle_index.loc['right_angle', 'Gjetetid'])
    else:
        circle_time.append(0)

    
    # Occlusion
    # df_occlusion_success = df_occlusion.loc[df_occlusion['Suksessrate'] == 100]
    # df_avg_time_occlusion = df_occlusion_success.groupby(['Testtype', 'Dronetype'], as_index=False).aggregate({'Gjetetid':'mean'})
    # df_avg_time_occlusion_index = df_avg_time_occlusion.copy()
    # df_avg_time_occlusion_index.set_index('Testtype', inplace=True, drop=True)
    # occlusion_time = []
    # if (df_avg_time_occlusion['Testtype'].eq('cooperative_flock')).any():
    #     occlusion_time.append(df_avg_time_occlusion_index.loc['cooperative_flock', 'Gjetetid'])
    # else:
    #     occlusion_time.append(0)
    # if (df_avg_time_occlusion['Testtype'].eq('lone_sheep')).any():
    #     occlusion_time.append(df_avg_time_occlusion_index.loc['lone_sheep', 'Gjetetid'])
    # else:
    #     occlusion_time.append(0)
    # if (df_avg_time_occlusion['Testtype'].eq('divided_flock')).any():
    #     occlusion_time.append(df_avg_time_occlusion_index.loc['divided_flock', 'Gjetetid'])
    # else:
    #     occlusion_time.append(0)
    # if (df_avg_time_occlusion['Testtype'].eq('right_angle')).any():
    #     occlusion_time.append(df_avg_time_occlusion_index.loc['right_angle', 'Gjetetid'])
    # else:
    #     occlusion_time.append(0)

    # Polygon
    df_polygon_success = df_polygon.loc[df_polygon['Suksessrate'] == 100]
    df_avg_time_polygon = df_polygon_success.groupby(['Testtype', 'Dronetype'], as_index=False).aggregate({'Gjetetid':'mean'})
    df_avg_time_polygon_index = df_avg_time_polygon.copy()
    df_avg_time_polygon_index.set_index('Testtype', inplace=True, drop=True)
    polygon_time = []
    if (df_avg_time_polygon['Testtype'].eq('cooperative_flock')).any():
        polygon_time.append(df_avg_time_polygon_index.loc['cooperative_flock', 'Gjetetid'])
    else:
        polygon_time.append(0)
    if (df_avg_time_polygon['Testtype'].eq('lone_sheep')).any():
        polygon_time.append(df_avg_time_polygon_index.loc['lone_sheep', 'Gjetetid'])
    else:
        polygon_time.append(0)
    if (df_avg_time_polygon['Testtype'].eq('divided_flock')).any():
        polygon_time.append(df_avg_time_polygon_index.loc['divided_flock', 'Gjetetid'])
    else:
        polygon_time.append(0)
    if (df_avg_time_polygon['Testtype'].eq('right_angle')).any():
       polygon_time.append(df_avg_time_polygon_index.loc['right_angle', 'Gjetetid'])
    else:
        polygon_time.append(0)

    
    N = 4
    ind = np.arange(N) # the x locations for the groups
    width = 0.25

    fig_time, ax_time = plt.subplots()

    circle_time = ax_time.bar(ind-0.25, circle_time, width, label='Circle')
    # occlusion_time = ax_time.bar(ind, occlusion_time, width, label='Occlusion')
    polygon_time = ax_time.bar(ind+0.25, polygon_time, width, label='Polygon')

    ax_time.bar_label(circle_time, label_type='center')
    # ax_time.bar_label(occlusion_time, label_type='center')
    ax_time.bar_label(polygon_time, label_type='center')

    ax_time.set_xlabel('Testtypes')
    ax_time.set_ylabel('Gjetetid')
    ax_time.set_xticks(ind)
    ax_time.set_xticklabels(["Cooperative flock", "Lone sheep", "Divided flock", "Right angle"])

    ax_time.set_title('Gjenomsnittlig gjetetid for hver dronealgoritme per testtype')
    ax_time.legend()

    plt.show()


    """Bar chart for successful and unsuccessful herding for all drone algorithms and every testtype"""
    # Find successful and unsuccessful herding for Circle algorithm per test
    df_circle['Suksess'] = np.where(df_circle['Suksessrate'] == 100, 1, 0)
    df_circle['Failure'] = np.where(df_circle['Suksessrate'] != 100, -1, 0)
    df_circle = df_circle.groupby(['Testtype', 'Dronetype'], as_index=False).aggregate({'Suksess': 'sum', 'Failure':'sum'})

    circle_failure = df_circle['Failure']
    circle_success = df_circle['Suksess']

    # Find successful and unsuccessful herding for Occlusion algorithm per test
    # df_occlusion['Suksess'] = np.where(df_occlusion['Suksessrate'] == 100, 1, 0)
    # df_occlusion['Failure'] = np.where(df_occlusion['Suksessrate'] != 100, -1, 0)
    # df_occlusion = df_occlusion.groupby(['Testtype', 'Dronetype'], as_index=False).aggregate({'Suksess': 'sum', 'Failure':'sum'})

    # occlusion_failure = df_occlusion['Failure']
    # occlusion_success = df_occlusion['Suksess']

    # Find successful and unsuccessful herding for Polygon algorithm per test
    df_polygon['Suksess'] = np.where(df_polygon['Suksessrate'] == 100, 1, 0)
    df_polygon['Failure'] = np.where(df_polygon['Suksessrate'] != 100, -1, 0)
    df_polygon = df_polygon.groupby(['Testtype', 'Dronetype'], as_index=False).aggregate({'Suksess': 'sum', 'Failure':'sum'})

    polygon_failure = df_polygon['Failure']
    polygon_success = df_polygon['Suksess']
    
    

    fig, ax = plt.subplots()

    circle_1 = ax.bar(ind-0.25, circle_success, width, label='Circle Successes')
    circle_2 = ax.bar(ind-0.25, circle_failure, width, label='Circle Failures')

    # occlusion_1 = ax.bar(ind, occlusion_success, width, label='Occlusion Successes')
    # occlusion_2 = ax.bar(ind, occlusion_failure, width, label='Occlusion Failures')

    polygon_1 = ax.bar(ind+0.25, polygon_success, width, label='Polygon Successes')
    polygon_2 = ax.bar(ind+0.25, polygon_failure, width, label='Polygon Failures')

    ax.bar_label(circle_1, label_type='center')
    ax.bar_label(circle_2, label_type='center')
    # ax.bar_label(occlusion_1, label_type='center')
    # ax.bar_label(occlusion_2, label_type='center')
    ax.bar_label(polygon_1, label_type='center')
    ax.bar_label(polygon_2, label_type='center')

    ax.axhline(0, color='grey', linewidth=0.8)
    ax.set_xlabel('Testtypes')
    ax.set_ylabel('Simuleringer')
    ax.set_xticks(ind)
    ax.set_xticklabels(["Cooperative flock", "Lone sheep", "Divided flock", "Right angle"])

    ax.set_title('Number of success and failure by testtype')
    ax.legend()

    plt.show()
    

if __name__ == "__main__":
    main()
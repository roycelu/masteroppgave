from matplotlib import pyplot as plt
import numpy as np
import pandas as pd
from constants import *

# PERCEPTIONS = [20, 30, 40]
# ANGLE = [10, 15, 20, 25, 30]
# TESTTYPES = ["cooperative_flock", "divided_flock", "lone_sheep", "right_angle"]
# OUR_DRONETYPES = ['v_polygon', 'com']

def average_time_existing(dir_path, df_circle, df_v, df_polygon, perception):
    """Bar chart for average herd time from successful herding for all algorithms per test"""
    # Circle
    df_circle_success = df_circle.loc[df_circle['Suksessrate'] == 100]
    df_avg_time_circle = df_circle_success.groupby(['Testtype'], as_index=False).aggregate({'Gjetetid':'mean', 'Oppsamlingstid':'mean', 'Drivetid':'mean'}).round(2) # Runder av til to desimaler
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
    df_avg_time_v = df_v_success.groupby(['Testtype'], as_index=False).aggregate({'Gjetetid':'mean', 'Oppsamlingstid':'mean', 'Drivetid':'mean'}).round(2) # Runder av til to desimaler
    df_avg_time_v_index = df_avg_time_v.copy()
    df_avg_time_v_index.set_index('Testtype', inplace=True, drop=True)
    v_time = []
    v_collect_time = []
    v_herd_time = []

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
    df_avg_time_polygon = df_polygon_success.groupby(['Testtype'], as_index=False).aggregate({'Gjetetid':'mean', 'Oppsamlingstid':'mean', 'Drivetid':'mean'}).round(2) # Runder av til to desimaler
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

    
    # Make figure
    N = 4
    ind = np.arange(N) # the x locations for the groups
    width = 0.20

    fig_time, ax_time = plt.subplots()

    circle_collect = ax_time.bar(ind-0.25, circle_collect_time, width, label='Sirkel: samletid = {}'.format(circle_collect_time), color='moccasin')
    circle_herd = ax_time.bar(ind-0.25, circle_herd_time, width, bottom=circle_collect_time, label='Sirkel: drivetid = {}'.format(circle_herd_time), color='orange')

    v_collect = ax_time.bar(ind, v_collect_time, width, label='V: samletid = {}'.format(v_collect_time), color='lightgreen')
    v_herd = ax_time.bar(ind, v_herd_time, width, bottom=v_collect_time, label='V: drivetid = {}'.format(v_herd_time), color='seagreen')

    polygon_collect = ax_time.bar(ind+0.25, polygon_collect_time, width, label='Polygon: samletid = {}'.format(polygon_collect_time), color='mediumpurple')
    polygon_herd = ax_time.bar(ind+0.25, polygon_herd_time, width, bottom=polygon_collect_time, label='Polygon: drivetid = {}'.format(polygon_herd_time), color='indigo')
    
    ax_time.bar_label(circle_herd, circle_time, rotation=90, padding=5)
    ax_time.bar_label(v_herd, v_time, rotation=90, padding=5)
    ax_time.bar_label(polygon_herd, polygon_time, rotation=90, padding=5)

    ax_time.margins(y=0.2)

    ax_time.set_xlabel('Testscenarioer')
    ax_time.set_ylabel('Gjennomsnittlig gjetetid')
    ax_time.set_xticks(ind)
    ax_time.set_xticklabels(["Cooperative flock", "Divided flock", "Lone sheep", "Right angle"])

    ax_time.set_title('Gjenomsnittlig total gjetetid, p={}'.format(perception))
    ax_time.legend(loc='center left', bbox_to_anchor=(1, 0.5))

    fig_time.savefig("{path}/gjetetid_{p}.png".format(path=dir_path, p=perception), bbox_inches='tight')
    plt.close(fig_time)



def succsessrate_existing(dir_path, df_circle, df_v, df_polygon, perception):
    """Bar chart for successful and unsuccessful herding for all drone algorithms and every testtype"""

    # Find successful and unsuccessful herding for circle algorithm per test
    df_circle['Suksess'] = np.where(df_circle['Suksessrate'] == 100, 1, 0)
    df_circle['Failure'] = np.where(df_circle['Suksessrate'] != 100, -1, 0)
    df_circle = df_circle.groupby(['Testtype'], as_index=False).aggregate({'Suksess': 'sum', 'Failure':'sum'})

    circle_success = df_circle['Suksess']
    circle_failure = df_circle['Failure']
    
    # Find successful and unsuccessful herding for v algorithm per test
    df_v['Suksess'] = np.where(df_v['Suksessrate'] == 100, 1, 0)
    df_v['Failure'] = np.where(df_v['Suksessrate'] != 100, -1, 0)
    df_v = df_v.groupby(['Testtype'], as_index=False).aggregate({'Suksess': 'sum', 'Failure':'sum'})

    v_success = df_v['Suksess']
    v_failure = df_v['Failure']
    
    # Find successful and unsuccessful herding for Polygon algorithm per test
    df_polygon['Suksess'] = np.where(df_polygon['Suksessrate'] == 100, 1, 0)
    df_polygon['Failure'] = np.where(df_polygon['Suksessrate'] != 100, -1, 0)
    df_polygon = df_polygon.groupby(['Testtype'], as_index=False).aggregate({'Suksess': 'sum', 'Failure':'sum'})

    polygon_success = df_polygon['Suksess']
    polygon_failure = df_polygon['Failure']
    
    # Make figure
    N = 4
    ind = np.arange(N) # the x locations for the groups
    width = 0.20
    
    fig, ax = plt.subplots()

    circle_1 = ax.bar(ind-0.25, circle_success, width, label='Sirkel: suksess', color='moccasin')
    circle_2 = ax.bar(ind-0.25, circle_failure, width, label='Sirkel: mislykket', color='orange')

    v_1 = ax.bar(ind, v_success, width, label='V: suksess', color='lightgreen')
    v_2 = ax.bar(ind, v_failure, width, label='V: mislykket', color='seagreen')

    polygon_1 = ax.bar(ind+0.25, polygon_success, width, label='Polygon: suksess', color='mediumpurple')
    polygon_2 = ax.bar(ind+0.25, polygon_failure, width, label='Polygon: mislykket', color='indigo')

    ax.bar_label(circle_1, padding=2)
    ax.bar_label(circle_2, padding=2)
    ax.bar_label(v_1, padding=2)
    ax.bar_label(v_2, padding=2)
    ax.bar_label(polygon_1, padding=2)
    ax.bar_label(polygon_2, padding=2)

    ax.margins(y=0.1)

    ax.axhline(0, color='grey', linewidth=0.8)
    ax.set_xlabel('Testscenarioer')
    ax.set_ylabel('Antall simuleringer')
    ax.set_xticks(ind)
    ax.set_xticklabels(["Cooperative flock", "Divided flock", "Lone sheep", "Right angle"])

    ax.set_title('Antall simuleringer som er suksess og mislykket, p={}'.format(perception))
    ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))

    fig.savefig("{path}/suksessrate_{p}.png".format(path=dir_path, p=perception), bbox_inches='tight')
    plt.close(fig)
    
def average_time_all(dir_path, df_circle, df_v, df_polygon, df_our, perception):
    """Bar chart for average herd time from successful herding for all algorithms per test"""
        
    # Circle
    df_circle_success = df_circle.loc[df_circle['Suksessrate'] == 100]
    df_avg_time_circle = df_circle_success.groupby(['Testtype'], as_index=False).aggregate({'Gjetetid':'mean', 'Oppsamlingstid':'mean', 'Drivetid':'mean'}).round(2) # Runder av til to desimaler
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
    df_avg_time_v = df_v_success.groupby(['Testtype'], as_index=False).aggregate({'Gjetetid':'mean', 'Oppsamlingstid':'mean', 'Drivetid':'mean'}).round(2) # Runder av til to desimaler
    df_avg_time_v_index = df_avg_time_v.copy()
    df_avg_time_v_index.set_index('Testtype', inplace=True, drop=True)
    v_time = []
    v_collect_time = []
    v_herd_time = []

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
    df_avg_time_polygon = df_polygon_success.groupby(['Testtype'], as_index=False).aggregate({'Gjetetid':'mean', 'Oppsamlingstid':'mean', 'Drivetid':'mean'}).round(2) # Runder av til to desimaler
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
    df_avg_time_our = df_our_success.groupby(['Testtype'], as_index=False).aggregate({'Gjetetid':'mean', 'Oppsamlingstid':'mean', 'Drivetid':'mean'}).round(2) # Runder av til to desimaler
    df_avg_time_our_index = df_avg_time_our.copy()
    df_avg_time_our_index.set_index('Testtype', inplace=True, drop=True)
    our_time = []
    our_collect_time = []
    our_herd_time = []

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

    fig_time, ax_time = plt.subplots()

    circle_collect = ax_time.bar(ind-0.3, circle_collect_time, width, label='Sirkel: samletid = {}'.format(circle_collect_time), color='moccasin')
    circle_herd = ax_time.bar(ind-0.3, circle_herd_time, width, bottom=circle_collect_time, label='Sirkel: drivetid = {}'.format(circle_herd_time), color='orange')

    v_collect = ax_time.bar(ind-0.1, v_collect_time, width, label='V: samletid = {}'.format(v_collect_time), color='lightgreen')
    v_herd = ax_time.bar(ind-0.1, v_herd_time, width, bottom=v_collect_time, label='V: drivetid = {}'.format(v_herd_time), color='seagreen')

    polygon_collect = ax_time.bar(ind+0.1, polygon_collect_time, width, label='Polygon: samletid = {}'.format(polygon_collect_time), color='mediumpurple')
    polygon_herd = ax_time.bar(ind+0.1, polygon_herd_time, width, bottom=polygon_collect_time, label='Polygon: drivetid = {}'.format(polygon_herd_time), color='indigo')
    
    our_collect = ax_time.bar(ind+0.3, our_collect_time, width, label='Massesenter: samletid = {}'.format(our_collect_time), color='lightcoral')
    our_herd = ax_time.bar(ind+0.3, our_herd_time, width, bottom=our_collect_time, label='Massesenter: drivetid = {}'.format(our_herd_time), color='crimson')

    ax_time.bar_label(circle_herd, circle_time, rotation=90, padding=5)
    ax_time.bar_label(v_herd, v_time, rotation=90, padding=5)
    ax_time.bar_label(polygon_herd, polygon_time, rotation=90, padding=5)
    ax_time.bar_label(our_herd, our_time, rotation=90, padding=5)

    ax_time.margins(y=0.2)

    ax_time.set_xlabel('Testscenarioer')
    ax_time.set_ylabel('Gjennomsnittlig gjetetid')
    ax_time.set_xticks(ind)
    ax_time.set_xticklabels(["Cooperative flock", "Divided flock", "Lone sheep", "Right angle"])

    ax_time.set_title('Gjenomsnittlig total gjetetid, p={}'.format(perception))
    ax_time.legend(loc='center left', bbox_to_anchor=(1, 0.5))

    fig_time.savefig("{path}/gjetetid_{p}.png".format(path=dir_path, p=perception), bbox_inches='tight')
    plt.close(fig_time)
    return

def successrate_all(dir_path, df_circle, df_v, df_polygon, df_our, perception):
    """Bar chart for successful and unsuccessful herding for all drone algorithms and every testtype"""

    # Find successful and unsuccessful herding for circle algorithm per test
    df_circle['Suksess'] = np.where(df_circle['Suksessrate'] == 100, 1, 0)
    df_circle['Failure'] = np.where(df_circle['Suksessrate'] != 100, -1, 0)
    df_circle = df_circle.groupby(['Testtype'], as_index=False).aggregate({'Suksess': 'sum', 'Failure':'sum'})

    circle_success = df_circle['Suksess']
    circle_failure = df_circle['Failure']
    
    # Find successful and unsuccessful herding for v algorithm per test
    df_v['Suksess'] = np.where(df_v['Suksessrate'] == 100, 1, 0)
    df_v['Failure'] = np.where(df_v['Suksessrate'] != 100, -1, 0)
    df_v = df_v.groupby(['Testtype'], as_index=False).aggregate({'Suksess': 'sum', 'Failure':'sum'})

    v_success = df_v['Suksess']
    v_failure = df_v['Failure']
    
    # Find successful and unsuccessful herding for Polygon algorithm per test
    df_polygon['Suksess'] = np.where(df_polygon['Suksessrate'] == 100, 1, 0)
    df_polygon['Failure'] = np.where(df_polygon['Suksessrate'] != 100, -1, 0)
    df_polygon = df_polygon.groupby(['Testtype'], as_index=False).aggregate({'Suksess': 'sum', 'Failure':'sum'})

    polygon_success = df_polygon['Suksess']
    polygon_failure = df_polygon['Failure']
    
    # Find successful and unsuccessful herding for our algorithm per test
    df_our['Suksess'] = np.where(df_our['Suksessrate'] == 100, 1, 0)
    df_our['Failure'] = np.where(df_our['Suksessrate'] != 100, -1, 0)
    df_our = df_our.groupby(['Testtype'], as_index=False).aggregate({'Suksess': 'sum', 'Failure':'sum'})

    our_success = df_our['Suksess']
    our_failure = df_our['Failure']
    
    # Make figure
    N = 4
    ind = np.arange(N) # the x locations for the groups
    width = 0.20
    
    fig, ax = plt.subplots()

    circle_1 = ax.bar(ind-0.3, circle_success, width, label='Sirkel: suksess', color='moccasin')
    circle_2 = ax.bar(ind-0.3, circle_failure, width, label='Sirkel: mislykket', color='orange')

    v_1 = ax.bar(ind-0.1, v_success, width, label='V: suksess', color='lightgreen')
    v_2 = ax.bar(ind-0.1, v_failure, width, label='V: mislykket', color='seagreen')

    polygon_1 = ax.bar(ind+0.1, polygon_success, width, label='Polygon: suksess', color='mediumpurple')
    polygon_2 = ax.bar(ind+0.1, polygon_failure, width, label='Polygon: mislykket', color='indigo')

    our_1 = ax.bar(ind+0.3, our_success, width, label='Massesenter: suksess', color='lightcoral')
    our_2 = ax.bar(ind+0.3, our_failure, width, label='Massesenter: mislykket', color='crimson')

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
    ax.set_xticklabels(["Cooperative flock", "Divided flock", "Lone sheep", "Right angle"])

    ax.set_title('Antall simuleringer som er suksess og mislykket, p={}'.format(perception))
    ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))

    fig.savefig("{path}/suksessrate_{p}.png".format(path=dir_path, p=perception), bbox_inches='tight')
    plt.close(fig)
    return

def lineplot_our(dir_path, df_com, df_polygon):
    """Lineplot for average herd time from successful herding per test"""

    df_com_success = df_com.loc[df_com['Suksessrate'] == 100]
    df_avg_time_com = df_com_success.groupby(['Testtype', 'Vinkel'], as_index=False).aggregate({'Gjetetid':'mean', 'Oppsamlingstid':'mean', 'Drivetid':'mean'}).round(2)
    df_avg_time_com_index = df_avg_time_com.copy()
    df_avg_time_com_index.set_index('Testtype', inplace=True, drop=True)

    df_polygon_success = df_polygon.loc[df_polygon['Suksessrate'] == 100]
    df_avg_time_polygon = df_polygon_success.groupby(['Testtype', 'Vinkel'], as_index=False).aggregate({'Gjetetid':'mean', 'Oppsamlingstid':'mean', 'Drivetid':'mean'}).round(2)
    df_avg_time_polygon_index = df_avg_time_polygon.copy()
    df_avg_time_polygon_index.set_index('Testtype', inplace=True, drop=True)

    for type in TESTTYPES:        
        polygon_time = []
        polygon_collect_time = []
        polygon_herd_time = [] 
        com_time = []
        com_collect_time = []
        com_herd_time = []

        for a in ANGLES:
            for drone in OUR_DRONETYPES:   
                if drone == "v_polygon":
                    if ((df_avg_time_polygon['Testtype'] == type) & (df_avg_time_polygon['Vinkel'] == a)).any():
                        p_row = df_avg_time_polygon.loc[(df_avg_time_polygon['Testtype'] == type)& (df_avg_time_polygon['Vinkel'] == a)]
                        polygon_time.append(p_row['Gjetetid'].iloc[0])
                        polygon_collect_time.append(p_row['Oppsamlingstid'].iloc[0])
                        polygon_herd_time.append(p_row['Drivetid'].iloc[0])
                    else:
                        polygon_time.append(0)
                        polygon_collect_time.append(0)
                        polygon_herd_time.append(0)
                    
                if drone == "com":
                    if ((df_avg_time_com['Testtype'] == type) & (df_avg_time_com['Vinkel'] == a)).any():
                        f_row = df_avg_time_com.loc[(df_avg_time_com['Testtype'] == type) & (df_avg_time_com['Vinkel'] == a)]
                        com_time.append(f_row['Gjetetid'].iloc[0])
                        com_collect_time.append(f_row['Oppsamlingstid'].iloc[0])
                        com_herd_time.append(f_row['Drivetid'].iloc[0])
                    else:
                        com_time.append(0)
                        com_collect_time.append(0)
                        com_herd_time.append(0)


        plt.plot(ANGLES, com_collect_time, label='Massesenter, samletid', color='lightcoral', marker='o')
        plt.plot(ANGLES, com_herd_time, label='Massesenter, drivetid', color='crimson', marker='o')
        plt.plot(ANGLES, com_time, label='Massesenter, totaltid', color='darkred', marker='o')

        plt.plot(ANGLES, polygon_collect_time, label='Polygon, samletid', color='skyblue', marker='o')
        plt.plot(ANGLES, polygon_herd_time, label='Polygon, drivetid', color='cornflowerblue', marker='o')
        plt.plot(ANGLES, polygon_time, label='Polygon, totaltid', color='mediumblue', marker='o')

        plt.xlabel('Vinkel i grader')
        plt.ylabel('Gjennomsnittlig total gjetetid')
        plt.xticks(ANGLES)
        plt.title("Gjennomsnittlig gjetetid basert på vinkler for '{}'".format(type))
        plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))
        plt.savefig('{path}/gjetetid_{t}.png'.format(path=dir_path, t=type), bbox_inches='tight')
        plt.close()

def avg_time_our(dir_path, df_com, df_polygon):
    """Bar chart for herd time"""
    df_com_success = df_com.loc[df_com['Suksessrate'] == 100]
    df_avg_time_com = df_com_success.groupby(['Testtype', 'Vinkel'], as_index=False).aggregate({'Gjetetid':'mean', 'Oppsamlingstid':'mean', 'Drivetid':'mean'}).round(2)
    df_avg_time_com_index = df_avg_time_com.copy()
    df_avg_time_com_index.set_index('Testtype', inplace=True, drop=True)

    df_polygon_success = df_polygon.loc[df_polygon['Suksessrate'] == 100]
    df_avg_time_polygon = df_polygon_success.groupby(['Testtype', 'Vinkel'], as_index=False).aggregate({'Gjetetid':'mean', 'Oppsamlingstid':'mean', 'Drivetid':'mean'}).round(2)
    df_avg_time_polygon_index = df_avg_time_polygon.copy()
    df_avg_time_polygon_index.set_index('Testtype', inplace=True, drop=True)

    for type in TESTTYPES:
        fig_time, ax_time = plt.subplots()

        polygon_time = []
        polygon_collect_time = []
        polygon_herd_time = [] 
        com_time = []
        com_collect_time = []
        com_herd_time = []

        N = len(ANGLES)
        ind = np.arange(N)
        width = 0.20

        for a in ANGLES:
            for drone in OUR_DRONETYPES:   
                if drone == "v_polygon":
                    if ((df_avg_time_polygon['Testtype'] == type) & (df_avg_time_polygon['Vinkel'] == a)).any():
                        p_row = df_avg_time_polygon.loc[(df_avg_time_polygon['Testtype'] == type) & (df_avg_time_polygon['Vinkel'] == a)]
                        polygon_time.append(p_row['Gjetetid'].iloc[0])
                        polygon_collect_time.append(p_row['Oppsamlingstid'].iloc[0])
                        polygon_herd_time.append(p_row['Drivetid'].iloc[0])
                    else:
                        polygon_time.append(0)
                        polygon_collect_time.append(0)
                        polygon_herd_time.append(0)
                    
                if drone == "com":
                    if ((df_avg_time_com['Testtype'] == type) & (df_avg_time_com['Vinkel'] == a)).any():
                        f_row = df_avg_time_com.loc[(df_avg_time_com['Testtype'] == type) & (df_avg_time_com['Vinkel'] == a)]
                        com_time.append(f_row['Gjetetid'].iloc[0])
                        com_collect_time.append(f_row['Oppsamlingstid'].iloc[0])
                        com_herd_time.append(f_row['Drivetid'].iloc[0])
                    else:
                        com_time.append(0)
                        com_collect_time.append(0)
                        com_herd_time.append(0)

        com_collect = ax_time.bar(ind-0.1, com_collect_time, width, label='Massesenter: samletid = {}'.format(com_collect_time), color='lightcoral')
        com_herd = ax_time.bar(ind-0.1, com_herd_time, width, bottom=com_collect_time, label='Massesenter: drivetid = {}'.format(com_herd_time), color='crimson')

        polygon_collect = ax_time.bar(ind+0.1, polygon_collect_time, width, label='Polygon: samletid = {}'.format(polygon_collect_time), color='skyblue')
        polygon_herd = ax_time.bar(ind+0.1, polygon_herd_time, width, bottom=polygon_collect_time, label='Polygon: drivetid = {}'.format(polygon_herd_time), color='cornflowerblue')

        ax_time.bar_label(com_herd, com_time, rotation=90, padding=5)
        ax_time.bar_label(polygon_herd, polygon_time, rotation=90, padding=5)

        ax_time.margins(y=0.2)

        ax_time.set_xlabel('Vinkel i grader')
        ax_time.set_ylabel('Gjennomsnittlig gjetetid')
        ax_time.set_xticks(ind)
        ax_time.set_xticklabels(ANGLES)

        ax_time.set_title('Gjennomsnittlig gjetetid per vinkel per testtype')
        ax_time.legend(loc='center left', bbox_to_anchor=(1, 0.5))

        fig_time.savefig("{path}/gjetetid_{t}_vinkel.png".format(path=dir_path, t=type), bbox_inches='tight')
        plt.close(fig_time)


def successrate_our(dir_path, df_com, df_polygon):
    """Bar chart for successful and unsuccessful herding for all drone algorithms and every testtype"""
    for type in TESTTYPES:  
        f_success = 0
        f_failure = 0
        polygon_success = 0
        polygon_failure = 0

        N = len(ANGLES)
        ind = np.arange(N)
        width = 0.20      

        # Find successful and unsuccessful herding for com algorithm per test
        com_testtype = df_com.loc[(df_com['Testtype'] == type)]
        com_testtype['Suksess'] = np.where(com_testtype['Suksessrate'] == 100, 1, 0)
        com_testtype['Failure'] = np.where(com_testtype['Suksessrate'] != 100, -1, 0)
        com_testtype = com_testtype.groupby(['Testtype', 'Vinkel'], as_index=False).aggregate({'Suksess': 'sum', 'Failure':'sum'})

        f_success = com_testtype['Suksess']
        f_failure = com_testtype['Failure']

        polygon_testtype = df_polygon.loc[(df_polygon['Testtype'] == type)]
        polygon_testtype['Suksess'] = np.where(polygon_testtype['Suksessrate'] == 100, 1, 0)
        polygon_testtype['Failure'] = np.where(polygon_testtype['Suksessrate'] != 100, -1, 0)
        polygon_testtype = polygon_testtype.groupby(['Testtype', 'Vinkel'], as_index=False).aggregate({'Suksess': 'sum', 'Failure':'sum'})

        polygon_success = polygon_testtype['Suksess']
        polygon_failure = polygon_testtype['Failure']
            
        # Make figure
        fig, ax = plt.subplots()

        com_1 = ax.bar(ind-0.1, f_success, width, label='Massesenter: suksess', color='lightcoral')
        com_2 = ax.bar(ind-0.1, f_failure, width, label='Massesenter: mislykket', color='crimson')

        polygon_1 = ax.bar(ind+0.1, polygon_success, width, label='Polygon: suksess', color='skyblue')
        polygon_2 = ax.bar(ind+0.1, polygon_failure, width, label='Polygon: mislykket', color='cornflowerblue')


        ax.bar_label(com_1, padding=2)
        ax.bar_label(com_2, padding=2)
        ax.bar_label(polygon_1, padding=2)
        ax.bar_label(polygon_2, padding=2)

        ax.axhline(0, color='grey', linewidth=0.8)
        ax.set_xlabel('Vinkler')
        ax.set_ylabel('Antall Simuleringer')
        ax.set_xticks(ind)
        ax.set_xticklabels(ANGLES)

        ax.set_title('Antall simuleringer som er suksess og mislykket')
        ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))

        fig.savefig("{path}/suksessrate_{p}.png".format(path=dir_path, p=type), bbox_inches='tight')
        plt.close(fig)


def main():
    dir_path = "./final"

    for perception in PERCEPTIONS:
        df_circle = pd.read_csv('{path}/circle_{p}.csv'.format(path=dir_path, p=perception))
        df_v = pd.read_csv('{path}/v_{p}.csv'.format(path=dir_path, p=perception))
        df_polygon = pd.read_csv('{path}/polygon_{p}.csv'.format(path=dir_path, p=perception))
        df_our = pd.read_csv('{path}/our_{p}.csv'.format(path=dir_path, p=perception))

        # average_time_existing(dir_path, df_circle, df_v, df_polygon, perception)
        # succsessrate_existing(dir_path, df_circle, df_v, df_polygon, perception)
        average_time_all(dir_path, df_circle, df_v, df_polygon, df_our, perception)
        successrate_all(dir_path, df_circle, df_v, df_polygon, df_our, perception)
    
    df_com = pd.read_csv('{}/com.csv'.format(dir_path))
    df_v_polygon = pd.read_csv('{}/v_polygon.csv'.format(dir_path))
    avg_time_our(dir_path, df_com, df_v_polygon)
    successrate_our(dir_path, df_com, df_v_polygon)
    lineplot_our(dir_path, df_com, df_v_polygon)

if __name__ == "__main__":
    main()
    
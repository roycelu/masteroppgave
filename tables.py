import os
import numpy as np
import pandas as pd
from scipy import stats
from constants import *

DRONENAMES = {'our': 'Massesenter', 'polygon': 'Polygon', 'circle': 'Sirkel', 'v': 'V'}
DRONENAMES_OUR = {'com': 'Massesenter', 'v_polygon': 'V-polygon'}
BEST_ANGLE = 20


def create_csv_angle(test, dronetypes, perception, testtypes = TESTTYPES, angles = ANGLES):
    file_columns = ["Testtype","Vinkel","Gjetetid","Suksessrate","Oppsamlingstid","Drivetid"]

    for testtype in testtypes:
        # Create a new table
        columns = [file_columns[0], "Dronetype", file_columns[1], file_columns[3], "Gjennomsnitt", "Standardavvik"]
        df = pd.DataFrame(columns=columns[1:]) # OBS! 'Testtype' no longer in use

        for drone in dronetypes:
            # Read from CSV file for a drone
            df_results = pd.read_csv("{path}/{d}_{p}.csv".format(path=OUR_RESULTS_PATH, d=drone, p=perception))

            for angle in angles:           
                # Retrieve the correct column by conditions from the CSV file
                data = df_results[(df_results[file_columns[0]] == testtype) & (df_results[file_columns[1]] == angle)]
                
                # Calculate the values
                success = len(data[data[file_columns[3]] == 100])

                # Calculate only herd time with 100% success
                data = data[(data[file_columns[3]] == 100)]
                average = data[file_columns[2]].mean().round(2)
                std = data[file_columns[2]].std().round(2)
                
                # Add the values to the table
                df.loc[len(df), df.columns] = DRONENAMES_OUR[drone], angle, success, average, std

        # Save the dataframe as a CSV file
        filename = "{}/tables/{}_{}{}.csv".format(OUR_RESULTS_PATH, test, testtype, perception)
        df.to_csv(filename, index=False)


def create_csv(test, dronetypes, perceptions = PERCEPTIONS, testtypes = TESTTYPES):
    file_columns = ["Testtype","Gjetetid","Suksessrate","Oppsamlingstid","Drivetid"]

    for testtype in testtypes:
        # Create a new table
        columns = [file_columns[0], "Dronetype", "Synsrekkevidde", file_columns[2], "Gjennomsnitt", "Standardavvik"]
        df = pd.DataFrame(columns=columns[1:]) # OBS! 'Testtype' no longer in use

        for drone in dronetypes:
            for perception in perceptions:
                # Read from CSV file for a drone and a perception
                if drone == 'our':
                    df_results = pd.read_csv("{path}/{d}_{p}_{a}.csv".format(path=RESULTS_PATH, d=drone, p=perception, a=BEST_ANGLE))
                else:
                    df_results = pd.read_csv("{path}/{d}_{p}.csv".format(path=RESULTS_PATH, d=drone, p=perception))

                # Retrieve the correct column by conditions from the CSV file
                data = df_results[(df_results[file_columns[0]] == testtype)]
                success = len(data[data[file_columns[2]] == 100])

                # Calculate only herd time with 100% success
                data = data[(data[file_columns[2]] == 100)]
                average = round(data[file_columns[1]].mean(), 2)
                std = round(data[file_columns[1]].std(), 2)
                
                # Add the values to the table
                df.loc[len(df), df.columns] = DRONENAMES[drone], perception, success, average, std
            
        # Save the dataframe as a CSV file
        filename = "{}/tables/{}_{}.csv".format(RESULTS_PATH, test, testtype)
        df.to_csv(filename, index=False)

def p_value(path):
    columns = ['Testtype', 'Dronetype', 'Synsrekkevidde', 'P-verdi']
    df = pd.DataFrame(columns=columns)

    for testtype in TESTTYPES:
        df_results = pd.read_csv(path + '/all_{}.csv'.format(testtype))
        for drone in DRONETYPES[1:]:
            for perception in PERCEPTIONS:
                # Find average and standard deviation for our method
                our_data = df_results[(df_results['Dronetype'] == DRONENAMES[DRONETYPES[0]])]
                our_data = our_data[(our_data['Synsrekkevidde'] == perception)]
                our_mean = our_data['Gjennomsnitt'].to_numpy()[0]
                our_std = our_data['Standardavvik'].to_numpy()[0]

                # Find average and standard deviation for the other metods
                data = df_results[(df_results['Dronetype'] == DRONENAMES[drone])]
                data = data[(data['Synsrekkevidde'] == perception)]
                mean = data['Gjennomsnitt'].to_numpy()[0]
                std = data['Standardavvik'].to_numpy()[0]

                # Only calculate p-value if the value is not NAN
                if not np.isnan(mean) and not np.isnan(std):
                    stat, p_value = stats.ttest_ind_from_stats(our_mean, our_std, NO_SIMULATIONS, mean, std, NO_SIMULATIONS)
                    # Add the table row to a CSV file
                    df.loc[len(df), df.columns] = TESTTYPES_NAME[TESTTYPES.index(testtype)], DRONENAMES[drone], perception, round(p_value, 4)
    
    # Save the dataframe as a CSV file
    filename = "{}/p-value.csv".format(path)
    df.to_csv(filename, index=False)


def main():
    # Make sure that the folders exist
    path = RESULTS_PATH + '/tables'
    if not os.path.exists(path):
        os.mkdir(path)

    path_our = OUR_RESULTS_PATH + '/tables'
    if not os.path.exists(path_our):
        os.mkdir(path_our)

    # Create tables for the different methods

    # Existing methods
    create_csv("existing", DRONETYPES[1:])

    # Our methods
    for perception in PERCEPTIONS:
        create_csv_angle("our", OUR_DRONETYPES, perception)

    # All methods
    create_csv("all", DRONETYPES)
    p_value(path)

if __name__ == "__main__":
    main()

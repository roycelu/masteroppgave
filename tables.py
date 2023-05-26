import os
import numpy as np
import pandas as pd
import scipy
from constants import *

PATH = "./final"
DRONENAMES = {'our': 'Massesenter', 'polygon': 'Polygon', 'circle': 'Sirkel', 'v': 'V'}
DRONENAMES_OUR = {'com': 'Massesenter', 'v_polygon': 'V-polygon'}
PERCEPTION = 20
ANGLE = 20


def create_csv_angle(test, dronetypes, perception, testtypes = TESTTYPES, angles = ANGLES):
    for testtype in testtypes:
        for drone in dronetypes:

            # Read from CSV file for a drone
            df_results = pd.read_csv("{path}/{d}_{p}.csv".format(path=PATH, d=drone, p=perception))
            file_columns = ["Testtype","Vinkel","Gjetetid","Suksessrate","Oppsamlingstid","Drivetid"]

            # Create a new table
            columns = [file_columns[0], "Dronetype", file_columns[1], file_columns[3], "Gjennomsnitt", "Standardavvik"]
            df = pd.DataFrame(columns=columns[1:]) # OBS! 'Testtype' no longer in use
        
            for angle in angles:                
                # Retrieve the correct column by conditions from the CSV file
                data = df_results[(df_results[file_columns[0]] == testtype) & (df_results[file_columns[1]] == angle)]
                
                # Calculate the values
                success = len(data[data[file_columns[3]] == 100])

                # Calculate only herd time with 100% success
                data = data[(data[file_columns[3]] == 100)]
                average = data[file_columns[2]].mean().round(2)
                std = data[file_columns[2]].std().round(2)

                print(testtype, drone, angle, success, average, std)
                
                # Add the values to the table
                df = df.append({columns[1]: DRONENAMES_OUR[drone], columns[2]: angle, columns[3]: success, columns[4]: average, columns[5]: std}, ignore_index=True)

            # Append the table row to a CSV file
            filename = "{}/overview/{}_{}{}.csv".format(PATH, test, testtype, perception)
            df.to_csv(filename, mode='a', index=False, header=False  if os.path.isfile(filename) else True)


def create_csv(test, dronetypes, perceptions = PERCEPTIONS, testtypes = TESTTYPES):
    for testtype in testtypes:
        for drone in dronetypes:
            for perception in perceptions:
                # Read from CSV file for a drone and a perception
                if drone == 'our':
                    df_results = pd.read_csv("{path}/{d}_{p}_{a}.csv".format(path=PATH, d=drone, p=perception, a=ANGLE))
                else:
                    df_results = pd.read_csv("{path}/{d}_{p}.csv".format(path=PATH, d=drone, p=perception))

                file_columns = ["Testtype","Gjetetid","Suksessrate","Oppsamlingstid","Drivetid"]

                # Create a new table
                columns = [file_columns[0], "Dronetype", "Synsrekkevidde", file_columns[2], "Gjennomsnitt", "Standardavvik"]
                df = pd.DataFrame(columns=columns[1:]) # OBS! 'Testtype' no longer in use

                # Retrieve the correct column by conditions from the CSV file
                data = df_results[(df_results[file_columns[0]] == testtype)]
                success = len(data[data[file_columns[2]] == 100])

                # Calculate only herd time with 100% success
                data = data[(data[file_columns[2]] == 100)]
                average = round(data[file_columns[1]].mean(), 2)
                std = round(data[file_columns[1]].std(), 2)
                
                # Add the values to the table
                df = df.append({columns[1]: DRONENAMES[drone], columns[2]: perception, columns[3]: success, columns[4]: average, columns[5]: std}, ignore_index=True)
            
                # Append the table row to a CSV file
                filename = "{}/overview/{}_{}.csv".format(PATH, test, testtype)
                df.to_csv(filename, mode='a', index=False, header=False  if os.path.isfile(filename) else True)

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
                    stat, p_value = scipy.stats.ttest_ind_from_stats(our_mean, our_std, NO_SIMULATIONS, mean, std, NO_SIMULATIONS)
                    # Add the table row to a CSV file
                    df.loc[len(df), df.columns] = testtype, drone, perception, round(p_value, 4)
    filename = "{}/overview/p-value.csv".format(PATH)
    df.to_csv(filename, index=False)

def main():
    # NB! Remember to delete the CSV-files in the PATH before running the code!

    path = PATH + '/overview'
    if not os.path.exists(path):
        os.mkdir(path)

    # # Existing methods
    # create_csv("existing", DRONETYPES[1:])

    # # Our methods
    # create_csv_angle("our", OUR_DRONETYPES, PERCEPTION)

    # # All methods
    # create_csv("all", DRONETYPES)
    p_value(path)

if __name__ == "__main__":
    main()

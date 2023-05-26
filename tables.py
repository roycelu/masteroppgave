import os
import pandas as pd
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


def main():
    # NB! Remember to delete the CSV-files in the PATH before running the code!

    path = PATH + '/overview'
    if not os.path.exists(path):
        os.mkdir(path)

    # Existing methods
    create_csv("existing", DRONETYPES[1:])

    # # Our methods
    # create_csv_angle("our", OUR_DRONETYPES, PERCEPTION)

    # # All methods
    # create_csv("all", DRONETYPES)

if __name__ == "__main__":
    main()

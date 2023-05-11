import os
import pandas as pd

PATH = "./results"
DRONETYPES = ['our', 'circle', 'v', 'polygon', 'com', 'v_polygon',]
TESTTYPES = ["cooperative_flock", "divided_flock", "lone_sheep", "right_angle"]
ANGLES = [10, 15, 20, 25, 30]
PERCEPTIONS = [20, 30, 40]


def create_csv_angle(test, dronetypes = DRONETYPES, testtypes = TESTTYPES, angles = ANGLES):
    for testtype in testtypes:
        for drone in dronetypes:

            # Read from CSV file for a drone
            df_results = pd.read_csv("{path}/{d}.csv".format(path=PATH, d=drone))
            file_columns = ["Testtype","Vinkel","Gjetetid","Suksessrate","Oppsamlingstid","Drivetid"]

            # Create a new table
            columns = [file_columns[0], "Dronetype", file_columns[1], file_columns[2], "Gjennomsnitt", "Standardavvik"]
            df = pd.DataFrame(columns=columns[1:]) # OBS! 'Testtype' no longer in use
        
            for angle in angles:                
                # Retrieve the correct column by conditions from the CSV file
                data = df_results[(df_results[file_columns[0]] == testtype) & (df_results[file_columns[1]] == angle)]
                
                # Calculate the values
                success = data[file_columns[3]].mean().round(2)

                # Calculate only herd time with 100% success
                data = data[(data[file_columns[2]] == 100)]
                average = round(data[file_columns[2]].mean(), 2)
                std = round(data[file_columns[2]].std(), 2)
                
                # Add the values to the table
                df = df.append({columns[1]: drone, columns[2]: angle, columns[3]: success, columns[4]: average, columns[5]: std}, ignore_index=True)

                # Append the table row to a CSV file
                filename = "{}/overview/{}_{}.csv".format(PATH, test, testtype)
                df.to_csv(filename, mode='a', index=False, header=False  if os.path.isfile(filename) else True)


def create_csv(test, dronetypes = DRONETYPES, perceptions = PERCEPTIONS, testtypes = TESTTYPES, ):
    for testtype in testtypes:
        for drone in dronetypes:
            for perception in perceptions:
                # Read from CSV file for a drone and a perception
                df_results = pd.read_csv("{path}/{d}_{p}.csv".format(path=PATH, d=drone, p=perception))
                file_columns = ["Testtype","Gjetetid","Suksessrate","Oppsamlingstid","Drivetid"]

                # Create a new table
                columns = [file_columns[0], "Dronetype", "Synsrekkevidde", file_columns[2], "Gjennomsnitt", "Standardavvik"]
                df = pd.DataFrame(columns=columns[1:]) # OBS! 'Testtype' no longer in use

                # Retrieve the correct column by conditions from the CSV file
                data = df_results[(df_results[file_columns[0]] == testtype)]
                success = round(data[file_columns[2]].mean(), 2)#.round(2)

                # Calculate only herd time with 100% success
                data = data[(data[file_columns[2]] == 100)]
                average = round(data[file_columns[1]].mean(), 2)
                std = round(data[file_columns[1]].std(), 2)
                
                # Add the values to the table
                df = df.append({columns[1]: drone, columns[2]: perception, columns[3]: success, columns[4]: average, columns[5]: std}, ignore_index=True)
            
                # Append the table row to a CSV file
                filename = "{}/overview/{}_{}.csv".format(PATH, test, testtype)
                df.to_csv(filename, mode='a', index=False, header=False  if os.path.isfile(filename) else True)


def main():
    # OBS! Husk å slette CSV-filene i PATH før man kjører koden!

    # Existing methods
    path = "./results"
    create_csv("existing", path, DRONETYPES[1:3+1])

    # # Our methods
    # path = "" # TODO
    # create_csv_angle("our", path, DRONETYPES[4:])

    # All methods
    path = "./results"
    create_csv("all", path, DRONETYPES[:3+1])

if __name__ == "__main__":
    main()

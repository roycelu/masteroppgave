import pandas as pd
import numpy as np
import pygame
from shared_main import SharedMain


NO_SHEEP = 3
NO_DRONES = 5
FPS = 100

def test(id, no_sheep, no_drones, FPS, dronetype):
    sim = SharedMain(id, no_sheep, no_drones, FPS, dronetype)
    successrate, herdtime = sim.main()
    return successrate, herdtime
    
def get_sheep_list(testtype):
    position_list = [x for x in range(NO_SHEEP)]
    
    if testtype == "cooperative_flock":
        for i in position_list:
            x = np.random.randint(400, 420)
            y = np.random.randint(200, 220)
            position_list[i] = pygame.Vector2(x, y) 
    
    if testtype == "lone_sheep":
        for i in position_list-1:
            x = np.random.randint(400, 420)
            y = np.random.randint(200, 220)
            position_list[i] = pygame.Vector2(x, y) 
        
        x = np.random.randint(100, 900)
        y = np.random.randint(100, 900)
        position_list[-1] = pygame.Vector2(x, y)
    
    if testtype == "divided_flock":
        # dele på to, ikke sikker på om i blir riktig nå
        middle_index = len(position_list)//2
        for i in position_list[:middle_index]:
            x = np.random.randint(400, 420)
            y = np.random.randint(200, 220)
            position_list[i] = pygame.Vector2(x, y) 
        for i in position_list[middle_index:]:
            x = np.random.randint(100, 900)
            y = np.random.randint(100, 900)
            position_list[i] = pygame.Vector2(x, y)

    if testtype == "right_angle":
        return

    return position_list


def main():
    df = pd.DataFrame(columns = ['id', 'Testtype', 'Successrate (%)', 'Herdtime (s)'])
    testtype = [] # list of tests; 1: cooperative sheep, one sheep takes off, divided flock, turn flock 90 degrees (må endre i shared main)
    for test in testtype:
        for id in range(50):
            successrate, herdtime = test(id, NO_SHEEP, NO_DRONES, FPS*NO_DRONES, "circle")
            df = df.append({'id' : id, 'Testtype': testtype, 'Successrate (%)' : successrate, 'Herdtime (s)' : herdtime}, ignore_index = True)

    #df_grouped1 = df.groupby(['no_drones', 'K_f4'], as_index=False).aggregate({'Successrate (%)': 'mean'})
    #df_pivoted1 = df_grouped1.pivot(index='K_f4', columns='no_drones', values='Successrate (%)')
    
    #fig = df_pivoted1.plot(xticks=df_pivoted1.index, title='Suksessrate', ylabel="Successrate", xlabel="K_f4", style=".-").get_figure()
    #fig.savefig('successrate.pdf')
                
    #df_grouped2 = df.groupby(['no_drones', 'K_f4'], as_index=False).aggregate({'Herdtime (s)': 'mean'})
    #df_pivoted2 = df_grouped2.pivot(index='K_f4', columns='no_drones', values='Herdtime (s)')
   
    #fig = df_pivoted2.plot(xticks=df_pivoted2.index, title='Gjetetid', ylabel="Herdtime (s)", xlabel="K_f4", style=".-").get_figure()
    #fig.savefig('herdrate.pdf')

    df.to_csv('test.csv', index=False)


    

if __name__ == "__main__":
    main()
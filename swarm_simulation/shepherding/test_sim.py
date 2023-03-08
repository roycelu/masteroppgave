import pandas as pd
import numpy as np
import pygame
from shared_main import SharedMain


NO_SHEEP = 5
NO_DRONES = 3
FPS = 50
TESTTYPE = ["cooperative_flock", "lone_sheep", "divided_flock", "right_angle"]

def test(id, no_sheep, no_drones, FPS, dronetype, test):
    sheep_positions = get_sheep_list(test, no_sheep)
    sim = SharedMain(id, sheep_positions, no_drones, FPS, dronetype)
    successrate, herdtime = sim.main()
    return successrate, herdtime
    
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
        # dele på to, ikke sikker på om i blir riktig nå
        middle_index = len(position_list)//2
        for i in position_list[:middle_index]:
            x = np.random.randint(400, 420)
            y = np.random.randint(200, 220)
            position_list[i] = pygame.Vector2(x, y) 
        for i in position_list[middle_index:]:
            x = np.random.randint(200, 220)
            y = np.random.randint(400, 420)
            position_list[i] = pygame.Vector2(x, y)

    #f testtype == "right_angle":
    #    return

    return position_list


def main():
    df = pd.DataFrame(columns = ['id', 'Testtype', 'Successrate (%)', 'Herdtime (s)'])
    for testtype in TESTTYPE:
        for id in range(3):
            successrate, herdtime = test(id, NO_SHEEP, NO_DRONES, FPS*NO_DRONES, "circle", testtype)
            df = df.append({'id' : id, 'Testtype': TESTTYPE, 'Successrate (%)' : successrate, 'Herdtime (s)' : herdtime}, ignore_index = True)

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
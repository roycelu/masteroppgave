import pandas as pd
from shared_main import SharedMain


NO_SHEEP = 20
FPS = 100

def test(id, no_sheep, no_drones, FPS, dronetype):
    sim = SharedMain(id, no_sheep, no_drones, FPS, dronetype)
    successrate, herdtime = sim.main()
    return successrate, herdtime
    

def main():
    df = pd.DataFrame(columns = ['id', 'no_drones', 'K_f4', 'Successrate (%)', 'Herdtime (s)'])
    no_drones = 15
    for drones in range(no_drones, 20):
        for kf4 in range(1000,8000,1000):
            for id in range(100):
                successrate, herdtime = test(id, NO_SHEEP, drones, FPS*(no_drones), "circle")
                df = df.append({'id' : id, 'no_drones' : drones, 'K_f4': kf4, 'Successrate (%)' : successrate, 'Herdtime (s)' : herdtime}, ignore_index = True)

    df_grouped1 = df.groupby(['no_drones', 'K_f4'], as_index=False).aggregate({'Successrate (%)': 'mean'})
    df_pivoted1 = df_grouped1.pivot(index='K_f4', columns='no_drones', values='Successrate (%)')

    
    fig = df_pivoted1.plot(xticks=df_pivoted1.index, title='Suksessrate', ylabel="Successrate", xlabel="K_f4", style=".-").get_figure()
    fig.savefig('successrate.pdf')
                
    df_grouped2 = df.groupby(['no_drones', 'K_f4'], as_index=False).aggregate({'Herdtime (s)': 'mean'})
    df_pivoted2 = df_grouped2.pivot(index='K_f4', columns='no_drones', values='Herdtime (s)')

    
    fig = df_pivoted2.plot(xticks=df_pivoted2.index, title='Gjetetid', ylabel="Herdtime (s)", xlabel="K_f4", style=".-").get_figure()
    fig.savefig('herdrate.pdf')

    df.to_csv('test.csv', index=False)


    

if __name__ == "__main__":
    main()
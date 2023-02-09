import pandas as pd
from circle_main import CircleMain

NO_SHEEP = 5
NO_DRONES = 3
FPS = 200

def test_circle(id, no_sheep, no_drones, FPS):
    circle_sim = CircleMain(id, no_sheep, no_drones, FPS)
    successrate, herdtime = circle_sim.main()
    return successrate, herdtime
    

def main():
    df = pd.DataFrame(columns = ['id', 'Successrate (%)', 'Herdtime (s)'])

    for id in range(4):
        successrate, herdtime = test_circle(id, NO_SHEEP, NO_DRONES, FPS)
        df = df.append({'id' : id, 'Successrate (%)' : successrate, 'Herdtime (s)' : herdtime}, ignore_index = True)

    df.to_csv('test.csv', index=False)


if __name__ == "__main__":
    main()
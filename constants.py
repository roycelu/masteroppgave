# DRONES
SIZE = 10
MAX_SPEED = 1.9
MAX_SPEED_SHEEP = 0.2
DESIRED_SEPARATION_SHEEP = 20
PERCEPTION = 100

# FOLDER PATHS
RESULTS_PATH = 'sim_results/2023-05-23 15:02:18.557143'
OUR_RESULTS_PATH = './our_sim_results/2023-05-23 15:08:48.771652'

# SIMULATIONS
NO_SHEEP = 5 # Amount of sheep
NO_DRONES = 3 # Amount of drones
NO_SIMULATIONS = 100
TIME_LIMIT = 70 # Time limit of simulation, seconds

TARGET_FPS = 100 # Ønsket hastighet på simuleringen
FPS = 30

OUR_DRONETYPES = ['com', 'v_polygon']
DRONETYPES = ['our', 'polygon', 'circle', 'v']
TESTTYPES =  ["cooperative_flock", "divided_flock", "lone_sheep", "right_angle"]
TESTTYPES_NAME = ["Kooperativ flokk", "Delt flokk", "Enslig sau", "Nytt mål"]
ANGLES = [10, 15, 20, 25, 30]
PERCEPTIONS = [20, 30, 40]
CAPTURE_TIMES = [x for x in range(0, TIME_LIMIT, 2)] # When to capture screenshots of simulations
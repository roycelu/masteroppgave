# DRONES
SIZE = 10
MAX_SPEED = 19
MAX_SPEED_SHEEP = 2
DESIRED_SEPARATION_SHEEP = 20
PERCEPTION = 100


# SIMULATIONS
NO_SHEEP = 5 # Amount of sheep
NO_DRONES = 3 # Amount of drones
NO_SIMULATIONS = 100
TIME_LIMIT = 70 # Time limit of simulation, seconds

TARGET_FPS = 10 # Ønsket hastighet på simuleringen
FPS = 30

OUR_DRONETYPES = ['com', 'v_polygon']
DRONETYPES = ['our', 'polygon', 'circle', 'v']
TESTTYPES =  ["cooperative_flock", "divided_flock", "lone_sheep", "right_angle"]
ANGLES = [10, 15, 20, 25, 30]
PERCEPTIONS = [20, 30, 40]
CAPTURE_TIMES = [x for x in range(0, TIME_LIMIT, 2)] # When to capture screenshots of simulations
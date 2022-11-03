import tkinter
import numpy as np
import random

from sheep import Sheep
from drone import Drone
from main_drone import MainDrone
from drones_path import DronesPath


def initialise_canvas(window, screen_size):
    canvas = tkinter.Canvas(window, width=screen_size, height=screen_size)
    canvas.pack()
    window.resizable(False, False)
    return canvas


def create_sheep(no_of_sheep):
    list_of_sheep = [None for _ in range(no_of_sheep)]
    for n in range(no_of_sheep):
        initial_position = np.zeros(2, dtype=np.int32)
        initial_position[0] = np.random.randint(250, 350) #x-coordinate
        initial_position[1] = np.random.randint(250, 350) #y-coordinate 
        list_of_sheep[n] = Sheep(initial_position, 'boid'+str(n))
    return list_of_sheep 

def sheep_behaviours(canvas, list_of_sheep, list_of_drones):
    for sheep in list_of_sheep:
        sheep.main_sheep(list_of_sheep, canvas, list_of_drones)
    canvas.after(100, sheep_behaviours, canvas, list_of_sheep, list_of_drones)


def create_main_drone(drone_path):
    main_drone = MainDrone('main_drone', drone_path)
    return main_drone

def main_drone_behaviour(canvas, main_drone, list_of_sheep, list_of_drones):
    main_drone.main(list_of_sheep, canvas, list_of_drones)
    canvas.after(100, main_drone_behaviour, canvas, main_drone, list_of_sheep, list_of_drones)


def create_drones(no_of_drones):
    list_of_drones = [None for _ in range(no_of_drones)]
    for n in range(no_of_drones):
        initial_position = np.zeros(2, dtype=np.int32)
        if n == 0:
            initial_position[0] = 0
            initial_position[1] = 0 
            list_of_drones[n] = Drone(initial_position, 'drone'+str(n))
        if n == 1:
            initial_position[0] = 0
            initial_position[1] = 40 
            list_of_drones[n] = Drone(initial_position, 'drone'+str(n))
        if n == 2:
            initial_position[0] = 40
            initial_position[1] = 0 
            list_of_drones[n] = Drone(initial_position, 'drone'+str(n))
    return list_of_drones

def drone_behaviours(canvas, list_of_drones, list_of_sheep):
    step_size = 5
    desired_position = np.zeros(2, dtype=np.int32)
    desired_position[0] = 800
    desired_position[1] = 800
    for drone in list_of_drones:
        #drone.fly_to_position(desired_position, step_size)
        drone.main_drone(list_of_drones, canvas, list_of_sheep)
    canvas.after(100, drone_behaviours, canvas, list_of_drones, list_of_sheep)


def create_drone_path():
    drone_path = DronesPath('path')
    return drone_path

def drone_path_behaviours(canvas, drone_path):
    points = []
    for i in range(4):
        points.append((random.randint(100, 500), random.randint(100, 500)))
    drone_path.draw_path(canvas, points)
    

def main():
    screen_size = 1000
    no_of_sheep = 5
    no_of_drones = 3
    
    
    window = tkinter.Tk()
    canvas = initialise_canvas(window, screen_size)
    
    list_of_sheep = create_sheep(no_of_sheep)
    drone_path = create_drone_path()
    drone_path_behaviours(canvas, drone_path)
    path = drone_path.get_path()
    main_drone = create_main_drone(path)
    list_of_drones = create_drones(no_of_drones)
    main_drone_behaviour(canvas, main_drone, list_of_sheep, list_of_drones)

    drone_behaviours(canvas, list_of_drones, list_of_sheep)
    sheep_behaviours(canvas, list_of_sheep, list_of_drones)
    
    window.mainloop()
    
    


main()
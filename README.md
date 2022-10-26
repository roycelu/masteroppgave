# prosjektoppgave

TDT4501 - Datateknologi, fordypningsprosjekt (høsten 2022)

## ROS2

ROS2 kode - [ros2_ws](./ros2_ws/)

### Nyttige ROS2 kommandoer

Build packages: `colcon build --packages-select drone_interfaces`

Source the environment, in order to use the executatbles or libraries (from colcon): `. install/local_setup.bash` (Linux). Remember to run the command before running scripts. Must run from the "ros2_ws"-folder.

#### Actions

- Request: pos (float32[]) - the position main drone want a drone to move to
- Response: final_pos (float32[]) - the final position of a drone
- Feedback: current_pos (float32[]) - the current position of a drone, a default start position is set.

Kjøre actionServer: `python3 drone_action_server.py` fra src-mappen

Kjøre actionClient: `python3 drone_action_client.py` fra src-mappen

For å teste at serveren funker: `ros2 action send_goal --feedback drone drone_interfaces/action/Drone "{pos: [3, 1]}"`

## Swarm simulation

<https://www.youtube.com/watch?v=44WMyzPyTd0>

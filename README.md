# prosjektoppgave

TDT4501 - Datateknologi, fordypningsprosjekt (høsten 2022)

## Nyttige ROS2 kommandoer

Build packages: `colcon build --packages-select drone_interfaces`

Source the setup file: `. install/local_setup.bash` (Linux)

### Actions

- Request: pos (float32[]) - the position main drone want a drone to go to
- Response: final_pos (float32[]) - the final position of a drone
- Feedback: current_pos (float32[]) - the current position of a drone

Kjøre actionServer: `python3 drone_action_server.py` fra src-mappen

Tester at serveren funker: `ros2 action send_goal --feedback drone drone_interfaces/action/Drone "{pos: [3, 1]}"`

## Mappestrukture

- ROS2 kode - [ros2_ws](./ros2_ws/)

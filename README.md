# prosjektoppgave
TDT4501 - Datateknologi, fordypningsprosjekt (høsten 2022)

## Nyttige ROS2 kommandoer

Build packages: `colcon build --packages-select <package name>`

Source the setup file: `. install/local_setup.bash` (Linux)

### Actions
Request: speed (float32), Response: final_position (float32[]), Feedback: current_position (float32[])

Kjøre actionServer: `python3 drone_action_server.py` fra src-mappen

Tester at serveren funker: `ros2 action send_goal --feedback drone drone_interfaces/action/Drone "{speed: 3.1}"`

## Mappestrukture
- ROS2 kode - [ros2_ws](./ros2_ws/)
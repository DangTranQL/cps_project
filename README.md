# cps_project
This is a multi-agent robotic system.
## RP-Lidar
In order to use RP-Lidar, first run `sudo vim .bashrc`

and find the [ROBOT_TYPE] parameter and modify it using `export  ROBOT_TYPE=X3`

First, run `roslaunch  yahboomcar_nav  laser_astrapro_bringup.launch`

Then, mapping command(robot side) `roslaunch  yahboomcar_nav  yahboomcar_map.launch  use_rviz:=false  map_type:=gmapping`

open the visual interface(virtual machine side) `roslaunch yahboomcar_nav view_map.launch`

@Todo: Save the opsition and scan QR code

Save the map `rosrun map_server map_saver -f ~/yahboomcar_ws/src/yahboomcar_nav/maps/my_map` or `bash ~/yahboomcar_ws/src/yahboomcar_nav/maps/map.sh`

The map will be saved to ~/yahboomcar_ws/src/yahboomcar_nav/maps/ folder, a pgm image, a yaml file

## Recording Position
New terminal:`roscore`

New terminal: `rosrun joy joy_node`

New terminal: `roslaunch  yahboomcar_nav  laser_astrapro_bringup.launch`

New terminal: `roslaunch  yahboomcar_nav  yahboomcar_map.launch  use_rviz:=false  map_type:=gmapping `

New terminal: `rosrun QR_Camera_Dist JoyCamOdom.py` after running `catkin_make` in ~/CPS_ws

Operater the Rosmaster X3 using the controller, and press A to record the current position and orientation. The data will be saved to  ~/QR_Dist_Camera/src.

# cps_project
## RP-Lidar
In order to use RP-Lidar, first run
`sudo vim .bashrc`
and find the [ROBOT_TYPE] parameter and modify it
`export  ROBOT_TYPE=X3    # ROBOT_TYPE: X1 X3 X3plus R2 X7`

First, run
`roslaunch  yahboomcar_nav  laser_astrapro_bringup.launch   # Astra + laser + yahboomcar`
Then, mapping command(robot side)
`roslaunch  yahboomcar_nav  yahboomcar_map.launch  use_rviz:=false  map_type:=gmapping`
open the visual interface(virtual machine side)
`roslaunch yahboomcar_nav view_map.launch`

@Todo: Save the opsition and scan QR code

Save the map
`rosrun map_server map_saver -f ~/yahboomcar_ws/src/yahboomcar_nav/maps/my_map` or `bash ~/yahboomcar_ws/src/yahboomcar_nav/maps/map.sh`

The map will be saved to ~/yahboomcar_ws/src/yahboomcar_nav/maps/ folder, a pgm image, a yaml file

## Recording Position
New terminal:`roscore`
New terminal: `rosrun joy joy_node`
New terminal: `roslaunch  yahboomcar_nav  laser_astrapro_bringup.launch`
New terminal: `roslaunch  yahboomcar_nav  yahboomcar_map.launch  use_rviz:=false  map_type:=gmapping `

New terminal: `rosrun QR_Dist_Camera JoyComOdom.py` after running `catkin_make` in ~/CPS_ws

Operater the Rosmaster X3 using the controller, and press A to record the current position and orientation.

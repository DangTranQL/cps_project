# cps_project
This is a multi-agent robotic system. The system consists of a Teleoperating Agent which is used to map the environment and locations of QR codes, and a Task Agent which is used to go the available QR code with highest priority.

## Phase One
In phase one, the user will control the Teleoperating Agent to map the environment, and record the locations of QR codes by pressing button A on the controller.

To run phase one, first go to the `root` directory and run `roslaunch launch/first_phase.launch`

Mark the initial location of the robot. The command will open gmap and the camera of the robot. Navigate the robot through the environment and go to each QR code, the ideal distance from the robot to each QR code should be around 15-20cm so that the robot won't label the QR code as an obstacle and tries to avoid it. When the camera has shown a clear image of the QR code and display its priority, press button A to save the priority and current location of the robot (as well as the QR code).

After scanning all QR codes, open a new terminal and run `rosrun map_server map_saver -f ~/CPS_ws/src/QR_Camera_Dist/maps/map_name` to store the map. Then terminate the launch of phase one.

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

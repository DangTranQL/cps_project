# cps_project
This is a multi-agent robotic system. The system consists of a Teleoperating Agent which is used to map the environment and locations of QR codes, and a Task Agent which is used to go the available QR code with highest priority.

## Phase One
In phase one, we will control the Teleoperating Agent to map the environment, and record the locations of QR codes by pressing button A on the controller.

To run phase one, first go to the `root` directory and run `roslaunch launch/first_phase.launch`

Mark the initial location of the robot. The command will open gmap and the camera of the robot. Navigate the robot through the environment and go to each QR code, the ideal distance from the robot to each QR code should be around 15-20cm so that the robot won't label the QR code as an obstacle and tries to avoid it. When the camera has shown a clear image of the QR code and display its priority, press button A to save the priority and current location of the robot (as well as the QR code) into `data.csv`. The file will have 8 columns, `priority`, `position_x`, `position_y`, `orientation_x`, `orientation_y`, `orientation_z`, `orientation_w`, `time`.g

After scanning all QR codes, open a new terminal and run `rosrun map_server map_saver -f ~/CPS_ws/src/QR_Camera_Dist/maps/map_name` to save the map. Then terminate the launch of phase one. Open `data.csv` to ensure that all QR codes are saved, there will be some duplicates in the file, but we will remove them in phase two.

## Phase Two
In phase two, the user will block whatever QR codes that 

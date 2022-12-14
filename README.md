# Path-guiding Multi-agent Robotic System
This is a multi-agent robotic system. The system consists of a Teleoperating Agent which is used to map the environment and locations of QR codes, and a Task Agent which is used to go the available QR code with highest priority.
<center><img src="./images/rosmasterx3.jpg" width="50%" /></center>

## Project Motivation & Scenarios
A parking lot hosting both electric and non-electric vechicles. There are electrical cars that autonomously navigate to their desired destination from their current locations. Commonly, vehicles are usually park into a parking lot. Additionally, electric vehicles would prefer to be park at a spot where there consist of a charging station. Therefore, creating a path guiding robot system to communicate the best spot towards the electric vehicle to park would help reduce the time complexity for the autonomous electric vehicle to find the optimal spot within the parking lot.

Scenarios Details:

    The non-electric vehicles are considered as virtual obstacles occupying parking spots. 

    Priority 1 is virtually simulated to be a parking spot consisting of nearby available charging electrical station.

    Priority 2 is virtually simulated to be a normal parking spot without any nearby available charging electrical station. 

    The path guiding robot will essentially guide the electric vehicle to the best spot consisting of priority 1, instead of priority 2 (Priority 1 > Priority 2)  

## Design Diagram
<center> <img src="./images/diagram.png" width="100%" /> </center>

## How to Compile?
### Editing source code
Within the ROS environment using Ubuntu, type <b>catkin_make</b> into the terminal within the root of the workspace is a required process to save and build a newly edited code to run the code

### Adding packages
In order to use packages within your ROS code, packages are required to include in the <b>CMakeLists.txt</b>, which is found within the root directory of the package file.

### Adding installation path
Prior to running the python file, the python file needs to be made as an executable with command line <b>"chmod +x (python_file_name)"</b>. Additionally, an installation path to the python file within the package file src directory is needed to be included into the <b>CMakeLists.txt</b>. 

### Summary on compiling
First edit the source code and make the python file as an executable, then add used packages and required installation path within the <i>CMakeLists.txt</i>. Once the prior step has complete, do <b>catkin_make</b> within the root of the entire workspace. Then, the python file can be run with the ros command "rosrun" or "roslaunch".

## How to Run?
### Phase One
In phase one, we will control the Teleoperating Agent to map the environment, and record the locations of QR codes by pressing button A on the controller.

To run phase one, first go to the `root` directory and run `roslaunch launch/first_phase.launch`

Mark the initial location of the robot. The command will open gmap and the camera of the robot. Navigate the robot through the environment and go to each QR code, the ideal distance from the robot to each QR code should be around 15-20cm so that the robot won't label the QR code as an obstacle and tries to avoid it. When the camera has shown a clear image of the QR code and display its priority, press button A to save the priority and current pose of the robot within the map (as well as the QR code) into `data.csv`. The file will have 8 columns: priority, position_x, position_y, orientation_x, orientation_y, orientation_z, orientation_w, time.

After scanning all QR codes, open a new terminal and run `rosrun map_server map_saver -f ~/CPS_ws/src/QR_Camera_Dist/maps/map_name` to save the map. Then terminate the launch of phase one. Open `data.csv` to ensure that all QR codes are saved, there will be some duplicates in the file, but we will remove them in phase two.

### Phase Two
In phase two, the Task Agent will go to the available QR code with highest priority.

To run phase two, first put the robot in the marked initial location (phase one initial location). Then go to the `root` directory and run `roslaunch launch/second_phase.launch map:=map_name`.

The command will open the map called "map_name". Then run `rosrun QR_Camera_Dist test_nav.py` to start phase two. This command will prompt us to input a list of QR codes that we want to block. Before enter the list, go to `test_data.csv` which is the list of QR codes with: priority, distance, position_x, position_y, orientation_x, orientation_y, orientation_z, orientation_w that we already remove the duplicates using pandas dataframe based on time, check the row number of each QR code. The QR codes are sorted in decreasing order of priority in which priority 1 is the highest, so all QR codes with priority 1 will be put on top, and in each priority, different QR codes are sorted in an increasing order of distance, down the list, to the initial location.

After enter the list of blocked QR codes, the robot will ignore the blocked QR codes and go to the first available QR code in `test_data.csv` file, then it will output `Goal Execution Done!` and stop.

## Main Software Artifacts Contributions

### JoyCamOdom.py
Packages:

    rospy               : ros functions in python

    csv                 : append informations into csv file

    message_filters     : approximate synchronization of multiple subscribe topics to be used in one callback function

    time                : remove duplicates through comparison

    std_msgs.msg        : receive string data

    nav_msgs.msg        : receive Odometry data

    sensors_msgs.msg    : receive Joy data

    rospy_tutorials.msg : receive HeaderString data
    

Within the <b>main</b> function, the node <i>CamJoyOdom</i> subscribe to three topics namely joy, odom, videos_frames (camera). To subscribe to these topic to use in one callback function, a package called message_filters and its imported function called ApproximateTimeSynchronizer are used. Before calling the callback function, a csv file, located within the current working directory, has opened to write priority, posx, posy, orix, oriy, oriz, oriw, time as categories into the file, to remove previous collections of old data and to be compatible with pandas dataframes function. 

Within the callback function called <b>buttonCallBack</b>, it receives data from subscribe topics to be used to essentially append the information about the pose of the robot and the priority about the parking location. When the button A on the controller has been pressed, it will open the same csv file to append the pose of the robot at each QR code locations into the csv file. Additionally, the controller will also append a time to essentially remove duplicates, consisting of the same informations of each QR code. 

### main.py
Packages:

    rospy                : ros functions in python

    rospy_tutorials.msg  : receive HeaderString data

    cv2                  : open camera and display image

    pyzbar               : read QR code or barcode

    numpy                : wrap QR code

<b>webcam()</b> fuction opens the camera through the path `/dev/video0`. When a QR code is detected, it will read the priority of the QR code, and publish the priority to the node <i>video_frames</i> as a HeaderString. In display we can see also see that the QR code is wrapped around by purple lines with its priority on top.

## test_nav.py
Packages:

    rospy               : ros functions in python

    csv                 : append informations into csv file

    queue               : data arrangement

    pandas              : remove duplicates

    math                : distance calculation

    move_base_msgs.msg  : commuicate with move_base node

    actionlib           : send base to target location

    geometry_msgs.msg   : receive pose

In <b>main</b> function, the system will prompt us to enter a string of QR codes that we want to block (i.e. 1 2 3).

To remove duplicates in `data.csv`, we read the file into pandas dataframe data, then use its sort_values and drop_duplicates functions to drop all duplicates based on time, and only keep the first value. To arrange the priorities, we use priority queue to put them in (priority, distance) order so that all QR codes with priority 1 are put on top, then next is priority 2. For QR codes with the same priority, we put them in increasing order of distance to initial location and append the queue into `test_data.csv` with priority, distance, posx, posy, orix, oriy, oriz, oriw. This way, the robot doesn't need to go through all values in `test_data.csv`, hence decreases time complexity.

Additionally, before to calling the function <b>movebase_client</b>, the <i>movebase_client_py</i> node will first publish its initial location to the initialpose topic to initialize the robot pose within a known map, obtained from phase one. For this current progress on the code, the initial pose of the robot must be the same for both the phases. 

Once the <b>movebase_client</b> has been called, it uses an actionlib.SimpleActionClient to essentially send the "goal" location request to a node called <i>move_base</i> to perform the task, where the robot will relocate its current location to the "goal" location. To send a request to the <i>move_base</i>, it uses a variable named "goal" to use the class called MoveBaseGoal to obtain all required information target_pose which consist of frame_id, stamp, positions, and orientations. These informations can be essentially obtained from the csv file `test_data.csv`.  

## Video Demo
[Link to video demo](https://drive.google.com/file/d/1WP3eAxKgsKSg2fDq-870fyxHzeAvRwC-/view?usp=sharing).
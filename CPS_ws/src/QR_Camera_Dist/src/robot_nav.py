#!/usr/bin/env python3
# encoding: utf-8

import rospy
import actionlib
import csv
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
from geometry_msgs.msg import *
from queue import PriorityQueue
import pandas as pd
import math
import cv2 as cv
from pyzbar.pyzbar import decode

def QRDetection(previous_time): # time => seconds
    image_cam = cv.VideoCapture('/dev/video0') # open astrapro camera
    image_cam.set(3,640)
    image_cam.set(4,480)

    print("Cmaer")
    rospy.loginfo("dskdmskdm")

    while not rospy.is_shutdown():
        ret, frame = image_cam.read()
        print(ret)
        rospy.loginfo("askjdnwiodwd")
        if ret:
            for barcode in decode(frame):
                mydata = barcode.data.decode('utf-8')
                print("POPOPOPOPOP")
                rospy.loginfo("PLPLPLPLP:")
                while rospy.Time.now().secs - previous_time <= 5: # while time is below 5 seconds
                    print(rospy.Time.now().secs - previous_time)
                    if mydata == '1' or mydata == '2':
                        break
                    else:
                        return "Parking Spot is Occupied"
            
             #   break # break out from for loop

            #break # break out from while loop

            cv.imshow("frame", frame)
            key=cv.waitKey(1)
            if key == ord('q'):
                break
        image_cam.release()
        cv.destroyAllWindows()

    # move into the available parking spot using "base_link" instead of "map"
    client = actionlib.SimpleActionClient('move_base', MoveBaseAction)
    client.wait_for_server()

    goal = MoveBaseGoal()
    goal.target_pose.header.frame_id = "base_link"
    goal.target_pose.header.stamp = rospy.Time.now()
    goal.target_pose.pose.position.x = 0.1          # move 0.5 meters ahead
    goal.target_pose.pose.orientation.w = 1.0   
    
    client.send_goal(goal)
    wait = client.wait_for_result()

    if not wait:
        rospy.logerr("Action server not available")
        rospy.signal_shutdown("Action server not available")
    else:
        return client.get_result()
    

def movebase_client(posx, posy, quadx, quady, quadz, quadw):
    client = actionlib.SimpleActionClient('move_base', MoveBaseAction)
    client.wait_for_server()

    goal = MoveBaseGoal()
    goal.target_pose.header.frame_id = "map"
    goal.target_pose.header.stamp = rospy.Time.now()
    goal.target_pose.pose.position.x = posx
    goal.target_pose.pose.position.y = posy
    goal.target_pose.pose.orientation.x = quadx
    goal.target_pose.pose.orientation.y = quady
    goal.target_pose.pose.orientation.z = quadz
    goal.target_pose.pose.orientation.w = quadw

    client.send_goal(goal)
    wait = client.wait_for_result()

    if not wait:
        rospy.logerr("Action server not available!")
        rospy.signal_shutdown("Action server not available!")
    else:
        return client.get_result()

#def initialpose_callback(msg):
 #   if not isinstance(msg, PoseWithCovarianceStamped): return
  #  pub_rtabinitPose.publish(msg)

if __name__ == "__main__":
    try:
        rospy.init_node("movebase_client_py")
    

        pub_init = rospy.Publisher("initialpose", PoseWithCovarianceStamped)
        p = PoseWithCovarianceStamped()
        msg = PoseWithCovariance()
        msg.pose = Pose(Point(0.0,0.0,0.0), Quaternion(0.00,0.00,0.00,1.0))
        p.pose = msg
        pub_init.publish(p)
       
       # pub_rtabinitPose = rospy.Publisher("rtabmap/initialpose", PoseWithCovarianceStamped, queue_size=10)
       # sub_initialpose = rospy.Subscriber("initialpose", PoseWithCovarianceStamped, initialpose_callback)

        q = PriorityQueue() 

        # Read csv file and remove duplicates
        data = pd.read_csv("/home/jetson/CPS_ws/src/QR_Camera_Dist/src/data.csv")
        data.sort_values('time', inplace=True)
        data.drop_duplicates(subset=('time'), keep='first', inplace=True)
        
        # Put in priority queue 
        for index, row in data.iterrows():
            if not math.isnan(float(row['time'])):
                q.put((int(row['priority']),float(row['posx']),float(row['posy']),float(row['orix']),float(row['oriy']),float(row['oriz']),float(row['oriw'])))

        # csv file to check priority queue
        f = open("/home/jetson/CPS_ws/src/QR_Camera_Dist/src/test_data.csv","w")
        # f.write('priority,posx,posy,orix,oriy,oriz,oriw\n')
        while not q.empty():
            pose = q.get()
            f.write(str(pose[0])+',')
            f.write(str(pose[1])+',')
            f.write(str(pose[2])+',')
            f.write(str(pose[3])+',')
            f.write(str(pose[4])+',')
            f.write(str(pose[5])+',')
            f.write(str(pose[6])+'\n')
        f.close()

        # START Navigation based on Priorities
        f = open("/home/jetson/CPS_ws/src/QR_Camera_Dist/src/test_data.csv","r")
        rows = csv.reader(f)
        for row in rows:
            # pose = q.get()
            # rospy.loginfo(pose)
            result = movebase_client(float(row[1]), float(row[2]), float(row[3]), float(row[4]), float(row[5]), float(row[6]))

            if result:
                previous_time = rospy.Time.now().secs
                rospy.loginfo("Goal execution done!")
                
#                image_cam = cv.VideoCapture(0)
#                image_cam.set(3,640)
#                image_cam.set(4,480)


                # scanning time
                strHolder = QRDetection(previous_time)
                rospy.loginfo(strHolder)

 #               while not rospy.is_shutdown():
  #                  image_cam.open()
   #                 ret,frame = image_cam.read() 
    #                print(ret)
     #               if ret == True:
      #                  for barcode in decode(frame):
       #                     mydata = barcode.data.decode('utf-8')

        #                    while rospy.Time.now().secs - previous_time <= 5:
         #                       if mydata == '1' or mydata == '2':
          #                          print("Hello")
           #                     else:
            #                        break
             #           cv.imshow("frame", frame)
             #           key = cv.waitKey(1)
             #           if key == ord('q'):
             #               break
             #   image_cam.release()
             #   cv.destroyAllWindows()

    except rospy.ROSInterruptException:
        rospy.loginfo("Navigation test finished")
    

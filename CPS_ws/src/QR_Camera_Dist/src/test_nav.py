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
import numpy

# def QRDetection(posx, posy, orix, oriy, oriz, oriw):
#     print('hello')
#     y = 2 * (oriw * oriz + orix * oriy)
#     x = 1 - 2 * (oriy * oriy + oriz * oriz)
#     yaw = numpy.arctan2(y, x)
#     angle = yaw * 180 / numpy.pi
#     # print(yaw)

#     # move into the available parking spot using "map"
#     client = actionlib.SimpleActionClient('move_base', MoveBaseAction)
#     client.wait_for_server()

#     goal = MoveBaseGoal()
#     goal.target_pose.header.frame_id = "map"
#     goal.target_pose.header.stamp = rospy.Time.now()
    
#     y = abs(0.1 * math.tan(yaw))
#     # print(y)
    
#     if angle > -90 and angle < 90:
#         goal.target_pose.pose.position.x = posx + 0.1
#         if angle < 0:
#             goal.target_pose.pose.position.y = posy - y
#         else:
#             goal.target_pose.pose.position.y = posy + y
#     else:
#         goal.target_pose.pose.position.x = posx - 0.1
#         if angle > 90 and angle < 180:
#             goal.target_pose.pose.position.y = posy + y
#         else:
#             goal.target_pose.pose.position.y = posy - y
            
#     # goal.target_pose.pose.position.x = posx - 0.1
#     # goal.target_pose.pose.position.y = posy + y
#     goal.target_pose.pose.orientation.z = oriz
#     goal.target_pose.pose.orientation.w = oriw
    
#     client.send_goal(goal)
#     wait = client.wait_for_result()

#     if not wait:
#         rospy.logerr("Action server not available")
#         rospy.signal_shutdown("Action server not available")
#     else:
#         return client.get_result()
    

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
        print('Codes that are blocked: ')
        blocked_code = list(input().split())
            
        rospy.init_node("movebase_client_py")
        pub_init = rospy.Publisher("initialpose", PoseWithCovarianceStamped, queue_size=20)
        p = PoseWithCovarianceStamped()
        msg = PoseWithCovariance()
        msg.pose = Pose(Point(0.0,0.0,0.0), Quaternion(0.00,0.00,0.00,1.0))
        p.pose = msg
        pub_init.publish(p)

        q = PriorityQueue() 

        # Read csv file and remove duplicates
        data = pd.read_csv("/home/jetson/CPS_ws/src/QR_Camera_Dist/src/data.csv")
        data.sort_values('time', inplace=True)
        data.drop_duplicates(subset=('time'), keep='first', inplace=True)
        
        # Put in priority queue 
        for index, row in data.iterrows():
            if not math.isnan(float(row['time'])):
                distance = math.sqrt(float(row[1])*float(row[1])+float(row[2])*float(row[2]))
                q.put((int(row['priority']),distance,float(row['posx']),float(row['posy']),float(row['orix']),float(row['oriy']),float(row['oriz']),float(row['oriw'])))

        # csv file to check priority queue
        count = 1
        f = open("/home/jetson/CPS_ws/src/QR_Camera_Dist/src/test_data.csv","w")
        while not q.empty():
            pose = q.get()
            f.write(str(pose[0])+',')
            f.write(str(pose[1])+',')
            f.write(str(pose[2])+',')
            f.write(str(pose[3])+',')
            f.write(str(pose[4])+',')
            f.write(str(pose[5])+',')
            f.write(str(pose[6])+',')
            f.write(str(pose[7])+'\n')
        f.close()

        # START Navigation based on Priorities
        f = open("/home/jetson/CPS_ws/src/QR_Camera_Dist/src/test_data.csv","r")
        rows = csv.reader(f)
        for row in rows:
            if not (str(count) in blocked_code):
                rospy.loginfo(row[0])
                result = movebase_client(float(row[2]), float(row[3]), float(row[4]), float(row[5]), float(row[6]), float(row[7]))

                if result:
                    rospy.loginfo("Goal execution done!")
                    break
            count = count + 1
    
                # QRDetection(float(row[2]), float(row[3]),float(row[4]), float(row[5]), float(row[6]),float(row[7]))

    except rospy.ROSInterruptException:
        rospy.loginfo("Navigation test finished")
    

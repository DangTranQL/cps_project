#!/usr/bin/env python3
# encoding: utf-8

import rospy
import actionlib
import csv
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
from geometry_msgs.msg import *
from rospy_tutorials.msg import HeaderString
from queue import PriorityQueue
import pandas as pd
import math
import cv2 as cv
from pyzbar.pyzbar import decode

class Cam:
    def __init__(self):
        rospy.on_shutdown(self.cancel)
        self.sub_cam = rospy.Subscriber('videos_frames', HeaderString, self.callBackPriority)
         
    def callBackPriority(self, cam_data):
        return int(self.cam_data)

def movebase(posx, posy, quadx, quady, quadz, quadw, frame_id):
    client = actionlib.SimpleActionClient('move_base', MoveBaseAction)
    client.wait_for_server()

    goal = MoveBaseGoal()
    goal.target_pose.header.frame_id = frame_id # needs to be input as string (map or base_link)
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

if __name__ == "__main__":
    try:
        subCam = Cam()
        print(subCam.callBackPriority)
        rospy.spin()
    except rospy.ROSInterruptException:
        rospy.loginfo("Failed")



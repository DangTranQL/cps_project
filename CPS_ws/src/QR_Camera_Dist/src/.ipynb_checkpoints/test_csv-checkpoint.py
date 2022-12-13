#!/usr/bin/env python
# encoding: utf-8

import rospy
from nav_msgs.msg import Odometry
import math
import numpy

def callback(data):
    siny_cosp = 2 * (data.pose.pose.orientation.w * data.pose.pose.orientation.z + data.pose.pose.orientation.x * data.pose.pose.orientation.y)
    cosy_cosp = 1 - 2 * (data.pose.pose.orientation.y * data.pose.pose.orientation.y + data.pose.pose.orientation.z * data.pose.pose.orientation.z)
    yaw = numpy.arctan2(siny_cosp, cosy_cosp)
    angle = yaw * 180 / numpy.pi
    rospy.loginfo(angle)

if __name__ == "__main__":
    
    rospy.init_node('angle', anonymous=True)
    rospy.Subscriber('/odom', Odometry, callback)
    rospy.spin()

#!/usr/bin/env python3

import rospy
from geometry_msgs.msg import *
import roslib; roslib.load_manifest('QR_Camera_Dist')
import csv

def gen_pose():
    pub = rospy.Publisher('initialpose', PoseWithCovarianceStamped)
    rospy.init_node('inital_pose', LOG_level=roslib.msg.Log.INFO)
    rospy.loginfo('Setting Pose')

    p = PoseWithCovarianceStamped()
    msg = PoseWithCovariance()
    msg.pose = Pose(Point(), Quaternion())
    msg.covariance = []
    p.pose = msg
    pub.publish(p)

def goal_dest():
    with open('data.csv', 'r') as f:
        csv_read = csv.reader()
    location = Pose(Point(), Quaternion())
    goal = MoveBaseGoal()
    goal.target_pose.pose = location
    goal.target_pose.header.frame_id = 'map'
    goal.target_pose.header.stamp = rospy.Time.now()

    move_base.send_goal(goal)

    time = move_base.wait_for_result(rospy.Duration(300))

if __name__ == '__main__':
    try:
        gen_pose()
        rospy.loginfo('done')
    except Exception, e:
        print "error: ", e
    


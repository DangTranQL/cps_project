#!/usr/bin/env python
# encoding: utf-8

import rospy
from nav_msgs.msg import Odometry

class Hello:
    def __init__(self):
        self.sub_pose = rospy.Subscriber('/odom', Odometry, self.callBack)

    def callBack(self, msg):
        self.position = msg.pose.pose.position
        self.orientation = msg.pose.pose.orientation
        rospy.loginfo(self.position)

if __name__ == "__main__":
    rospy.init_node("ODOMMMMMM")
    POSES = Hello()
    
    try:
        rospy.spin()
    except rospy.ROSInterruptException:
        rospy.loginfo('exception')

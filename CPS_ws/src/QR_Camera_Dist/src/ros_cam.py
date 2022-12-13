#!/usr/bin/env python3
# encoding: utf-8

import time
import rospy
import camera
import data_sort
from sensor_msgs.msg import Joy

class rosCam:
    def __init__(self):
        rospy.on_shutdown(self.cancel)
        self.sub_Joy = rospy.Subscriber('/joy', Joy, self.receiveJoyInput)
        self.rate = rospy.Rate(20)
        self.Joy_state = False

    def cancel(self):
        self.sub_Joy.unregister()

    def receiveJoyInput(self, joy_data):
        if not isinstance(joy_data, Joy): return
        indexInput1 = joy_data.axes[1] # driving (forward == 1.0) and (backward == -1.0) value
        indexInput0 = joy_data.axes[0] # driving (left == 1.0) and (right == -1.0) value
        indexInput2 = joy_data.axes[2] # rotating (Rleft == 1.0) and (Rright == -1.0) value

if __name__ == "__main__":
    rospy.init_node('rosCam')
    rosCam = rosCam()

    a = []
    b = []
    a, b = camera.camera()
    data_sort.sorting(a,b)
    ros.loginfo("Sucessssssssssssssssssssssssssssssssssss")

    try:
        rospy.spin()

    except rospy.ROSInterruptException:
        rospy.loginfo('exception')

    

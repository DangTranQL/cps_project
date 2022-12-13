#!/usr/bin/env python
# encoding: utf-8

import time
import rospy
from sensor_msgs.msg import Joy
from std_msgs.msg import String

class CamDistAxes:
    def __init__(self):
        rospy.on_shutdown(self.cancel)
        self.sub_Joy = rospy.Subscriber('/joy', Joy, self.buttonCallback)
        self.pub_Joy = rospy.Publisher('/joy_Buttons', String, queue_size = 1000)
        self.Joy_state = False
        rate = rospy.Rate(20)

    def cancel(self):
        self.sub_Joy.unregister()

    def talker(self, joy_data):

        if joy_data.buttons[0] == 1.0:
                self.pub_Joy.publish("ButtonA")
        if joy_data.buttons[1] == 1:
                self.pub_Joy.publish("ButtonB")
        if joy_data.buttons[3] == 1:
                self.pub_Joy.publish("ButtonX")

    def buttonCallback(self, joy_data):
        if not isinstance(joy_data, Joy): return
        self.Joy_time = time.time()
        self.talker(joy_data)

if __name__ == '__main__':
    rospy.init_node('AxesQR_QR')
    CamDistAxes()
    try:
        rospy.spin()
    except rospy.ROSInterruptException:
        rospy.loginfo('exception')


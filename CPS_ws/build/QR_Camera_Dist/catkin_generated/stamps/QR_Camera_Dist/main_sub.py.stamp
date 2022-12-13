#!/usr/bin/env python3

import rospy
import csv
from std_msgs.msg import String
from nav_msgs.msg import Odometry 
from sensor_msgs.msg import Joy

class sub:
    
    def __init__ (self):
        self.numbutton = 0
        self.strbutton = 'abc'
        self.positionX = 0.00
        self.positionY = 0.00
        #self.pub_Joy = rospy.Publisher("/joy_Buttons", String, queue_size = 1000)
        self.sub_Joy = rospy.Subscriber('/joy', Joy, self.buttonCallJoy)
        #self.sub_Cam = rospy.Subscriber('videos_frames', String, self.buttonCallCam)
       # self.sub_Odom = rospy.Subscriber('/odom', Odometry, self.buttonCallOdom)
        #rate = rospy.Rate(20)


    def buttonCallJoy(self, joy_data):
        self.numbutton = joy_data.buttons[0] # buttonA
        return self.numbutton

#def buttonCallback(button):
 #   if button == 1.0:
  #      pub_Joy.publish("ButtonA")
    
#    def buttonCallOdom(self, odom_data):
 #       self.positionX = odom_data.pose.pose.position.x
  #      self.positionY = odom_data.pose.pose.position.y

   # def buttonCall(self, odomx, odomy):
    #    rospy.loginfo("Hello1")
     #   self.pub_Call = rospy.Publisher("ECHO", String, queue_size = 1000)
      #  self.rate = rospy.Rate(20)
       # rospy.loginfo("Hello2")
    
       # if self.numbutton == 1: # ButtonA
       #     self.pub_Call.publisher("ButtonA")
       #     with open('data.csv', 'w') as f:
       #         writer = f.writer(f, delimiter = ',')
       #         writer.writerow(odomx, odomy)

if __name__ == "__main__":
    rospy.init_node("CamJoyOdom")
    pub_Joy = rospy.Publisher("/joy_Buttons", String, queue_size = 1000)
    rate = rospy.Rate(20)

    subs = sub()
    rospy.loginfo("Hello")
    rospy.loginfo(subs.numbutton)
    if subs.numbutton == 1.0:
        pub_Joy.publish("ButtonA")

    rospy.spin()

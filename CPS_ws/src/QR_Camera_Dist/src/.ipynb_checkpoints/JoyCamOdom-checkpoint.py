#!/usr/bin/env python3

import rospy
import csv
import message_filters
import time
from std_msgs.msg import String
from nav_msgs.msg import Odometry
from sensor_msgs.msg import Joy
from rospy_tutorials.msg import HeaderString


# Global Variables
numbutton = 0
strbutton = 'abc'
positionX = 0.00
positionY = 0.00
#:flag = 0
    
def buttonCallBack(joy_data, odom_data, qr_data):
    if joy_data.buttons[0] == 1 or joy_data.buttons[0] == 1.0: #ButtonA
        
            rospy.loginfo("ButtonA")
            # t = rospy.Time.now()

            f = open("/home/jetson/CPS_ws/src/QR_Camera_Dist/src/data.csv","a")
            f.write(str(qr_data.data) + ',')
            f.write(str(odom_data.pose.pose.position.x) + ',')
            f.write(str(odom_data.pose.pose.position.y) + ',')
            f.write(str(odom_data.pose.pose.orientation.x) + ',')
            f.write(str(odom_data.pose.pose.orientation.y) + ',')
            f.write(str(odom_data.pose.pose.orientation.z) + ',')
            f.write(str(odom_data.pose.pose.orientation.w) + ',')
            f.write(str(int(time.time())) + '\n')
            #f.writerow([qr_data.data,odom_data.pose.pose.position.x,odom_data.pose.pose.position.y,odom_data.pose.pose.orientation.x,odom_data.pose.pose.orientation.y,odom_data.pose.pose.orientation.z,odom_data.pose.pose.orientation.w])
            f.close()
        
            rospy.loginfo(odom_data.pose.pose.position)
        
# main function
if __name__ == "__main__":
    rospy.init_node("CamJoyOdom")
    
    flag = 0 #remove old data from csv

    sub_Joy = message_filters.Subscriber('/joy', Joy)
    sub_Odom = message_filters.Subscriber('/odom', Odometry)
    sub_QR = message_filters.Subscriber('/video_frames', HeaderString)
   # pub_Joy = rospy.Publisher("/joy_Buttons", String, queue_size = 100)

    # f = open("/home/jetson/CPS_ws/src/QR_Camera_Dist/src/data.csv","w")
    # f.write("")
    # f.close()
    
    # if flag == 0:
    #     ts = message_filters.ApproximateTimeSynchronizer([sub_Joy, sub_Odom, sub_QR], 100, 10)
    #     ts.registerCallback(buttonCallBack)
    #     flag = 1
    # elif flag == 1:
    #     flag = 0

    if flag == 0:
        ff = open("/home/jetson/CPS_ws/src/QR_Camera_Dist/src/data.csv","w")
        ff.write('priority,posx,posy,orix,oriy,oriz,oriw,time\n')
        # ff.write('')
        ff.close
        flag = 1
    
    ts = message_filters.ApproximateTimeSynchronizer([sub_Joy, sub_Odom, sub_QR], 1, 2)
    ts.registerCallback(buttonCallBack)
    
   # ff = open("/home/jetson/CPS_ws/src/QR_Camera_Dist/src/data.csv","w")
    #ff.write('priority,position.x,position.y,orientaiton.x,orientaiton.y,orientaiton.z,orientaiton.w')
    #ff.write("")
    #ff.close()

    #rate = rospy.Rate(10)
    rospy.spin()






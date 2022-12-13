#!/usr/bin/env python2

import rospy
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import cv2

def callback(data):
    br = CvBridge()
    rospy.loginfo("receiving video frame")
    current_frame = br.imgmsg_to_cv2(data)
    cv2.imshow("camera", current_frame)
    cv2.waitKey(1)

def receive_message():
    rospy.init_node("video_sub_py")
    rospy.Subscriber("video_frames", Image, callback)
    rospy.spin()
    cv2.destroyALllWindows()

if __name__ == "__main__":
    receive_message()

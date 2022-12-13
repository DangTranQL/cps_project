#!/usr/bin/env python3

import rospy
import cv2 as cv
import numpy as np
import math
from pyzbar.pyzbar import decode
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
from rospy_tutorials.msg import HeaderString
from std_msgs.msg import String


def webcam():
    pub = rospy.Publisher('video_frames', HeaderString, queue_size=10)
    rospy.init_node('video_pub_py', anonymous=True)
    rate = rospy.Rate(10)

    image_cam = cv.VideoCapture('/dev/video0')
    image_cam.set(3,640)
    image_cam.set(4,480)

   # br = CvBridge()
    qr = HeaderString()

    while not rospy.is_shutdown():
        ret, frame = image_cam.read()

        for barcode in decode(frame):
            mydata = barcode.data.decode('utf-8')
            pts = np.array([barcode.polygon], np.int32)
            pts = pts.reshape((-1,1,2))
            cv.polylines(frame, [pts], True, [255,0,255], 5)
            pts2 = barcode.rect
            cv.putText(frame, mydata, (pts2[0], pts2[1]), cv.FONT_HERSHEY_SIMPLEX, 0.9, (255,0,255), 2)

            if ret==True:
                qr.header.stamp = rospy.Time.now()
                qr.header.frame_id = "qr_code"
                qr.data = mydata
               # rospy.loginfo(qr.data)
               # pub.publish(br.cv2_to_imgmsg(frame))
                pub.publish(qr)

        #rospy.loginfo(mydata)

        cv.imshow("frame", frame)

        key = cv.waitKey(1)
        if key == ord('q'):
            break
    image_cam.release()
    cv.destroyAllWindows()
    return

if __name__ == "__main__":
    webcam()

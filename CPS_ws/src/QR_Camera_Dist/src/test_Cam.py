#!/usr/bin/env python3

import rospy
from std_msgs.msg import String

def talker():
    # creating a publisher node
    # queue_size ... a buffer that keeps the value in place
    #                Should be >= rate size
    pub = rospy.Publisher('Video_Camera', String, queue_size=10)
    
    # Initializing ROS Node (a.k.a publisher node)
    rospy.init_node('Astra_Camera')

    # Initializing the output Rate
    rate = rospy.Rate(10) # 10 Hz

    while not rospy.is_shutdown():
        hello_str = "hello World %s" % rospy.get_time()
        rospy.loginfo(hello_str)
        pub.publish(hello_str) # publish to the topic
        rate.sleep()

if __name__ == '__main__':
    try:
        talker()

    except rospy.ROSInterruptException:
        pass
    

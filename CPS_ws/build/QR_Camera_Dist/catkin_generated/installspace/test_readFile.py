#!/usr/bin/env python2
# encoding: utf-8

import rospy
import actionlib
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
from geometry_msgs.msg import *

# Reading csv files to get pose (position, orientation)
def movebase_client():
    client = actionlib.SimpleActionClient('move_base', MoveBaseAction)
    client.wait_for_server()

    goal = MoveBaseGoal()
    goal.target_pose.header.frame_id = 'map'
    goal.target_pose.header.stamp = rospy.Time.now()
    goal.target_pose.pose.position.x = 0.4683212016385259
    goal.target_pose.pose.position.y = 0.028475343858408133
    goal.target_pose.pose.orientation.z = 0.6497042880079889 
    goal.target_pose.pose.orientation.w = 0.7601870415522961
    client.send_goal(goal)
    wait = client.wait_for_result()

    if not wait:
        rospy.logerr("Action server not available")
        rospy.signal_shutdown("Action server not available!")
    else:
        return client.get_result()

def movebase_server():
    client = actionlib.SimpleActionClient('move_base', MoveBaseAction)
    client.wait_for_server()

    goal = MoveBaseGoal()
    goal.target_pose.header.frame_id = 'map'
    goal.target_pose.header.stamp = rospy.Time.now()
    goal.target_pose.pose.position.x = 1.63535549431
    goal.target_pose.pose.position.y = 0.453396091002
    goal.target_pose.pose.orientation.z = 0.0405670970979
    goal.target_pose.pose.orientation.w = 0.999176816501
    client.send_goal(goal)
    wait = client.wait_for_result()

    if not wait:
        rospy.logerr("Action server not available")
        rospy.signal_shutdown("Action server not available!")
    else:
        return client.get_result()

def initialpose_callback(msg):
    if not isinstance(msg, PoseWithCovarianceStamped): return
    pub_rtabinitPose.publish(msg)

if __name__ == "__main__":
    rospy.init_node("movebase_client_py")

    pub_init = rospy.Publisher("initialpose", PoseWithCovarianceStamped)
    p = PoseWithCovarianceStamped()
    msg = PoseWithCovariance()
    msg.pose = Pose(Point(0.0, 0.0, 0.0), Quaternion(0.000,0.000,0.00,1.00))
   # msg.covariance = [1.5878378359197372, 4.335603068449437e-24, 0.0, 0.0, 0.0, 0.0, -2.444835940792473e-24, 1.5878378359197372, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 9.669143534893922e-07, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 9.36956916389746e-07, -1.0914649364941133e-33, 0.0, 0.0, 0.0, 0.0, 5.9580102154582855e-34, 9.36956916389746e-07, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.9046721363368944]
    p.pose = msg

    pub_init.publish(p)

   # pub_rtabinitPose = rospy.Publisher("rtabmap/initialpose", PoseWithCovarianceStamped, queue_size=10)

   # sub_initialpose = rospy.Subscriber('initialpose', PoseWithCovarianceStamped, initialpose_callback)

    try:
        result = movebase_client()
        rospy.loginfo("Goal")
       # for x in range(10):
       #     rospy.loginfo("Heelo")
       # result2 = movebase_server()
       # rospy.loginfo("Gaol")

    except:
             rospy.ROSInterruptException
             rospy.loginfo("Navigation test finished")
    

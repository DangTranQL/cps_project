#!/usr/bin/env python2.7
# encoding: utf-8

from tf.transformations import euler_from_quaternion

def euler_angle(orix, oriy, oriz, oriw):
    (_, _, yaw) = euler_from_quaternion ([orix, oriy, oriz, oriw])
    
    return yaw
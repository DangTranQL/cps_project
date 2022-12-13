import rospy
import cv2 as cv
import numpy as np
import math
from pyzbar.pyzbar import decode

# Real world measured Distance and width of QR code
KNOWN_DISTANCE = 9.54  # cm
KNOWN_WIDTH = 4.0  # cm

# define the fonts
fonts = cv.FONT_HERSHEY_COMPLEX
Pos =(50,50)
# colors (BGR)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
MAGENTA = (255, 0, 255)
GREEN = (0, 255, 0)
CYAN = (255, 255, 0)
GOLD = (0, 255, 215)
YELLOW = (0, 255, 255)
ORANGE = (0, 165, 230)

# finding Distance between two points
def eucaldainDistance(x, y, x1, y1):
    eucaldainDist = math.sqrt((x1 - x) ** 2 + (y1 - y) ** 2)
    return eucaldainDist

# focal length
def focalLengthFinder(knowDistance, knownWidth, widthInImage):
    '''Find the distance between  object and camera 
    knownDistance: distance from object to camera measured in real world
    knownWidth: real width of object, in real world
    widthInImage: the width of object in the image in pixels'''
    
    focalLength = ((widthInImage * knowDistance) / knownWidth)
    return focalLength

def distanceFinder(focalLength, knownWidth, widthInImage):
    '''focalLength: focal length found through another function
    knownWidth : width of object in the real world
    widthInImage: width of object in the image'''
    
    distance = ((knownWidth * focalLength) / widthInImage)/10
    return distance

def DetectQRcode(image):
    codeWidth = 0
    x, y = 0, 0
    euclaDistance = 0
    global Pos 
    # convert the color image to gray scale image
    Gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)

    # create QR code object
    objectQRcode = decode(Gray)
    for obDecoded in objectQRcode:
        points = obDecoded.polygon
        if len(points) > 4:
            hull = cv.convexHull(
                np.array([points for point in points], dtype=np.float32))
            hull = list(map(tuple, np.squeeze(hull)))
        else:
            hull = points

        n = len(hull)
        # draw the lines on the QR code 
        for j in range(0, n):
            cv.line(image, hull[j], hull[(j + 1) % n], ORANGE, 2)
        # finding width of QR code in the image 
        x, x1 = hull[0][0], hull[1][0]
        y, y1 = hull[0][1], hull[1][1]
        
        Pos = hull[3]
        # using Eucaldain distance finder function to find the width 
        euclaDistance = eucaldainDistance(x, y, x1, y1)

        # return the QR code width  
        return euclaDistance


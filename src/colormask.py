import cv2
import numpy as np
from matplotlib import pyplot as plt
import constants

coord = constants.CIRCLE_INIT_POINT
radius = constants.CIRCLE_RADIUS

def createColorMask(frame, lowerLimit, upperLimit):
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    return cv2.inRange(hsv, lowerLimit, upperLimit)

def combineMaskWithVideo(frame, mask):
    return cv2.bitwise_and(frame, frame, mask=mask)

def getCoords(event, x, y, flags, param):
    global coord, pressed
    #Event is triggered when mouse is moving
    if event == cv2.EVENT_MOUSEMOVE:
        print("Mouse coords:", (x, y))
        coord = (x, y)

#function to generate video feed into window
def loadVideo(webcamVersion):
   #Load camera frame
    cv2.namedWindow("frame")
    cv2.setMouseCallback("frame", getCoords)
    video = cv2.VideoCapture(webcamVersion)

    while True:
        ret, frame = video.read()

        #Prepare color mask
        #First apply a Gaussian blur
        blurredFrame = cv2.GaussianBlur(frame, (9,9), cv2.BORDER_DEFAULT)
        mask1 = createColorMask(blurredFrame, np.array([0, 150, 85]), np.array([10, 255, 255]))
        mask2 = createColorMask(blurredFrame, np.array([170, 150, 85]), np.array([180, 255, 255]))

        colorMask = mask1 | mask2
        resultMask = combineMaskWithVideo(frame, colorMask)

        #Add a circle to part of the video
        cv2.circle(frame, coord, radius, constants.CIRCLE_COLOR, constants.LINE_THICKNESS)
        frame = cv2.resize(frame, (0,0), fx=0.99, fy=0.99)
        #Start video
        cv2.imshow('frame', frame)
        cv2.imshow('mask', resultMask)

        #Press q to end video transmission and close window
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    #Release video capture object and close all windows
    video.release()
    cv2.destroyAllWindows()

def main():
    loadVideo(constants.WEBCAM)

if __name__ == '__main__':
    main()
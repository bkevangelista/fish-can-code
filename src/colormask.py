import cv2
import numpy as np
from matplotlib import pyplot as plt
import constants

color = constants.CIRCLE_COLOR
thickness = constants.LINE_THICKNESS
coord = constants.CIRCLE_INIT_POINT
radius = constants.CIRCLE_RADIUS

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

        #Add a circle to part of the video
        cv2.circle(frame, coord, radius, color, thickness)
        frame = cv2.resize(frame, (0,0), fx=0.99, fy=0.99)
        #Start video
        cv2.imshow('frame', frame)

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
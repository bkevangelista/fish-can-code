from random import random
import cv2
import numpy as np
from matplotlib import pyplot as plt
import constants
from database import initDatabase
from configparser import ConfigParser
import imutils

from timer import timer

#Constants
coord = constants.CIRCLE_INIT_POINT
radius = constants.CIRCLE_RADIUS

config_object = ConfigParser()
config_object.read('secrets.ini')
dbCred = config_object['DB']

#Helper Functions
def createColorMask(frame, lowerLimit, upperLimit):
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    return cv2.inRange(hsv, lowerLimit, upperLimit)

def combineMaskWithVideo(frame, mask):
    return cv2.bitwise_and(frame, frame, mask=mask)

#Used to draw circle around filtered object and get coordinates of center + radius
def getCoords(contour):
    global coord, radius
    (x, y), radius = cv2.minEnclosingCircle(contour)
    coord = (int(x), int(y))
    radius = int(radius)

#function to generate video feed into window
def loadVideo(webcamVersion, db):
    #Load camera frame
    video = cv2.VideoCapture(webcamVersion-1)

    #Draw random four song titles from Database

    track = db.test_database.tracks.aggregate([{"$sample": {"size": 4}}])
    randomSongs = []
    for doc in track:
        randomSongs.append(doc)

    while not (cv2.waitKey(1) & 0xFF == ord('q')):
        ret, frame = video.read()
        frame = imutils.resize(frame, width=constants.FRAME_WIDTH, height=constants.FRAME_HEIGHT)
        
        # if not timerThread.is_alive():
        #     x, y = coord[0], coord[1]
        #     #Fish landed in Quadrant 1
        #     if x > 320 and x <= 640 and y > 240 and y <= 480:
        #         print("Quadrant 1: " + str(randomSongs[0]['songTitle']) + "chosen!")
        #     #Fish landed in Quadrant 2
        #     elif x > 320 and x <= 640 and y >= 0 and y <= 240:
        #         print("Quadrant 2: "+ str(randomSongs[3]['songTitle']) + "chosen!")
        #     #Fish landed in Quadrant 3
        #     elif x >= 0 and x < 320 and y >= 0 and y <= 240:
        #         print("Quadrant 3: "+ str(randomSongs[1]['songTitle']) + "chosen!")
        #     #Fish landed in Quadrant 4
        #     elif x >= 0 and x < 320 and y > 240 and y <= 480:
        #         print("Quadrant 4: "+ str(randomSongs[2]['songTitle']) + "chosen!")
        #     timerThread = Thread(target=timer, args=(10))
        #     timerThread.start()

        #Prepare color mask
        mask1 = createColorMask(frame, np.array([0, 130, 80]), np.array([10, 255, 255]))
        mask2 = createColorMask(frame, np.array([170, 130, 80]), np.array([180, 255, 255]))

        colorMask = mask1 | mask2
        
        #Remove noise from mask
        kernel = np.ones((7,7), np.uint8)
        colorMask = cv2.morphologyEx(colorMask, cv2.MORPH_CLOSE, kernel)
        colorMask = cv2.morphologyEx(colorMask, cv2.MORPH_OPEN, kernel)

        #Combine the color mask with video frame
        resultMask = combineMaskWithVideo(frame, colorMask)

        # Create a blank window to draw on
        blank_image = np.zeros((constants.FRAME_HEIGHT,constants.FRAME_WIDTH,3), np.uint8)
        blank_image[:]=(0,124,255)

        #Find contours from mask and draw a circle around it, getting the coordinates as well
        contours, hierarchy = cv2.findContours(colorMask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        if len(contours) != 0:
            getCoords(contours[0])
            cv2.circle(frame, coord, radius, constants.CIRCLE_COLOR, constants.LINE_THICKNESS)

        #Draw lines to represent the four quadrants of coordinate system
        cv2.line(blank_image, (constants.FRAME_WIDTH // 2, 0), (constants.FRAME_WIDTH // 2, constants.FRAME_HEIGHT), (0, 0, 0), constants.LINE_THICKNESS+1)
        cv2.line(blank_image, (0, constants.FRAME_HEIGHT // 2), (constants.FRAME_WIDTH, constants.FRAME_HEIGHT // 2), (0, 0, 0), constants.LINE_THICKNESS+1)

        # Draw the song titles
        # Quadrant 1
        textSize = cv2.getTextSize(randomSongs[0]['songTitle'], cv2.FONT_HERSHEY_SIMPLEX, 0.5, constants.LINE_THICKNESS)
        cv2.putText(blank_image, text=randomSongs[0]['songTitle'], org=((3 *( constants.FRAME_WIDTH - textSize[0][0]) // 4) , constants.FRAME_HEIGHT // 4),
                    fontFace=cv2.FONT_HERSHEY_SIMPLEX, color=(0, 0, 0), fontScale=0.5, thickness=constants.LINE_THICKNESS
        )
        #Quadrant 2
        textSize = cv2.getTextSize(randomSongs[3]['songTitle'], cv2.FONT_HERSHEY_SIMPLEX, 0.5, constants.LINE_THICKNESS)
        cv2.putText(blank_image, text=randomSongs[3]['songTitle'], org=((3 * (constants.FRAME_WIDTH - textSize[0][0]) // 4) - textSize[0][0], 3 * constants.FRAME_HEIGHT // 4),
                    fontFace=cv2.FONT_HERSHEY_SIMPLEX, color=(0, 0, 0), fontScale=0.5, thickness=constants.LINE_THICKNESS
        )
        #Quadrant 3
        textSize = cv2.getTextSize(randomSongs[1]['songTitle'], cv2.FONT_HERSHEY_SIMPLEX, 0.5, constants.LINE_THICKNESS)
        cv2.putText(blank_image, text=randomSongs[1]['songTitle'], org=(((constants.FRAME_WIDTH - textSize[0][0]) // 4) - textSize[0][0], 3 * constants.FRAME_HEIGHT // 4),
                    fontFace=cv2.FONT_HERSHEY_SIMPLEX, color= (0, 0, 0), fontScale=0.5, thickness=constants.LINE_THICKNESS
        )
        #Quadrant 4
        textSize = cv2.getTextSize(randomSongs[2]['songTitle'], cv2.FONT_HERSHEY_SIMPLEX, 0.5, constants.LINE_THICKNESS)
        cv2.putText(blank_image, text=randomSongs[2]['songTitle'], org=(((constants.FRAME_WIDTH - textSize[0][0]) // 4) - textSize[0][0], constants.FRAME_HEIGHT // 4),
                    fontFace=cv2.FONT_HERSHEY_SIMPLEX, color= (0, 0, 0), fontScale=0.5, thickness=constants.LINE_THICKNESS
        )

       

        #Start video
        cv2.imshow('video', frame)
        cv2.imshow('mask', resultMask)
        cv2.imshow('gui', blank_image)

    #Release video capture object and close all windows
    video.release()
    cv2.destroyAllWindows()

    #Close DB client
    db.close()
    
def main():
    db = initDatabase(dbCred['username'], dbCred['password'])
    loadVideo(constants.WEBCAM, db)

if __name__ == '__main__':
    main()
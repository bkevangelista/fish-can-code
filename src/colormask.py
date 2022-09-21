import cv2
import numpy as np
from matplotlib import pyplot as plt
import constants
from database import initDatabase
from configparser import ConfigParser

#Constants
coord = constants.CIRCLE_INIT_POINT
radius = constants.CIRCLE_RADIUS

config_object = ConfigParser()
config_object.read('src/secrets.ini')
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
    print(coord, radius)

#function to generate video feed into window
def loadVideo(webcamVersion, db):
    #Load camera frame
    video = cv2.VideoCapture(webcamVersion-1)

    #Draw random four song titles from Database
    track = db.tracks.aggregate([{"$sample": {"size": 4}}])
    randomSongs = []
    for doc in track:
        randomSongs.append(doc)

    while True:
        ret, frame = video.read()

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

        #Find contours from mask and draw a circle around it, getting the coordinates as well
        contours, hierarchy = cv2.findContours(colorMask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        if len(contours) != 0:
            getCoords(contours[0])
            cv2.circle(frame, coord, radius, constants.CIRCLE_COLOR, constants.LINE_THICKNESS)

        #Draw lines to represent the four quadrants of coordinate system
        cv2.line(frame, (constants.FRAME_WIDTH // 2, 0), (constants.FRAME_WIDTH // 2, constants.FRAME_HEIGHT), (0, 0, 0), constants.LINE_THICKNESS+1)
        cv2.line(frame, (0, constants.FRAME_HEIGHT // 2), (constants.FRAME_WIDTH, constants.FRAME_HEIGHT // 2), (0, 0, 0), constants.LINE_THICKNESS+1)

        #Draw the song titles
        cv2.putText(frame, text=randomSongs[0]['songTitle'], org=(constants.FRAME_WIDTH // 4, constants.FRAME_HEIGHT // 4),
                    fontFace=cv2.FONT_HERSHEY_SIMPLEX, color= (0, 0, 0), fontScale=2, thickness=constants.LINE_THICKNESS
        )

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
    db = initDatabase(dbCred['username'], dbCred['password'])
    loadVideo(constants.WEBCAM, db)

if __name__ == '__main__':
    main()
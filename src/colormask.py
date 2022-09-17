import cv2
import numpy as np
from matplotlib import pyplot as plt
import constants

#function to generate video feed into window
def loadVideo(webcamVersion):
    #Load camera frame
    video = cv2.VideoCapture(webcamVersion)

    while True:
        ret, frame = video.read()
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
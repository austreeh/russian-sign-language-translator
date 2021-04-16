# import block
import cv2
import mediapipe as mp
import time
import math
import numpy as np
import tensorflow as tf

from hand_detector import *
from hand_calculator import *
from drawing_help import *
from gesture_recognizer import *

WINDOW_HEIGHT = 720
WINDOW_WIDTH = 1280

# main function
def main():
    pTime = 0
    cTime = 0
    gesture_time = time.time()
    colors = ["R", "Y", "G"]
    times = [1, 1, 3]
    i = 0
    cap = cv2.VideoCapture(0)

    track_time = time.time()

    detector = handDetector()
    calculator = handCalculator()
    drawing = drawingHelp(WINDOW_HEIGHT, WINDOW_WIDTH)
    recognizer = recognGesture(WINDOW_HEIGHT, WINDOW_WIDTH)

    test_gesture_list = []
    traj_gesture_list_index = []
    traj_gesture_list_ring = []

    prediction_model = tf.keras.models.load_model('trajectory_recognition.model')

    while True:
        # get input image
        success, img = cap.read()
        image = detector.findHands(img)
        landmarks_list = detector.findPosition(img)

        # gesture analisys
        if (round(time.time() - track_time, 1) >= 0.125):
            if len(landmarks_list) != 0:
                gesture = calculator.getStaticGesture(landmarks_list)
                # gd.drawTraj(image)
                # print(gesture[0])
                test_gesture_list.append(gesture[0])
                traj_gesture_list_index.append(gesture[1][1])
                traj_gesture_list_ring.append(gesture[2][1])
                # print(getStaticGesture(landmarks_list)[1][1])
                # print(traj_gesture_list)
            track_time = time.time()
                
        if colors[i] == "G":
            drawing.drawTraj(image, traj_gesture_list_index)
        # draw frame
        gTime = round(time.time() - gesture_time, 1)
        drawing.drawFrame(image, colors[i], gTime)
        if (gTime > times[i]):
            gesture_time = time.time()
            i = (i+1) % 3
            # print(getMaxCountedLetter(test_gesture_list))
            if colors[i] == "R":
                res = recognizer.getResult(recognizer.getMaxCountedLetter(test_gesture_list), traj_gesture_list_index, traj_gesture_list_ring, prediction_model, "blank_image.jpg")
                print(recognizer.getLetter(res)[1], sep='', end='', flush=True)
                # print(recognizer.getLetter(res))

                # trajToImg(traj_gesture_list)
                # recognTraj("blank_image.jpg", prediction_model)
            test_gesture_list = []
            traj_gesture_list_index = []
            traj_gesture_list_ring = []


        # calculate fps
        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime

        # put fps counter on screen
        cv2.putText(image, str(int(fps)), (50,50), cv2.FONT_HERSHEY_TRIPLEX, 1, (0, 200,0), 2)
        #
        cv2.imshow("Image", image) 
        
        if cv2.waitKey(10) & 0xFF == ord('q'):
                break


if __name__ == "__main__":
    main()
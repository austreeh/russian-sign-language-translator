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

class G():

    letters = []
    if_traj = []
    rf_traj = []
    tails_indexes = [0]
    is_active = False # True if rn we read gesture, False if pause
    prev_time = 0
    sum_time = 0

    prev_frame_time = 0

    def __init__(self, calculator, drawing, recognizer, prediction_model):
        self.pause_time = 1
        self.read_time = 1.5 + 0.3 # +fault
        self.adding = 0.5
        self.true_frames = 4 # add
        self.calculator = calculator
        self.drawing = drawing
        self.recognizer = recognizer
        self.prediction_model = prediction_model
        self.if_traj = []

    def add_note(self, landmarks_list):
        if len(landmarks_list) != 0:
            gesture = self.calculator.getStaticGesture(landmarks_list)
            G.letters.append(gesture[0])
            G.if_traj.append(gesture[1][1])
            G.rf_traj.append(gesture[2][1])

    def process(self, start_time, current_time, image, landmarks_list):
        time = round(current_time - start_time,3)

        if G.is_active:
            if landmarks_list:
                self.drawing.drawFrame(image, "G", time)
                G.prev_frame_time = current_time

                if time >= self.read_time:                        
                    self.drawing.drawTraj(image, G.if_traj)

                    mc_letter = self.recognizer.getMaxCountedLetter(G.letters)
                    res = self.recognizer.getResult(mc_letter, G.if_traj, G.rf_traj, self.prediction_model, "blank_image.jpg")
                    recognized_letter = self.recognizer.getLetter(res)[1]

                    if recognized_letter == "":
                        cut = G.tails_indexes.pop(0)
                        # print(G.tails_indexes)
                        G.letters = G.letters[cut:]
                        G.if_traj = G.if_traj[cut:]
                        G.rf_traj = G.rf_traj[cut:]
                        G.prev_time -= self.adding
                        return start_time + self.adding
                    else:
                        print(recognized_letter, sep='', end='', flush=True)
                        G.is_active = False
                        return current_time

                else:
                    G.sum_time += time - G.prev_time
                    
                    if time - G.prev_time >= 0.125:
                        self.add_note(landmarks_list)
                        G.prev_time = time
                        if G.sum_time >= self.adding:
                            G.tails_indexes.append(len(G.letters)-1) # maybe w/o -1
                            G.sum_time = 0
                    
                    self.drawing.drawTraj(image, G.if_traj)
                    return start_time
            else:
                self.drawing.drawFrame(image, "G", round(G.prev_frame_time - start_time, 3))
                new_start = start_time + (current_time - G.prev_frame_time)
                G.prev_frame_time = current_time
                return new_start
        else:
            self.drawing.drawFrame(image, "R", time)
            G.prev_frame_time = current_time
            if time >= self.pause_time:
                G.is_active = True
                G.letters.clear()
                G.if_traj.clear()
                G.tails_indexes.clear()
                G.tails_indexes = [0]
                G.prev_time = 0
                G.sum_time = 0
                return current_time
            return start_time

# main function
def main():
    pTime = 0
    cTime = 0
    cap = cv2.VideoCapture(0)

    detector = handDetector()
    calculator = handCalculator()
    drawing = drawingHelp(WINDOW_HEIGHT, WINDOW_WIDTH)
    recognizer = recognGesture(WINDOW_HEIGHT, WINDOW_WIDTH)
    prediction_model = tf.keras.models.load_model('trajectory_recognition.model')

    Go = G(calculator, drawing, recognizer, prediction_model)
    start_time = time.time()

    while True:
        # get input image
        success, img = cap.read()
        image = detector.findHands(img)
        landmarks_list = detector.findPosition(img)
                
        start_time = Go.process(start_time, time.time(),image, landmarks_list)

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
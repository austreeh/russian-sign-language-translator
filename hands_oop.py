# import block
import cv2
import mediapipe as mp
import time
import math
import numpy as np
import tensorflow as tf

from hand_detector import *
from hands_configuration import *
from db import Database

# connect to DB
db = Database("signs.db")

static_gestures = ["А", "Б", "В", "Г", "Е", "Ж", "Л", "М", "Н", "О", "П", "Р", "С", "Т", "У", "Ф", "Х", "Ч", "Ы", "Э", "Ю", "Я"]
dynamic_gestures = ["Д", "Ш", "И", "З", "К", "Ь"]

#           variables:  one_two
# classes and methods:  oneTwo

# for index finger
# 5, 6, 7 on image
def getAngle(point_one, point_two, point_three, edge):
    # point_one = ALWAYS WRIST POINT (0)
    # point_two = 5 (for index finger)
    # point_three  = 6 (for index finger)
    # edge is edge for action
    # point structure is [id, [x, y, z]]

    # preparations
    alpha_point_one = np.array(point_one[1]) - np.array(point_two[1])
    alpha_point_three = np.array(point_three[1]) - np.array(point_two[1])

    # formula
    alpha = 180 - math.acos( math.fabs(alpha_point_one[0] * alpha_point_three[0] +
                                alpha_point_one[1] * alpha_point_three[1] +
                                alpha_point_one[2] * alpha_point_three[2]
                                ) / math.sqrt(
                                    alpha_point_one[0]*alpha_point_one[0] +
                                    alpha_point_one[1]*alpha_point_one[1] +
                                    alpha_point_one[2]*alpha_point_one[2]
                                ) / math.sqrt(
                                    alpha_point_three[0]*alpha_point_three[0] +
                                    alpha_point_three[1]*alpha_point_three[1] +
                                    alpha_point_three[2]*alpha_point_three[2]
                                )) * (180 / math.pi)
    
    return alpha > edge

def getFingerAngle(point_two, point_three, foo, index_high_point, middle_high_point):
    if foo:
        if (index_high_point[1][0] > middle_high_point[1][0]):
            if point_two[1][0] < point_three[1][0]:
                return "cross"
            else:
                return "close"
        else:
            if point_two[1][0] > point_three[1][0]:
                return "cross"
            else:
                return "close"
    else:
        return "open"
    
# point one is palm point, other - for finger
# alpha and beta edges - angle bariers
def fingerPose(point_one, point_two, point_three, point_four, alpha_edge, beta_edge):
    if getAngle(point_one, point_two, point_three, alpha_edge):
        if getAngle(point_two, point_three, point_four, beta_edge):
            return "direct"
        else:
            return "arc"
    else:
        if getAngle(point_two, point_three, point_four, beta_edge):
            return "half"
        else:
            return "fold"

# get direction of hand
# point_one is for palm point, point_two is for middle finer firs point
def getDirection(point_one, point_two):
    if point_one[1][1] > point_two[1][1]:
        return "Up"
    else:
        return "Down"

# distance function for two landmarks
def getDistance(point_one, point_two):
    return math.sqrt((point_two[1][0] - point_one[1][0]) * (point_two[1][0] - point_one[1][0]) +
                    (point_two[1][1] - point_one[1][1]) * (point_two[1][1] - point_one[1][1]) +
                    (point_two[1][2] - point_one[1][2]) * (point_two[1][2] - point_one[1][2]))

# check if landmarks are "touched"
def isTouched(point_one, point_two, touch_edge):
    return getDistance(point_one, point_two) <= touch_edge

def getMiddle(point_one, point_two):
    return [0,[(point_one[1][0]+point_two[1][0])/2, (point_one[1][1]+point_two[1][1])/2, (point_one[1][2]+point_two[1][2])/2]]

def getStaticGesture(landmarks):
    result = []

    # direction
    result.append(getDirection(landmarks[0], landmarks[9]))

    # big_finger
    result.append(fingerPose(landmarks[1], landmarks[2], landmarks[3], landmarks[4], BIG_ALPHA_ANGLE, BIG_BETA_ANGLE))
    # index_finger
    result.append(fingerPose(landmarks[0], landmarks[5], landmarks[6], landmarks[7], INDEX_ALPHA_ANGLE, INDEX_BETA_ANGLE))
    # middle_finger
    result.append(fingerPose(landmarks[0], landmarks[9], landmarks[10], landmarks[11], MIDDLE_ALPHA_ANGLE, MIDDLE_BETA_ANGLE))
    # ring_finger
    result.append(fingerPose(landmarks[0], landmarks[13], landmarks[14], landmarks[15], RING_ALPHA_ANGLE, RING_BETA_ANGLE))
    # little_finger
    result.append(fingerPose(landmarks[0], landmarks[17], landmarks[18], landmarks[19], LITTLE_ALPHA_ANGLE, LITTLE_BETA_ANGLE))


    # touch index-big
    result.append(isTouched(landmarks[4], getMiddle(landmarks[7], landmarks[8]) , getDistance(landmarks[3], landmarks[4]) * 1.4))   
    # touch middle-big
    result.append(isTouched(landmarks[4], getMiddle(landmarks[11], landmarks[12]), getDistance(landmarks[3], landmarks[4]) * 1.4))
    # touch ring-big
    result.append(isTouched(landmarks[4], landmarks[15], getDistance(landmarks[3], landmarks[4]) * 1.4))

    # index_middle_closed
    # result.append(getAngle(landmarks[6], landmarks[5], landmarks[10],INDEX_MIDDLE_ANGLE))
    result.append(getFingerAngle(landmarks[5], landmarks[9], getAngle(landmarks[6], landmarks[5], landmarks[10], INDEX_MIDDLE_ANGLE), landmarks[8], landmarks[12]))

    # middle_ring_closed
    # result.append(getAngle(landmarks[10], landmarks[9], landmarks[14], MIDDLE_RING_ANGLE))
    result.append(getFingerAngle(landmarks[9], landmarks[13], getAngle(landmarks[10], landmarks[9], landmarks[14], MIDDLE_RING_ANGLE), landmarks[12], landmarks[16]))

    # print(result)
    # return letter and index and ring fingers highest points xyz
    return [db.get_element(result), landmarks[8], landmarks[16]]

class gestureDetector(): 
    trajectory_index = []
    trajectory_ring = []
    letter = ''
    true_letter = 0
    fault = 0
    
    def __init__(self):
        self.static_letter_approve = 13 #frames
        self.dynamic_letter_approve = 20 # frames # maybe change to 9
        self.static_letter_fault = 4 # frames
        self.dynamic_letter_fault = 50 # frames # maybe change to 3

    def cleanVariables(self):
        gestureDetector.letter = ''
        gestureDetector.true_letter = 0
        gestureDetector.fault = 0
        gestureDetector.trajectory_index = []
        gestureDetector.trajectory_ring = []

    def twoPointDist(self, first_point, second_point):
        return math.sqrt( (second_point[0] - first_point[0]) * (second_point[0] - first_point[0]) +
                        (second_point[1] - first_point[1]) * (second_point[1] - first_point[1]) )

    def getTwoDimensionAngle(self, first_point, second_point, third_point):
        p1 = np.array(first_point) - np.array(second_point)
        p2 = np.array(third_point) - np.array(second_point)

        return math.acos((p1[0]*p2[0] + p1[1]*p2[1]) / ((math.sqrt((p1[0]*p1[0]) + (p1[1]*p1[1]))) * math.sqrt((p2[0]*p2[0]) + (p2[1]*p2[1]))))

    def getIndexTrajectory(self):
        if gestureDetector.letter == 'Ь':
            edge = len(gestureDetector.trajectory_index)//3
            list_of_x = [item[0] for item in gestureDetector.trajectory_index]
            min_start_x = min(list_of_x[0:edge])
            max_start_x = max(list_of_x[0:edge])

            min_end_x = min(list_of_x[edge:])
            max_end_x = max(list_of_x[edge:])

            if abs(min_start_x - max_end_x) > abs(max_start_x - min_end_x):
                return "Ъ"
            else:
                return "Ь" 
        if gestureDetector.letter == 'Д':
            list_of_x = [item[0] for item in gestureDetector.trajectory_index]
            list_of_y = [item[1] for item in gestureDetector.trajectory_index]

            # max "left" point
            mlpoint = gestureDetector.trajectory_index[list_of_x.index(min(list_of_x))]
            # max "down" point
            mdpoint = gestureDetector.trajectory_index[list_of_y.index(min(list_of_y))]
            # max "right" point
            mrpoint = gestureDetector.trajectory_index[list_of_x.index(max(list_of_x))]
            # max "upper" point 
            mupoint = gestureDetector.trajectory_index[list_of_y.index(max(list_of_y))]

            traj_h = abs(mupoint[1] - mdpoint[1])
            traj_w = abs(mlpoint[0] - mrpoint[0])

            # print(traj_h, traj_w)

            if traj_w >= traj_h/2:
                return "Д"
            else:
                return "Ц"

    def drawTraj(self, image):
        if gestureDetector.trajectory_index:
            for point in gestureDetector.trajectory_index:
                cv2.circle(image,(int(round(1280*point[0])),int(round(720*point[1]))), 10, (0,0,255), -1)
        # cv2.rectangle(image,(0,0),(1280,720),(0,255,0),3)

    def drawFrame(self, image, color, time):
        # can do it smarter
        if color == "R":
            cv2.rectangle(image, (0,0), (1280, 720), (0,0,255), 10)
            cv2.putText(image, str(time), (1200,50), cv2.FONT_HERSHEY_TRIPLEX, 1, (0, 0, 255), 2)
        if color == "G":
            cv2.rectangle(image, (0,0), (1280, 720), (0,255,0), 10)
            cv2.putText(image, str(time), (1200,50), cv2.FONT_HERSHEY_TRIPLEX, 1, (0, 255, 0), 2)
        if color == "Y":
            cv2.rectangle(image, (0,0), (1280, 720), (0, 255, 255), 10)
            cv2.putText(image, str(time), (1200,50), cv2.FONT_HERSHEY_TRIPLEX, 1, (0, 255, 255), 2)

    def checkFrame(self, letter_pack):
        letter = letter_pack[0]
        if letter != None:
            letter = letter[0]
        # print(letter)
        index_finger_points = letter_pack[1][1]
        ring_finger_points = letter_pack[2][1]

        if gestureDetector.letter in dynamic_gestures:
            if letter == gestureDetector.letter:
                gestureDetector.true_letter += 1
                gestureDetector.trajectory_index.append(index_finger_points)
                gestureDetector.trajectory_ring.append(ring_finger_points)
                if gestureDetector.true_letter == self.dynamic_letter_approve:
                    print(self.getIndexTrajectory(), end='',flush=True)
                    self.cleanVariables()
            else:
                gestureDetector.fault += 1
                gestureDetector.trajectory_index.append(index_finger_points)
                gestureDetector.trajectory_ring.append(ring_finger_points)
                if gestureDetector.fault >= self.dynamic_letter_fault:
                    self.cleanVariables()
                    gestureDetector.letter = letter
        else:
            if letter != None:
                if letter == gestureDetector.letter:
                    gestureDetector.true_letter += 1
                    if gestureDetector.true_letter == self.static_letter_approve:
                        print(letter[0], end='',flush=True)
                        self.cleanVariables()
                else:
                    gestureDetector.fault += 1
                    if gestureDetector.fault >= self.static_letter_fault:
                        self.cleanVariables()
                        gestureDetector.letter = letter
            else:
                gestureDetector.trajectory_index.append(index_finger_points)
                gestureDetector.trajectory_ring.append(ring_finger_points)
            
def getMaxCountedLetter(lst):
    print(lst)
    if lst:
        return max(lst,key=lst.count)

def drawTraj(image, traj_lst):
    if traj_lst:
        for point in traj_lst:
            cv2.circle(image,(int(round(1280*point[0])),int(round(720*point[1]))), 10, (0,0,255), -1)
        for i in range(1,len(traj_lst)):
            start_point = (int(round(1280*traj_lst[i-1][0])), int(round(720*traj_lst[i-1][1])))
            end_point = (int(round(1280*traj_lst[i][0])), int(round(720*traj_lst[i][1])))
            cv2.arrowedLine(image, start_point, end_point, (200, 100, 0), 4)

def trajToImg(traj_lst):
    trj_image = np.ones((720, 1280)) * 255 # create empty image
    # draw trajectory by dots
    if traj_lst:
        for i in range(1,len(traj_lst)):
            start_point = (int(round(1280*traj_lst[i-1][0])), int(round(720*traj_lst[i-1][1])))
            end_point = (int(round(1280*traj_lst[i][0])), int(round(720*traj_lst[i][1])))
            cv2.line(trj_image, start_point, end_point, (0, 0, 0), 40)
        
    # crop trajectory to square
        list_of_x = [item[0] for item in traj_lst] 
        list_of_y = [item[1] for item in traj_lst]
        # max "left" point
        minX = round(min(list_of_x) * 1280)
        # max "down" point
        minY = round(min(list_of_y) * 720)
        # max "right" point
        maxX = round(max(list_of_x) * 1280)
        # max "upper" point 
        maxY = round(max(list_of_y) * 720)
        # get height and width of trajectory "box" 
        height = maxY - minY
        width = maxX - minX
        # cget cutting borders
        if height > width:
            maxX = maxX + (height//2 - width//2) 
            minX = minX - (height//2 - width//2)
        else:
            maxY = maxY + (width//2 - height//2) 
            minY = minY - (width//2 - height//2)
        # CUT CUT CUT
        crop_image = trj_image[minY-100:maxY+100, minX-100:maxX+100]
    
    # resize square to 28x28
        resized_image = cv2.resize(crop_image, (28, 28))
        cv2.imwrite('blank_image.jpg', resized_image)

def recognTraj(image_path, recognition_model):
    im = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    im = cv2.bitwise_not(im)
    im = tf.keras.utils.normalize(im, axis=1)

    # prediction
    prediction = recognition_model.predict([np.array([im])])
    res = np.argmax(prediction)
    if res == 2:
        print("-")
    else:
        print(res)

# main function
def main():
    pTime = 0
    cTime = 0
    gesture_time = time.time()
    colors = ["R", "Y", "G"]
    i = 0
    cap = cv2.VideoCapture(0)

    track_time = time.time()

    detector = handDetector()

    test_gesture_list = []
    traj_gesture_list = []

    prediction_model = tf.keras.models.load_model('trajectory_recognition.model')

    while True:
        # get input image
        success, img = cap.read()
        image = detector.findHands(img)
        landmarks_list = detector.findPosition(img)
        gd = gestureDetector()

        # gesture analisys
        if (round(time.time() - track_time, 1) >= 0.125):
            if len(landmarks_list) != 0:
                # gd.checkFrame(getStaticGesture(landmarks_list))
                # gd.drawTraj(image)
                test_gesture_list.append(getStaticGesture(landmarks_list)[0])
                traj_gesture_list.append(getStaticGesture(landmarks_list)[1][1])
                # print(getStaticGesture(landmarks_list)[1][1])
                # print(traj_gesture_list)
            track_time = time.time()
                
        if colors[i] == "G":
            drawTraj(image, traj_gesture_list)
        # draw frame
        gTime = round(time.time() - gesture_time, 1)
        gd.drawFrame(image, colors[i], gTime)
        if (gTime > 3):
            gesture_time = time.time()
            i = (i+1) % 3
            print(getMaxCountedLetter(test_gesture_list))
            if colors[i] == "R":
                trajToImg(traj_gesture_list)
                recognTraj("blank_image.jpg", prediction_model)
            test_gesture_list = []
            traj_gesture_list = []


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
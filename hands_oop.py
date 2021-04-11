# import block
import cv2
import mediapipe as mp
import time
import math
import numpy as np

from hands_configuration import *
from db import Database

# connect to DB
db = Database("signs.db")

static_gestures = ["А", "Б", "В", "Г", "Е", "Ж", "Л", "М", "Н", "О", "П", "Р", "С", "Т", "У", "Ф", "Х", "Ч", "Ы", "Э", "Ю", "Я"]
dynamic_gestures = ["Д", "Ш", "И", "З", "К", "Ь"]

#           variables:  one_two
# classes and methods:  oneTwo

class handDetector():
    def __init__(self, mode=False, max_hands=1, detection_conf=0.5, track_conf=0.5):
        self.mode = mode
        self.max_hands = max_hands
        self.detection_conf = detection_conf
        self.track_conf = track_conf

        # need to comment it !!!!
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(self.mode, self.max_hands, 
                                        self.detection_conf, self.track_conf)
        self.mp_draw = mp.solutions.drawing_utils

    def findHands(self, img, draw=True):
        image = cv2.cvtColor(cv2.flip(img, 1), cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(image)
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        if self.results.multi_hand_landmarks:
            for hand_landmarks in self.results.multi_hand_landmarks:
                if draw:
                    self.mp_draw.draw_landmarks(image, hand_landmarks, self.mp_hands.HAND_CONNECTIONS, 
                    self.mp_draw.DrawingSpec(color=(255,0,0), thickness=2, circle_radius=3),
                    self.mp_draw.DrawingSpec(color=(255,255,255), thickness=2, circle_radius=2))

        
        return image


    def findPosition(self, img, hand_number=0):
        landmarks_list = []
        if self.results.multi_hand_landmarks:
            my_hand = self.results.multi_hand_landmarks[hand_number]
            for id, lm in enumerate(my_hand.landmark):
                landmarks_list.append([id, [lm.x, lm.y, lm.z]])

        # list of [id, x, y, z]
        return landmarks_list

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
            

# main function
def main():
    pTime = 0
    cTime = 0

    cap = cv2.VideoCapture(0)

    detector = handDetector()

    while True:
        # get input image
        success, img = cap.read()
        image = detector.findHands(img)
        landmarks_list = detector.findPosition(img)
        gd = gestureDetector()
        # cv2.rectangle(image,(0,0),(1280,720),(0,255,0),3)

        if len(landmarks_list) != 0:
            # finger poses #############
            # pose for big finger
            # print(fingerPose(landmarks_list[1], landmarks_list[2], landmarks_list[3], landmarks_list[4], 0, 150))
            
            # pose for index finger
            # print(fingerPose(landmarks_list[0], landmarks_list[5], landmarks_list[6], landmarks_list[7], 150, 110))

            # pose for middle finger
            # print(fingerPose(landmarks_list[0], landmarks_list[9], landmarks_list[10], landmarks_list[11], 150, 110))

            # pose for ring finger
            # print(fingerPose(landmarks_list[0], landmarks_list[13], landmarks_list[14], landmarks_list[15], 150, 130))

            # pose for little finger
            # print(fingerPose(landmarks_list[0], landmarks_list[17], landmarks_list[18], landmarks_list[19], 150, 130))

            # direction #################
            # print(getDirection(landmarks_list[0], landmarks_list[9]))

            # distance index-big
            # print(getDistance(landmarks_list[4], landmarks_list[8]))

            # touches check ####################
            # touch index-big
            # print(isTouched(landmarks_list[4], landmarks_list[8], getDistance(landmarks_list[3], landmarks_list[4]) / 1.2))
            
            # touch middle-big
            # print(isTouched(landmarks_list[4], landmarks_list[12], getDistance(landmarks_list[3], landmarks_list[4]) / 1.2))

            # touch ring-big
            # print(isTouched(landmarks_list[4], landmarks_list[16], getDistance(landmarks_list[3], landmarks_list[4]) / 1.2))


            # Open - Closed fingers ###################
            # true - close
            # false - far
            # index-middle
            # print(getAngle(landmarks_list[6], landmarks_list[5], landmarks_list[10],160, landmarks_list[8], landmarks_list[12]))

            # middle - ring
            # print(getAngle(landmarks_list[10], landmarks_list[9], landmarks_list[14],158))
            
            # big finger test
            # fingerPose(landmarks_list[1], landmarks_list[2], landmarks_list[3], landmarks_list[4], 0, 150)
            # print(" ")

            gd.checkFrame(getStaticGesture(landmarks_list))
            gd.drawTraj(image)

            # print(getStaticGesture(landmarks_list)[0])
            



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
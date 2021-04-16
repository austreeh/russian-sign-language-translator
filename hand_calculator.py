
import math
import numpy as np

from hand_configuration import *
from db_creator import Database

db = Database("signs.db")

class handCalculator():
    def __init__(self):
        pass

    def getAngle(self, point_one, point_two, point_three, edge):
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

    def getFingerAngle(self, point_two, point_three, foo, index_high_point, middle_high_point):
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

    def fingerPose(self, point_one, point_two, point_three, point_four, alpha_edge, beta_edge):
        if self.getAngle(point_one, point_two, point_three, alpha_edge):
            if self.getAngle(point_two, point_three, point_four, beta_edge):
                return "direct"
            else:
                return "arc"
        else:
            if self.getAngle(point_two, point_three, point_four, beta_edge):
                return "half"
            else:
                return "fold"

    def getDirection(self, point_one, point_two):
        if point_one[1][1] > point_two[1][1]:
            return "Up"
        else:
            return "Down"

    def getDistance(self, point_one, point_two):
        return math.sqrt((point_two[1][0] - point_one[1][0]) * (point_two[1][0] - point_one[1][0]) +
                        (point_two[1][1] - point_one[1][1]) * (point_two[1][1] - point_one[1][1]) +
                        (point_two[1][2] - point_one[1][2]) * (point_two[1][2] - point_one[1][2]))

    def isTouched(self, point_one, point_two, touch_edge):
        return self.getDistance(point_one, point_two) <= touch_edge

    def getMiddle(self, point_one, point_two):
        return [0,[(point_one[1][0]+point_two[1][0])/2, (point_one[1][1]+point_two[1][1])/2, (point_one[1][2]+point_two[1][2])/2]]

    def getStaticGesture(self, landmarks):
        result = []

        # direction
        result.append(self.getDirection(landmarks[0], landmarks[9]))

        # big_finger
        result.append(self.fingerPose(landmarks[1], landmarks[2], landmarks[3], landmarks[4], BIG_ALPHA_ANGLE, BIG_BETA_ANGLE))
        # index_finger
        result.append(self.fingerPose(landmarks[0], landmarks[5], landmarks[6], landmarks[7], INDEX_ALPHA_ANGLE, INDEX_BETA_ANGLE))
        # middle_finger
        result.append(self.fingerPose(landmarks[0], landmarks[9], landmarks[10], landmarks[11], MIDDLE_ALPHA_ANGLE, MIDDLE_BETA_ANGLE))
        # ring_finger
        result.append(self.fingerPose(landmarks[0], landmarks[13], landmarks[14], landmarks[15], RING_ALPHA_ANGLE, RING_BETA_ANGLE))
        # little_finger
        result.append(self.fingerPose(landmarks[0], landmarks[17], landmarks[18], landmarks[19], LITTLE_ALPHA_ANGLE, LITTLE_BETA_ANGLE))


        # touch index-big
        result.append(self.isTouched(landmarks[4], self.getMiddle(landmarks[7], landmarks[8]) , self.getDistance(landmarks[3], landmarks[4]) * 1.4))   
        # touch middle-big
        result.append(self.isTouched(landmarks[4], self.getMiddle(landmarks[11], landmarks[12]), self.getDistance(landmarks[3], landmarks[4]) * 1.4))
        # touch ring-big
        result.append(self.isTouched(landmarks[4], landmarks[15], self.getDistance(landmarks[3], landmarks[4]) * 1.4))

        # index_middle_closed
        # result.append(getAngle(landmarks[6], landmarks[5], landmarks[10],INDEX_MIDDLE_ANGLE))
        result.append(self.getFingerAngle(landmarks[5], landmarks[9], self.getAngle(landmarks[6], landmarks[5], landmarks[10], INDEX_MIDDLE_ANGLE), landmarks[8], landmarks[12]))

        # middle_ring_closed
        # result.append(getAngle(landmarks[10], landmarks[9], landmarks[14], MIDDLE_RING_ANGLE))
        result.append(self.getFingerAngle(landmarks[9], landmarks[13], self.getAngle(landmarks[10], landmarks[9], landmarks[14], MIDDLE_RING_ANGLE), landmarks[12], landmarks[16]))

        # print(result)
        # return letter and index and ring fingers highest points xyz
        return [db.get_element(result), landmarks[8], landmarks[16]]
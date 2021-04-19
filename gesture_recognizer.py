import math
import cv2
import sys
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '1' 
import tensorflow as tf
import numpy as np

class recognGesture():
    def __init__(self, window_height, window_width):
        self.static = ["А", "Б", "Г", "Е", "Ж", "Л", "М", "Н", "О", "П", "Р", "С", "Т", "У", "Ф", "Х", "Ч", "Ы", "Э", "Ю", "Я"]
        self.dynamic = ["Д", "Ш", "И", "З", "К", "Ь", "В"]
        self.window_height = window_height
        self.window_width = window_width
        self.dot_area = 40 # in pixels
        

    def getMaxCountedLetter(self, letters_lst):
        if letters_lst:
            letters_lst = list(filter(lambda a: a != None, letters_lst))
            if letters_lst:
                let = max(letters_lst,key=letters_lst.count)
                count = np.count_nonzero(np.array(letters_lst) == let)
                if count >= 5:  # was 6
                    return max(letters_lst,key=letters_lst.count)
        return [""]

    def twoPointDist(self, first_point, second_point):
        return math.sqrt( (second_point[0] - first_point[0]) * (second_point[0] - first_point[0]) +
                        (second_point[1] - first_point[1]) * (second_point[1] - first_point[1]) )

    def recognTraj(self, image_path, recognition_model, traj_lst):
        if len(traj_lst) >= 3:
            im = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
            im = cv2.blur(im, (4,4))
            im = tf.keras.utils.normalize(im, axis=-1, order=0)

            work_traj = []

            for element in traj_lst:
                work_traj.append([element[0] * self.window_width, element[1] * self.window_height])

            # prediction
            prediction = recognition_model.predict([np.array([im])])
            res = np.argmax(prediction)


            isDot = True
            for i in range(1,len(work_traj)):
                if self.twoPointDist(work_traj[0], work_traj[i]) > self.dot_area:
                    isDot = False
            # print(work_traj)
            if isDot:
                return "."


            # if res is "-" then check direction
            if res == 2:
                list_of_x = [item[0] for item in work_traj] 
                if min(list_of_x[0:2]) < max(list_of_x[-2:]):
                    return "->"
                else:
                    return "<-"
                
            return str(res)

    def getResult(self, letter, trajectory_index, trajectory_ring, prediction_model, image_path):
        if letter[0] in self.static:
            return [letter[0], ""]
        else:
            if letter == "И":
                self.trajToImg(trajectory_ring)
                return [letter[0], self.recognTraj(image_path, prediction_model, trajectory_ring)]
            else:
                self.trajToImg(trajectory_index)
                return [letter[0], self.recognTraj(image_path, prediction_model, trajectory_index)]

    def getLetter(self, result_list):
        if result_list[0] in self.dynamic:
            if result_list[0] in ["Д", "К"]:
                if result_list[1] == "1":
                    return(result_list,"Ц")
                if result_list[1] == "0":
                    return(result_list,"Д")
                if result_list[1] == "->":
                    return(result_list,"К")
                else:
                    return(result_list,"")
            if result_list[0] == "И":
                if result_list[1] == "->":
                    return(result_list,"Й")
                if result_list[1] == ".":
                    return(result_list,"И")
                return("","")
            if result_list[0] == "В":
                if result_list[1] == "->":
                    return(result_list," ")
                if result_list[1] == "<-":
                    return(result_list, "\b")
                if result_list[1] == ".":
                    return(result_list, "В")
                return("","")
            if result_list[0] == "Ш": 
                if result_list[1] == "1":
                    return(result_list,"Щ")
                if result_list[1] == ".":
                    return(result_list,"Ш")
                return("","")
            if result_list[0] == "З":
                if result_list[1] == "3":
                    return(result_list,"З")
                if result_list[1] == ".":
                    return(result_list,".")
                if result_list[1] == "1":
                    return(result_list, ",")
                return("","")
            if result_list[0] == "Ь": 
                if result_list[1] == "->":
                    return (result_list,"Ь")
                if result_list[1] == "<-":
                    return (result_list,"Ъ")
                else:
                    return(result_list,"")
        return(result_list,result_list[0])

    def trajToImg(self, traj_lst):
        # step 0. create empty image
        IMG_SIZE = 28
        PADDING_PART = 4
        trj_image = np.ones((IMG_SIZE, IMG_SIZE))
        work_traj = []
        # step 1. transform all points to pixels
        if traj_lst:
            for element in traj_lst:
                work_traj.append([int(round(element[0] * self.window_width)), int(round(element[1] * self.window_height))])

        # step 2. find lowest x,y of optimal square
            list_of_x = [item[0] for item in work_traj] 
            list_of_y = [item[1] for item in work_traj]
            # max "left" point
            minX = min(list_of_x)
            # max "down" point
            minY = min(list_of_y)
            # max "right" point
            maxX = max(list_of_x)
            # max "upper" point 
            maxY = max(list_of_y)
            # get height and width of trajectory "box" 
            height = maxY - minY
            width = maxX - minX
            # get cutting borders
            PADDING = max([height, width]) // PADDING_PART

            if height > width:
                minX = minX - (height//2 - width//2)
                maxX = maxX + (height//2 - width//2)
            else: 
                minY = minY - (width//2 - height//2)
                maxY = maxY + (width//2 - height//2)
                
            # add padding
            minX -= PADDING
            minY -= PADDING
            maxX += PADDING
            maxY += PADDING

        # step 3. using lowest x,y transform all traj points
            SQUARES_MULTIPLY = IMG_SIZE / (maxY-minY)
            for element in work_traj:
                element[0] = int(round((element[0] - minX) * SQUARES_MULTIPLY))
                element[1] = int(round((element[1] - minY) * SQUARES_MULTIPLY))

        # step 4. draw traj by dots
            for i in range(1,len(work_traj)):
                cv2.line(trj_image, (work_traj[i-1][0],work_traj[i-1][1]) , (work_traj[i][0], work_traj[i][1]), (255, 255, 255), 2)

            cv2.imwrite('blank_image.jpg', trj_image)
        # print("*******")
        # print(traj_lst)
        # print("-------")
        # print(work_traj)
        # print("*******")

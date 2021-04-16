import math
import cv2
import tensorflow as tf
import numpy as np

class recognGesture():
    def __init__(self, window_height, window_width):
        self.static = ["А", "Б", "В", "Г", "Е", "Ж", "Л", "М", "Н", "О", "П", "Р", "С", "Т", "У", "Ф", "Х", "Ч", "Ы", "Э", "Ю", "Я"]
        self.dynamic = ["Д", "Ш", "И", "З", "К", "Ь"]
        self.window_height = window_height
        self.window_width = window_width
        self.dot_area = 20 # in pixels
        

    def getMaxCountedLetter(self, letters_lst):
        if letters_lst:
            letters_lst = list(filter(lambda a: a != None, letters_lst))
            if letters_lst:
                return max(letters_lst,key=letters_lst.count)
        return " "

    def twoPointDist(self, first_point, second_point):
        return math.sqrt( (second_point[0] - first_point[0]) * (second_point[0] - first_point[0]) +
                        (second_point[1] - first_point[1]) * (second_point[1] - first_point[1]) )

    def recognTraj(self, image_path, recognition_model, traj_lst):
        if len(traj_lst) >= 3:
            im = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
            im = cv2.blur(im, (4,4))
            im = tf.keras.utils.normalize(im, axis=-1, order=0)

            for element in traj_lst:
                element[0] = element[0] * self.window_width
                element[1] = element[1] * self.window_height

            # prediction
            prediction = recognition_model.predict([np.array([im])])
            res = np.argmax(prediction)


            # isDot = True
            # for i in range(1,len(traj_lst)):
            #     if self.twoPointDist(traj_lst[0], traj_lst[i]) > self.dot_area:
            #         isDot = False

            # if isDot:
            #     return "."

            # if res is "-" then check direction
            if res == 2:
                list_of_x = [item[0] for item in traj_lst] 
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

                isDot = True
                for i in range(1,len(trajectory_ring)):
                    first_point = [trajectory_ring[0][0]*self.window_width, trajectory_ring[0][1]*self.window_height]
                    second_point = [trajectory_ring[i][0]*self.window_width, trajectory_ring[i][1]*self.window_height]
                    if self.twoPointDist(first_point, second_point) > self.dot_area:
                        isDot = False

                if isDot:
                    return[letter[0],"."]

                self.trajToImg(trajectory_ring)
                return [letter[0], self.recognTraj(image_path, prediction_model, trajectory_ring)]
            else:

                isDot = True
                for i in range(1,len(trajectory_index)):
                    first_point = [trajectory_index[0][0]*self.window_width, trajectory_index[0][1]*self.window_height]
                    second_point = [trajectory_index[i][0]*self.window_width, trajectory_index[i][1]*self.window_height]
                    if self.twoPointDist(first_point, second_point) > self.dot_area:
                        isDot = False

                if isDot:
                    return[letter[0],"."]

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
                    return(result_list,"Unknown gesture")
            if result_list[0] == "И":
                if result_list[1] == "->":
                    return(result_list,"Й")
                else:
                    return(result_list,"И")
            if result_list[0] == "Ш": 
                if result_list[1] == "1":
                    return(result_list,"Щ")
                else:
                    return(result_list,"Ш")
            if result_list[0] == "З":
                if result_list[1] == "3":
                    return(result_list,"З")
                else:
                    return(result_list,"Unknown gesture")
            if result_list[0] == "Ь": 
                if result_list[1] == "->":
                    return (result_list,"Ь")
                if result_list[1] == "<-":
                    return (result_list,"Ъ")
                else:
                    return(result_list,"Unknown gesture")
        return(result_list,result_list[0])

    def trajToImg(self, traj_lst):
        # step 0. create empty image
        IMG_SIZE = 28
        PADDING_PART = 4
        trj_image = np.ones((IMG_SIZE, IMG_SIZE))

        # step 1. transform all points to pixels
        if traj_lst:
            for element in traj_lst:
                element[0] = int(round(element[0] * self.window_width))
                element[1] = int(round(element[1] * self.window_height))

        # step 2. find lowest x,y of optimal square
            list_of_x = [item[0] for item in traj_lst] 
            list_of_y = [item[1] for item in traj_lst]
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
            for element in traj_lst:
                element[0] = int(round((element[0] - minX) * SQUARES_MULTIPLY))
                element[1] = int(round((element[1] - minY) * SQUARES_MULTIPLY))

        # step 4. draw traj by dots
            for i in range(1,len(traj_lst)):
                cv2.line(trj_image, (traj_lst[i-1][0],traj_lst[i-1][1]) , (traj_lst[i][0], traj_lst[i][1]), (255, 255, 255), 2)

            cv2.imwrite('blank_image.jpg', trj_image)

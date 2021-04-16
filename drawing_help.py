import cv2

class drawingHelp():
    def __init__(self, window_height, window_width):
        self.window_height = window_height
        self.window_width = window_width

    def drawTraj(self, image, traj_lst):
        if traj_lst:
            for point in traj_lst:
                cv2.circle(image,(int(round(self.window_width*point[0])),int(round(self.window_height*point[1]))), 10, (0,0,255), -1)
            for i in range(1,len(traj_lst)):
                start_point = (int(round(self.window_width*traj_lst[i-1][0])), int(round(self.window_height*traj_lst[i-1][1])))
                end_point = (int(round(self.window_width*traj_lst[i][0])), int(round(self.window_height*traj_lst[i][1])))
                cv2.arrowedLine(image, start_point, end_point, (200, 100, 0), 4)

    def drawFrame(self, image, color, time):
        # can do it smarter
        if color == "R":
            cv2.rectangle(image, (0,0), (self.window_width, self.window_height), (0,0,255), 10)
            cv2.putText(image, str(time), (self.window_width-80,50), cv2.FONT_HERSHEY_TRIPLEX, 1, (0, 0, 255), 2)
        if color == "G":
            cv2.rectangle(image, (0,0), (self.window_width, self.window_height), (0,255,0), 10)
            cv2.putText(image, str(time), (self.window_width-80,50), cv2.FONT_HERSHEY_TRIPLEX, 1, (0, 255, 0), 2)
        if color == "Y":
            cv2.rectangle(image, (0,0), (self.window_width, self.window_height), (0, 255, 255), 10)
            cv2.putText(image, str(time), (self.window_width-80,50), cv2.FONT_HERSHEY_TRIPLEX, 1, (0, 255, 255), 2)

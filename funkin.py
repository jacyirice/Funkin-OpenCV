import cv2
import numpy as np
import pyautogui


class Funkin:
    color = [163, 250]
    kernel = np.ones((5, 5), np.uint8)
    keydown = ""
    action_executing = False

    def __init__(self, pathTemplate="arrows.png", area_setas=[739, 135, 326, 48]) -> None:
        self.imTemplate = cv2.imread(pathTemplate, 0)
        self.area_setas = area_setas
        
    def arrow_action(self, x: float, width: float) -> None:
        w_arrow = width / 4
        if x==0:
            pass
        elif x <= w_arrow:
            self.action("a")
            print("esquerda")
        elif x <= w_arrow * 2:
            self.action("s")
            print("baixo")
        elif x <= w_arrow * 3:
            self.action("w")
            print("cima")
        else:
            self.action("d")
            print("direita")

    def action(self, key: str) -> None:
        self.keydown = key
        pyautogui.keyDown(key)
        pyautogui.sleep(0.1)
        pyautogui.keyUp(key)

    def check_action(self, center_obj: float, im_setas: np.ndarray) -> None:
        self.arrow_action(center_obj, im_setas.shape[1])

    def get_center_obj(self, difference: np.ndarray) -> float:
        opening = cv2.morphologyEx(difference, cv2.MORPH_OPEN, self.kernel)
        x, _, w, _ = cv2.boundingRect(opening)
        return x + w / 2

    def get_frame(self) -> np.ndarray:
        im = np.array(pyautogui.screenshot())
        return cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)

    def play(self) -> None:
        imTemplate = self.imTemplate
        area_setas = self.area_setas
        
        while True:
            im = self.get_frame()

            im_setas = im[
                int(area_setas[1]) : int(area_setas[1] + area_setas[3]),
                int(area_setas[0]) : int(area_setas[0] + area_setas[2]),
            ]
            mask_color = cv2.inRange(im_setas, self.color[0], self.color[1])

            difference = cv2.subtract(imTemplate, mask_color)

            center_obj = self.get_center_obj(difference)
            self.check_action(center_obj, im_setas)

            cv2.imshow("difference", difference)
            if cv2.waitKey(25) & 0xFF == ord("q"):
                break
    
    def get_color(self,event, y,x, flags, param, *args, **kwargs):
        if (event == cv2.EVENT_LBUTTONDOWN):
            self.color = [int(param[x,y]),250]
            self.imTemplate = cv2.inRange(param, self.color[0], self.color[1])
            cv2.imwrite("arrows.png", self.imTemplate)
            print(self.color)
            
    def set_area(self) -> None:
        im = self.get_frame()
        area_setas = cv2.selectROI(im, False)
        print(area_setas)
        im_setas = im[
            int(area_setas[1]) : int(area_setas[1] + area_setas[3]),
            int(area_setas[0]) : int(area_setas[0] + area_setas[2]),
        ]
        cv2.imshow('Setas',im_setas)
        cv2.setMouseCallback('Setas',self.get_color, im_setas)

        cv2.waitKey(0)
        
        self.area_setas = area_setas

        
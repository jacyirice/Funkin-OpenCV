import cv2
import numpy as np
import pyautogui


class Funkin:
    color = [100, 255]
    kernel = np.ones((5, 5), np.uint8)
    keydown = ""
    action_executing=False

    def __init__(self, pathTemplate="") -> None:
        self.imTemplate = cv2.imread(f"{pathTemplate}arrows.png", 0)

    def arrow_action(self, x: float, width: float) -> None:
        w_arrow = width / 4
        if x <= w_arrow:
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
        
    def check_action(self, center_obj: float, im_setas: np.ndarray) -> None:
        if center_obj and not self.action_executing:
            self.action_executing = True
            self.arrow_action(center_obj, im_setas.shape[1])
        elif not center_obj and self.action_executing:
            pyautogui.keyUp(self.keydown)
            self.keydown = ""
            self.action_executing = False

    def get_center_obj(self, difference: np.ndarray) -> float:
        opening = cv2.morphologyEx(difference, cv2.MORPH_OPEN, self.kernel)
        x, _, w, _ = cv2.boundingRect(opening)
        return x + w / 2

    def play(self):
        imTemplate = self.imTemplate
        while True:
            im = np.array(pyautogui.screenshot())
            im = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)

            im_setas = im[126:229, 709:1049]
            mask_color = cv2.inRange(im_setas, self.color[0], self.color[1])

            difference = cv2.subtract(imTemplate, mask_color)

            center_obj = self.get_center_obj(difference)
            self.check_action(center_obj, im_setas)

            cv2.imshow("difference", difference)
            if cv2.waitKey(25) & 0xFF == ord("q"):
                break

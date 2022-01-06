import cv2
import numpy as np
import pyautogui


class Funkin:
    color = [100, 255]
    kernel = np.ones((5, 5), np.uint8)
    action = False
    keydown = ""

    def __init__(self, pathTemplate="") -> None:
        self.imTemplate = cv2.imread(f"{pathTemplate}arrows.png", 0)

    def arrow_action(self, x: float, width: float) -> None:
        w_arrow = width / 4
        if x <= w_arrow:
            self.action('a')
            print("esquerda")
        elif x <= w_arrow * 2:
            self.action('s')
            print("baixo")
        elif x <= w_arrow * 3:
            self.action('w')
            print("cima")
        else:
            self.action('d')
            print("direita")

    def action(self, key: str) -> None:
        self.keydown = key
        pyautogui.keyDown("s")

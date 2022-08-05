from time import sleep
import cv2
import numpy as np
import pyautogui


class ArrowFunkin:
    kernel = np.ones((5, 5), np.uint8)
    stopped = False
    frame = None

    def __init__(self, path_template, area_arrow, color, key_action) -> None:
        self.imTemplate = cv2.imread(path_template, 0)[
            int(area_arrow[1]): int(area_arrow[1] + area_arrow[3]),
            int(area_arrow[0]): int(area_arrow[0] + area_arrow[2]),
        ]
        self.area_arrow = area_arrow
        self.color = color
        self.key_action = key_action

    def arrow_action(self) -> None:
        pyautogui.keyDown(self.key_action)
        pyautogui.sleep(10**-100000000000000000)
        pyautogui.keyUp(self.key_action)

    def check_action(self, x: float, y: float) -> bool:
        if x == 0:
            return False
        return True

    def get_frame(self) -> np.ndarray:
        return self.frame

    def set_frame(self, screenshot) -> None:
        self.frame = screenshot

    def get_center_obj(self, difference: np.ndarray) -> float:
        opening = cv2.morphologyEx(difference, cv2.MORPH_OPEN, self.kernel)
        x, y, w, z = cv2.boundingRect(opening)
        return x + w / 2, y+z

    def start(self) -> None:
        imTemplate:np.ndarray = self.imTemplate
        area_arrow = self.area_arrow
        while True:
            im = self.get_frame()
            if im is not None:
                im_arrow = im[
                    int(area_arrow[1]): int(area_arrow[1] + area_arrow[3]),
                    int(area_arrow[0]): int(area_arrow[0] + area_arrow[2]),
                ]
                difference = cv2.absdiff(imTemplate, im_arrow)
                # center_x, center_y = self.get_center_obj(difference)
                if(difference is not None and difference.any() != 0):
                    # if self.check_action(center_x, center_y):
                    # print(self.key_action)
                    self.arrow_action()
                    # cv2.imshow(self.key_action, difference)
            if self.stopped:
                cv2.destroyAllWindows()
                break

    def stop(self):
        print('parando', self.key_action)
        self.stopped = True

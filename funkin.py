from threading import Thread
from time import sleep
from arrow_funkin import ArrowFunkin
import cv2
import numpy as np
# import pyautogui
from mss import mss


class Funkin:
    def __init__(self, path_template="arrows.png", area_arrows=[739, 140, 326, 50], color=[163, 250], sufix=0) -> None:
        self.path_template = f'data/{sufix}.'.join(path_template.split('.'))
        self.name_json = f'data/areas{sufix}.json'
        self.area_arrows = area_arrows
        self.width_arrow = int(area_arrows[2]/4)
        self.color = color
        self.arrows = []

        self.bounding_box = {
            'top': area_arrows[1], 'left': area_arrows[0], 'width': area_arrows[2], 'height': area_arrows[3]}
        self.sct = mss()

    def start_thread_arrow(self, area_arrow, name_thread, key_action):
        arrow = ArrowFunkin(path_template=self.path_template,
                            area_arrow=area_arrow, color=self.color, key_action=key_action)

        t = Thread(target=arrow.start, name=name_thread, args=())
        t.daemon = True
        t.start()
        return arrow

    def get_area_arrow(self, pos):
        from json import loads
        with open(self.name_json, 'r') as f:
            j1 = loads(f.read())
            j=j1[list(j1.keys())[pos]]
            aux = [
                j['width']['start'],
                j['heigth']['start'],
                j['width']['end'],
                j['heigth']['end'],
            ]
        return aux

    def get_frame(self):
        im = np.array(self.sct.grab(self.bounding_box))
        im_gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
        return cv2.inRange(im_gray, self.color[0], self.color[1])

    def start_thread_arrow_left(self):
        area_arrow = self.get_area_arrow(0)
        name_thread = "funkin_arrow_left"
        key_action = "a"
        self.arrows.append(self.start_thread_arrow(
            area_arrow, name_thread, key_action))

    def start_thread_arrow_down(self):
        area_arrow = self.get_area_arrow(1)
        name_thread = "funkin_arrow_down"
        key_action = "s"
        self.arrows.append(self.start_thread_arrow(
            area_arrow, name_thread, key_action))

    def start_thread_arrow_up(self):
        area_arrow = self.get_area_arrow(2)
        name_thread = "funkin_arrow_up"
        key_action = "w"
        self.arrows.append(self.start_thread_arrow(
            area_arrow, name_thread, key_action))

    def start_thread_arrow_right(self):
        area_arrow = self.get_area_arrow(3)
        name_thread = "funkin_arrow_right"
        key_action = "d"
        self.arrows.append(self.start_thread_arrow(
            area_arrow, name_thread, key_action))

    def start(self):

        self.start_thread_arrow_left()
        self.start_thread_arrow_down()
        self.start_thread_arrow_up()
        self.start_thread_arrow_right()
        try:
            while True:
                im = self.get_frame()
                for arrow in self.arrows:
                    arrow.set_frame(im)
        except KeyboardInterrupt:
            pass
        self.stop()

    def stop(self):
        for arrow in self.arrows:
            arrow.stop()

    def set_template(self) -> None:
        from json import dumps
        im = self.get_frame()
        # num = int(input('Numero de teclas: '))
        with open(self.name_json, 'w') as f:
            areas = {
                "arrow_left": {},
                "arrow_down": {},
                "arrow_up": {},
                "arrow_rigth": {},
            }
            for k in areas.keys():
                area_setas = cv2.selectROI(im, False)
                areas[k] = {
                    "width": {
                        "start": area_setas[0],
                        "end": area_setas[2]
                    },
                    "heigth": {
                        "start": area_setas[1],
                        "end": area_setas[3]
                    },
                }
                print(area_setas)
            f.write(dumps(areas))
        cv2.imwrite(self.path_template, im)

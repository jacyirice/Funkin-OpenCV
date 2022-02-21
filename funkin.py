from threading import Thread
from time import sleep
from arrow_funkin import ArrowFunkin
import cv2
import numpy as np
import pyautogui

class Funkin:
    def __init__(self, path_template="arrows.png", area_arrows=[739, 140, 326, 50], color=[163, 250]) -> None:
        self.path_template = path_template
        self.area_arrows = area_arrows
        self.width_arrow = int(area_arrows[2]/4)
        self.color = color
        self.arrows = []

    def start_thread_arrow(self, area_arrow, name_thread, key_action):
        arrow = ArrowFunkin(path_template=self.path_template,
                            area_arrow=area_arrow, color=self.color, key_action=key_action)

        t = Thread(target=arrow.start, name=name_thread, args=())
        t.daemon = True
        t.start()
        return arrow

    def get_area_arrow(self,pos):
        aux= self.area_arrows.copy()
        aux[0]= aux[0] + self.width_arrow * pos +20
        aux[2] = self.width_arrow-40
        return aux
    
    def start_thread_arrow_left(self):
        area_arrow = self.get_area_arrow(0)
        area_arrow[3]+=15
        name_thread = "funkin_arrow_left"
        key_action = "a"
        self.arrows.append(self.start_thread_arrow(
            area_arrow, name_thread, key_action))

    def start_thread_arrow_down(self):
        area_arrow = self.get_area_arrow(1)
        area_arrow[3]+=15
        name_thread = "funkin_arrow_down"
        key_action = "s"
        self.arrows.append(self.start_thread_arrow(
            area_arrow, name_thread, key_action))
    
    def start_thread_arrow_up(self):
        area_arrow = self.get_area_arrow(2)
        area_arrow[3]+=15
        name_thread = "funkin_arrow_up"
        key_action = "w"
        self.arrows.append(self.start_thread_arrow(
            area_arrow, name_thread, key_action))
    
    def start_thread_arrow_right(self):
        area_arrow = self.get_area_arrow(3)
        area_arrow[3]+=15
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
                sleep(60)
        except KeyboardInterrupt:
            pass
        self.stop()
        
    def stop(self):
        for arrow in self.arrows:
            arrow.stop()

    def set_template(self) -> None:
        im = np.array(pyautogui.screenshot())
        cv2.imwrite(self.path_template, im)
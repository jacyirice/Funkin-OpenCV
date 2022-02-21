import cv2
import numpy as np
import pyautogui


class ArrowFunkin:
	kernel = np.ones((5, 5), np.uint8)
	stopped = False
	action_executing = False

	def __init__(self, path_template, area_arrow, color, key_action) -> None:
		self.imTemplate = cv2.cvtColor(cv2.imread(path_template), cv2.COLOR_BGR2GRAY)[
			int(area_arrow[1]): int(area_arrow[1] + area_arrow[3]),
			int(area_arrow[0]): int(area_arrow[0] + area_arrow[2]),
		]
		self.area_arrow = area_arrow
		self.color = color
		self.key_action = key_action

	def arrow_start_action(self) -> None:
		if not self.action_executing:
			pyautogui.keyDown(self.key_action)
			self.action_executing = not self.action_executing

	def arrow_stop_action(self) -> None:
		if self.action_executing:
			pyautogui.keyUp(self.key_action)
			self.action_executing = not self.action_executing

	def check_action(self, x: float) -> bool:
		if x == 0:
			return False
		return True

	def get_frame(self) -> np.ndarray:
		im = np.array(pyautogui.screenshot())
		return cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)

	def get_center_obj(self, difference: np.ndarray) -> float:
		opening = cv2.morphologyEx(difference, cv2.MORPH_OPEN, self.kernel)
		x, _, w, _ = cv2.boundingRect(opening)
		return x + w / 2

	def start(self) -> None:
		imTemplate = cv2.inRange(self.imTemplate, self.color[0], self.color[1])
		area_arrow = self.area_arrow

		while True:
			im = self.get_frame()

			im_arrow = im[
				int(area_arrow[1]): int(area_arrow[1] + area_arrow[3]),
				int(area_arrow[0]): int(area_arrow[0] + area_arrow[2]),
			]
			mask_color = cv2.inRange(im_arrow, self.color[0], self.color[1])

			difference = cv2.subtract(imTemplate, mask_color)

			if self.check_action(self.get_center_obj(difference)):
				pyautogui.keyDown(self.key_action)
				pyautogui.sleep(10**-100000000000000000)
				pyautogui.keyUp(self.key_action)
			# 	self.arrow_start_action()
			# else:
			# 	self.arrow_stop_action()

			# cv2.imshow("difference "+self.key_action, difference)
			# if cv2.waitKey(25) & 0xFF == ord("q"):
			# 	break

			if self.stopped:
				break

	def stop(self):
		print('parando', self.key_action)
		self.stopped = True

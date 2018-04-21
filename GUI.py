import kivy
kivy.require('1.10.1')
import requests as req

from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.properties import StringProperty

import cv2
# import numpy as np
# import sys

import time


face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
smile_cascade = cv2.CascadeClassifier('haarcascade_smile.xml')
url = "https://icanhazdadjoke.com/"
choice =  True
search_q = ""
ch = ""

# class cameraBuilder :
# 	def __init__(self):
# 		self.cap = cv2.VideoCapture(0)


class YLYL(GridLayout):
	def __init__(self, **kwargs):
		super(YLYL, self).__init__(**kwargs)

	def newJoke(self):
		try:
			res = req.get(
				url,
				headers ={"Accept" : "application/json"}
			).json()
			self.display.text = str(res["joke"])
			return
		except Exception:
			self.display.text = "Error finding the joke"
			return
		#camera = self.ids['camera2']
		
	def camTester(self):
		try:
			cap = cv2.VideoCapture(0)
			counter, ctr2 = 0,0
			flag = 0
			fls = cv2.CASCADE_SCALE_IMAGE
			while True:
				ret, img = cap.read()
				gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
				faces = face_cascade.detectMultiScale(gray, 1.05, 8, minSize = (55, 55), flags = fls)
				for (x, y, w, h) in faces:
					cv2.rectangle(img, (x,y), (x+w, y+h), (255, 0, 0), 2)
					roi_gray = gray[y: y+h, x: x+w]
					roi_color = img[y: y+h, x: x+w]
					smiles = smile_cascade.detectMultiScale(roi_gray, 1.7, 22, minSize = (25, 25), flags = fls)
					if len(smiles) >= 0:
						counter += 1
					else:
						counter = 0 
					for (sx, sy, sw, sh) in smiles:
						cv2.rectangle(roi_color, (sx, sy), (sx+sw, sy+sh), (0, 255, 0), 1)
					if counter == 200:
						cv2.VideoCapture.release(cap)
						print ("You Smiled")
						flag = 1
						break
				cv2.imshow('img', img)
				ctr2 += 1
				if flag == 1:
					break
		except Exception as e:
			print (f"That didn't work out: {e}") 
		return

	def checkLaughter (self):
		content = ConfirmPopup(text = 'Did you laugh?')
		content.bind(on_answer = self._on_answer)
		self.popup = Popup(title = "The big question",
			content = content,
			size_hint = (None, None),
			size = (480, 480))
		self.popup.open()

	def _on_answer(self, instance, answer):
		print ("User answer: ", answer)
		if answer == "yes" :
			self.display.text = "Oh No you lose!"
		elif answer == "no" :
			self.display.text = "Congrats you win!"
		else:
			print("someerror")
		self.popup.dismiss()


class ConfirmPopup(GridLayout):
	text = StringProperty()
	def __init__(self, **kwargs):
		self.register_event_type('on_answer')
		super(ConfirmPopup,self).__init__(**kwargs)
		
	def on_answer(self, *args):
		pass	
		

# class CameraClick(BoxLayout):
#     def capture(self):
#         '''
#         Function to capture the images and give them the names
#         according to their captured time and date.
#         '''
#         camera = self.ids['camera']
#         timestr = time.strftime("%Y%m%d_%H%M%S")
#         camera.export_to_png(f"IMG_{timestr}.png")
#         print("Captured")


class ylylApp(App):
	def build(self):
		# newObj.initialize()
		return YLYL()

ylylApp().run()
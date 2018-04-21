from PIL import Image
from PIL import ImageTk
import tkinter as tk
import threading
import time
import imutils as utils
import cv2
import sys
import argparse
import requests as req
from tkinter import ttk
from imutils.video import VideoStream

face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
smile_cascade = cv2.CascadeClassifier('haarcascade_smile.xml')
url = "https://icanhazdadjoke.com/"
choice =  True
search_q = ""
ch = ""

class MainApplicationPage():
	def __init__(self, stream):
		"""
		Store the stream object, initialize the most recently read frame,
		thread for reading frames and the thread for stoping the read operation
		"""
		self.stream = stream
		self.frame = None
		self.thread = None
		self.stopEvent = None

		self.root = tk.Tk()
		self.panel = None
		self.fls = cv2.CASCADE_SCALE_IMAGE
		self.currentJoke = tk.StringVar()
		self.jokeDisplay = ttk.Label(self.root, textvariable = self.currentJoke)
		self.jokeDisplay.pack(side = "bottom", expand = "yes", padx = 10, pady = 10)

		self.currentResult = tk.StringVar()
		self.resultDisplay = ttk.Label(self.root, textvariable = self.currentResult)
		self.resultDisplay.pack(side = "bottom", expand = "yes", padx = 10, pady = 10)

		btn1 = ttk.Button(self.root, text = "Make me Laugh!", command = self.newJoke)
		btn1.pack(side = "bottom", fill = "both", expand = "yes", padx = 10, pady = 10)

		btn2 = ttk.Button(self.root, text = "Quit", command = self.exitOption)
		btn2.pack(side = "top", fill = "both", expand = "yes", padx = 10, pady = 10)

		self.stopEvent = threading.Event()
		self.thread = threading.Thread(target = self.videoLoop, args = ())
		self.thread.start()

		self.root.wm_title("You Laugh You Loose Challenge")
		self.root.wm_protocol("WM_DELETE_WINDOW", self.onClose)

	def videoLoop(self):
		try:
			while not self.stopEvent.is_set():
				self.frame = self.stream.read()
				self.frame = utils.resize(self.frame, width = 300)
				gray = cv2.cvtColor(self.frame, cv2.COLOR_BGR2GRAY)
				faces = face_cascade.detectMultiScale(gray, 1.05, 8, minSize = (55, 55), flags = self.fls)
				for (x, y, w, h) in faces:
					cv2.rectangle(self.frame, (x,y), (x+w, y+h), (255, 255, 0), 2)
					roi_gray = gray[y: y+h, x: x+w]
					roi_color = self.frame[y: y+h, x: x+w]
					smiles = smile_cascade.detectMultiScale(roi_gray, 1.7, 22, minSize = (15, 15), flags = self.fls)
					for (sx, sy, sw, sh) in smiles:
						cv2.rectangle(roi_color, (sx, sy), (sx+sw, sy+sh), (0, 255, 255), 1)
					self.counter = self.counter + 1 if len(smiles) > 0 else 0
					if self.counter >= 50:
						self.currentResult.set("You Laughed! You Lose!")
				image = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB)
				image = Image.fromarray(image)
				image = ImageTk.PhotoImage(image)

				if self.panel is None:
					self.panel = tk.Label(image = image)
					self.panel.image = image
					self.panel.pack(side = "left", padx = 10, pady = 10)
				else:
					self.panel.configure(image = image)
					self.panel.image = image
		except Exception as e:
			print(f"Caught a Runtime Error: {e}")

	def newJoke(self):
		try:
			res = req.get(
				url,
				headers ={"Accept" : "application/json"}
			).json()
			self.currentJoke.set(str(res["joke"])) 
			return
		except Exception as e:
			self.currentJoke.set(f"Error finding the joke \nError: {e}")
			return

	def onClose(self):
		print("[INFO] Closing the app")
		self.stopEvent.set()
		self.stream.stop()
		self.root.quit()

	def exitOption(self):
		print("[INFO] Closing the app")
		self.stopEvent.set()
		self.stream.stop()
		self.root.quit()


print ("Initializing the Camera")
stream = VideoStream().start()
time.sleep(2.0)

appObject = MainApplicationPage(stream)
appObject.root.mainloop()
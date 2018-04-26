from PIL import Image
from PIL import ImageTk
import tkinter as tk
import threading
import imutils as utils
import cv2
import time
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

class MainApp(tk.Tk):
	def __init__(self, streamObj, *args, **kwargs):
		tk.Tk.__init__(self, *args, **kwargs)
		# self.resizable(width = False, height = False)
		self.wm_title("You Laugh You Loose Challenge")
		self.wm_protocol("WM_DELETE_WINDOW", self.onClose)
		container = tk.Frame(self)
		self.streamObj = streamObj
		container.pack(side = "top", fill = "both", expand = False)
		self.stopEvent = threading.Event()

		container.grid_rowconfigure(0, weight = 1)
		container.grid_columnconfigure(0, weight = 1)

		self.frames = {}
		frame = MainApplicationPage(container, self, self.streamObj)		
		self.frames[MainApplicationPage] = frame
		frame.grid(row = 0, column = 0, sticky = "nsew")
		# for F in (UserLoginPage, RegisterPage):
		# 	frame = F(container, self)		
		# 	self.frames[F] = frame
		# 	frame.grid(row = 0, column = 0, sticky = "nsew")
		self.show_frame(MainApplicationPage)

	def show_frame(self, cont):
		frame = self.frames[cont]
		frame.tkraise()

	def onClose(self):
		print("[INFO] Closing the app")
		self.stopEvent.set()
		print("[INFO] Event Stopped")
		self.streamObj.stop()
		time.sleep(2.0)
		print("[INFO] Stopped Camera")
		self.quit()
		print("[INFO] Stopped App")
		self.destroy()
		print("[INFO] Quitting the window")
		cv2.destroyAllWindows()
		return

class UserLoginPage(tk.Frame):
	def __init__(self, parent, controller):
		tk.Frame.__init__(self, parent, width = 400, height = 200)
		self.usernameLabel = tk.Label(self, text = "Username")
		self.grid_rowconfigure(0, weight = 1)
		self.grid_columnconfigure(0, weight = 1)
		self.usernameLabel.grid(row = 0 , column = 0, sticky = "nsew")
		self.usernameText = tk.Text(self)
		self.usernameText.grid(row = 0, column = 1, sticky = "nsew")
		self.passwordLabel = tk.Label(self, text = "Password")
		self.passwordLabel.grid(row = 1, column = 0, sticky = "nsew")
		self.passwordText = tk.Text(self)
		self.passwordText.grid(row = 1, column = 1, sticky = "nsew")
		self.loginBtn = tk.Button(self, text = "Login", command = lambda: controller.show_frame(MainApplicationPage))
		self.loginBtn.grid(row = "2", column = "0", sticky = "nsew")
		self.registerBtn = tk.Button(self, text = "Register", command = lambda: controller.show_frame(RegisterPage))
		self.registerBtn.grid(row = "2", column = "1", sticky = "nsew")

	def login(self):
		usrname = self.usernameText.get("1.0", 'end-1c')
		password = self.passwordText.get("1.0", 'end-1c')
		print (f"Username = {usrname}, Password = {password}")

class RegisterPage(tk.Frame):
	def __init__(self, parent, controller):
		tk.Frame.__init__(self, parent)
		self.Label1 = ttk.Label(self, text = "Register Page !!")
		self.Label1.pack()

class MainApplicationPage(tk.Frame):
	def __init__(self, parent, controller, stream):
		"""
		Store the stream object, initialize the most recently read frame,
		thread for reading frames and the thread for stoping the read operation
		"""
		tk.Frame.__init__(self, parent)
		print ("Initializing the Camera")
		
		self.frame = None
		self.thread = None
		self.stopEvent = None
		# self = tk.Tk()
		self.stream = stream
		self.panel = None
		self.parent = controller
		self.fls = cv2.CASCADE_SCALE_IMAGE
		self.currentJoke = tk.StringVar()
		self.jokeDisplay = ttk.Label(self, textvariable = self.currentJoke)
		self.jokeDisplay.pack(side = "bottom", expand = "yes", padx = 10, pady = 10)

		self.currentResult = tk.StringVar()
		self.resultDisplay = ttk.Label(self, textvariable = self.currentResult)
		self.resultDisplay.pack(side = "bottom", expand = "yes", padx = 10, pady = 10)

		btn1 = ttk.Button(self, text = "Make me Laugh!", command = self.newJoke)
		btn1.pack(side = "bottom", fill = "both", expand = "yes", padx = 10, pady = 10)

		btn2 = ttk.Button(self, text = "Quit", command = lambda: controller.onClose())
		btn2.pack(side = "top", fill = "both", expand = "yes", padx = 10, pady = 10)
		self.thread = threading.Thread(target = self.videoLoop, args = ())
		self.thread.start()


	def videoLoop(self):
		try:
			while not(self.parent.stopEvent.is_set()):
				# print("Entering the Loop")
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
			self.currentResult.set("")
			return
		except Exception as e:
			self.currentJoke.set(f"Error finding the joke \nError: {e}")
			return

stream = VideoStream().start()
time.sleep(2.0)
appObject = MainApp(streamObj = stream)
appObject.mainloop()

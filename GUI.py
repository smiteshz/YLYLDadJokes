import kivy
kivy.require('1.10.1')
import requests as req

from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.properties import StringProperty

import time

url = "https://icanhazdadjoke.com/"
choice =  True
search_q = ""
ch = ""

class YLYL(GridLayout):
	def newJoke(self):
		try:
			res = req.get(
				url,
				headers ={"Accept" : "application/json"}
			).json()
			self.display.text = str(res["joke"])
		except Exception:
			self.display.text = "Error finding the joke"

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
		

class CameraClick(BoxLayout):
    def capture(self):
        '''
        Function to capture the images and give them the names
        according to their captured time and date.
        '''
        camera = self.ids['camera']
        timestr = time.strftime("%Y%m%d_%H%M%S")
        camera.export_to_png(f"IMG_{timestr}.png")
        print("Captured")


class ylylApp(App):
	def build(self):
		return YLYL()

ylylApp().run()
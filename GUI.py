import kivy
kivy.require('1.10.1')
import requests as req

from kivy.app import App
from kivy.uix.gridlayout import GridLayout

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

class ylylApp(App):
	def build(self):
		return YLYL()

ylylApp().run()
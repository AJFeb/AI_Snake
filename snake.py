from kivy.app import App
from kivy.uix.widget import Widget
from kivy.clock import Clock


class SnakeBody(Widget):
	pass


class SnakeGame(Widget):
	pass












class SnakeApp(App):
	def build(self):
		game = SnakeGame()
		return game


SnakeApp().run()
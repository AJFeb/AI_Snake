import kivy
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.clock import Clock
from kivy.properties import *
from random import randint

#this is the position of cells/snakebody on the environment -- this may replace snakebody class
class Cell(Widget):
	pos_on_graph = ListProperty([1,1])#listproperty is a kivy function
	size_on_graph = ListProperty([1,1])

	def __init__(self, x, y, size, margin = 4):
		super().__init__()#not sure what this does
		self.actual_size = (size, size)
		self.size_on_graph = (size - margin, size - margin)
		self.margin = margin
		self.actual_pos = (x,y)
		self.pos_on_graph_connect()

	def pos_on_graph_connect(self):
		self.pos_on_graph = ((self.actual_pos[0] - self.size_on_graph[0]) / 2, (self.actual_pos[1] - self.size_on_graph[1]) / 2)#not sure why this is the case

	def move_to(self, x, y):
		self.actual_pos = (x, y)
		self.pos_on_graph_connect()

	def move_by(self, x, y, **kwargs):#kwargs allows for variable lenght argument list
		self.move_to(self.actual_pos[0]+x, self.actual_pos[1]+y, **kwargs)

	def get_pos(self):
		return self.actual_pos

	def step_by(self, direction, **kwargs):
		self.move_by(self.actual_size[0] * direction[0], self.actual_size[1] * direction[1], **kwargs)

#this is the environment
class Environment(Widget):
	def __init__(self, config):
		super().__init__()#not sure what this does
		self.config = config
		self.snake = None

	def start(self):
		self.snake = Snake(self.config)
		self.add_widget(self.snake)
		Clock.schedule_interval(self.update, self.config.interval)
	
	#def update(self, _):
	#	for cell in self.cells:
	#		cell.pos = (cell.pos[0]+2, cell.pos[1]+3)#makes sense, not sure why chose 2 and 3

	#def tap(self, touch):
	#	cell = Cell(touch.x, touch.y, 20)
	#	self.add_widget(cell)#add an actual cell to the environment that we see
	#	self.cells.append(cell)

class Config:
	default_length = 10
	cell_size = 15
	rat_size = 15
	margin = 4
	interval = 0.2
	dead_cell = (1,0,0,1)
	rat_color = (1,1,0,1)

#details for how the objective Rat/Apple will be placed on the 
#environment
class Rat(Widget):
	pass

#details for how snake moves within Environment
class Snake(Widget):
	def __init__(self, config):
		super().__init__()
		self.cells = []
		self.config = config
		self.cell_size = config.cell_size
		self.snakehead_init((100,100))
		for i in range(config.default_length):
			self.lengthen()
	def destroy(self):
		for i in range(len(self.cells)):
			self.remove_widget(self.cells[i])
			self.cells = []
	def lengthen(self, pos=None, direction=(0, 1)):
	    if pos is None:
	        px = self.cells[-1].get_pos()[0] + direction[0] * self.cell_size
	        py = self.cells[-1].get_pos()[1] + direction[1] * self.cell_size
	        pos = (px, py)
        self.cells.append(Cell(*pos, self.cell_size, margin = self.config.margin))
        self.add_widget(self.cells[-1])
    def head_init(self, pos):
    	self.lengthen(pos=pos)

#for snake movement and growth
class SnakeHead(Widget):
	pass

#for snake movement and growth
class SnakeTail(Widget):
	pass

#estabilsh game
class SnakeApp(App):
	def __init__(self):
		super().__init__()
		self.config = Config()
		self.environment = Environment(self.config)

	def build(self):
		self.environment.start()
		#self.environment.start()
		return self.environment

SnakeApp().run()
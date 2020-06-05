import pygame
from random import randint
import math

#initialize pygame
pygame.init()

#display canvas
HEIGHT = 400
WIDTH = 300
display = pygame.display.set_mode((WIDTH,HEIGHT))

#define colors
WHITE = (200, 200, 200)
BLACK = (0, 0, 0)

#define the size of the grid
GRID_SIZE = 20

#load the snake head
snakeHead = pygame.image.load("snakeHead.jpg")
snakeHead = pygame.transform.scale(snakeHead, (GRID_SIZE, GRID_SIZE)) #scale the image to fit in onr grid box
snakerect = snakeHead.get_rect()
#set the initial snake head position in the middle of the canvas
snakeRow = math.floor(HEIGHT/GRID_SIZE/2)*GRID_SIZE
snakeCol = math.floor(WIDTH/GRID_SIZE/2)*GRID_SIZE


#draw the grid by looping through the whole canvas and draw small squares
def drawGrid():
	for x in range(WIDTH):
		for y in range(HEIGHT):
			rect = pygame.Rect(x*GRID_SIZE, y*GRID_SIZE,GRID_SIZE, GRID_SIZE)
			pygame.draw.rect(display, WHITE, rect, 1)

#function for snake movement
#the snake head moves according to the key press
def moveSnakeHead(key, grid_size, snake_row, snake_col):
	if key == pygame.K_LEFT:
		snake_col -= grid_size
	if key == pygame.K_RIGHT:
		snake_col += grid_size
	if key == pygame.K_UP:
		snake_row -= grid_size
	if key == pygame.K_DOWN:
		snake_row += grid_size
	return (snake_row, snake_col)

#Infinite loop that keeps the program running
stop = False
while stop == False:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			stop = True
		if event.type == pygame.KEYDOWN: #if a key is pressed, the snake picture is updated 
			key = event.key
			snakeRow, snakeCol = moveSnakeHead(key, GRID_SIZE, snakeRow, snakeCol)
	pygame.display.update() 
	 '''fill the canvas with black. In pygame, 
	 the canvas is redraw after each loop so in order to draw the 
	 new picture the original picture needs to be coverd by black first,
	 otherwise, when the new snake head is drawn the previous snake head is still on the canvas
	 '''
	display.fill(BLACK)
	drawGrid() #draw the grid
	display.blit(snakeHead,(snakeCol,snakeRow)) #snake is placed column first and then row 
	pygame.display.flip() #update the canvas
pygame.quit()
quit()

class Game:
	def quit(self, event):
		if self.event.type == pygame.QUIT:
			pygame.quit()

	def function():
		pass

class Movements(keyPress):
	#
	x = 10
	y = 10
	speed = 1

	def up(self):
		self.y += self.speed
	def down(self):
		self.y -= self.speed
	def right(self):
		self.x += self.speed
	def left(self):
		self.x -= self.speed


class App:
	pass

#App().run()
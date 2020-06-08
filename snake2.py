import pygame
from random import randint
import math
import random
 
#initialize pygame

#define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (124,252,0)
BEST_SCORE = 0
CURRENT_SCORE = 0

class Snake:
	#Initialize snake head at the display's center
	def __init__(self, width, height, grid_size):
		initRow = math.floor(height/grid_size/2)*grid_size
		initCol = math.floor(width/grid_size/2)*grid_size
		snakeHead = pygame.image.load("snakeHead.jpg")
		self.snakeHead = pygame.transform.scale(snakeHead, (grid_size, grid_size))
		self.body = [[initCol,initRow]]
		self.length = len(self.body)
		self.colDir = 0
		self.rowDir = 0
		self.tail = None

	#Each time the snake moves, we update our snake body list with the new column and row location at the beginning of the list
	#and get rid of the location it was at before (tail).
	def move(self):
		newCol = self.body[0][0]+self.colDir
		newRow = self.body[0][1]+self.rowDir
		self.body.insert(0,[newCol,newRow])
		self.tail = self.body.pop()

	#When the snake head touches food, we keep the tail and allow the head to continue moving.
	#This effectively adds 1 to the length of the snake body.
	def hit(self):
		self.body.append(self.tail)

#We initialize the food at a random location that is not where the snake head starts
#and continue spawning, one at a time, where none of the snake body is as each food is eaten
class Food:
	def __init__(self, width, height, grid_size, snake_body):
		food = pygame.image.load("food_mouse.jpg")
		self.foodImage = pygame.transform.scale(food, (grid_size, grid_size))
		foodRow = randint(0,(width-grid_size)/grid_size)*grid_size
		foodCol = randint(0,(height-grid_size)/grid_size)*grid_size
		while [foodCol,foodRow] in snake_body:
			foodRow = randint(0,(width-grid_size)/grid_size)*grid_size
			foodCol = randint(0,(height-grid_size)/grid_size)*grid_size
		self.row = foodRow
		self.col = foodCol


#draw the grid on the canvas by looping through the whole canvas and drawing small squares
def drawGrid(display, width, height, grid_size, color):
	for x in range(width):
		for y in range(height):
			rect = pygame.Rect(x*grid_size, y*grid_size, grid_size, grid_size)
			pygame.draw.rect(display, color, rect, 1)

#function for snake movement
#the snake head moves according to the key press
#This function updates the direction of the snake
def moveSnakeHead(key, grid_size, snake_row_dir, snake_col_dir):
	if key == pygame.K_LEFT:
		snake_col_dir -= grid_size
		snake_row_dir = 0
	elif key == pygame.K_RIGHT:
		snake_col_dir += grid_size
		snake_row_dir = 0 
	elif key == pygame.K_UP:
		snake_row_dir -= grid_size
		snake_col_dir = 0
	elif key == pygame.K_DOWN:
		snake_row_dir += grid_size
		snake_col_dir = 0
	return (snake_row_dir, snake_col_dir)

def displayText(display, text, size, x, y, font):
	font = pygame.font.Font(pygame.font.match_font(font), size)
	display_surface = font.render(text, True, WHITE)
	rect = display_surface.get_rect()
	rect.midtop = (x,y)
	return (display_surface, rect)

def main(canvasWidth, canvasHeight, gridSize):
	global BEST_SCORE
	global CURRENT_SCORE
	#Initiliaze pygame, 
	#our canvas as display, 
	#the snake at the display's center, 
	#and the first, random spawn location of the food
	pygame.init()
	display = pygame.display.set_mode((canvasWidth,canvasHeight))
	snakeObj = Snake(canvasWidth, canvasHeight, gridSize)
	foodObj = Food(canvasWidth, canvasHeight, gridSize, snakeObj.body)
	#The game will always run unless we close its window
	stop = False
	GameOver =False
	while stop == False:
		for event in pygame.event.get():
			#To quit the game by closing the window
			if event.type == pygame.QUIT:
				stop = True
			#For movements
			if event.type == pygame.KEYDOWN:
				key = event.key
				if GameOver == False:
					snakeObj.rowDir, snakeObj.colDir = moveSnakeHead(key, gridSize,snakeObj.rowDir, snakeObj.colDir)
				else: 
					if key == pygame.K_SPACE:
						snakeObj.__init__(canvasWidth, canvasHeight, gridSize)
						foodObj.__init__(canvasWidth, canvasHeight, gridSize, snakeObj.body)
						GameOver = False
		if GameOver == False:
			snakeObj.move()
		#When the snake head reaches the food, the snake grows by a length of 1 
		#and we generate a new random location for the next food
		if foodObj.col == snakeObj.body[0][0] and foodObj.row == snakeObj.body[0][1]:
			snakeObj.hit()
			CURRENT_SCORE += 1
			if CURRENT_SCORE > BEST_SCORE:
				BEST_SCORE = CURRENT_SCORE
			foodObj.__init__(canvasWidth, canvasHeight, gridSize, snakeObj.body)

		pygame.display.update() 
		display.fill(BLACK)
		drawGrid(display, canvasWidth, canvasHeight, gridSize, WHITE)
		display.blit(snakeObj.snakeHead ,(snakeObj.body[0][0], snakeObj.body[0][1]))
		display.blit(foodObj.foodImage,(foodObj.col, foodObj.row))
		#Draw white filled, green outlined rectangles for each part of snake body, after the snake head
		for i in range(1,len(snakeObj.body)):
			snake_bod_rect = [snakeObj.body[i][0], snakeObj.body[i][1], gridSize, gridSize]
			pygame.draw.rect(display, WHITE, snake_bod_rect)
			pygame.draw.rect(display, GREEN, snake_bod_rect,1)
		#Snake dies if the snake head reaches the boundaries of the screen or if the snake head touches any part of snake body
			if snakeObj.body[0] == snakeObj.body[i]:
				#print("Game Over")
				CURRENT_SCORE = 0
				GameOver = True
		if snakeObj.body[0][0] > canvasHeight or snakeObj.body[0][0] < 0 or snakeObj.body[0][1] > canvasWidth or snakeObj.body[0][1] < 0:
				#print("Game Over")
				CURRENT_SCORE = 0
				GameOver = True
		bestSurface, bestRect = displayText(display, "Best Score: "+str(BEST_SCORE), 20, canvasWidth/2, 20, "Times")
		currentSurface, currentRect = displayText(display, "Current Score: "+str(CURRENT_SCORE), 20, canvasWidth/2, 0, "Times")
		display.blit(bestSurface, bestRect)
		display.blit(currentSurface, currentRect)
		pygame.display.flip()

	pygame.quit()
	quit()


main(300,300,20)


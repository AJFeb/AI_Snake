import pygame
from random import randint
import math

#initialize pygame
pygame.init()

#display canvas
HEIGHT = 300
WIDTH = 300
display = pygame.display.set_mode((WIDTH,HEIGHT))

#define colors
WHITE = (200, 200, 200)
BLACK = (0, 0, 0)

#define the size of the grid
GRID_SIZE = 20

#load the snake head
snakeHead = pygame.image.load("snakeHead.jpg")
snakeHead = pygame.transform.scale(snakeHead, (GRID_SIZE, GRID_SIZE)) #scale the image to fit in our grid box
#snake_rect = snakeHead.get_rect() #i dont think this line is needed

#set the initial snake head position in the middle of the canvas
snakeRow = math.floor(HEIGHT/GRID_SIZE/2)*GRID_SIZE
snakeCol = math.floor(WIDTH/GRID_SIZE/2)*GRID_SIZE

#load the food
food = pygame.image.load("food_mouse.jpg")
food = pygame.transform.scale(food, (GRID_SIZE, GRID_SIZE))
#food_rect = food.get_rect() #i dont think this line is needed

#initialize location of food at random location on canvas
foodRow = randint(0,WIDTH/GRID_SIZE)*GRID_SIZE
foodCol = randint(0,HEIGHT/GRID_SIZE)*GRID_SIZE


#draw the grid on the canvas by looping through the whole canvas and drawing small squares
def drawGrid():
	for x in range(WIDTH):
		for y in range(HEIGHT):
			rect = pygame.Rect(x*GRID_SIZE, y*GRID_SIZE, GRID_SIZE, GRID_SIZE)
			pygame.draw.rect(display, WHITE, rect, 1)

#function for snake movement
#the snake head moves according to the key press
def moveSnakeHead(key, grid_size, snake_row, snake_col):
	if key == pygame.K_LEFT:
		snake_col -= grid_size
	elif key == pygame.K_RIGHT:
		snake_col += grid_size
	elif key == pygame.K_UP:
		snake_row -= grid_size
	elif key == pygame.K_DOWN:
		snake_row += grid_size
	return (snake_row, snake_col)
	#we also have to restrict movement, eventually, on how snake cant move back on itself
	#i.e. cant make a direct 180 degree turn once its lenght > 1

#function for generating new food once initial food has been eaten
def newfood(food_row, food_col, snake_row, snake_col, grid_size):
	newfoodRow = randint(0,WIDTH/GRID_SIZE)*GRID_SIZE
	newfoodCol = randint(0,HEIGHT/GRID_SIZE)*GRID_SIZE
	#we don't want the food to appear in the same space it just was, 
	#so we iterate until both the row and column are no longer the same as what they just were.
	#food location can repeat over the course of the game but not back-to-back
	
	#newfood location also cannot be a space the snakehead or body already occupies
	## UPDATE this once snake body is made so food doesnt spawn in snake body either
	if newfoodRow != food_row and newfoodCol != food_col:
		if newfoodRow != snake_row and newfoodCol != snake_col:
			return (newfoodRow, newfoodCol)
		else:
			while newfoodRow == snake_row and newfoodCol == snake_col:
				newfoodRow = randint(0,WIDTH/GRID_SIZE)*GRID_SIZE
				newfoodCol = randint(0,HEIGHT/GRID_SIZE)*GRID_SIZE
			return (newfoodRow, newfoodCol)
	else:
		while newfoodRow == food_row and newfoodCol == food_col:
			#change this inner while loop for the snake body b/c the snake head space is occupying
			#the same space as the food right now, eating it, so that is already covered in our 
			#outer while loop 
			while newfoodRow == snake_row and newfoodCol == snake_col:
				newfoodRow = randint(0,WIDTH/GRID_SIZE)*GRID_SIZE
				newfoodCol = randint(0,HEIGHT/GRID_SIZE)*GRID_SIZE
			newfoodRow = randint(0,WIDTH/GRID_SIZE)*GRID_SIZE
			newfoodCol = randint(0,HEIGHT/GRID_SIZE)*GRID_SIZE
		return (newfoodRow, newfoodCol)

#function for growing snake's length
#snake length grows when location of snakehead on grid = location of food on grid
#def growth():
#	pass

#functions for how the snake can die
#def boundary_death():
#	pass

#def body_hit_death():
#	pass

#Infinite loop that keeps the program running
stop = False
while stop == False:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			stop = True
		if event.type == pygame.KEYDOWN: #if a key is pressed, the snakehead location is updated 
			key = event.key
			snakeRow, snakeCol = moveSnakeHead(key, GRID_SIZE, snakeRow, snakeCol)
	if snakeRow == foodRow and snakeCol == foodCol:
		foodRow, foodCol = newfood(foodRow, foodCol, snakeRow, snakeCol, GRID_SIZE)
		#growth()
		#something to add to length of snake
	#if :
		#boundary_death()
	pygame.display.update() 
	'''
	fill the canvas with black. In pygame, 
	 the canvas is redrawn after each loop so in order to draw the 
	 new picture the original picture needs to be coverd by black first,
	 otherwise, when the new snake head is drawn the previous snake head is still on the canvas
	'''
	display.fill(BLACK)
	drawGrid() #draw the grid
	display.blit(snakeHead,(snakeCol, snakeRow)) #snake is placed column first and then row 
	display.blit(food,(foodRow, foodCol))
	pygame.display.flip() #update the entire canvas

pygame.quit()
quit()
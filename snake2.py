import pygame
from random import randint
import math
import random

random.seed(42) 
#initialize pygame
pygame.init()

#display canvas
HEIGHT = 300
WIDTH = 300
display = pygame.display.set_mode((WIDTH,HEIGHT))

#define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (124,252,0)

#define the size of the grid
GRID_SIZE = 20

#load the snake head
snakeHead = pygame.image.load("snakeHead.jpg")
snakeHead = pygame.transform.scale(snakeHead, (GRID_SIZE, GRID_SIZE)) #scale the image to fit in our grid box
#snake_rect = snakeHead.get_rect() #i dont think this line is needed

#set the initial snake head position in the middle of the canvas
snakeRow = math.floor(HEIGHT/GRID_SIZE/2)*GRID_SIZE
snakeCol = math.floor(WIDTH/GRID_SIZE/2)*GRID_SIZE

#initialize our snake body
#members of the list will be of the form [[row1, col1], [row2, col2], etc]
snakeBody = []

#each individual block that will be added to our snake body has a row and col coordinate
snakeBlock = []
snakeBlock.append(snakeRow)
snakeBlock.append(snakeCol)
#updating our snake body to include the head we have initiliazed at the screen's center
snakeBody.append(snakeBlock)
snakeLength = 1
#can probably use snakeLength to keep track of the score -- score = snakeLength - 1

#!!!!!!direction of the snake head. Can change into an array once we need to update the whole snake
snakeRow_dir = 0
snakeCol_dir = 0

#load the food
food = pygame.image.load("food_mouse.jpg")
food = pygame.transform.scale(food, (GRID_SIZE, GRID_SIZE))
#food_rect = food.get_rect() #i dont think this line is needed

#initialize location of food at random location on canvas
#have to change this so it doesnt spawn in center of screen, where the snake starts
foodRow = randint(0,WIDTH/GRID_SIZE)*GRID_SIZE
foodCol = randint(0,HEIGHT/GRID_SIZE)*GRID_SIZE

#add a clock
clock = pygame.time.Clock()

#draw the grid on the canvas by looping through the whole canvas and drawing small squares
def drawGrid():
	for x in range(WIDTH):
		for y in range(HEIGHT):
			rect = pygame.Rect(x*GRID_SIZE, y*GRID_SIZE, GRID_SIZE, GRID_SIZE)
			pygame.draw.rect(display, WHITE, rect, 1)

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
	#we also have to restrict movement, eventually, on how snake cant move back on itself
	#i.e. cant make a direct 180 degree turn once its lenght > 1

#function for generating new food once initial food has been eaten
def newfood(food_row, food_col, snake_body_list, grid_size):
	newfoodRow = randint(0,(WIDTH-GRID_SIZE)/GRID_SIZE)*GRID_SIZE
	newfoodCol = randint(0,(HEIGHT-GRID_SIZE)/GRID_SIZE)*GRID_SIZE
	"""
	we don't want the food to appear in the same space it just was, 
	so we iterate until both the row and column are no longer the same as what they just were.
	food location can repeat over the course of the game but not back-to-back
	newfood location also cannot be a space any of the snake body already occupies
	"""

	while [newfoodCol,newfoodRow] in snake_body_list:
		newfoodRow = randint(0,(WIDTH-GRID_SIZE)/GRID_SIZE)*GRID_SIZE
		newfoodCol = randint(0,(HEIGHT-GRID_SIZE)/GRID_SIZE)*GRID_SIZE
	return (newfoodRow,newfoodCol)

	'''
	if newfoodRow != food_row and newfoodCol != food_col:
		for block in snake_body_list:
			if newfoodRow != block[0] and newfoodCol != block[1]:
				return (newfoodRow, newfoodCol)
			else:
				while newfoodRow == block[0] and newfoodCol == block[1]:
					newfoodRow = randint(0,(WIDTH-GRID_SIZE)/GRID_SIZE)*GRID_SIZE
					newfoodCol = randint(0,(HEIGHT-GRID_SIZE)/GRID_SIZE)*GRID_SIZE
				return (newfoodRow, newfoodCol)
	else:
		while newfoodRow == food_row and newfoodCol == food_col:
			#change this inner while loop for the snake body b/c the snake head space is occupying
			#the same space as the food right now, "eating" it, so that is already covered in our 
			#outer while loop 
			for block in snake_body_list:
				while newfoodRow == block[0] and newfoodCol == block[1]:
					newfoodRow = randint(0,(WIDTH-GRID_SIZE)/GRID_SIZE)*GRID_SIZE
					newfoodCol = randint(0,(HEIGHT-GRID_SIZE)/GRID_SIZE)*GRID_SIZE
			newfoodRow = randint(0,(WIDTH-GRID_SIZE)/GRID_SIZE)*GRID_SIZE
			newfoodCol = randint(0,(HEIGHT-GRID_SIZE)/GRID_SIZE)*GRID_SIZE
		return (newfoodRow, newfoodCol)
	'''

#function for growing snake's length
#snake length grows when location of snakehead on grid = location of food on grid
#def growth(snake_row, snake_col):
	#whenever food is eaten, we create a new block [row,col] to be added to our snake body list of lists
	#we also update the length of the snake
	#snake_block = [snake_row, snake_col]
	#snake_length += 1
	#snakeBody.insert(0,snake_block)
	#snakeBody.pop()

	#return snake_body_list
	
	#draw new, white blocks after first snake head block in snake body list
	#!! tbh, this for loop may be unnecessary because we run growth function each time we add a block so
	#a rectangle is already being drawn... dang
	#for i in range(1,len(snake_body_list)):
		#pygame.draw.rect(display, WHITE, [snake_body_list[i][0], snake_body_list[i][1], grid_size, grid_size])
	
	#so this should work, but it will get rid of our head with the image and we'll just have white blocks, making
	#the above for loop even more unnecessary lol but im cool with that
	#if len(snake_body_list) > snake_length:
		#del snake_body_list[0]
	#snake body length increases when we append a new block to its tail, so as the snake keeps moving we must cut off its head
	#to maintain accurate length of snake as it continues growing

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
		if event.type == pygame.KEYDOWN: 
			key = event.key
			#if a key is pressed then the direction of the snake is updated 
			snakeRow_dir, snakeCol_dir = moveSnakeHead(key, GRID_SIZE, snakeRow_dir, snakeCol_dir)
	#for each loop, the snake head moves in the direction assigned
	snakeRow, snakeCol = snakeRow+snakeRow_dir, snakeCol+snakeCol_dir
	snakeBody.insert(0,[snakeCol,snakeRow])
	tail = snakeBody.pop()
	print(snakeBody, "not hit")
	#update food position if the snake head passes the food
	if snakeRow == foodRow and snakeCol == foodCol:
		#growth(snakeRow, snakeCol,snakeLength, GRID_SIZE)
		snakeBody.append(tail)
		foodRow, foodCol = newfood(foodRow, foodCol, snakeBody, GRID_SIZE)
		print(snakeBody, "hit food")
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
	display.blit(food,(foodCol, foodRow))
	for i in range(1,len(snakeBody)):
		snake_bod_rect = [snakeBody[i][0], snakeBody[i][1], GRID_SIZE, GRID_SIZE]
		pygame.draw.rect(display, WHITE, snake_bod_rect)
		pygame.draw.rect(display, GREEN, snake_bod_rect,1)
	pygame.display.flip() #update the entire canvas

pygame.quit()
quit()
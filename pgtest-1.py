import pygame
from random import randint
import math
import random
import AlgoTest as Al
import numpy as np 


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
		self.length = len(self.body)

#We initialize the food at a random location that is not where the snake head starts
#and continue spawning, one at a time, where none of the snake body is as each food is eaten
class Food:
	def __init__(self, width, height, grid_size, snake_body):
		#random.seed(42)
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

#if the snake dies by hitting the boundary
def deathBoundary(headCol, headRow, width, height):
	if headCol < 0 or headCol >= width:
		return True
	if headRow < 0 or headRow >= height:
		return True
	return False

#if the snake dies by hitting its own body
def deathBody(headCol, headRow, snake_body):
	if [headCol, headRow] in snake_body:
		return True
	return False

#for one of the eight directions, [distance to the wall, distance to food, distane to body]
def oneDirInput(headCol, headRow, dCol, dRow, foodCol, foodRow, snake_body, grid_size, width, height):
	if (dCol == 0 and dRow == 0):
		dCol = 0
		dRow = -grid_size
	result = [0,0,0]
	currentHeadCol, currentHeadRow = headCol+dCol, headRow+dRow
	distance = 1
	hitBody = False
	hitFood = False
	while (not deathBoundary(currentHeadCol,currentHeadRow, width, height) and hitFood==False):
		if (foodCol==currentHeadCol and foodRow==currentHeadRow and hitFood == False):
			result[1] = 1/distance
			hitFood = True
		if ([currentHeadCol, currentHeadRow] in snake_body[1:] and hitBody==False) :
			result[2] = 1/distance 
			hitBody == True
		distance += 1
		currentHeadCol, currentHeadRow = currentHeadCol+dCol, currentHeadRow+dRow

	result[0] = 1/distance

	return result

def generateInput(headCol, headRow, headColDir, headRowDir, foodCol, foodRow, snake_body, grid_size,
					width, height):
	#print("generate")
	inputs = []
	#straight ahead
	inputs.extend(oneDirInput(headCol, headRow, headColDir, headRowDir, foodCol, foodRow, snake_body, grid_size, width, height))
	#print("1")

	#45 degrees to the left 
	dCol, dRow = headColDir+headRowDir, headRowDir-headColDir
	inputs.extend(oneDirInput(headCol, headRow, dCol, dRow, foodCol, foodRow, snake_body, grid_size, width, height))
	#print("2")

	#90 degrees to the left
	dCol, dRow = headRowDir, -headColDir
	inputs.extend(oneDirInput(headCol, headRow, dCol, dRow, foodCol, foodRow, snake_body, grid_size, width, height))
	#print(3)
	#135 degrees to the left
	dCol, dRow = dCol+dRow, dRow-dCol
	inputs.extend(oneDirInput(headCol, headRow, dCol, dRow, foodCol, foodRow, snake_body, grid_size, width, height))

	#180 degrees 
	dCol, dRow = -headColDir, -headRowDir
	inputs.extend(oneDirInput(headCol, headRow, dCol, dRow, foodCol, foodRow, snake_body, grid_size, width, height))
	#print(4)
	#225 degrees 
	dCol, dRow = dCol+dRow, dRow-dCol
	inputs.extend(oneDirInput(headCol, headRow, dCol, dRow, foodCol, foodRow, snake_body, grid_size, width, height))
	#print(5)
	#270 degrees
	dCol, dRow = -headRowDir, headColDir
	inputs.extend(oneDirInput(headCol, headRow, dCol, dRow, foodCol, foodRow, snake_body, grid_size, width, height))
	#print(6)
	#315 degrees 
	dCol, dRow = dCol+dRow, dRow-dCol
	inputs.extend(oneDirInput(headCol, headRow, dCol, dRow, foodCol, foodRow, snake_body, grid_size, width, height))
	#print(7)
	#print(inputs)
	return inputs

"""
#this function generates the input for the neural network
#it returns a list of binary values
def generateInput(headCol, headRow, headColDir, headRowDir, foodCol, foodRow, snake_body, grid_size,
					width, height): #positions are a tuple or list of col and row
	result = []
	#when the snake is first initialized, it doesn't have a direction to move to
	#so we will arbitrarily define straight ahead as the top of the board
	if headColDir==0 or headRowDir==0: 
		headColDir = 0 
		headRowDir = -grid_size

	if headColDir!=0 or headRowDir!=0:
		#calculate the new direction of the snake IF it goes straight ahead, turns left, or turns right
		#Because forward, left and right are relative to the snake current direction, we can achieve this by manipulating the current direction
		aheadCol, aheadRow = headCol+headColDir, headRow+headRowDir
	
		leftColDir, leftRowDir =  headRowDir, -headColDir
		leftCol, leftRow = headCol+leftColDir, aheadRow+leftRowDir
	
		rightColDir, rightRowDir =  -headRowDir, headColDir
		rightCol, rightRow = headCol+rightColDir, aheadRow+rightRowDir

		if deathBoundary(aheadCol, aheadRow, width, height) or deathBody(aheadCol, aheadRow, snake_body):
			result.append(0)
		else:
			result.append(1)

		if deathBoundary(leftCol, leftRow, width, height) or deathBody(leftCol, leftRow, snake_body):
			result.append(0)
		else:
			result.append(1)

		if deathBoundary(rightCol, rightRow, width, height) or deathBody(rightCol, rightRow, snake_body):
			result.append(0)
		else:
			result.append(1)

		#see where the food is
		#in the input, the order will be forward,  behind, left, right
		foodColDiff, foodRowDiff = foodCol-headCol, foodRow-headRow
		if (headColDir,headRowDir)==(grid_size, 0):
			result.append(foodColDiff>0)
			result.append(foodColDiff<0)
			result.append(foodRowDiff<0)
			result.append(foodRowDiff>0)

		elif (headColDir,headRowDir)==(-grid_size, 0):
			result.append(foodColDiff<0)
			result.append(foodColDiff>0)
			result.append(foodRowDiff>0)
			result.append(foodRowDiff<0)

		elif (headColDir,headRowDir)==(0, grid_size):
			result.append(foodRowDiff>0)
			result.append(foodRowDiff<0)
			result.append(foodColDiff>0)
			result.append(foodColDiff<0)

		elif (headColDir,headRowDir)==(0, -grid_size):
			result.append(foodRowDiff<0)
			result.append(foodRowDiff>0)
			result.append(foodColDiff<0)
			result.append(foodColDiff>0)

	return [i*1 for i in result]
"""
			
#This function translates the AI output into actual directional change
def changeDirAI(Dir,headColDir, headRowDir, grid_size): # 0=straight ahead, 1 = left, 2 = right
	if headColDir != 0 or headRowDir != 0:
		if Dir == 0:
			colDir, rowDir = headColDir, headRowDir
		elif Dir == 1:
			colDir, rowDir =  headRowDir, -headColDir
		elif Dir == 2:
			colDir, rowDir =  -headRowDir, headColDir
	else:
		if Dir == 0:
			colDir, rowDir = 0, -grid_size
		elif Dir == 1:
			colDir, rowDir =  -grid_size, 0
		elif Dir == 2:
			colDir, rowDir =  grid_size, 0
	return colDir, rowDir
	
#calculates the distance between any two points
def distance(x1, y1, x2, y2):
	dist = math.sqrt((x1-x2)**2+(y1-y2)**2)
	return dist

#The fitness score is calculated by adding the length of the snake and how close the snake gets to the current food from it's previous position
#The latter is calcualted by calculating the distance reduced 
def fitness(bodyLength, initialDist, currentMinDist,deathByLoop,
								deathByBoundary, deathByBody, totalSteps):
	#return bodyLength*10+(initialDist- currentMinDist)/initialDist#+deathByLoop+deathByBoundary+deathByBody
	apples = bodyLength - 1
	return totalSteps+(2**apples+500*apples**2.1)-(apples**1.2)*((0.25*totalSteps)**1.3)

def main(canvasWidth, canvasHeight, gridSize, generation,
			inputNum, population, hiddenLayers, outputNum,
			neuronNums):
	global BEST_SCORE
	global CURRENT_SCORE
	#Initiliaze pygame, 
	#our canvas as display, 
	#the snake at the display's center, 
	#and the first, random spawn location of the food
	#pygame.init()
	#display = pygame.display.set_mode((canvasWidth,canvasHeight))
	snakeObj = Snake(canvasWidth, canvasHeight, gridSize)
	foodObj = Food(canvasWidth, canvasHeight, gridSize, snakeObj.body)
	#The game will always run unless we close its window
	stop = False
	GameOver =False

	#inputNum = 7
	#population = 10
	#hiddenLayers = 2
	#outputNum = 3
	#neuronNums = [150, 100]

	#a list of initial population
	#matVec = Al.initPopMat(inputNum,population,hiddenLayers,outputNum,neuronNums)

	#a list containing the fitness scores for each snake in a given population
	scores = []

	deathByLoop = 0
	deathByBody = 0
	deathByBoundary = 0
	
	currentMaxLength = 0

	#loop through each network in the population
	for vec in generation:
		snakeObj.__init__(canvasWidth, canvasHeight, gridSize)
		foodObj.__init__(canvasWidth, canvasHeight, gridSize, snakeObj.body)
		GameOver = False

		#convert the vector into the matrix network form
		matMat = Al.vecToMat(vec,inputNum,hiddenLayers,outputNum,neuronNums)
		stop = False

		#count the steps taken to reach the current food
		#if too many steps are taken then we will assume that the snake is going in a loop and thus will terminate
		stepCounter = 0
		totalSteps = 0

		#the current Minimum distance between the snake and the food since
		currentMinDist = distance(snakeObj.body[0][0],snakeObj.body[0][1],
									foodObj.col, foodObj.row)

		#the original distance between the snake and the food
		#this means that if the game is first initialized, it's the distance between the initial position of the snake and the food
		#if the snake is long than 1 then this means the distance between the newly generated food and where the snake last ate food
		ogDist = distance(snakeObj.body[0][0],snakeObj.body[0][1],
									foodObj.col, foodObj.row)
		while stop == False:
			#print(currentMinDist)
			#for event in pygame.event.get():
				#To quit the game by closing the window
				#if event.type == pygame.QUIT:
					#stop = True
				#For movements


				
				#if event.type == pygame.KEYDOWN:
					#key = event.key
					#if GameOver == False:
						#snakeObj.rowDir, snakeObj.colDir = moveSnakeHead(key, gridSize,snakeObj.rowDir, snakeObj.colDir)
					#else: 
						#if key == pygame.K_SPACE:
							#snakeObj.__init__(canvasWidth, canvasHeight, gridSize)
							#foodObj.__init__(canvasWidth, canvasHeight, gridSize, snakeObj.body)
							#GameOver = False
					#if GameOver == True: 
						#if key == pygame.K_SPACE:
							#snakeObj.__init__(canvasWidth, canvasHeight, gridSize)
							#foodObj.__init__(canvasWidth, canvasHeight, gridSize, snakeObj.body)
							#GameOver = False
				
			#generate input
			algo_input = generateInput(snakeObj.body[0][0], snakeObj.body[0][1], snakeObj.colDir, snakeObj.rowDir, 
											foodObj.col, foodObj.row, snakeObj.body, gridSize, canvasWidth, canvasHeight)
			#print(algo_input)
			#predict the next move
			newPred = Al.predict(algo_input, matMat)
			#translate the prediction into movements on the grid
			newColDir, newRowDir = changeDirAI(newPred, snakeObj.colDir,snakeObj.rowDir, gridSize)

			#set the snake direction to the newly calculated one
			snakeObj.colDir,snakeObj.rowDir = newColDir, newRowDir
			#print(algo_predict)


			if GameOver == False:
				snakeObj.move()
				totalSteps += 1

			#calculate the new distance between the snake and the food
			#if the new distance after moving is closer than the current minimum, then we update the current min
			newDist = distance(snakeObj.body[0][0],snakeObj.body[0][1],
							foodObj.col, foodObj.row)
			if newDist < currentMinDist:
				currentMinDist = newDist

			#we add one more step to the step counter
			#if the snake steps through more than 80% of the grid to reach to the food, then we assume it's in a loop and will never reach or terminate
			#so we terminate it by breaking this loop
			stepCounter += 1
			if stepCounter >= (canvasWidth*canvasHeight/(gridSize*gridSize))*0.8:
				deathByLoop = -5
				break

			#When the snake head reaches the food, the snake grows by a length of 1 
			#and we generate a new random location for the next food
			if foodObj.col == snakeObj.body[0][0] and foodObj.row == snakeObj.body[0][1]:
				snakeObj.hit()
				#CURRENT_SCORE += 1

				#we set the step counter to 0 once the snake grows to count for how many steps the snake will take to get to the food at the new length and food position
				stepCounter = 0
				#if CURRENT_SCORE > BEST_SCORE:
					#BEST_SCORE = CURRENT_SCORE

				foodObj.__init__(canvasWidth, canvasHeight, gridSize, snakeObj.body)
				
				#since the snake grew and the food is regenerated, 
				#we reset the ogDist and the current minimum distance for the current snake and food
				ogDist = distance(snakeObj.body[0][0],snakeObj.body[0][1],
									foodObj.col, foodObj.row)
				currentMinDist = distance(snakeObj.body[0][0],snakeObj.body[0][1],
									foodObj.col, foodObj.row)
				

			#pygame.display.update() 
			#display.fill(BLACK)
			#drawGrid(display, canvasWidth, canvasHeight, gridSize, WHITE)
			#display.blit(snakeObj.snakeHead ,(snakeObj.body[0][0], snakeObj.body[0][1]))
			#display.blit(foodObj.foodImage,(foodObj.col, foodObj.row))
			#Draw white filled, green outlined rectangles for each part of snake body, after the snake head
			for i in range(1,len(snakeObj.body)):
				snake_bod_rect = [snakeObj.body[i][0], snakeObj.body[i][1], gridSize, gridSize]
				#pygame.draw.rect(display, WHITE, snake_bod_rect)
				#pygame.draw.rect(display, GREEN, snake_bod_rect,1)
			#Snake dies if the snake head reaches the boundaries of the screen or if the snake head touches any part of snake body
				if snakeObj.body[0] == snakeObj.body[i]:
					#print("Game Over")
					deathByBody = -50
					CURRENT_SCORE = 0
					GameOver = True
					stop = True
					
					#print(snakeObj.length, "LENGTH")
			if snakeObj.body[0][0] > canvasHeight or snakeObj.body[0][0] < 0 or snakeObj.body[0][1] > canvasWidth or snakeObj.body[0][1] < 0:
					#print("Game Over")
					deathByBoundary = -50
					CURRENT_SCORE = 0
					GameOver = True
					stop = True
				
					#print(snakeObj.length, "LENGTH")
			#bestSurface, bestRect = displayText(display, "Best Score: "+str(BEST_SCORE), 20, canvasWidth/2, 20, "Times")
			#currentSurface, currentRect = displayText(display, "Current Score: "+str(CURRENT_SCORE), 20, canvasWidth/2, 0, "Times")
			#display.blit(bestSurface, bestRect)
			#display.blit(currentSurface, currentRect)
			#pygame.display.flip()
		
		if snakeObj.length > currentMaxLength:
			currentMaxLength = snakeObj.length
		fitnessScore = fitness(snakeObj.length,ogDist,currentMinDist, deathByLoop,
								deathByBoundary, deathByBody, totalSteps)
		scores.append(fitnessScore)
		#print(ogDist, currentMinDist)
		#print(snakeObj.length, (ogDist- currentMinDist)/ogDist)

	#print(scores)
	scores = np.array(scores)
	#bestScores = generation[np.argmax(scores)]

	print("maximum length: "+str(currentMaxLength))
	return scores

	pygame.quit()
	quit()

	
def train(inputNum, population, hiddenLayers, outputNum, neuronNums, generationNum):
	canvasWidth = 300
	canvasHeight = 300
	gridSize = 50

	initalMat = Al.initPopMat(inputNum, population, hiddenLayers, outputNum, neuronNums)

	for g in range(generationNum):
		print("Generation:" + str(g))
		fitnessScores = main(canvasWidth, canvasHeight, gridSize, initalMat,
							inputNum, population, hiddenLayers, outputNum, neuronNums)
		
		print("Max Scores:"+str(max(fitnessScores)))
		print("Standard Deviation: "+str(np.std(fitnessScores)))
		parents = Al.bestParents(fitnessScores, initalMat)
		print("parents")
		
		pairs = Al.pairings(parents)
		#print(pairs)
		
		children = Al.offspring(pairs)
		#print(children)
		
		randomChildren = Al.randChildren(children)
		
		mutantChildren = Al.mutChildren(children)
		
		
		nextGeneration = Al.nextGen(parents, children, randomChildren, mutantChildren)
		

		initialMat = nextGeneration
		print(len(initialMat))


train(inputNum=24, population=1000, hiddenLayers=2, outputNum=3, neuronNums=[18, 18], generationNum=50)


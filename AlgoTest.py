import numpy as np 
import copy
from random import randint

#input neurons, total of 7 features 
"""
can move straight ahead, can move to the left, can move to the right, 
is the food straight ahead, is the food behind, is the food on the left,
is the on the right. 
"""

#the number of hidden layers and the number of neurons each layer can be defined by the user

#output neurons, total of 3 outcomes
"""
Move straight ahead, move to the left, move to the right
"""

#The following function initializes any number of population with the given parameters
"""
input_num: number of features in the input
pop_num: population number 
layer_num: number of hidden layers
output_num: number final output
neuron_num: A list indicating the number of neurons in each layer 
"""
#This function returns a list of lists where each inner list is one network/chormosome and the entire list is a collection of networks
def initPopMat(input_num, pop_num, layer_num, output_num, neuron_nums): 
	vec_len = 0
	for j in range(len(neuron_nums)):
		if j == 0:
			vec_len += input_num*neuron_nums[j]
		elif j > 0:
			vec_len += neuron_nums[j-1]*neuron_nums[j]
		if j == len(neuron_nums)-1:
			vec_len += neuron_nums[j]*output_num
	networks = np.empty([pop_num,vec_len])
	for i in range(pop_num):
		new_pop = np.random.uniform(-1,1, [1,vec_len])
		networks[i] = new_pop
	return networks


#This function converts a given network in the vector form to the matrix form
"""
vector: one single network
input_num: number of input features
layer_num: number of layers
output_num: number of output
neuron_nums: a list indicating the number of neurons in each layer
"""
#This function returns of list of matrics where each matrix is the weights used in between two layers
def vecToMat(vector, input_num, layer_num, output_num, neuron_nums): #vector to matrix for one nextwork
	newVec = copy.deepcopy(vector)
	result = []
	firstMat = np.reshape(newVec[0:input_num*neuron_nums[0]],(input_num,neuron_nums[0]))
	newVec = newVec[input_num*neuron_nums[0]:]
	result.append(firstMat)
	for i in range(1,len(neuron_nums)):
		matEndInd = neuron_nums[i-1]*neuron_nums[i]
		mat = np.reshape(newVec[0:matEndInd],(neuron_nums[i-1],neuron_nums[i]))
		result.append(mat)
		newVec = newVec[matEndInd:]
	lastMat = np.reshape(newVec, (neuron_nums[-1],output_num))
	result.append(lastMat)
	return result

#--------------------------------

#creating a list of the 25% most fit snakes from the previous generation which will appear in our next generation as well and
#from which we will create children in our next generation
def bestParents(scores, listofParents): 
	scorePairings = []
	for i in range(len(scores)):
		scorePairings.append([listofParents[i], scores[i]])
	scorePairings.sort(key = lambda x: x[1], reverse = True)
	bestParents = []
	i = 0
	while i < len(scorePairings)/4:
		bestParents.append(scorePairings[i][0])
		i += 1
	return bestParents

#creating random pairings between each of the most fit snake parents to produce 1 child each
#such that 50% of our next gen population will be offspring of these parents
def pairings(bestParents, pop_num):
	pairs = []
	for x in range(int(pop_num/2)):
		rand_index1 = randint(0, len(bestParents)-1)
		rand_index2 = randint(0, len(bestParents)-1)
		while rand_index1 == rand_index2:
			rand_index1 = randint(0, len(bestParents)-1)
		pair = [bestParents[rand_index1], bestParents[rand_index2]]
		while pair in pairs:
			rand_index1 = randint(0, len(bestParents)-1)
			rand_index2 = randint(0, len(bestParents)-1)
			pair = [bestParents[rand_index1], bestParents[rand_index2]]
		pairs.append(pair)
	return pairs

#create children for the next generation that are random combinations of their parents
#and are of the same length as each parent
def offspring(pairs):
	children = []
	for pair in pairs:
		offspring = []
		mom = pair[0]
		dad = pair[1]
		for i in range(len(mom)):
			offspring.append(random.choice([mom[i], dad[i]]))#we can also add weights to see whether mama or papa is more likely to be chosen
		children.append(offspring)
	return children

#mutant children will make up the remaining 25% of the next generation
def mutations(children):
	mutantChildren = []
	for x in range(int(len(children)/2)):
		mutantChild = []
		for i in range(len(children[0])):
			mutantChild.append(random.uniform(-1,1))
		mutantChildren.append(mutantChild)
	return mutantChildren

#create a new vector for our next population
def nextGen(bestParents, children, mutantChildren):
	nextGen = [bestParents+children+mutantChildren]
	return nextGen

#to use each nextGen's populations after the initial/preceding gen is done,
#i think we have to change some stuff in the main pgtest-1 file so we can feed this
#newly created vector into vectoMat function so the network can run with the new gen

#also -- maybe we make a function or set a condition in nextGen to determine 
#when to stop creating new gens once the system converges

#-----------------------------

def sigmoid(x):
	return 1/(1+np.exp(-x))

def tanh(x):
	return 2/(1+np.exp(-2*x))-1

#This function predicts the most likely move for the snake from a single network
"""
inputs: the configuration of the board (where the snake can go and where the food is)
weights: a list of weight matrices
activation: activation function used
"""
#This function returns a number which then will be translate into the snake movement in the game file
def predict(inputs, weights, activation = "tanh"):
	#print(weights[0])
	layer = np.dot(inputs, weights[0])
	#print(layer, "layer")
	#layer = np.reshape(layer, (1,len(layer)))
	if activation == 'sigmoid':
		layer = sigmoid(layer)
	elif activation == "tanh":
		layer = tanh(layer)

	#print(layer, "layer")
	for i in range(1, len(weights)):
		layer = np.dot(layer, weights[i])
		#print(layer,"layer")
		#layer = np.reshape(layer, (1,len(layer)))
		if activation == 'sigmoid':
			layer = sigmoid(layer)
		elif activation == "tanh":
			layer = tanh(layer)

	return np.argmax(layer)



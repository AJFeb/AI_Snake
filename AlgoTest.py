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
	gen_num = 0
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

#creating a list of the 25% most fit snakes from the previous generation
#from which we will create children in our succeeding generation
def bestParents(scores):
	scores.sort(reverse = True)
	best = []
	i = 0
	while i < len(scores)/4:
		best.append(scores[i])
	return best

#creating random pairings between each of the best snakes
def pairings(best):
	pairs = []
	for parent in best:
		rand_index = randint(0, len(best)-1)
		#so that each snake is guaranteed to be a mother and father at elast once
		pairs.append([parent, best[rand_index]])
		pairs.append([best[rand_index], parent])
	return pairs

#create children for the next generation that are random combinations of their parents
#and are of the same length as each parent
def offspring(pairs):
	offsprings = []
	for i in range(len(pairs)-1):
		mom = pairs[i][0]
		dad = pairs[i][1]
		offspring = np.random.choice(np.concatenate([mom, dad]), N, replace = False)
		offsprings.append(offspring)
	return offsprings

#Im not sure that this is necessary since we are already creating random 
#combinations of parents in the offspring function
#def mutations():

#include mutants as an argument and in nextGen list if they actually are necessary
#create a new vector for our next population
def nextGen(best, offsprings):
	nextGen = [best+offsprings]
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



import numpy as np 
import copy

#input neurons, total of 7 features  
"""
can move straight ahead, can move to the left, can move to the right, 
is the food on the right, is the food on the left, is the food straight ahead,
is the food directly behind
"""


def initPopMat(input_num, pop_num, layer_num, output_num, neuron_nums): #neuron_num is a list of numbers indicating the number of neurons in each layer
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


def sigmoid(x):
	return 1/(1+np.exp(-x))

def tanh(x):
	return 2/(1+np.exp(-2*x))-1

def predict(inputs, weights, activation = "sigmoid"):
	layer = np.dot(inputs, weights[0])
	layer = no.reshape(layer, (1,len(layer)))
	if activation == 'sigmoid':
		layer = sigmoid(layer)
	elif activation == "tanh":
		layer = tanh(layer)

	for i in range(1, len(weights)):
		layer = np.dot(layer, weights[i])
		layer = no.reshape(layer, (1,len(layer)))
		if activation == 'sigmoid':
			layer = sigmoid(layer)
		elif activation == "tanh":
			layer = tanh(layer)

	return np.argmax(layer)



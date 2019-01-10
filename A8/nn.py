import numpy as np
import random
from util import oneHotEncodeY
from util import sigmoid


class NeuralNetwork:

	def __init__(self, inputSize, outputSize, numHiddenLayers, hiddenLayerSizes, alpha, batchSize, epochs):
		# Method to initialize a Neural Network Object
		# Parameters
		# inputSize - Size of the input layer
		# outputSize - Size of the output layer
		# numHiddenLayers - Number of hidden layers in the neural network
		# hiddenLayerSizes - List of the hidden layer node sizes
		# alpha - learning rate
		# batchSize - Mini batch size
		# epochs - Number of epochs for training
		self.inputSize = inputSize
		self.outputSize = outputSize
		self.numLayers = numHiddenLayers + 2
		self.layerSizes = [inputSize] + hiddenLayerSizes + [outputSize]
		self.alpha = alpha
		self.batchSize = batchSize
		self.epochs = epochs

		# Initializes the Neural Network Weights and Biases using a Normal Distribution with Mean 0 and Standard Deviation 1
		# weights - a list of matrices correspoding to the weights in various layers of the network
		# biases - corresponding list of biases for each layer
		self.weights = []
		self.biases = []

		for i in range(self.numLayers-1):
			size = self.layerSizes[i], self.layerSizes[i+1]
			self.biases.append(np.random.normal(0, 1, self.layerSizes[i+1]))
			self.weights.append(np.random.normal(0,1,size))

		self.weights = np.asarray(self.weights)
		self.biases = np.asarray(self.biases)


	def train(self, trainX, trainY, validX=None, validY=None, printTrainStats=True, printValStats=True):
		# Method for training the Neural Network
		# Input
		# trainX - A list of training input data to the neural network
		# trainY - Corresponding list of training data labels
		# validX - A list of validation input data to the neural network
		# validY - Corresponding list of validation data labels
		# printTrainStats - Print training loss and accuracy for each epoch
		# printValStats - Prints validation set accuracy after each epoch of training
		# The methods trains the weights and baises using the training data(trainX, trainY)
		# and evaluates the validation set accuracy after each epoch of training
		
		for epoch in range(self.epochs):
			# A Training Epoch
			if printTrainStats or printValStats:
				print("Epoch: ", epoch)

			# Shuffle the training data for the current epoch
			X = np.asarray(trainX)
			Y = np.asarray(trainY)
			perm = np.arange(X.shape[0])
			np.random.shuffle(perm)
			X = X[perm]
			Y = Y[perm]

			# Initializing training loss and accuracy
			trainLoss = 0
			trainAcc = 0

			# Divide the training data into mini-batches
			numBatches = int(np.ceil(float(X.shape[0]) / self.batchSize))
			for batchNum in range(numBatches):
				XBatch = np.asarray(X[batchNum*self.batchSize: (batchNum+1)*self.batchSize])
				YBatch = np.asarray(Y[batchNum*self.batchSize: (batchNum+1)*self.batchSize])

				# Calculate the activations after the feedforward pass
				activations = self.feedforward(XBatch)	

				# Compute the loss	
				loss = self.computeLoss(YBatch, activations)
				trainLoss += loss
				
				# Estimate the one-hot encoded predicted labels after the feedword pass
				predLabels = oneHotEncodeY(np.argmax(activations[-1], axis=1), self.outputSize)

				# Calculate the training accuracy for the current batch
				acc = self.computeAccuracy(YBatch, predLabels)
				trainAcc += acc

				# Backpropagation Pass to adjust weights and biases of the neural network
				self.backpropagate(activations, YBatch)

			# Print Training loss and accuracy statistics
			trainAcc /= numBatches
			if printTrainStats:
				print("Epoch ", epoch, " Training Loss=", loss, " Training Accuracy=", trainAcc)
			
			# Estimate the prediction accuracy over validation data set
			if validX is not None and validY is not None and printValStats:
				_, validAcc = self.validate(validX, validY)
				print("Validation Set Accuracy: ", validAcc, "%")

	def computeLoss(self, Y, activations):
		# Returns the squared loss function given the activations and the true labels Y
		loss = (Y - activations[-1]) ** 2
		loss = np.mean(loss)
		return loss

	def computeAccuracy(self, Y, predLabels):
		# Returns the accuracy given the true labels Y and predicted labels predLabels
		correct = 0
		for i in range(len(Y)):
			if np.array_equal(Y[i], predLabels[i]):
				correct += 1
		accuracy = (float(correct) / len(Y)) * 100
		return accuracy

	def validate(self, validX, validY):
		# Input 
		# validX : Validation Input Data
		# validY : Validation Labels
		# Returns the validation accuracy evaluated over the current neural network model
		valActivations = self.feedforward(validX)
		pred = np.argmax(valActivations[-1], axis=1)
		validPred = oneHotEncodeY(pred, self.outputSize)
		validAcc = self.computeAccuracy(validY, validPred)
		return pred, validAcc

	def feedforward(self, X):
		# Input
		# X : Current Batch of Input Data as an nparray
		# Output
		# Returns the activations at each layer(starting from the first layer(input layer)) to 
		# the output layer of the network as a list of np arrays
		# Note: Activations at the first layer(input layer) is X itself

		activations = []
		###############################################
		# TASK 1 - YOUR CODE HERE

		activations.append(X)
		for i in range(self.numLayers-1):
			h = np.dot(activations[i], self.weights[i]) + self.biases[i]
			activations.append(sigmoid(h))
		# print('for',self.weights)

		###############################################
		return activations

	def backpropagate(self, activations, Y):
		# Input
		# activations : The activations at each layer(starting from second layer(first hidden layer)) of the
		# neural network calulated in the feedforward pass
		# Y : True labels of the training data
		# This method adjusts the weights(self.weights) and biases(self.biases) as calculated from the
		# backpropagation algorithm
		
		###############################################				 
		# TASK 2 - YOUR CODE HERE
		
		def derSigmoid(x):
			return sigmoid(x)*(1-sigmoid(x))

		delta = derSigmoid(activations[-1])*(Y - activations[-1])
		# print(delta)
		# print(self.weights)
		for i in range(self.numLayers-2, -1, -1):
			# print(delta)
			# print('update', self.alpha*np.dot(np.transpose(activations[i]), delta))
			# print('weight', self.weights[-i])
			oldDelta = np.copy(delta)
			delta = derSigmoid(activations[i])*np.dot(delta, np.transpose(self.weights[i]))
			self.weights[i] = self.weights[i] + self.alpha*np.dot(np.transpose(activations[i]), oldDelta)
			# print('weight', self.weights[i])
			self.biases[i] = self.biases[i] + self.alpha*np.sum(np.transpose(oldDelta),1)
			# if i!=0:

		# print('back',self.weights)
		###############################################
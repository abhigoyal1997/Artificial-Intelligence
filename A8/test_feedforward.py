import nn
import sys
import numpy as np
import _pickle as cPickle
from util import readMNIST

np.random.seed(0)

X1 = np.asarray([2, 3])
nn1 = nn.NeuralNetwork(2, 2, 1, [1], 0.0, 1, 1)
activations = nn1.feedforward(X1)
activations = np.asarray(activations)
actRound = []
for i in range(len(activations)):
	actRound.append(np.around(activations[i].astype(np.double), 6))

actRound = np.asarray(actRound)
# print(actRound)

f=open("testcases/t1.pkl", "wb")
cPickle.dump(activations, f)
f.close()

f=open("testcases/testcase1.pkl", 'rb')
trueActivations = cPickle.load(f)
f.close()

f=open("testcases/t1.pkl", 'rb')
studActivations = cPickle.load(f)
f.close()

print("Your output :", studActivations)
print("Expected output : ", trueActivations)


correct = True

if len(activations) != len(trueActivations):
	correct = False
	print("Shape of the 'returned activations' did not match")

if correct and type(activations) != type(trueActivations):
	correct = False
	print("Type of returned 'activations' is incorrect")

if correct:
	for i in range(len(trueActivations)):
		if np.array_equal(trueActivations[i], studActivations[i]):
			pass
		else:
			print("Values Don't Match")
			correct = False
			break

if correct:
	print("Test Case 1 Passed")
else:
	print("Test Case 1 Failed")

XTrain, _, _, _, _, _ = readMNIST()
X2 = np.asarray(XTrain[0])
nn2 = nn.NeuralNetwork(784, 10, 1, [100], 0.0, 1, 1)
activations = nn2.feedforward(X2)
activations = np.asarray(activations)

actRound = []
for i in range(len(activations)):
	actRound.append(np.around(activations[i].astype(np.double), 6))

actRound = np.asarray(actRound)
# print(actRound)

f=open("testcases/t2.pkl", "wb")
cPickle.dump(actRound, f)
f.close()

f=open("testcases/testcase2.pkl", 'rb')
trueActivations = cPickle.load(f)
f.close()

f=open("testcases/t2.pkl", 'rb')
studActivations = cPickle.load(f)
f.close()

# print("Your output :", studActivations)
# print("Expected output : ", trueActivations)


correct = True

if len(activations) != len(trueActivations):
	correct = False
	print("Shape of the 'returned activations' did not match")

if correct and type(activations) != type(trueActivations):
	correct = False
	print("Type of returned 'activations' is incorrect")

if correct:
	for i in range(len(trueActivations)):
		if np.array_equal(trueActivations[i], studActivations[i]):
			pass
		else:
			print("Values Don't Match")
			correct = False
			break

if correct:
	print("Test Case 2 Passed")
else:
	print("Test Case 2 Failed")

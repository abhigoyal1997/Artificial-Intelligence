import sys
from util import *
from visualize import *
import numpy as np

# Script Usage: python3 visualizeTruth.py <task>

def visualizeGroundTruth(task=1):
	if task == 1:
		XTrain, YTrain, XVal, YVal, XTest, YTest = readLinear()
		groundTruth=np.argmax(YTest, axis=1)
		drawLinear(XTest,groundTruth)
	elif task == 2:
		XTrain, YTrain, XVal, YVal, XTest, YTest = readSquare()
		groundTruth=np.argmax(YTest, axis=1)
		drawSquare(XTest,groundTruth)
	elif task == 3:
		XTrain, YTrain, XVal, YVal, XTest, YTest = readCircle()
		groundTruth=np.argmax(YTest, axis=1)
		drawCircle(XTest,groundTruth)
	elif task == 4:
		XTrain, YTrain, XVal, YVal, XTest, YTest = readSemiCircle()
		groundTruth=np.argmax(YTest, axis=1)
		drawSemiCircle(XTest,groundTruth)

visualizeGroundTruth(int(sys.argv[1]))
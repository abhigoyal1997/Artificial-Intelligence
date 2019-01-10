# multiAgents.py
# --------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

class ReflexAgent(Agent):
		"""
			A reflex agent chooses an action at each choice point by examining
			its alternatives via a state evaluation function.

			The code below is provided as a guide.  You are welcome to change
			it in any way you see fit, so long as you don't touch our method
			headers.
		"""


		def getAction(self, gameState):
				"""
				You do not need to change this method, but you're welcome to.

				getAction chooses among the best options according to the evaluation function.

				Just like in the previous project, getAction takes a GameState and returns
				some Directions.X for some X in the set {North, South, West, East, Stop}
				"""
				# Collect legal moves and successor states
				legalMoves = gameState.getLegalActions()

				# Choose one of the best actions
				scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
				bestScore = max(scores)
				bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
				chosenIndex = random.choice(bestIndices) # Pick randomly among the best

				"Add more of your code here if you want to"

				return legalMoves[chosenIndex]

		def evaluationFunction(self, currentGameState, action):
				"""
				Design a better evaluation function here.

				The evaluation function takes in the current and proposed successor
				GameStates (pacman.py) and returns a number, where higher numbers are better.

				The code below extracts some useful information from the state, like the
				remaining food (newFood) and Pacman position after moving (newPos).
				newScaredTimes holds the number of moves that each ghost will remain
				scared because of Pacman having eaten a power pellet.

				Print out these variables to see what you're getting, then combine them
				to create a masterful evaluation function.
				"""
				# Useful information you can extract from a GameState (pacman.py)
				successorGameState = currentGameState.generatePacmanSuccessor(action)
				newPos = successorGameState.getPacmanPosition()
				newFood = successorGameState.getFood()
				newGhostStates = successorGameState.getGhostStates()
				newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

				"*** YOUR CODE HERE ***"

				if successorGameState.isWin():
					return successorGameState.getScore()
				if successorGameState.isLose():
					return -float('inf')

				ghostDist = [manhattanDistance(newPos, ghostState.getPosition()) for ghostState in newGhostStates]

				closestFood = float('inf')
				n, m = newFood.width, newFood.height
				for i in range(0,n):
					for j in range(0,m):
						if newFood[i][j]:
							closestFood = min(closestFood, manhattanDistance(newPos, (i,j)))

				return successorGameState.getScore() - 0.5*closestFood + 0.5*min(ghostDist)

def scoreEvaluationFunction(currentGameState):
		"""
			This default evaluation function just returns the score of the state.
			The score is the same one displayed in the Pacman GUI.

			This evaluation function is meant for use with adversarial search agents
			(not reflex agents).
		"""
		return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
		"""
			This class provides some common elements to all of your
			multi-agent searchers.  Any methods defined here will be available
			to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

			You *do not* need to make any changes here, but you can if you want to
			add functionality to all your adversarial search agents.  Please do not
			remove anything, however.

			Note: this is an abstract class: one that should not be instantiated.  It's
			only partially specified, and designed to be extended.  Agent (game.py)
			is another abstract class.
		"""

		def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
				self.index = 0 # Pacman is always agent index 0
				self.evaluationFunction = util.lookup(evalFn, globals())
				self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
		"""
			Your minimax agent (question 2)
		"""

		def getAction(self, gameState):
				"""
					Returns the minimax action from the current gameState using self.depth
					and self.evaluationFunction.

					Here are some method calls that might be useful when implementing minimax.

					gameState.getLegalActions(agentIndex):
						Returns a list of legal actions for an agent
						agentIndex=0 means Pacman, ghosts are >= 1

					gameState.generateSuccessor(agentIndex, action):
						Returns the successor game state after an agent takes an action

					gameState.getNumAgents():
						Returns the total number of agents in the game
				"""
				"*** YOUR CODE HERE ***"
				return self.getValue(gameState, self.depth, self.index)[1]

		def getValue(self, state, depth, agent):
				if depth == 0 or state.isWin() or state.isLose():
					return (self.evaluationFunction(state), None)

				maxAgent = False
				if agent == 0:
					maxAgent = True
					
				legalMoves = state.getLegalActions(agent)
				action = None
				
				if maxAgent:
					val = -float('inf')
				else:
					val = float('inf')

				nextAgent = (agent+1)%state.getNumAgents()
				if nextAgent == 0:
					depth -= 1

				for a in legalMoves:
					iVal = self.getValue(state.generateSuccessor(agent, a), depth, nextAgent)[0]

					if (maxAgent and val < iVal) or (not maxAgent and val > iVal):
						val = iVal
						action = a

				return (val, action)

class AlphaBetaAgent(MultiAgentSearchAgent):
		"""
			Your minimax agent with alpha-beta pruning (question 3)
		"""

		def getAction(self, gameState):
				"""
					Returns the minimax action using self.depth and self.evaluationFunction
				"""
				"*** YOUR CODE HERE ***"
				return self.getValue(gameState, -float('inf'), float('inf'), self.depth, self.index)[1]

		def getValue(self, state, alpha, beta, depth, agent):
				if depth == 0 or state.isWin() or state.isLose():
					return (self.evaluationFunction(state), None)

				maxAgent = False
				if agent == 0:
					maxAgent = True
					
				legalMoves = state.getLegalActions(agent)
				action = None
				
				if maxAgent:
					val = -float('inf')
				else:
					val = float('inf')

				nextAgent = (agent+1)%state.getNumAgents()
				if nextAgent == 0:
					depth -= 1

				for a in legalMoves:
					iVal = self.getValue(state.generateSuccessor(agent, a), alpha, beta, depth, nextAgent)[0]

					if (maxAgent and val < iVal) or (not maxAgent and val > iVal):
						val = iVal
						action = a

					if (maxAgent and val > beta) or (not maxAgent and val < alpha):
						return (val, action)

					if maxAgent:
						alpha = max(alpha, val)
					else:
						beta = min(beta, val)

				return (val, action)


def betterEvaluationFunction(currentGameState):
		"""
			Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
			evaluation function (question 5).

			DESCRIPTION: This function evaluates the current state of game using 
					features including the current score, the manhattan distance to
					the closest food point, the manhattan distance to the closest ghost
					and the minimum scared time among all the ghosts
		"""
		"*** YOUR CODE HERE ***"
		# util.raiseNotDefined()

		newPos = currentGameState.getPacmanPosition()
		newFood = currentGameState.getFood()
		newGhostStates = currentGameState.getGhostStates()
		newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

		"*** YOUR CODE HERE ***"

		if currentGameState.isWin():	# if it is a win state, return the actual score of the game (to differentiate among different win states)
			return currentGameState.getScore()
		if currentGameState.isLose():	# if it is a lose state, return -infinity (because we never wanna loose)
			return -float('inf')

		ghostDist = [manhattanDistance(newPos, ghostState.getPosition()) for ghostState in newGhostStates]	# calculating the distance to all the ghosts
		closestGhostDist = float('inf')
		closestGhost = -1
		for i in range(0, len(ghostDist)):	# fidn the mannhattan distance to the closest ghost
			if closestGhostDist > ghostDist[i]:
				closestGhostDist = ghostDist[i]
				closestGhost = i

		if newScaredTimes[closestGhost] != 0:	# if the closet ghost is scared, pacman can move towards it to eat it (to get extra points)
			closestGhostDist *= -3

		# the following snippet calculates the minimum manhattan distance to a food item
		closestFood = float('inf')
		n, m = newFood.width, newFood.height
		for i in range(0,n):
			for j in range(0,m):
				if newFood[i][j]:
					closestFood = min(closestFood, manhattanDistance(newPos, (i,j)))

		# finally combine all the features
		# positive features : score, min ghost distance (better that normal ghosts are far away p.s. in case of scared ghosts, this feature is negative), min scared time (better if ghosts are scared for more time)
		# negative features : distance to the closest food item (the closer the better) 
		return currentGameState.getScore() - 0.5*closestFood + 0.2*closestGhostDist + 0.5*min(newScaredTimes)

# Abbreviation
better = betterEvaluationFunction
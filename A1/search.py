# search.py
# ---------
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


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util

class SearchProblem:
	"""
	This class outlines the structure of a search problem, but doesn't implement
	any of the methods (in object-oriented terminology: an abstract class).

	You do not need to change anything in this class, ever.
	"""

	def getStartState(self):
		"""
		Returns the start state for the search problem.
		"""
		util.raiseNotDefined()

	def isGoalState(self, state):
		"""
		  state: Search state

		Returns True if and only if the state is a valid goal state.
		"""
		util.raiseNotDefined()

	def getSuccessors(self, state):
		"""
		  state: Search state

		For a given state, this should return a list of triples, (successor,
		action, stepCost), where 'successor' is a successor to the current
		state, 'action' is the action required to get there, and 'stepCost' is
		the incremental cost of expanding to that successor.
		"""
		util.raiseNotDefined()

	def getCostOfActions(self, actions):
		"""
		 actions: A list of actions to take

		This method returns the total cost of a particular sequence of actions.
		The sequence must be composed of legal moves.
		"""
		util.raiseNotDefined()


def tinyMazeSearch(problem):
	"""
	Returns a sequence of moves that solves tinyMaze.  For any other maze, the
	sequence of moves will be incorrect, so only use this for tinyMaze.
	"""
	from game import Directions
	s = Directions.SOUTH
	w = Directions.WEST
	return  [s, s, w, s, w, w, s, w]

def depthFirstSearch(problem):
	"""
	Search the deepest nodes in the search tree first.

	Your search algorithm needs to return a list of actions that reaches the
	goal. Make sure to implement a graph search algorithm.

	To get started, you might want to try some of these simple commands to
	understand the search problem that is being passed in:
	
	print "Start:", problem.getStartState()
	print "Is the start a goal?", problem.isGoalState(problem.getStartState())
	print "Start's successors:", problem.getSuccessors(problem.getStartState())
	"""

	explored = {}
	exploredList = []
	nodeCounter = 0

	frontier = util.Stack()
	frontier.push((problem.getStartState(), None, None, 0))

	while not frontier.isEmpty():
		node = frontier.pop()
		if problem.isGoalState(node[0]):
			return reconstructPath(exploredList, node)

		exploredList.append(node)
		explored[node[0]] = True

		successors = problem.getSuccessors(node[0])
		for s in successors:
			if s[0] not in explored:
				frontier.push((s[0], nodeCounter, s[1], node[3] + s[2]))

		nodeCounter += 1

def breadthFirstSearch(problem):
	"""Search the shallowest nodes in the search tree first."""

	visited = {}
	exploredList = []
	nodeCounter = 0

	frontier = util.Queue()
	frontier.push((problem.getStartState(), None, None, 0))
	visited[problem.getStartState()] = True

	while not frontier.isEmpty():
		node = frontier.pop()
		if problem.isGoalState(node[0]):
			return reconstructPath(exploredList, node)

		exploredList.append(node)

		successors = problem.getSuccessors(node[0])
		for s in successors:
			if s[0] not in visited:
				frontier.push((s[0], nodeCounter, s[1], node[3] + s[2]))
				visited[s[0]] = True

		nodeCounter += 1

def uniformCostSearch(problem):
	"""Search the node of least total cost first."""

	visited = {}
	exploredList = []
	nodeCounter = 0
	
	frontier = util.PriorityQueue()
	frontier.push((problem.getStartState(), None, None, 0), 0)
	visited[problem.getStartState()] = 0

	while not frontier.isEmpty():
		node = frontier.pop()
		if problem.isGoalState(node[0]):
			return reconstructPath(exploredList, node)

		exploredList.append(node)

		successors = problem.getSuccessors(node[0])
		for s in successors:
			if s[0] in visited and node[3] + s[2] < visited[s[0]]:
				frontier.update(s[0], node[3] + s[2])
				visited[s[0]] = node[3] + s[2]
			elif s[0] not in visited:
				frontier.push((s[0], nodeCounter, s[1], node[3] + s[2]), node[3] + s[2])
				visited[s[0]] = node[3] + s[2]
				
		nodeCounter += 1

def nullHeuristic(state, problem=None):
	"""
	A heuristic function estimates the cost from the current state to the nearest
	goal in the provided SearchProblem.  This heuristic is trivial.
	"""
	return 0

def aStarSearch(problem, heuristic=nullHeuristic):
	"""Search the node that has the lowest combined cost and heuristic first."""
	
	visited = {}
	exploredList = []
	nodeCounter = 0
	
	frontier = util.PriorityQueue()
	hcost = heuristic(problem.getStartState(), problem)
	frontier.push((problem.getStartState(), None, None, 0), hcost)
	visited[problem.getStartState()] = hcost

	while not frontier.isEmpty():
		node = frontier.pop()
		if problem.isGoalState(node[0]):
			return reconstructPath(exploredList, node)

		exploredList.append(node)

		successors = problem.getSuccessors(node[0])
		for s in successors:
			hcost = node[3] + s[2] + heuristic(s[0], problem)
			snode = (s[0], nodeCounter, s[1], node[3] + s[2])
			if s[0] in visited and hcost < visited[s[0]]:
				frontier.update(snode, hcost)
				visited[s[0]] = hcost
			elif s[0] not in visited:
				frontier.push(snode, hcost)
				visited[s[0]] = hcost
				
		nodeCounter += 1

def reconstructPath(listNodes, node):
	path = []
	while node[1] != None:
		path.insert(0,node[2])
		node = listNodes[node[1]]

	return path


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch

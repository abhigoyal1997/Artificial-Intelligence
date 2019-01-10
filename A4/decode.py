import sys

gridFile = open(sys.argv[1], 'r')
policyFile = open(sys.argv[2], 'r')

grid_data = [x.split() for x in gridFile.readlines()]
policy = [x.split()[1] for x in policyFile.readlines()[:-1]]

nStates = 0

actions = ['N', 'E', 'S', 'W']

nRows = len(grid_data)
nCols = len(grid_data[0])

north = 0
east = 1
south = 2
west = 3

start = None
end = None

def getNextPos(i, j, a):
	if a == north:
		return (i-1, j)
	if a == east:
		return (i, j+1)
	if a == south:
		return (i+1, j)
	if a == west:
		return (i, j-1)

state_dict = {}

for i in range(0,nRows):
	for j in range(0, nCols):
		val = int(grid_data[i][j])
		if val == 2:
			start = (i, j)
		elif val == 3:
			end = (i, j)
		elif val == 1:
			continue

		state_dict[(i, j)] = nStates
		nStates += 1

pos = start
path = ''
while pos != end:
	a = int(policy[state_dict[pos]])
	path += actions[a] + ' '
	pos = getNextPos(pos[0], pos[1], a)

print(path)
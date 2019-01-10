import sys

gridFile = open(sys.argv[1], 'r')

grid_data = [x.split() for x in gridFile.readlines()]

nStates = 0
nActions = 4
start = -1
end = -1
transitions = []
gamma = 1

state_dict = {}

nRows = len(grid_data)
nCols = len(grid_data[0])

north = 0
east = 1
south = 2
west = 3

for i in range(0,nRows):
	for j in range(0, nCols):
		val = int(grid_data[i][j])
		if val == 2:
			start = nStates
		elif val == 3:
			end = nStates
		elif val == 1:
			continue

		state_dict[(i, j)] = nStates
		if i != 0 and int(grid_data[i-1][j]) != 1:
			transitions.append((nStates, north, state_dict[(i-1, j)]))
			transitions.append((state_dict[(i-1, j)], south, nStates))

		if j != 0 and int(grid_data[i][j-1]) != 1:
			transitions.append((nStates, west, state_dict[(i, j-1)]))
			transitions.append((state_dict[(i, j-1)], east, nStates))

		nStates += 1

reward = -1
prob = 1

print('numStates', nStates)
print('numActions', nActions)
print('start', start)
print('end', end)
for x in transitions:
	print('transitions', x[0], x[1], x[2], reward, prob)
print('discount', gamma)
import sys, operator

mdpFile = open(sys.argv[1], 'r')

data = [x.split() for x in mdpFile.readlines()]

nStates = int(data[0][1])
nActions = int(data[1][1])
start = int(data[2][1])
end = int(data[3][1])

transition_data = data[4:-1]

transitions = {}
valid_actions = {}
for x in transition_data:
	s, a, sp, r, p = int(x[1]), int(x[2]), int(x[3]), float(x[4]), float(x[5])
	if (s, a) not in transitions:
		transitions[(s, a)] = [(sp, r, p)]
		if s not in valid_actions:
			valid_actions[s] = [a]
		else:
			valid_actions[s].append(a)
	else:
		transitions[(s, a)].append((sp, r, p))

gamma = float(data[-1][1])

epsilon = 10**(-16)
v_old = [-float('inf')]*nStates
v = [0.0]*nStates
t = 0

while max(list(map(operator.abs, map(operator.sub, v, v_old)))) > epsilon:
	v_old = v[:]
	for s in range(0,nStates):
		if s == end:
			continue
		v[s] = max([sum(list(map(lambda x: x[2]*(x[1] + gamma*v_old[x[0]]), transitions[(s, a)]))) for a in valid_actions[s]])
	t += 1

p = [None]*nStates

for s in range(0, nStates):
	if s == end:
		p[s] = -1
	else:
		v_list = [sum(list(map(lambda x: x[2]*(x[1] + gamma*v[x[0]]), transitions[(s, a)]))) for a in valid_actions[s]]
		index, value = max(enumerate(v_list), key=operator.itemgetter(1))
		p[s] = valid_actions[s][index]
	print(round(v[s], 11), p[s])

print('iterations', t)
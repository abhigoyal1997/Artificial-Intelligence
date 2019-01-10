import sys
from tasks import *

# Script Usage: python3 test.py <task_num> <seed>
# Read task number and seed value from command line
task_num=int(sys.argv[1])
seed=int(sys.argv[2])

np.random.seed(int(seed))

task={
	1 : taskLinear,
	2 : taskSquare,
	3 : taskCircle,
	4 : taskSemiCircle,
	5 : taskMnist
}

task[task_num]()
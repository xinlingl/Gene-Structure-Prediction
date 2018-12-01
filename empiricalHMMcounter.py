import itertools
import sys
import numpy as np
from transitionIndex import transitionIndex, OBSERVATION_INDICES

n =  sys.argv[1]
print n
n = int(n)
file_nucleotides = sys.argv[2]
file_annotations = sys.argv[3]

#Reading in and organizing input file data
def openFile(input_file):
    s = ""
    with open(input_file) as f:
        lines = f.read().splitlines()
        for num in range(0,len(lines)):
            if lines[num][0] != ">":
                s+=str(lines[num])
    return s


def count_params(n, file_nucleotides, file_annotations):
    obs_string = openFile(file_nucleotides)
    state_string = openFile(file_annotations)

    # TODO: Create matrix of zeros with 9^n*4^n rows and 9 columns
    transitionMatrix = np.zeros(((9**n)*(4**n),9))
    print transitionMatrix

    for i in range(0, len(obs_string)-n+1):
        obs = obs_string[i:i+n]
        state = state_string[i:i+n]
        row_index = transitionIndex(state, obs)
        col_index = OBSERVATION_INDICES[obs]
        transitionMatrix[row_index, col_index] += 1

    # TODO: normalize each row by its sum
    for j in range(0, transitionMatrix):
        sumRows = 0
        for k in range(0, transitionMatrix[0]):
            sumRows = sumRows + transitionMatrix[0][k]
        for l in range(0, transitionMatrix[0]):
            transitionMatrix[0] = transitionMatrix[0]/sumRows

    return transitionMatrix

nucleotide_file = openFile(file_nucleotides)

annotations_file = openFile(file_annotations)

#x = count_params(2,nucleotide_file,annotations_file)
#print x




#combos =  list(itertools.permutations('ACGT', num_read))

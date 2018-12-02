import itertools
import sys
import numpy as np
from transitionIndex import transitionIndex, OBSERVATION_INDICES

n =  sys.argv[1]
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
    transitionMatrix = [][]
    
    for i in range(0, len(obs_string)-n+1):
        obs = obs_string[i:i+n]
        state = state_string[i:i+n]
        row_index = transitionIndex(state, obs)
        col_index = OBSERVATION_INDICES[obs]
        transitionMatrix[row_index, col_index] += 1

    # TODO: normalize each row by its sum
        
    


#combos =  list(itertools.permutations('ACGT', num_read))

#transitionMatrix = np.zeros((9,9))
#combinationMatrix = np.zeros((len(combos),9))

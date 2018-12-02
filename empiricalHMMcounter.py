import itertools
import sys
import numpy as np

STATE_INDICES = {
    'N' : 0,
    'E' : 1,
    'I' : 2,
    'p' : 3,
    'P' : 4,
    'Z' : 5,
    'z' : 6,
    's' : 7,
    'S' : 8,
}


OBSERVATION_INDICES = {
    'A' : 0,
    'C' : 1,
    'G' : 2,
    'T' : 3,
}


def transitionIndex(states, observations):
    row_index = 0
    n = len(states)
    for i in range(0, n):
        o_i = OBSERVATION_INDICES[observations[i]]
        s_i = STATE_INDICES[states[i]]
        row_index += s_i *(9**i * 4**n) + o_i*(4**i)
    return row_index

#Reading in and organizing input file data
def openFile(input_file_nucleotides, input_file_annotations):
    s = ""
    t = ""
    with open(input_file_nucleotides) as f, open(input_file_annotations) as g:
        lines_nuc = f.read().splitlines()
        lines_annot = g.read().splitlines()
        for num in range(0,len(lines_nuc)):
            if lines_nuc[num][0] != ">":
                s+=str(lines_nuc[num])
            if lines_annot[num][0] != ">":
                t+=str(lines_annot[num])
    return s,t


def count_params_transition(n, file_nucleotides, file_annotations):
    obs_string, state_string = openFile(file_nucleotides, file_annotations)

    # TODO: Create matrix of zeros with 9^n*4^n rows and 9 columns
    transitionMatrix = np.ones(((9**n)*(4**n),9))
    emissionMatrix = np.ones((4,9))

    for i in range(0, len(obs_string)-n):
        obs = obs_string[i:i+n]
        state = state_string[i:i+n]
        row_index = transitionIndex(state, obs)
        col_index = STATE_INDICES[state_string[i+n]]
        transitionMatrix[row_index][col_index] = np.add(transitionMatrix[row_index][col_index], 1)

    for j in range(0, len(transitionMatrix)):
        sumRows = float(sum(transitionMatrix[j]))
        transitionMatrix[j] = transitionMatrix[j]/sumRows

    for k in range(0,len(obs_string)):
        obs_emit = obs_string[k]
        state_emit = state_string[k]
        obs_i = OBSERVATION_INDICES[obs_emit]
        state_i = STATE_INDICES[state_emit]
        emissionMatrix[obs_i,state_i] = emissionMatrix[obs_i,state_i]+1

    for l in range(0, len(emissionMatrix)):
        sumRows = float(sum(emissionMatrix[l]))
        emissionMatrix[l] = emissionMatrix[l]/sumRows


    return transitionMatrix, emissionMatrix

n =  sys.argv[1]
n = int(n)
file_nucleotides = sys.argv[2]
file_annotations = sys.argv[3]

transition_matrix, emission_matrix = count_params_transition(2,file_nucleotides,file_annotations)
for i in range(0,100):
    print transition_matrix[i]

print emission_matrix

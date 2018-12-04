from random import randint, uniform
import numpy as np
from transitionIndex import transitionIndex, STATE_INDICES, OBSERVATION_INDICES


STATES = ['N', 'E','I', 'p', 'P', 'Z', 'z', 's', 'S']


def calc_total_prob(n, state_str, obs_str, transitionMatrix, emissionMatrix, initial_transition_matrices, initial_state_probs):
    total_prob = 1
    total_prob = total_prob * initial_state_probs[STATE_INDICES[state_str[0]]]

    for i in range(1,n):
        state = state_str[:i]
        obs = obs_str[:i]
        row_index = transitionIndex(state, obs)
        col_index = STATE_INDICES[state_str[i + 1]]
        total_prob * initial_transition_matrices[i-1][row_index, col_index]

    for i in range(n, len(state_str)-1):
        prev_states = state_str[i-n: i]
        prev_obs = obs_str[i-n: i]
        cur_state = state_str[i+1]
        cur_obs = obs_str[i+1]
        total_prob =  total_prob * transitionMatrix[transitionIndex(prev_states,prev_obs), STATE_INDICES[cur_state]] * emissionMatrix[OBSERVATION_INDICES[cur_obs], STATE_INDICES[cur_state]]
    return total_prob


def calc_pi(state_str, obs_str, i, n, transitionMatrix, emissionMatrix):
    prev_states = state_str[i - n:i]
    prev_obs = obs_str[i-n:i]
    obs = obs_str[i]
    cur_state = state_str[i]
    return transitionMatrix[transitionIndex(prev_states, prev_obs)][STATE_INDICES[cur_state]] * emissionMatrix[
        OBSERVATION_INDICES[obs], STATE_INDICES[cur_state]]


def gibbsSampler(transitionMatrix, emissionMatrix, obs_str, iterations, n, initial_transition_matrices, initial_state_probs):
    # Start with random state str
    #state_str = "N" * len(obs_str)
    state_str = ""
    for i in range(0, len(obs_str)):
        state_str += STATES[randint(0,len(STATES)-1)]

    cur_p = calc_total_prob(n, state_str, obs_str, transitionMatrix, emissionMatrix, initial_transition_matrices, initial_state_probs)
    if cur_p == 0:
        cur_p += 1e-5
    print cur_p
    for i in range(0, iterations): # maybe a size proportional to the input?
        assert len(state_str) == len(obs_str), str(i)

        obs_i = randint(n, len(obs_str) - 1) # should allow 0 -> n and handle edge cases with initial_trnasition_matrices and initial_state_probs
        obs = obs_str[obs_i]

        prev_obs = obs_str[obs_i-n:obs_i]
        prev_states = state_str[obs_i-n:obs_i]

        ps = [] # each possible state's probability
        for state in STATES:
            ps.append(transitionMatrix[transitionIndex(prev_states,prev_obs)][STATE_INDICES[state]])

        ps = np.array(ps)
        ps = ps/float(sum(ps))

        dart = uniform(0,1)
        threshold = 0
        for j, p in enumerate(ps):  # pick a new state based on its probability
            threshold += p
            if dart < threshold:
                break

        # REJECTION SAMPLER - decision in logic of while loop
        new_state_str = state_str[:obs_i] + STATES[j] + state_str[obs_i + 1:]
        new_p = cur_p
        for j in range(0,n):
            if obs_i + j == len(obs_str):
                break
            new_p = new_p / calc_pi(state_str, obs_str, obs_i + j, n, transitionMatrix, emissionMatrix)
            new_p = new_p * calc_pi(new_state_str, obs_str, obs_i+j, n, transitionMatrix, emissionMatrix)

        if new_p >= cur_p:
            state_str = new_state_str
    return state_str



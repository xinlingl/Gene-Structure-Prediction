from random import randint, uniform
import numpy as np
from transitionIndex import transitionIndex, STATE_INDICES, OBSERVATION_INDICES


STATES = ['N', 'E','I', 'p', 'P', 'Z', 'z', 's', 'S']


def calc_total_prob(n, state_str, obs_str, transitionMatrix, emissionMatrix, initial_transition_matrices, intial_state_probs):
    total_prob = 1
    total_prob = total_prob * intial_state_probs[STATE_INDICES[state_str[0]]]

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



def gibbsSampler(transitionMatrix, emissionMatrix, obs_str, iterations, n, initial_transition_matrices, initial_state_probs):
    # Start with random state str
    state_str = "N" * len(obs_str)
    cur_p = calc_total_prob(n, state_str, obs_str, transitionMatrix, emissionMatrix, initial_transition_matrices,
                            initial_state_probs)
    print cur_p
    for i in range(0, iterations): # maybe a size proportional to the input?
        assert len(state_str) == len(obs_str), str(i)

        obs_i = randint(n, len(obs_str)) # should allow 0 -> n and handle edge cases with initial_trnasition_matrices and initial_state_probs
        print obs_i
        obs = obs_str[obs_i]

        prev_obs = obs_str[obs_i-n:obs_i]
        prev_states = state_str[obs_i-n:obs_i]

        ps = []
        for state in STATES:
            if len(prev_states) != len(prev_obs):
                print obs_i
                print n
                print prev_states
                print prev_obs
                exit()
            ps.append(transitionMatrix[transitionIndex(prev_states,prev_obs)][STATE_INDICES[state]])

        ps = np.array(ps)
        ps = ps/float(sum(ps))

        dart = uniform(0,1)
        threshold = 0
        for j, p in enumerate(ps):
            threshold += p
            if dart < threshold:
                break

        # REJECTION SAMPLER - decision in logic of while loop

        new_state_str = state_str[:obs_i] + STATES[j] + state_str[obs_i+1:]
        cur_state = state_str[obs_i]

        new_p = cur_p / (transitionMatrix[transitionIndex(prev_states,prev_obs)][STATE_INDICES[cur_state]] *
                         emissionMatrix[OBSERVATION_INDICES[obs], STATE_INDICES[cur_state]] )* p * emissionMatrix[OBSERVATION_INDICES[obs], j]
        #calc_total_prob(n,new_state_str, obs_str, transitionMatrix, emissionMatrix, initial_transition_matrices, initial_state_probs)
        if new_p >= cur_p:
            cur_p = new_p
            state_str = new_state_str
    return state_str



from random import randint, uniform
import numpy as np
from transitionIndex import transitionIndex, STATE_INDICES


STATES = ['N', 'E','I', 'p', 'P', 'Z', 'z', 's', 'S']


def calc_total_prob(n, state_str, obs_str, transitionMatrix, emissionMatrix):
    total_prob = 1
    for i in range(n, len(state_str)-1):
        prev_states = state_str[i-n: i]
        prev_obs = obs_str[i-n: i]
        cur_state = state_str[i+1]
        cur_obs = obs_str[i+1]
        total_prob =  total_prob * transitionMatrix[transitionIndex(prev_states,prev_obs), STATE_INDICES[cur_state]] * emissionMatrix[cur_obs]
    return total_prob




def gibbsSampler(transitionMatrix, emissionMatrix, obs_str, iterations, n):
    # Start with random state str
    state_str = ""
    for i in range(0, len(obs_str)):
        state_str += STATES[randint(0,8)]

    for i in range(0, iterations ): # maybe a size proportional to the input?
        cur_p = 0
        new_p = 0

        while new_p <= cur_p:
            obs_i = randint(n, len(obs_str))
            obs = obs_str[obs_i]

            prev_obs = obs[obs_i-n:obs_i]
            prev_states = state_str[obs_i]

            ps = []
            for state in STATES:
                ps.append(transitionMatrix[transitionIndex(prev_states,prev_obs)][STATE_INDICES[state]])

            ps = np.array(ps)
            ps = ps/float(sum(ps))
            print sum(ps)

            dart = uniform(0,1)
            threshold = 0
            for j, p in enumerate(ps):
                threshold += p
                if dart < p:
                    break

            # REJECTION SAMPLER

            new_state_str = state_str[:obs_i] + STATES[j] + state_str[obs_i+1:]
            cur_p = calc_total_prob(state_str, obs_str,transitionMatrix, emissionMatrix)
            new_p = calc_total_prob(new_state_str, obs_str, transitionMatrix, emissionMatrix)
        state_str = new_state_str
    return state_str



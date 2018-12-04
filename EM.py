import numpy as np
from annotation import load_state, OBS_DICT
from forward_backward import initialization, forward, backward


def EM(filename):
    # states are the true labels
    # observations are the training data
    states, observations = load_state(filename)
    print(states)
    print(observations)
    nepoch = 1
    for e in range(nepoch):
        if e == 0:
            # initialize lambda.
            # lambda are the parameters that we want to optimize.
            # it contains a initial state distribution pi = {pi1, ..., pin}
            # a transition matrix p, shape is (n_hidden_states, n_hidden_states)
            # an emission matrix B, shape is (n_hidden_states, n_unique_obs)
            pi, p, B = initialization()

        # forward
        alpha = forward(observations, pi, p, B)
        alpha = np.array(alpha)

        # backward
        beta = backward(observations, pi, p, B)
        beta = np.array(beta)

        # expectation
        C_list, gamma = Expectation(alpha, beta, p, B, observations)

        # maximization
        pi, p, B = Maximization(C_list, gamma, observations)
    
    return pi, p, B

def Expectation(alpha, beta, p, B, observations):
    """
    Compute C_t(i,j) and gamma_it.
    Parameters:
    
    Return:
    C_t(i,j): the probability that go from state q_i to state q_j 
              during the transition from step t tp step t+1.
    gamma_it: the probability that the hidden state is q_i at step t.
    """
    timestep = len(alpha[0])
    C_list = []
    for t in range(timestep - 1):
        C = np.zeros((n_hidden_states, n_hidden_states))
        for i in range(len(alpha)):
            for j in range(len(beta)):
                C[i][j] = alpha[i][t] * p[i][j] * beta[j][t+1] * B[j][OBS_DICT[observations[t+1]]]
        denominator = np.sum(C)
        C = C / denominator
        C_list.append(C)
    C_list = np.array(C_list)
    print(C_list.shape)
    
    gamma = np.zeros((n_hidden_states, timestep))
    for i in range(n_hidden_states):
        for t in range(timestep-1):
            gamma[:, t] = np.sum(C_list[t], axis=1).T
    gamma[:, -1] = np.sum(C_list[-1], axis=0).T
    print("gamma", gamma)

    return C_list, gamma

def Maximization(C_list, gamma, observations):
    # estimate Pi
    pi = gamma[:, 0] # 1 x 9
    print("pi", pi)
    # estimate transition matrix p
    numerator = np.sum(C_list, axis=0)
    p = numerator / np.sum(gamma[:,:-1], axis=1) # 9 x 9
    print("p", p)
    # estimate emission matrix B
    B = np.zeros((n_hidden_states, n_unique_observations))
    observations_index = [0 for i in range(len(gamma[0]))]
    for i in range(len(gamma[0])):
            observations_index[i] = OBS_DICT[observations[i]]
    for k in range(n_unique_observations):
        mask = []
        for s in observations_index:
            if s == k:
                mask.append(True)
            else:
                mask.append(False)
        B[:, k] = np.sum(gamma[:, mask], axis=1) / np.sum(gamma, axis=1)
    print("B", B)
    
    return pi, p, B

if __name__ == '__main__':
    n_hidden_states = 9
    n_unique_observations = 4
    EM("")

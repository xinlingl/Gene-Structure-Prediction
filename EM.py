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

        # backward
        beta = backward(observations, pi, p, B)

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
    
    gamma = np.zeros((n_hidden_states, timestep-1))
    for i in range(n_hidden_states):
        for t in range(timestep-1):
            print(np.sum(C_list[t], axis=1))
            gamma[:, t] = np.sum(C_list[t], axis=1).T

    return C_list, gamma

def Maximization(C_list, gamma, observations):
    # estimate Pi
    pi = gamma[:, 0] # 1 x 9
    print("pi", pi)
    # estimate transition matrix p
    numerator = np.sum(np.array(C_list), axis=0)
    p = numerator / np.sum(gamma[:,:-1], axis=1) # 9 x 9
    print("p", p.shape)
    # estimate emission matrix B
    B = np.zeros((n_hidden_states, n_unique_observations))
    for k in range(n_unique_observations):
        mask = observations == k
        print(mask)
        B[:, k] = np.sum(gamma[:, mask], axis=1) / np.sum(gamma, axis=1)
    
    return pi, p, B


if __name__ == '__main__':
    n_hidden_states = 9
    n_unique_observations = 4
    EM("")

"""
# transition probability
p = np.array([
    [0.7, 0.3],
    [0.4, 0.6]
])

# emission probability
B = np.array([
    [0.5, 0.4, 0.1],
    [0.1, 0.3, 0.6]
])

# initial state distribution
pi = np.array([0.6, 0.4])

# [N, N, C, C, D, C, D, D, D, N]
observations = np.array([0, 0, 1, 1, 2])

# [H, H, H, H, F, F, F, F, F, H]
states = np.array([0, 0, 0, 0, 1])

alpha = np.array([
    [0.3, 0.113, 0.033464, 0.01132544, 0.001],
    [0.04, 0.114, 0.012222, 0.0052117, 0.0039147984]
])

beta = np.array([
    [0.0150296, 0.03976, 0.106, 0.25, 1],
    [0.0101792, 0.03712, 0.112, 0.4, 1]
])
"""
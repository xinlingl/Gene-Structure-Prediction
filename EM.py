import numpy as np
from annotation import load_state

def main():
    

# initialize lambda.
# lambda is the parameter that we want to optimize.
# it contains a initial state distribution pi = {pi1, ..., pin}
# a transition matrix p (2d array)
# an emission matrix B (2d array)

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
observations = np.array([0,0,1,1,2])

# [H, H, H, H, F, F, F, F, F, H]
states = np.array([0, 0, 0, 0, 1])
# pi = np.randn(9)
# p = np.randn((9, 9))
# B = np.randn((9, 4))

alpha = np.array([
    [0.3, 0.113, 0.033464, 0.01132544, 0.001],
    [0.04, 0.114, 0.012222, 0.0052117, 0.0039147984]
])

beta = np.array([
    [0.0150296, 0.03976, 0.106, 0.25, 1],
    [0.0101792, 0.03712, 0.112, 0.4, 1]
])

n_hidden_states = 2
n_unique_observations = 3

def Expectation(timestep):
    """
    Compute C_t(i,j) and gamma_it.
    Parameters:
    
    Return:
    C_t(i,j): the probability that go from state q_i to state q_j 
              during the transition from step t tp step t+1.
    gamma_it: the probability that the hidden state is q_i at step t.
    """
    C_list = []
    for t in range(timestep - 1):
        C = np.zeros((n_hidden_states, n_hidden_states))
        for i in range(len(alpha)):
            for j in range(len(beta)):
                C[i][j] = alpha[i][t] * p[i][j] * beta[j][t+1] * B[j][states[t+1]]
        denominator = np.sum(C)
        print("denominator", denominator)
        C = C / denominator
        C_list.append(C)
    
    gamma = np.zeros((n_hidden_states, timestep-1))
    for i in range(n_hidden_states):
        for t in range(timestep-1):
            print(np.sum(C_list[t], axis=1))
            gamma[:, t] = np.sum(C_list[t], axis=1).T
    print(gamma)

    return C_list, gamma

def Maximizeation(C_list, gamma):
    # estimate Pi
    pi = gamma[:, 0]
    print(pi)
    numerator = np.sum(np.array(C_list), axis=0)
    p = np.zeros((n_hidden_states, n_hidden_states))
    p = numerator / np.sum(gamma[:,-1], axis=1)
    print(p)
    b = np.zeros((n_hidden_states, n_unique_observations))
    for k in range(n_unique_observations):




if __name__ == '__main__':
    # states = load_state("./data/Mus_musculus.GRCm38.dna.chromosome.1.NoN_annotations.fa")
    Expectation(5)

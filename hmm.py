from hmmlearn import hmm
import numpy as np
from sklearn.metrics import confusion_matrix

obs = np.loadtxt( "../data/Mus_musculus.GRCm38.dna.chromosome.1.NoN.fa", dtype=str)[1][33714212:33834212]
states = np.loadtxt("../data/Mus_musculus.GRCm38.dna.chromosome.1.NoN_annotations.fa", dtype=str)[1][33714212:33834212]
STATE_DICT = {
    'N': 0,
    'E': 1,
    'I': 2, # intron
    'p': 3, # first base of an intron
    'P': 4, # second base of an intron
    'Z': 5, # second to last base of an intron
    'z': 6, # last base of an intron
    's': 7, # first base of an exon
    'S': 8 # second base of an exon
}
OBS_DICT = {
    'A': 0,
    'C': 1,
    'G': 2,
    'T': 3
}
initial_prob = {}
timestep = len(obs)
states_index = [0 for i in range(timestep)]
observations_index = [0 for i in range(timestep)]
print("timestep:", timestep)
for i in range(timestep):
    if states[i] not in initial_prob:
        initial_prob[states[i]] = 1
    else:
        initial_prob[states[i]] += 1
    states_index[i] = STATE_DICT[states[i]]
    observations_index[i] = OBS_DICT[obs[i]]
observations_index = np.array(observations_index).reshape(-1, 1)
print(observations_index.shape)
print(initial_prob)
initial_prob_list = []
for key in initial_prob:
    initial_prob_list.append(initial_prob[key])
initial_prob_list = np.array(initial_prob_list)
initial_prob_list = initial_prob_list / sum(initial_prob_list)
print(initial_prob_list)

model = hmm.MultinomialHMM(n_components=9, n_iter=1000, startprob_prior=initial_prob_list)
model.startprob_ = initial_prob_list
model.fit(observations_index)
prob, states = model.decode(observations_index)
np.savetxt("prediction.txt", states, fmt='%.0f')
print(states)

STATE_DICT = {
    'N': 0,
    'E': 1,
    'I': 2, # intron
    'p': 3, # first base of an intron
    'P': 4, # second base of an intron
    'Z': 5, # second to last base of an intron
    'z': 6, # last base of an intron
    's': 7, # first base of an exon
    'S': 8 # second base of an exon
}
REVERSE_DICT = {
    0: 'N',
    1: 'E',
    2: 'I',
    3: 'p',
    4: 'P',
    5: 'Z',
    6: 'z',
    7: 's',
    8: 'S'
}

preds = np.loadtxt("prediction.txt")
# preds_letter = []
# for i in range(len(preds)):
#     preds_letter.append(REVERSE_DICT[int(preds[i])])

# print(preds_letter)

print("!!!")
print(preds)

c_m = confusion_matrix(states_index, preds)


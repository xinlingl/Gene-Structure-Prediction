import numpy as np
from gibbsSampler import gibbsSampler
from empiricalHMMcounter import count_params_transition, openFile, initial_state_prob, transition_probs_to_n

def load_matrices(files):
    with open(files[0], "r") as f:
        initial_state_probs = [float(x) for x in f.readline().strip().split("\t")]

    transition_matrix = []
    with open(files[1], "r") as f:
        line = f.readline()
        while line != "":
            row = line.strip().split("\t")
            row = [float(x) for x in row]
            transition_matrix.append(row)
            line = f.readline()
    transition_matrix = np.array(transition_matrix)

    emission_matrix = []
    with open(files[2], "r") as f:
        line = f.readline()
        while line != "":
            row = line.strip().split("\t")
            row = [float(x) for x in row]
            emission_matrix.append(row)
            line = f.readline()
    emission_matrix = np.array(emission_matrix)

    initial_transition_matrices = []
    if len(files) > 3:
        for i in range(3, len(files)):
            m = []
            with open(files[i], "r") as f:
                line = f.readline()
                while line != "":
                    row = line.strip().split("\t")
                    row = [float(x) for x in row]
                    m.append(row)
                    line = f.readline()
                m = np.array(m)
            initial_transition_matrices.append(m)
    return initial_state_probs, transition_matrix, emission_matrix, initial_transition_matrices


def error_rate(s1, s2):
    num = sum([1 for a,b in zip(s1,s2) if a!=b])
    den = len(s1)
    return num /float(den)


def main(file_nucleotides, file_annotations, n):
    files = ["initial_state_probs.tab","emiprical_transition_matrix_n1.tab","emiprical_emission_matrix_n1.tab"]
    # n =1
    initial_state_probs, transition_matrix, emission_matrix, initial_transition_matrices = load_matrices(files)

    obs_str, state_str = openFile(file_nucleotides, file_annotations)

    iterations = len(obs_str) * 2

    new_state_str = gibbsSampler(transition_matrix, emission_matrix, obs_str, iterations, n, initial_transition_matrices,
                 initial_state_probs)

    print "empirical training error rate, n=1:", error_rate(state_str, new_state_str)
    exit()

    obs_str, state_str = openFile(file_nucleotides, file_annotations)
    initial_state_p = initial_state_prob([state_str])
    initial_transition_matrices = transition_probs_to_n(n, obs_str, state_str)


    with open("initial_state_probs.tab", "w") as f:
        line = [str(x) for x in initial_state_p]
        f.write("\t".join(line) + "\n")

    for i in range(0, len(initial_transition_matrices)):
        with open("initial_transition_matrices" + str(i) + ".tab", "w") as f:
            for row in initial_transition_matrices:
                line = [str(x) for x in row]
                f.write("\t".join(line)+ "\n")

    transition_matrix, emission_matrix = count_params_transition(n,file_nucleotides,file_annotations)

    print transition_matrix
    print emission_matrix

    with open("empirical_transition_matrix_n" + str(n)+".tab", "w"):
        for row in transition_matrix:
            line = [str(x) for x in row]
            f.write("\t".join(line) + "\n")

    with open("empirical_emission_matrix_n" + str(n)+".tab", "w"):
        for row in emission_matrix:
            line = [str(x) for x in row]
            f.write("\t".join(line) + "\n")


    #gibbsSampler(transition_matrix,emission_matrix,obs_str,len(obs_str)*5,n)






main("Mus_musculus.GRCm38.dna.chromosome.1.NoN.fa", "Mus_musculus.GRCm38.dna.chromosome.1.NoN_annotations.fa", 1)
import numpy as np
from gibbsSampler import gibbsSampler
from empiricalHMMcounter import count_params_transition, openFile, initial_state_prob, transition_probs_to_n
import matplotlib.pyplot as plt

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
    num_wrong = [1 for a,b in zip(s1,s2) if a!=b]
    num = sum(num_wrong)
    den = len(s1)
    return num /float(den)


def analyze_result(new_string, real_string):
    er_num = 0# error rate
    er_den = 0
    sS_num = 0
    sS_den = 0# start site sensitivity - s, S
    pP_num = 0
    pP_den = 0# Intron beginning sensitivity - p, P
    zZ_den = 0
    zZ_num = 0# last bases of intron sensitivity - Z, z
    E_num = 0
    E_den = 0
    I_num = 0
    I_den = 0
    N_num = 0
    N_den = 0
    for a,b in zip(new_string, real_string):
        er_den += 1
        if a!=b:
            er_num += 1
        if b in "sS":
            sS_den += 1
            if a in "sS":
                sS_num += 1
        elif b in "pP":
            pP_den += 1
            if a in "pP":
                pP_num += 1
        elif b in "zZ":
            zZ_den += 1
            if a in "zZ":
                zZ_num += 1
        elif b =="N":
            N_den += 1
            if a == "N":
                N_num += 1
        elif b =="E":
            E_den += 1
            if a == "E":
                E_num += 1
        elif b =="I":
            I_den += 1
            if a == "I":
                I_num += 1
    return er_num/float(er_den),N_num/float(N_den), E_num/float(E_den), I_num/float(I_den), pP_num/float(pP_den), zZ_num/float(zZ_den), sS_num/float(sS_den), N_num, E_num, I_num, pP_num, zZ_num, sS_num


def predict_train_and_test(train_nucleotides, train_annotations, test_nucleotides, test_annotations, transition_matrix, emission_matrix, initial_transition_matrices, initial_state_probs, n):
    obs_str, state_str = openFile(train_nucleotides, train_annotations)

    train_obs_str = obs_str[4778053:4828063]
    train_state_str = state_str[4778053:4828063]
    assert len(train_obs_str) == len(train_state_str)

    iterations = len(train_obs_str) * 40
    new_train_state_str = gibbsSampler(transition_matrix, emission_matrix, train_obs_str, iterations, n,
                                       initial_transition_matrices,
                                       initial_state_probs)

    er, N, E, I, pP, zZ, sS, N_cor, E_cor, I_cor, pP_cor, zZ_cor, sS_cor, = analyze_result(new_train_state_str,
                                                                                           train_state_str)
    print "train"
    print er
    print N
    print E
    print I
    print pP
    print zZ
    print sS
    print ""

    obs_str, state_str = openFile(test_nucleotides, test_annotations)

    test_obs_str = obs_str[3284212:3334212]
    test_state_str = state_str[3284212:3334212]

    iterations = len(test_obs_str) * 40

    new_state_str = gibbsSampler(transition_matrix, emission_matrix, test_obs_str, iterations, n,
                                 initial_transition_matrices,
                                 initial_state_probs)

    er, N, E, I, pP, zZ, sS, N_cor, E_cor, I_cor, pP_cor, zZ_cor, sS_cor, = analyze_result(new_state_str,
                                                                                           test_state_str)
    print "test"
    print er
    print N
    print E
    print I
    print pP
    print zZ
    print sS
    print ""


def plot_metrics_v_iter(train_nucleotides, train_annotations, transition_matrix, emission_matrix, initial_transition_matrices, initial_state_probs, n):
    obs_str, state_str = openFile(train_nucleotides, train_annotations)

    train_obs_str = obs_str[4778053:4828063]
    train_state_str = state_str[4778053:4828063]

    iterationables = [len(train_obs_str) * 10, len(train_obs_str) * 20, len(train_obs_str) * 30, len(train_obs_str) * 40, len(train_obs_str) * 100, len(train_obs_str) * 200]
    ers = []
    ns = []
    es = []
    ies = []
    ps = []
    zs = []
    ses = []

    for iterations in iterationables:

        new_train_state_str = gibbsSampler(transition_matrix, emission_matrix, train_obs_str, iterations, n, initial_transition_matrices,
                     initial_state_probs)

        print new_train_state_str

        er, N, E, I, pP, zZ, sS, N_cor, E_cor, I_cor, pP_cor, zZ_cor, sS_cor, = analyze_result(new_train_state_str, train_state_str)

        ers.append(er)
        ns.append(N)
        es.append(E)
        ies.append(I)
        ps.append(pP)
        zs.append(zZ)
        ses.append(sS)

    for y, y_label in [(ers, "Error rate"), (ns,"N_specificity"), (es,"E_specificity"), (ies, "I_specificity"), (ps, "P_specificity"), (zs, "Z_specificity"), (ses, "S_specificity")]:
        plt.plot(iterationables, y, label=y_label)
    plt.xlabel("Iterations")
    plt.ylabel("%")
    plt.title("Performance Over Time")
    leg = plt.legend(loc='best', ncol=2, mode="expand", shadow=True, fancybox=True)
    leg.get_frame().set_alpha(0.5)
    plt.savefig("Performance_over_Time_n=" + str(n) + ".png", format="png")
    plt.clf()




def main(train_nucleotides, train_annotations, test_nucleotides, test_annotations, n):
    files = []
    if n == 1:
        files = ["initial_state_probs.tab","empirical_transition_matrix_n1.tab","empirical_emission_matrix_n1.tab"]
    elif n == 2:
        files = ["initial_state_probs.tab", "empirical_transition_matrix_n2.tab", "empirical_emission_matrix_n2.tab", "initial_transition_matrices_1.tab"]
    elif n == 3:
        files = ["initial_state_probs.tab", "empirical_transition_matrix_n3.tab", "empirical_emission_matrix_n3.tab", "initial_transition_matrices_1.tab", "initial_transition_matrices_2.tab"]
    else:
        raise ValueError, "Parameters have not been generated for this n yet."
    initial_state_probs, transition_matrix, emission_matrix, initial_transition_matrices = load_matrices(files)

    #predict_train_and_test(train_nucleotides, train_annotations, test_nucleotides, test_annotations, transition_matrix,
    #                       emission_matrix, initial_transition_matrices, initial_state_probs, n)


    plot_metrics_v_iter(train_nucleotides, train_annotations, transition_matrix, emission_matrix, initial_transition_matrices, initial_state_probs,n)

    # split strings into much much smaller test cases.
    # the str in roughly 200 million
    # test a 100,000 bp?
    # test obs_str will 1/2000 the length of the original








    """print "empirical training error rate, n=" + str(n) + ":", er
    print "Sensitivity to non-genes, n=" + str(n) + ":", N
    print "Sensitivity to exons, n=" + str(n) + ":", E
    print "Sensitivity to introns, n=" + str(n) + ":", I
    print "Sensitivity to beginning of intron, n=" + str(n) + ":", pP
    print "Sensitivity to end of intron, n=" + str(n) + ":", zZ
    print "Sensitivity to start site, n=" + str(n) + ":", sS
    print "Number of correctly labeled non-gene nucleotides, n=" + str(n) + ":", N_cor
    print "Number of correctly labeled exon nucleotides, n=" + str(n) + ":", E_cor
    print "Number of correctly labeled intron nucleotides, n=" + str(n) + ":", I_cor
    print "Number of correctly labeled beginning intron nucleotides, n=" + str(n) + ":", pP_cor
    print "Number of correctly labeled ending intron nucleotides, n=" + str(n) + ":", zZ_cor
    print "Number of correctly labeled start site nucleotides, n=" + str(n) + ":", sS_cor"""

    # analyze_result()
    """
    obs_str, state_str = openFile(test_nucleotides, test_annotations)

    test_obs_str = obs_str[3284212:3334212]
    test_state_str = state_str[3284212:3334212]

    iterations = len(test_obs_str) * 40

    new_state_str = gibbsSampler(transition_matrix, emission_matrix, test_obs_str, iterations, n,
                                 initial_transition_matrices,
                                 initial_state_probs)

    er,N,E,I, pP, zZ, sS, N_cor, E_cor, I_cor, pP_cor, zZ_cor, sS_cor, = analyze_result(new_state_str, test_state_str)

    print er
    print N
    print E
    print I
    print pP
    print zZ
    print sS"""

    """print "empirical training error rate, n=" + str(n) + ":", er
    print "Sensitivity to non-genes, n=" + str(n) + ":", N
    print "Sensitivity to exons, n=" + str(n) + ":", E
    print "Sensitivity to introns, n=" + str(n) + ":", I
    print "Sensitivity to beginning of intron, n=" + str(n) + ":", pP
    print "Sensitivity to end of intron, n=" + str(n) + ":", zZ
    print "Sensitivity to start site, n=" + str(n) + ":", sS
    print "Number of correctly labeled non-gene nucleotides, n=" + str(n) + ":", N_cor
    print "Number of correctly labeled exon nucleotides, n=" + str(n) + ":", E_cor
    print "Number of correctly labeled intron nucleotides, n=" + str(n) + ":", I_cor
    print "Number of correctly labeled beginning intron nucleotides, n=" + str(n) + ":", pP_cor
    print "Number of correctly labeled ending intron nucleotides, n=" + str(n) + ":", zZ_cor
    print "Number of correctly labeled start site nucleotides, n=" + str(n) + ":", sS_cor"""


def write_empirical_matrices(file_nucleotides, file_annotations, n):
    obs_str, state_str = openFile(file_nucleotides, file_annotations)
    initial_state_p = initial_state_prob([state_str])
    initial_transition_matrices = transition_probs_to_n(n, obs_str, state_str)

    with open("initial_state_probs.tab", "w") as f:
        line = [str(x) for x in initial_state_p]
        f.write("\t".join(line) + "\n")

    for i in range(0, len(initial_transition_matrices)):
        with open("initial_transition_matrices_" + str(i+1) + ".tab", "w") as f:
            for row in initial_transition_matrices[i]:
                line = [str(x) for x in row]
                f.write("\t".join(line) + "\n")

    transition_matrix, emission_matrix = count_params_transition(n, file_nucleotides, file_annotations)

    with open("empirical_transition_matrix_n" + str(n) + ".tab", "w") as f:
        for row in transition_matrix:
            line = [str(x) for x in row]
            f.write("\t".join(line) + "\n")

    with open("empirical_emission_matrix_n" + str(n) + ".tab", "w") as f:
        for row in emission_matrix:
            line = [str(x) for x in row]
            f.write("\t".join(line) + "\n")


#write_empirical_matrices("Mus_musculus.GRCm38.dna.chromosome.1.NoN.fa", "Mus_musculus.GRCm38.dna.chromosome.1.NoN_annotations.fa", 3)


#exit()

for h in range(1,4):
    print h
    main("Mus_musculus.GRCm38.dna.chromosome.1.NoN.fa", "Mus_musculus.GRCm38.dna.chromosome.1.NoN_annotations.fa", "Mus_musculus.GRCm38.dna.chromosome.2.NoN.fa", "Mus_musculus.GRCm38.dna.chromosome.2.NoN_annotations.fa", h)
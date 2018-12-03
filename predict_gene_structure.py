from gibbsSampler import gibbsSampler
from empiricalHMMcounter import count_params_transition

def main(file_nucleotides, file_annotations, n):
    transition_matrix, emission_matrix = count_params_transition(2, file_nucleotides, file_annotations)
    for i in range(0, 100):
        print transition_matrix[i]

    print emission_matrix

main()
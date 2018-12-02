from sys import argv
from csv import reader
from Bio import SeqIO
from os.path import splitext

"""Takes in a single fasta entry and annotation file"""


def label_data(fasta, csvfile):
    fa = [f for f in SeqIO.parse(open(fasta), 'fasta')][0]
    title = fa.id
    seq = str(fa.seq)
    rev_complement = str(fa.reverse_complement())

    print len(seq)

    annotation = ""

    rev_annotation = "N" * len(rev_complement)

    prev_exon_range = (0,0)

    count = 0

    with open(csvfile, 'rb') as csvfile:
        annotreader = reader(csvfile, delimiter=',')
        in_gene = False
        for row in annotreader:
            if count % 100 == 0 :
                print count, "annotations processed"
            count += 1

            if row[2] == "gene":
                in_gene = False

            elif row[6] == "+" and row[2] == "exon":
                exon_range = (int(row[3]) - 1, int(row[4]))
                if exon_range[0] < prev_exon_range[1]:
                    continue

                if in_gene:
                    if (exon_range[0] - prev_exon_range[1])  < 5:
                        continue
                    else:
                        Is = "I" * (exon_range[0] - prev_exon_range[1] - 4)
                        es = "E" * (exon_range[1] - exon_range[0] - 2)
                        annotation = annotation + "pP" + Is + "Zz" + "sS" + es

                else:
                    Ns = "N" * (exon_range[0] - prev_exon_range[1])
                    es = "E" * (exon_range[1] - exon_range[0] - 2)
                    annotation = annotation + Ns + "sS" + es
                if annotation[exon_range[0]] != "s":
                    print row
                    exit()
                prev_exon_range = exon_range
                in_gene = True
            else:
                # reverse annotation will happen here
                pass


    Ns = "N" * (len(seq) - len(annotation))
    annotation = annotation + Ns
    print len(annotation)

    outfile  = splitext(fasta)[0] + "_annotations.fa"
    with open(outfile, "w") as f:
        f.write(">" + title + "\n")
        f.write(annotation)


#label_data("two_exon_test.fa", "two_exon.csv")
#label_data("test.fa", "test_annot.csv")
label_data("Mus_musculus.GRCm38.dna.chromosome.1.fa", "mouse_chr1_annot.csv")

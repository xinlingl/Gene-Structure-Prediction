from Bio import SeqIO
from random import randint
from os.path import splitext

BASES = ["A","C","G","T"]

def replace_ns(fasta):
    prefix, ext = splitext(fasta)
    fa = [f for f in SeqIO.parse(open(fasta), 'fasta')][0]
    title = fa.id
    seq = str(fa.seq)
    new_seq = ""
    for base in seq:
        if base == "N":
            base = BASES[randint(0,3)]
        new_seq += base

    with open(prefix + ".NoN" + ext, "w") as f:
        f.write(">"+title+"\n")
        f.write(new_seq+ "\n")

replace_ns("Mus_musculus.GRCm38.dna.chromosome.2.fa")
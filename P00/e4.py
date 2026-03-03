from seq0 import *

folder = "../SO4/sequences/"
genes = ["U5", "ADA", "FRAT1", "FXN"]
bases = ["A", "C", "T", "G"]

print("-----| Exercise 4 |------")

for gene_name in genes:
    fullpath = folder + gene_name + ".txt"
    sequence = seq_read_fasta(fullpath)

    result_line = f"Gene {gene_name}:"

    for b in bases:
        count = seq_count_base(sequence, b)
        result_line += f"  {b}: {count}"

    print(result_line)
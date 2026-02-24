from seq0 import *


folder = "../SO4/sequences/"
genes = ["U5", "ADA", "FRAT1", "FXN"]

print("-----| Exercise 3 |------")

for gene_name in genes:
    filename = gene_name + ".txt"
    fullpath = folder + filename

    sequence = seq_read_fasta(fullpath)
    length = seq_len(sequence)

    print(f"Gene {gene_name} -> Length: {length}")
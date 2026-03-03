from seq0 import *

folder = "../SO4/sequences/"
genes = ["U5", "ADA", "FRAT1", "FXN"]

print("-----| Exercise 5 |------")

for gene_name in genes:
    fullpath = folder + gene_name + ".txt"
    sequence = seq_read_fasta(fullpath)

    diccionario_bases = seq_count(sequence)

    print(f"Gene {gene_name}: {diccionario_bases}")
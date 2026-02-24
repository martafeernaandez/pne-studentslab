from seq0 import *

folder = "../SO4/sequences/"
genes = ["U5", "ADA", "FRAT1", "FXN"]

print("-----| Exercise 8 |------")

for gene_name in genes:
    fullpath = folder + gene_name + ".txt"
    sequence = seq_read_fasta(fullpath)

    counts = seq_count(sequence)

    most_frequent_base = ""
    max_value = -1

    for base in counts:
        if counts[base] > max_value:
            max_value = counts[base]
            most_frequent_base = base

    print(f"Gene {gene_name}: Most frequent Base: {most_frequent_base}")
from seq0 import *

folder = "../SO4/sequences/"
filename = "U5.txt"
fullpath = folder + filename

print("------| Exercise 6 |------")

gene_u5 = seq_read_fasta(fullpath)
fragment = gene_u5[0:20]
reverse_fragment = seq_reverse(fragment)

print(f"Gene U5")
print(f"Fragment: {fragment}")
print(f"Reverse:  {reverse_fragment}")
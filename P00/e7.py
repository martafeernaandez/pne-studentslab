from seq0 import *

folder = "../SO4/sequences/"
filename = "U5.txt"
fullpath = folder + filename

print("-----| Exercise 7 |------")

sequence = seq_read_fasta(fullpath)
fragment = sequence[0:20]
complement_fragment = seq_complement(fragment)

print(f"Gene U5:")
print(f"Frag: {fragment}")
print(f"Comp: {complement_fragment}")
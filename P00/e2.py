from seq0 import *

folder = "../SO4/sequences/"
filename = "U5.txt"
fullpath = folder + filename

sequence = seq_read_fasta(fullpath)

print(f"DNA file: {filename}")
print(f"The first 20 bases are: {sequence[0:20]}")
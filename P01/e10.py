from seq1 import Seq

print("-----| Practice 1, Exercise 10 |------")

roadmap = [
    "../SO4/sequences/U5.txt",
    "../SO4/sequences/ADA.txt",
    "../SO4/sequences/FRAT1.txt",
    "../SO4/sequences/FXN.txt",
    "../SO4/sequences/RNU6_269P.txt"
]

names = ["U5", "ADA", "FRAT1", "FXN", "RNU6_269P"]

for i in range(len(roadmap)):

    s = Seq()
    s.read_fasta(roadmap[i])
    dictionary = s.count()

    frequent_base = ""
    bigger_number = 0

    for base in ['A', 'C', 'T', 'G']:
        if dictionary[base] > bigger_number:
            bigger_number = dictionary[base]
            frequent_base = base

    print("Gene " + names[i] + ": Most frequent Base: " + frequent_base)
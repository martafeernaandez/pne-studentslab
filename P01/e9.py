from seq1 import Seq

print("-----| Practice 1, Exercise 9 |------")

s = Seq()
s.read_fasta("../SO4/sequences/U5.txt")

print("Sequence : (Length: " + str(s.len()) + ") " + str(s))
print("  Bases: " + str(s.count()))
print("  Rev:   " + s.reverse())
print("  Comp:  " + s.complement())
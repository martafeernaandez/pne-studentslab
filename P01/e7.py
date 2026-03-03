from seq1 import Seq

print("-----| Practice 1, Exercise 7 |------")

s0 = Seq()
s1 = Seq("ACTGA")
s2 = Seq("Invalid sequence")

print("Sequence 0: (Length: " + str(s0.len()) + ") " + str(s0))
print("  Bases: " + str(s0.count()))
print("  Rev:   " + s0.reverse())

print("Sequence 1: (Length: " + str(s1.len()) + ") " + str(s1))
print("  Bases: " + str(s1.count()))
print("  Rev:   " + s1.reverse())

print("Sequence 2: (Length: " + str(s2.len()) + ") " + str(s2))
print("  Bases: " + str(s2.count()))
print("  Rev:   " + s2.reverse())
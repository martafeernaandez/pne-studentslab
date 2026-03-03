from seq1 import Seq

print("-----| Practice 1, Exercise 5 |------")

s0 = Seq()
s1 = Seq("ACTGA")
s2 = Seq("Invalid sequence")

print("Sequence 0: (Length: " + str(s0.len()) + ") " + str(s0))
print("  A: " + str(s0.count_base('A')) + ",   C: " + str(s0.count_base('C')) + ",   T: " + str(s0.count_base('T')) + ",   G: " + str(s0.count_base('G')))
print("Sequence 1: (Length: " + str(s1.len()) + ") " + str(s1))
print("  A: " + str(s1.count_base('A')) + ",   C: " + str(s1.count_base('C')) + ",   T: " + str(s1.count_base('T')) + ",   G: " + str(s1.count_base('G')))

print("Sequence 2: (Length: " + str(s2.len()) + ") " + str(s2))
print("  A: " + str(s2.count_base('A')) + ",   C: " + str(s2.count_base('C')) + ",   T: " + str(s2.count_base('T')) + ",   G: " + str(s2.count_base('G')))
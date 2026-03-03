from seq1 import Seq

print("-----| Practice 1, Exercise 4 |------")

s1 = Seq()
s2 = Seq("ACTGA")
s3 = Seq("Invalid sequence")

print("Sequence 1: (Length: " + str(s1.len()) + ") " + str(s1))
print("Sequence 2: (Length: " + str(s2.len()) + ") " + str(s2))
print("Sequence 3: (Length: " + str(s3.len()) + ") " + str(s3))
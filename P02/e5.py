from client0 import client
from seq0 import seq

PRACTICE = 2
EXERCISE = 5

print(f"-----| Practice {PRACTICE}, Exercise {EXERCISE} |------")

IP = "192.168.1.45"
PORT = 8080

c = client(IP, PORT)
print(c)

s = seq()
s.read_fasta("../S04/sequences/FRAT1.txt")
allsequence = str(s)

print(f"Gene FRAT1: {allsequence[:71]}...")


for i in range(5):
    start = i * 10
    end = start + 10

    fragment = allsequence[start:end]

    print(f"Fragment {i + 1}: {fragment}")

    c.talk(fragment)
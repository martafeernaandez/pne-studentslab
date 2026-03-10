from client0 import client
from seq0 import seq

PRACTICE = 2
EXERCISE = 6

print(f"-----| Practice {PRACTICE}, Exercise {EXERCISE} |------")

IP = "192.168.1.45"
PORT1 = 8080
PORT2 = 8081

c1 = client(IP, PORT1)
c2 = client(IP, PORT2)

print(c1)
print(c2)

s = seq()
s.read_fasta("../S04/sequences/FRAT1.txt")
seq_str = str(s)

print(f"Gene FRAT1: {seq_str[:76]}...")

for i in range(10):
    start = i * 10
    end = start + 10
    fragment = seq_str[start:end]

    print(f"Fragment {i + 1}: {fragment}")

    if i % 2 == 0:
        c1.talk(fragment)
    else:
        c2.talk(fragment)
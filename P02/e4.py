from client0 import client
from seq0 import seq

PRACTICE = 2
EXERCISE = 4

print(f"-----| Practice {PRACTICE}, Exercise {EXERCISE} |------")

IP = "192.168.1.45"
PORT = 8080

c = client(IP, PORT)
print(c)

genes = ["U5", "FRAT1", "ADA"]

for gene_name in genes:
    s = seq()

    path = f"../S04/sequences/{gene_name}.txt"

    s.read_fasta(path)

    print(f"Sending the {gene_name} Gene to the server...")
    response = c.talk(str(s))
    print(f"Response: {response}")
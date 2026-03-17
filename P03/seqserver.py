import socket
from seq1 import Seq

IP = "127.0.0.1"
PORT = 8080

SEQUENCES = ["ACGT", "GATC", "TTCA", "GGGTA", "ACTGGG"]

ls = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ls.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
ls.bind((IP, PORT))
ls.listen(5)

print("server in " + IP + ":" + str(PORT))

while True:
    (cs, address) = ls.accept()

    msg = cs.recv(2048).decode().strip()
    response = ""

    # e1
    if msg == "PING":
        print("PING command!")
        response = "OK!\n"

    # e2
    elif msg.startswith("GET"):
        print("GET command!")
        parts = msg.split()
        number = int(parts[1])
        response = SEQUENCES[number] + "\n"

    # e3
    elif msg.startswith("INFO"):
        print("INFO command!")
        parts = msg.split()
        sequence = parts[1]
        s = Seq(sequence)
        total = s.len()

        n_a = s.count_base('A')
        n_c = s.count_base('C')
        n_g = s.count_base('G')
        n_t = s.count_base('T')

        if total > 0:
            p_a = (n_a * 100.0) / total
            p_c = (n_c * 100.0) / total
            p_g = (n_g * 100.0) / total
            p_t = (n_t * 100.0) / total
        else:
            p_a = p_c = p_g = p_t = 0.0

        response = "Sequence: " + sequence + "Total length: " + str(total) + "\n"
        response = response + "A: " + str(n_a) + " (" + str(round(p_a, 1)) + "%)\n"
        response = response + "C: " + str(n_c) + " (" + str(round(p_c, 1)) + "%)\n"
        response = response + "G: " + str(n_g) + " (" + str(round(p_g, 1)) + "%)\n"
        response = response + "T: " + str(n_t) + " (" + str(round(p_t, 1)) + "%)\n"

    # e4
    elif msg.startswith("COMP"):
        print("COMP command!")
        parts = msg.split()
        sequence = parts[1]
        s = Seq(sequence)
        response = s.complement() + "\n"

    # e5
    elif msg.startswith("REV"):
        print("REV command!")
        parts = msg.split()
        sequence = parts[1]
        s = Seq(sequence)
        response = s.reverse() + "\n"

    # e6
    elif msg.startswith("GENE"):
        print("GENE command!")

        parts = msg.split()
        gene_name = parts[1]

        ruta = "../S04/sequences/" + gene_name + ".txt"

        s = Seq()
        s.read_fasta(ruta)

        response = s.strbases + "\n"

    print(response, end="")

    cs.send(response.encode())
    cs.close()
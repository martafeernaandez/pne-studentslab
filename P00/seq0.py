def seq_ping():
    print("OK")


def seq_read_fasta(filename):
    seq = ""
    with open(filename, "r") as f:
        for line in f:
            if not line.startswith(">"):
                seq = seq + line.strip()
    return seq


def seq_len(seq):
    return len(seq)


def seq_count_base(seq, base):
    return seq.count(base)


def seq_count(seq):
    return {
        "A": seq.count("A"),
        "T": seq.count("T"),
        "C": seq.count("C"),
        "G": seq.count("G")
    }


def seq_reverse(seq):
    return seq[::-1]


def seq_complement(seq):
    complement = ""
    for base in seq:
        if base == "A":
            complement += "T"
        elif base == "T":
            complement += "A"
        elif base == "G":
            complement += "C"
        elif base == "C":
            complement += "G"
    return complement
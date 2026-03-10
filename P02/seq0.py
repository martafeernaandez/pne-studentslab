class seq:
    def __init__(self, str_bases=None):
        self.bases = str_bases

    def __str__(self):
        return str(self.bases)

    def read_fasta(self, filename):
        seq_data = ""
        with open(filename, "r") as f:
            for line in f:
                if not line.startswith(">"):
                    seq_data = seq_data + line.strip()
        self.bases = seq_data
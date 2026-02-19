from pathlib import Path

# -- Constant with the new of the file to open
FILENAME = "sequences/ADA.txt"

# -- Open and read the file
file_contents = Path(FILENAME).read_text()
body = "".join(file_contents.split("\n")[1::])
sequence = "".join(body.replace(" ", "").split("\n"))

exon1 = sequence.find("GCTGGCCCCAGGGAAAGCCGAGCGGCCACCGAGCCGGCAGAGACCCACCGAGCGGCGGCGGAGGGAGCAGCGCCGGGGCGCACGAGGGCACCATGGCCCAGACGCCCGCCTTCGACAAGCCCAAA")

def coord(seq):
    position = sequence.find(seq)
    start =
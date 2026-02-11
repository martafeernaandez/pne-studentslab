dna = "ATGCGATCGATCGATCGATCGA"

print("Lenght: ", len(dna))
print("First 5: ", dna[:5])
print("Last 3: ", dna[-3:])
print("Lowercase: ", dna.lower())

atc = dna.count('ATC')
print("ATC count: ", atc)

rna = dna.replace("T","U")
print("RNA: ", rna)


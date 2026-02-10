#lines = ["AGTACACTGGT" , "ACCAGTGTACT" , "ATGGCCATTGTAATGGGCCGCTGAAAGGGTGCCCGATAG"]
#print("From variable:", lines)


#Option 1
f = open("dna_file.txt", "r")
lines = f.readlines()
f.close()

#Option 2
with open('dna_file.txt', 'r') as f:
    lines = f.readlines()


total_number = 0

bases = {"A":0, "C":0, "G":0, "T":0}

for sequence in lines:
    sequence = sequence.strip() #Remove spaces and newline characters at the end of the string
    total_number += len(sequence)

    for base in sequence:
        if base in bases:
            bases[base] += 1

for base, count in bases.items():
    print(f'{base}: {count}')

print("Total number of bases", total_number)

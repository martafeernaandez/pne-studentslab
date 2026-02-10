#lines = ["AGTACACTGGT" , "ACCAGTGTACT" , "ATGGCCATTGTAATGGGCCGCTGAAAGGGTGCCCGATAG"]
#print("From variable:", lines)

f = open("dna_file.txt", "r")
#Here we put the code
lines = f.readlines()
f.close()

#print("From file:", lines)

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

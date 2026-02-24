class Seq:
    def __init__(self, str_bases):
        valid_bases = ['A', 'C', 'G', 'T']
        is_valid = True
        for letra in str_bases:
            if letra not in valid_bases:
                is_valid = False
                break

        if is_valid:
            self.bases = str_bases
            print("New sequence created!")
        else:
            self.bases = "ERROR"
            print("ERROR!!")


def print_seqs(seq_list):
    indice = 0
    for s in seq_list:
        largo = len(s.bases)
        print(f"Sequence {indice}: (Length: {largo}) {s.bases}")
        indice = indice + 1


def generate_seqs(pattern, number):
    results = []

    for i in range(1, number + 1):
        new_chain = pattern * i

        new_object = Seq(new_chain)

        results.append(new_object)

    return results

seq_list1 = generate_seqs("A", 3)
seq_list2 = generate_seqs("AC", 5)

print("List 1:")
print_seqs(seq_list1)
print() 
print("List 2:")
print_seqs(seq_list2)
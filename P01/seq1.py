class Seq:
    def __init__(self, strbases=None):
        if strbases == None:
            print("NULL sequence created")
            self.strbases = ""
            return

        is_valid = True
        for letter in strbases:
            if letter == 'A' or letter == 'C' or letter == 'T' or letter == 'G':
                pass
            else:
                is_valid = False

        if is_valid == True:
            print("New sequence created!")
            self.strbases = strbases
        else:
            print("INVALID sequence!")
            self.strbases = "ERROR"

    def __str__(self):
        if self.strbases == "":
            return "NULL"
        return self.strbases

    def len(self):
        if self.strbases == "" or self.strbases == "ERROR":
            return 0
        else:
            return len(self.strbases)

    def count_base(self, base):
        if self.strbases == "" or self.strbases == "ERROR":
            return 0

        total = 0
        for b in self.strbases:
            if b == base:
                total = total + 1
        return total

    def count(self):
        result = {'A': 0, 'T': 0, 'C': 0, 'G': 0}

        if self.strbases == "" or self.strbases == "ERROR":
            return result

        for base in self.strbases:
            result[base] = result[base] + 1

        return result

    def reverse(self):
        if self.strbases == "":
            return "NULL"
        if self.strbases == "ERROR":
            return "ERROR"
        return self.strbases[::-1]

    def complement(self):
        if self.strbases == "":
            return "NULL"
        if self.strbases == "ERROR":
            return "ERROR"

        result = ""
        for base in self.strbases:
            if base == "A":
                result = result + "T"
            elif base == "T":
                result = result + "A"
            elif base == "C":
                result = result + "G"
            elif base == "G":
                result = result + "C"
        return result

    def read_fasta(self, filename):
        f = open(filename, "r")
        lines = f.readlines()
        f.close()

        text = ""
        for i in range(1, len(lines)):
            text = text + lines[i].strip()

        self.strbases = text
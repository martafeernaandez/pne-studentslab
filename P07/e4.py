import http.client
import json
import termcolor
import sys

sys.path.append('../P01')

from seq1 import Seq

genes = {
    "FRAT1": "ENSG00000165879",
    "ADA": "ENSG00000196839",
    "FXN": "ENSG00000165060",
    "RNU6_269P": "ENSG00000212379",
    "MIR633": "ENSG00000207552",
    "TTTY4C": "ENSG00000228296",
    "RBMY2YP": "ENSG00000227633",
    "FGFR3": "ENSG00000068078",
    "KDR": "ENSG00000128052",
    "ANK2": "ENSG00000145362"
}

name = input("Write the gene name: ")

if name not in genes:
    print("Error: Gene not found.")
    exit()

gene_id = genes[name]

SERVER = 'rest.ensembl.org'
REQ = f'/sequence/id/{gene_id}?content-type=application/json'

print(f"\nServer: {SERVER}")
print(f"URL: {SERVER}{REQ}")

conn = http.client.HTTPConnection(SERVER)

try:
    conn.request("GET", REQ)

except ConnectionRefusedError:
    print("ERROR! Cannot connect to the Server")
    exit()

r1 = conn.getresponse()
print(f"Response received!: {r1.status} {r1.reason}\n")

data1 = r1.read().decode("utf-8")
gene = json.loads(data1)

termcolor.cprint("Gene", 'green', end="")
print(f": {name}")

termcolor.cprint("Description", 'green', end="")
print(f": {gene['desc']}")

genestr = gene['seq']
s = Seq(genestr)


total_len = s.len()

termcolor.cprint("Total lengh", 'green', end="")
print(f": {total_len}")


for b in ['A', 'C', 'G', 'T']:
        count = s.count_base(b)
        percent = (count / total_len) * 100 if total_len > 0 else 0
        termcolor.cprint(b, 'green', end="")
        print(f": {count} ({percent:.1f}%)")


diccionario_bases = s.count()
base_mas_frecuente = max(diccionario_bases, key=diccionario_bases.get)

termcolor.cprint("Most frequent Base", 'green', end="")
print(f": {base_mas_frecuente}")

conn.close()
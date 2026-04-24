import http.client
import json
import termcolor
import sys

sys.path.append('../P1')
from seq1 import Seq

GENES = {
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

SERVER = 'rest.ensembl.org'
ENDPOINT = '/sequence/id/'
PARAMS = '?content-type=application/json'

for name in GENES:

    REQ = ENDPOINT + GENES[name] + PARAMS
    URL = SERVER + REQ

    print(f"Server: {SERVER}")
    print(f"URL: {URL}")

    conn = http.client.HTTPConnection(SERVER)

    try:
        conn.request("GET", REQ)

    except ConnectionRefusedError:
        print("ERROR! Cannot connect to the Server")
        sys.exit()

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

    bases_dictionary = s.count()
    frequent_base = max(bases_dictionary, key=bases_dictionary.get)

    termcolor.cprint("Most frequent Base", 'green', end="")
    print(f": {frequent_base}")
    print()

    conn.close()
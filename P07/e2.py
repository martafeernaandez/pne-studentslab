import http.client
import json
from termcolor import colored

gene_names = ["FRAT1", "ADA", "FXN", "RNU6-269P", "MIR633", "TTTY4C", "RBMY2YP", "FGFR3", "KDR", "ANK2"]

genes_dictionary = {}

SERVER = 'rest.ensembl.org'

print("Dictionary of Genes!")
print("There are 10 genes in the dictionary:")

conn = http.client.HTTPConnection(SERVER)

for gene in gene_names:
    endpoint = f"/lookup/symbol/human/{gene}?content-type=application/json"

    conn.request("GET", endpoint)
    response = conn.getresponse()

    if response.status == 200:
        data = response.read().decode("utf-8")
        json_data = json.loads(data)

        genes_dictionary[gene] = json_data['id']
        print(f"{colored(gene, 'green')} --> {genes_dictionary[gene]}")
    else:
        print(f"Error finding {gene}: {response.status}")

conn.close()
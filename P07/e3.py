import http.client
import json
from termcolor import colored

SERVER = 'rest.ensembl.org'
GENE_NAME = 'MIR633'
GENE_ID = 'ENSG00000207552'

ENDPOINT = f'/sequence/id/{GENE_ID}'
PARAMS = '?content-type=application/json'
URL = SERVER + ENDPOINT + PARAMS

print(f"Server: {SERVER}")
print(f"URL: {URL}")

conn = http.client.HTTPConnection(SERVER)

try:
    conn.request("GET", ENDPOINT + PARAMS)
    response = conn.getresponse()

    print(f"Response received!: {response.status} {response.reason}\n")

    if response.status == 200:
        data = response.read().decode("utf-8")
        json_data = json.loads(data)

        desc = json_data['desc']
        seq = json_data['seq']

        print(colored(f"Gene: {GENE_NAME}", 'green'))
        print(colored(f"Description: {desc}", 'green'))
        print(colored(f"Bases: {seq}", 'green'))

    else:
        print(f"Error retrieving the gene: {response.status}")

except Exception as e:
    print(f"An error occurred: {e}")

finally:
    conn.close()
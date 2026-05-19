import http.client
import json

SERVER = "localhost"
PORT = 8080


def server_request(endpoint):
    try:
        conn = http.client.HTTPConnection(SERVER, PORT)
        if "?" in endpoint:
            url = endpoint + "&json=1"
        else:
            url = endpoint + "?json=1"

        conn.request("GET", url)
        response = conn.getresponse()
        data = json.loads(response.read().decode("utf-8"))
        return data
    except ConnectionRefusedError:
        print("ERROR: Cannot connect to the server.")
        return None


def separator(title):
    print("\n")
    print(f" {title}")
    print("\n")


separator("TEST 1: List of 5 species")
data = server_request("/listSpecies?limit=5")

if data:
    if "error" in data:
        print(f" ERROR: {data['error']}")
    else:
        print(f" Total species shown: {len(data['species_list'])}")
        for species in data['species_list']:
            print(f" - {species}")

separator("TEST 2: Karyotype of human")
data = server_request("/karyotype?species=human")

if data:
    if "error" in data:
        print(f" ERROR: {data['error']}")
    else:
        print(f" Karyotype: {data['karyotype']}")

separator("TEST 3: Length of human chromosome 10")
data = server_request("/chromosomeLength?species=human&chromo=10")

if data:
    if "error" in data:
        print(f" ERROR: {data['error']}")
    else:
        print(f" Length of chromosome {data['chromosome']}: {data['length']}")

separator("TEST 4: Gene lookup for FRAT1")
data = server_request("/geneLookup?gene=FRAT1")

if data:
    if "error" in data:
        print(f" ERROR: {data['error']}")
    else:
        print(f" Gene {data['gene']} Ensembl ID: {data['gene_id']}")

separator("TEST 5: Gene sequence for FRAT1")
data = server_request("/geneSeq?gene=FRAT1")

if data:
    if "error" in data:
        print(f" ERROR: {data['error']}")
    else:
        print(f" Sequence for {data['gene']}: {data['sequence']}...")

separator("TEST 6: Gene info for FRAT1")
data = server_request("/geneInfo?gene=FRAT1")

if data:
    if "error" in data:
        print(f" ERROR: {data['error']}")
    else:
        print(f" Gene {data['gene']} is in Chromosome {data['chromosome']}")
        print(f" Start: {data['start']}")
        print(f" End: {data['end']}")
        print(f" Length: {data['length']}")

separator("TEST 7: Gene calculations for FRAT1")
data = server_request("/geneCalc?gene=FRAT1")

if data:
    if "error" in data:
        print(f" ERROR: {data['error']}")
    else:
        print(f" Gene: {data['gene']}")
        print(f" Total length: {data['total_length']}")
        print(f" Percentages: A:{data['percentages']['A']}% C:{data['percentages']['C']}% G:{data['percentages']['G']}% T:{data['percentages']['T']}%")

separator("TEST 8: Gene list in chromosome 10, region 97319000 - 97322000")
data = server_request("/geneList?chromo=10&start=97319000&end=97322000")

if data:
    if "error" in data:
        print(f" ERROR: {data['error']}")
    else:
        print(f" Genes found in Chromosome {data['chromosome']}")
        print(f" Region {data['start']}-{data['end']}:")
        for gene in data['genes']:
            print(f" - {gene}")

separator("TEST 9: Error handling - gene does not exist")

data = server_request("/geneInfo?gene=THISDOESNOTEXIST")

if data:
    if "error" in data:
        print(f" Server correctly returned and error")
        print(f" ERROR: {data['error']}")
    else:
        print(f" Unexpected response: {data}")

print("ALL TEST FINISHED")
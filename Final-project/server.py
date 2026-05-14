import http.server
import socketserver
import urllib.parse
import http.client
import json
from jinja2 import Environment, FileSystemLoader

PORT = 8080
SERVER = 'rest.ensembl.org'

env = Environment(loader=FileSystemLoader('html'))


class Seq:
    def __init__(self, sequence):
        self.seq = sequence

    def get_length(self):
        return len(self.seq)

    def get_percentages(self):
        total = len(self.seq)
        if total == 0:
            return {'A': 0, 'C': 0, 'G': 0, 'T': 0}

        a = (self.seq.count('A') / total) * 100
        c = (self.seq.count('C') / total) * 100
        g = (self.seq.count('G') / total) * 100
        t = (self.seq.count('T') / total) * 100

        return {
            'A': round(a, 2),
            'C': round(c, 2),
            'G': round(g, 2),
            'T': round(t, 2)
        }


class FinalProjectHandler(http.server.BaseHTTPRequestHandler):

    def get_ensembl_data(self, endpoint):
        conn = http.client.HTTPConnection(SERVER)

        # Check if the endpoint already has query parameters (?)
        if "?" in endpoint:
            req = endpoint + "&content-type=application/json"
        else:
            req = endpoint + "?content-type=application/json"

        try:
            conn.request("GET", req)
            response = conn.getresponse()
            data = response.read().decode("utf-8")
            conn.close()

            if response.status == 200:
                if data:  # Extra check to prevent empty data crashes
                    return json.loads(data)
                return None
            else:
                return None
        except ConnectionRefusedError:
            print("ERROR! Cannot connect to the Server")
            return None

    def do_GET(self):
        parsed_url = urllib.parse.urlparse(self.path)
        path = parsed_url.path
        params = urllib.parse.parse_qs(parsed_url.query)

        if path == "/" or path == "/index.html":
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            template = env.get_template("index.html")
            self.wfile.write(template.render().encode('utf-8'))

        elif path == "/listSpecies":
            limit = params.get('limit', [None])[0]
            data = self.get_ensembl_data("/info/species")

            species_list = []
            species_total = 0
            limit_exceeded = False

            if data and 'species' in data:
                species_list = data['species']
                species_total = len(species_list)

                if limit and limit.isdigit():
                    n = int(limit)
                    if n > species_total:
                        limit_exceeded = True
                    else:
                        species_list = species_list[:n]

            if not data or limit_exceeded:
                self.send_response(404)
                self.send_header('Content-type', 'text/html')
                self.end_headers()

                template = env.get_template("error.html")
                self.wfile.write(template.render().encode('utf-8'))
            else:
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()

                template = env.get_template("species.html")
                context = {
                    "limit": limit,
                    "species_total": species_total,
                    "species_list": species_list
                }
                self.wfile.write(template.render(context).encode('utf-8'))

        elif path == "/karyotype":
            species_input = params.get('species', [''])[0].strip()
            species_formatted = species_input.replace(" ", "_").lower()

            data = self.get_ensembl_data(f"/info/assembly/{species_formatted}")

            karyotype_list = []
            if data and 'karyotype' in data:
                karyotype_list = data['karyotype']

            if not data or not karyotype_list:
                self.send_response(404)
                self.send_header('Content-type', 'text/html')
                self.end_headers()

                template = env.get_template("error.html")
                self.wfile.write(template.render().encode('utf-8'))
            else:
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()

                template = env.get_template("karyotype.html")
                context = {
                    "species": species_input,
                    "karyotype": karyotype_list
                }
                self.wfile.write(template.render(context).encode('utf-8'))

        elif path == "/chromosomeLength":
            species_input = params.get('species', [''])[0].strip()
            chromo_input = params.get('chromo', [''])[0].strip()
            species_formatted = species_input.replace(" ", "_").lower()

            data = self.get_ensembl_data(f"/info/assembly/{species_formatted}")

            length_str = None
            if data and 'top_level_region' in data:
                for region in data['top_level_region']:
                    if region['name'] == chromo_input:
                        length_str = str(region['length'])
                        break

            if not data or not length_str:
                self.send_response(404)
                self.send_header('Content-type', 'text/html')
                self.end_headers()

                template = env.get_template("error.html")
                self.wfile.write(template.render().encode('utf-8'))
            else:
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()

                template = env.get_template("chromosome.html")
                context = {
                    "species": species_input,
                    "chromosome": chromo_input,
                    "length": length_str
                }
                self.wfile.write(template.render(context).encode('utf-8'))

        # --- MEDIUM LEVEL SERVICES ---

        elif path == "/geneLookup":
            gene = params.get('gene', [''])[0].strip()
            data = self.get_ensembl_data(f"/lookup/symbol/homo_sapiens/{gene}?expand=0")

            if not data or 'id' not in data:
                self.send_response(404)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                template = env.get_template("error.html")
                self.wfile.write(template.render().encode('utf-8'))
            else:
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                template = env.get_template("gene_lookup.html")
                context = {"gene": gene, "gene_id": data['id']}
                self.wfile.write(template.render(context).encode('utf-8'))

        elif path == "/geneSeq":
            gene = params.get('gene', [''])[0].strip()
            lookup_data = self.get_ensembl_data(f"/lookup/symbol/homo_sapiens/{gene}?expand=0")

            seq_str = None
            if lookup_data and 'id' in lookup_data:
                gene_id = lookup_data['id']
                seq_data = self.get_ensembl_data(f"/sequence/id/{gene_id}")
                if seq_data and 'seq' in seq_data:
                    seq_str = seq_data['seq']

            if not seq_str:
                self.send_response(404)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                template = env.get_template("error.html")
                self.wfile.write(template.render().encode('utf-8'))
            else:
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                template = env.get_template("gene_seq.html")
                context = {"gene": gene, "sequence": seq_str}
                self.wfile.write(template.render(context).encode('utf-8'))

        elif path == "/geneInfo":
            gene = params.get('gene', [''])[0].strip()
            data = self.get_ensembl_data(f"/lookup/symbol/homo_sapiens/{gene}?expand=0")

            if not data or 'id' not in data:
                self.send_response(404)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                template = env.get_template("error.html")
                self.wfile.write(template.render().encode('utf-8'))
            else:
                length = data['end'] - data['start'] + 1
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                template = env.get_template("gene_info.html")
                context = {
                    "gene": gene,
                    "gene_id": data['id'],
                    "start": data['start'],
                    "end": data['end'],
                    "length": length,
                    "chromosome": data['seq_region_name']
                }
                self.wfile.write(template.render(context).encode('utf-8'))

        elif path == "/geneCalc":
            gene = params.get('gene', [''])[0].strip()
            lookup_data = self.get_ensembl_data(f"/lookup/symbol/homo_sapiens/{gene}?expand=0")

            seq_obj = None
            if lookup_data and 'id' in lookup_data:
                gene_id = lookup_data['id']
                seq_data = self.get_ensembl_data(f"/sequence/id/{gene_id}")
                if seq_data and 'seq' in seq_data:
                    seq_obj = Seq(seq_data['seq'])

            if not seq_obj:
                self.send_response(404)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                template = env.get_template("error.html")
                self.wfile.write(template.render().encode('utf-8'))
            else:
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                template = env.get_template("gene_calc.html")
                context = {
                    "gene": gene,
                    "total_length": seq_obj.get_length(),
                    "percentages": seq_obj.get_percentages()
                }
                self.wfile.write(template.render(context).encode('utf-8'))

        elif path == "/geneList":
            chromo = params.get('chromo', [''])[0].strip()
            start = params.get('start', [''])[0].strip()
            end = params.get('end', [''])[0].strip()

            data = self.get_ensembl_data(f"/overlap/region/homo_sapiens/{chromo}:{start}-{end}?feature=gene")

            if data is None:
                self.send_response(404)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                template = env.get_template("error.html")
                self.wfile.write(template.render().encode('utf-8'))
            else:
                gene_names = []
                for g in data:
                    if 'external_name' in g:
                        gene_names.append(g['external_name'])
                    elif 'id' in g:
                        gene_names.append(g['id'])

                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                template = env.get_template("gene_list.html")
                context = {
                    "chromosome": chromo,
                    "start": start,
                    "end": end,
                    "genes": gene_names
                }
                self.wfile.write(template.render(context).encode('utf-8'))

        else:
            self.send_response(404)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            template = env.get_template("error.html")
            self.wfile.write(template.render().encode('utf-8'))


with socketserver.TCPServer(("", PORT), FinalProjectHandler) as httpd:
    print(f"Server is running at http://localhost:{PORT}")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nServer stopped.")

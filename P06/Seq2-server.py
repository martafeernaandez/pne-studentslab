import http.server
import socketserver
import urllib.parse

PORT = 8080
SEQUENCES = ["ACGTACGT", "ATGCATGC", "CGTACGTA", "GCATGCAT", "AAAAACCC"]


class SeqServerHandler(http.server.BaseHTTPRequestHandler):

    def do_GET(self):

        parsed_url = urllib.parse.urlparse(self.path)
        path = parsed_url.path
        params = urllib.parse.parse_qs(parsed_url.query)

        #MAIN PAGE
        if path == "/" or path == "/index.html":
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            with open("html/index.html", "r") as f:
                self.wfile.write(f.read().encode('utf-8'))

        #PING
        elif path == "/ping":
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            with open("html/ping.html", "r") as f:
                self.wfile.write(f.read().encode('utf-8'))

        #GET
        elif path == "/get":
            n = int(params['n'][0])  # Direct, no safety checks
            seq = SEQUENCES[n]

            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            with open("html/get.html", "r") as f:
                html = f.read()
                html = html.replace("{number}", str(n)).replace("{sequence}", seq)
                self.wfile.write(html.encode('utf-8'))

        #GENE
        elif path == "/gene":
            gene_name = params['name'][0]

            # Read file directly without try/except
            with open(f"../S04/sequences/{gene_name}.txt", "r") as f:
                gene_sequence = f.read()

            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            with open("html/gene.html", "r") as f:
                html = f.read()
                html = html.replace("{gene_name}", gene_name).replace("{gene_seq}", gene_sequence)
                self.wfile.write(html.encode('utf-8'))

        #OPERATION
        elif path == "/operation":
            seq = params['seq'][0].upper()
            op = params['op'][0].lower()

            if op == "info":
                l = len(seq)
                result = f"Total length: {l}\nA: {seq.count('A')} ({seq.count('A') / l * 100:.1f}%)\nC: {seq.count('C')} ({seq.count('C') / l * 100:.1f}%)\nG: {seq.count('G')} ({seq.count('G') / l * 100:.1f}%)\nT: {seq.count('T')} ({seq.count('T') / l * 100:.1f}%)"
            elif op == "comp":
                result = seq.translate(str.maketrans("ACGT", "TGCA"))
            elif op == "rev":
                result = seq[::-1]

            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            with open("html/operation.html", "r") as f:
                html = f.read()
                html = html.replace("{operation}", op.upper()).replace("{sequence}", seq).replace("{result}", result)
                self.wfile.write(html.encode('utf-8'))

        #ERROR 404
        else:
            self.send_response(404)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            with open("html/error.html", "r") as f:
                self.wfile.write(f.read().encode('utf-8'))



with socketserver.TCPServer(("", PORT), SeqServerHandler) as httpd:
    print(f"Server is running at http://localhost:{PORT}")
    httpd.serve_forever()
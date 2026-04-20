import http.server
import socketserver
import urllib.parse

PORT = 8080

# Dummy data for the sequences and genes
SEQUENCES = ["ACGTACGT", "ATGCATGC", "CGTACGTA", "GCATGCAT", "AAAAACCC"]

GENES = {
    "U5": "ATAGACCAAACATGAGAGGCT",
    "ADA": "AAATTTGGGGCCC",
    "FRAT1": "ATGCATGC",
    "RNU6_269P": "CGTACGTA",
    "FXN": "GATTACA"
}


class SeqServerHandler(http.server.BaseHTTPRequestHandler):

    def do_GET(self):

        parsed_url = urllib.parse.urlparse(self.path)
        ruta_limpia = parsed_url.path

        # 1. Main Page
        if ruta_limpia == "/" or ruta_limpia == "/index.html":
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            with open("html/index.html", "r") as file:
                content = file.read()
                self.wfile.write(content.encode('utf-8'))

        # 2. Ping Service
        elif ruta_limpia == "/ping":
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            with open("html/ping.html", "r") as file:
                content = file.read()
                self.wfile.write(content.encode('utf-8'))

        # 3. Get Service
        elif ruta_limpia == "/get":
            params = urllib.parse.parse_qs(parsed_url.query)
            n_str = params.get('n', ['0'])[0]
            n = int(n_str)
            sequence_data = SEQUENCES[n]

            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            with open("html/get.html", "r") as file:
                content = file.read()
                content = content.replace("{number}", str(n))
                content = content.replace("{sequence}", sequence_data)
                self.wfile.write(content.encode('utf-8'))

        # 4. Gene Service (NEW BLOCK)
        elif ruta_limpia == "/gene":
            # Extract the 'name' parameter from the URL (e.g., ?name=U5)
            params = urllib.parse.parse_qs(parsed_url.query)

            # Default to U5 if nothing is sent
            gene_name = params.get('name', ['U5'])[0]

            # Look up the gene sequence in our dictionary
            gene_sequence = GENES.get(gene_name, "Sequence not found")

            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            with open("html/gene.html", "r") as file:
                content = file.read()

                # Replace the placeholders with the real data
                content = content.replace("{gene_name}", gene_name)
                content = content.replace("{gene_seq}", gene_sequence)

                self.wfile.write(content.encode('utf-8'))

        # 5. Error Page
        else:
            self.send_response(404)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            with open("html/error.html", "r") as file:
                content = file.read()
                self.wfile.write(content.encode('utf-8'))


# Start the server
with socketserver.TCPServer(("", PORT), SeqServerHandler) as httpd:
    print(f"Server is running at http://localhost:{PORT}")
    httpd.serve_forever()
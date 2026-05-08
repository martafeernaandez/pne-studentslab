import http.server
import socketserver
import urllib.request
import urllib.parse
import json
import jinja2
import os

PORT = 8080
ENSEMBL_SERVER = "https://rest.ensembl.org"

# ==========================================
# Jinja2 Environment Setup
# ==========================================
# Point Jinja2 to the "html" directory relative to this script
template_dir = os.path.join(os.path.dirname(__file__), 'html')
env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir))


def fetch_ensembl_data(endpoint):
    """Helper function to make GET requests to the Ensembl REST API."""
    url = ENSEMBL_SERVER + endpoint
    req = urllib.request.Request(url, headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req) as response:
            if response.status == 200:
                return json.loads(response.read().decode('utf-8'))
    except Exception as e:
        print(f"API Request failed: {e}")
        return None


class GenomeRequestHandler(http.server.BaseHTTPRequestHandler):

    def render_html(self, template_name, context=None, status_code=200):
        """Helper function to load a template, insert variables, and send it."""
        if context is None:
            context = {}

        try:
            # Load the template from the html folder
            template = env.get_template(template_name)
            html_content = template.render(**context)

            self.send_response(status_code)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(html_content.encode('utf-8'))

        except jinja2.exceptions.TemplateNotFound:
            self.send_response(500)
            self.end_headers()
            self.wfile.write(b"500 Internal Server Error: Template file not found.")

    def do_GET(self):
        parsed_url = urllib.parse.urlparse(self.path)
        path = parsed_url.path
        params = urllib.parse.parse_qs(parsed_url.query)

        # Main Endpoint
        if path == "/":
            self.render_html('index.html')

        # Endpoint 1: List Species
        elif path == "/listSpecies":
            limit = params.get('limit', [None])[0]

            data = fetch_ensembl_data("/info/species")
            if data and 'species' in data:
                species_names = [s['name'] for s in data['species']]

                if limit and limit.isdigit():
                    species_names = species_names[:int(limit)]

                context = {"title": "List of Species", "data_type": "list", "data": species_names}
            else:
                context = {"title": "List of Species", "error_msg": "Could not fetch data from Ensembl API."}

            self.render_html('results.html', context)

        # Endpoint 2: Karyotype
        elif path == "/karyotype":
            species = params.get('species', [''])[0]
            if not species:
                self.render_html('results.html',
                                 {"title": "Karyotype Info", "error_msg": "Species parameter is missing."})
                return

            data = fetch_ensembl_data(f"/info/assembly/{species}")
            if data and 'karyotype' in data:
                karyotype_list = data['karyotype']
                context = {"title": f"Karyotype for {species}", "data_type": "list", "data": karyotype_list}
            else:
                context = {"title": "Karyotype Info",
                           "error_msg": f"Could not find karyotype data for species: {species}"}

            self.render_html('results.html', context)

        # Endpoint 3: Chromosome Length
        elif path == "/chromosomeLength":
            species = params.get('species', [''])[0]
            chromo = params.get('chromo', [''])[0]

            if not species or not chromo:
                self.render_html('results.html', {"title": "Chromosome Length",
                                                  "error_msg": "Species or Chromosome parameter is missing."})
                return

            data = fetch_ensembl_data(f"/info/assembly/{species}")
            length_found = None

            if data and 'top_level_region' in data:
                for region in data['top_level_region']:
                    if region['name'] == chromo:
                        length_found = region['length']
                        break

            if length_found:
                msg = f"The length of chromosome {chromo} in {species} is {length_found} base pairs."
                context = {"title": "Chromosome Length", "data_type": "text", "data": msg}
            else:
                context = {"title": "Chromosome Length",
                           "error_msg": f"Could not find chromosome {chromo} for species {species}."}

            self.render_html('results.html', context)

        # Handle 404 Errors
        else:
            self.render_html('error.html', status_code=404)


if __name__ == "__main__":
    with socketserver.TCPServer(("", PORT), GenomeRequestHandler) as httpd:
        print(f"Serving HTTP on port {PORT}...")
        print(f"Open your browser and navigate to http://127.0.0.1:{PORT}")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nShutting down server.")
            httpd.server_close()
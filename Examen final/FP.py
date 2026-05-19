import http.server
import socketserver
import urllib.parse
import http.client
import json
from jinja2 import Environment, FileSystemLoader

PORT = 8080
SERVER = 'rest.ensembl.org'

# EVITA EL ERROR "Dirección ya en uso"
socketserver.TCPServer.allow_reuse_address = True

# INICIA EL  Jinja2 PARA CARGAR PLANTILLAS HTML DESDE LA CARPETA DE 'HTML'
env = Environment(loader=FileSystemLoader('html'))


class Seq:
    """
    Una clase para representar y analizar una secuencia de ADN.
    """
    def __init__(self, sequence):
        """Inicializa el objeto Seq con una cadena de secuencia de ADN dada."""
        self.seq = sequence

    def get_length(self):
        """Devuelve el número total de bases en la secuencia de ADN."""
        return len(self.seq)

    def get_percentages(self):
        """
        Calcula y devuelve el porcentaje de cada nucleótido (A, C, G, T)
        presente en la secuencia de ADN.
        """
        total = len(self.seq)
        if total == 0:
            return {'A': 0, 'C': 0, 'G': 0, 'T': 0}

        # Calcula la frecuencia de cada base
        a = (self.seq.count('A') / total) * 100
        c = (self.seq.count('C') / total) * 100
        g = (self.seq.count('G') / total) * 100
        t = (self.seq.count('T') / total) * 100

        # Devuelve los porcentajes redondeados en un diccionario
        return {
            'A': round(a, 2),
            'C': round(c, 2),
            'G': round(g, 2),
            'T': round(t, 2)
        }


class FinalProjectHandler(http.server.BaseHTTPRequestHandler):
    """
    Manejador de peticiones HTTP personalizado para el servidor web de bioinformática.
    Procesa las URLs de los clientes, obtiene datos de la API REST de Ensembl
    y devuelve páginas HTML o datos JSON.
    """

    def get_ensembl_data(self, endpoint):
        """
        Método auxiliar para comunicarse con la API REST de Ensembl.
        Toma un endpoint de la API (ej. '/info/species'), hace una petición GET
        y devuelve los datos JSON parseados como un diccionario de Python.
        """
        conn = http.client.HTTPConnection(SERVER)

        # Añade el parámetro content-type correcto dependiendo de si ya existen parámetros en la URL
        if "?" in endpoint:
            url = endpoint + "&content-type=application/json"
        else:
            url = endpoint + "?content-type=application/json"

        try:
            conn.request("GET", url)
            response = conn.getresponse()
            # Lee, decodifica y parsea la respuesta JSON de Ensembl
            data = json.loads(response.read().decode("utf-8"))
            conn.close()

            return data
        except ConnectionRefusedError:
            print("ERROR! Cannot connect to the Server")
            return None

    def do_GET(self):
        """
        Método principal que maneja todas las peticiones HTTP GET entrantes desde el navegador del cliente.
        Actúa como un enrutador, dirigiendo la petición a la lógica correcta basándose en la ruta de la URL.
        """
        # Analiza la URL solicitada para separar la ruta y los parámetros de consulta
        parsed_url = urllib.parse.urlparse(self.path)
        path = parsed_url.path
        params = urllib.parse.parse_qs(parsed_url.query)

        # Comprueba si el cliente quiere datos JSON crudos en lugar de una página HTML (ej. ?json=1)
        wants_json = params.get('json', [''])[0].strip() == '1'

        # Ruta: Página de inicio
        if path == "/" or path == "/index.html":
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            template = env.get_template("index.html")
            self.wfile.write(template.render().encode('utf-8'))

            # Ruta: Lista de especies
            elif path == "/listSpecies":
            limit = params.get('limit', [None])[0]
            data = self.get_ensembl_data("/info/species")

            species_list = []
            species_total = 0
            limit_exceeded = False

            # Extrae la lista de especies de los datos de la API
            if data and 'species' in data:
                species_list = data['species']
                species_total = len(species_list)

                # Aplica el límite solicitado a la lista si se proporciona
                if limit and limit.isdigit():
                    n = int(limit)
                    if n > species_total:
                        limit_exceeded = True
                    else:
                        species_list = species_list[:n]

            # Maneja errores o renderiza la respuesta de éxito
            if not data or limit_exceeded:
                if wants_json:
                    self.send_response(404)
                    self.send_header('Content-type', 'application/json')
                    self.end_headers()
                    self.wfile.write(json.dumps({"error": "Data not found or limit exceeded"}).encode('utf-8'))
                else:
                    self.send_response(404)
                    self.send_header('Content-type', 'text/html')
                    self.end_headers()
                    template = env.get_template("error.html")
                    self.wfile.write(template.render().encode('utf-8'))
            else:
                context = {
                    "limit": limit,
                    "species_total": species_total,
                    "species_list": species_list
                }
                if wants_json:
                    self.send_response(200)
                    self.send_header('Content-type', 'application/json')
                    self.end_headers()
                    self.wfile.write(json.dumps(context).encode('utf-8'))
                else:
                    self.send_response(200)
                    self.send_header('Content-type', 'text/html')
                    self.end_headers()
                    template = env.get_template("species.html")
                    self.wfile.write(template.render(context).encode('utf-8'))

        # Ruta: Lista de especies
        elif path == "/listSpecies":
            limit = params.get('limit', [None])[0]
            startswith = params.get('startswith', [''])[0].strip().lower()
            data = self.get_ensembl_data("/info/species")

            species_list = []
            species_total = 0
            limit_exceeded = False

            if data and 'species' in data:
                if startswith:
                    for species in data['species']:
                        if species['name'].lower().startswith(startswith)
                            species_list.append(species)
                else:
                    species_list = data['species']

            # Extrae la lista de especies de los datos de la API
            if data and 'species' in data:
                species_list = data['species']
                species_total = len(species_list)

                # Aplica el límite solicitado a la lista si se proporciona
                if limit and limit.isdigit():
                    n = int(limit)
                    if n > species_total:
                        limit_exceeded = True
                    else:
                        species_list = species_list[:n]

            # Maneja errores o renderiza la respuesta de éxito
            if not data or limit_exceeded:
                if wants_json:
                    self.send_response(404)
                    self.send_header('Content-type', 'application/json')
                    self.end_headers()
                    self.wfile.write(json.dumps({"error": "Data not found or limit exceeded"}).encode('utf-8'))
                else:
                    self.send_response(404)
                    self.send_header('Content-type', 'text/html')
                    self.end_headers()
                    template = env.get_template("error.html")
                    self.wfile.write(template.render().encode('utf-8'))
            else:
                context = {
                    "limit": limit,
                    "species_total": species_total,
                    "species_list": species_list
                }
                if wants_json:
                    self.send_response(200)
                    self.send_header('Content-type', 'application/json')
                    self.end_headers()
                    self.wfile.write(json.dumps(context).encode('utf-8'))
                else:
                    self.send_response(200)
                    self.send_header('Content-type', 'text/html')
                    self.end_headers()
                    template = env.get_template("species.html")
                    self.wfile.write(template.render(context).encode('utf-8'))

        # Ruta: Obtener el cariotipo de una especie específica
        elif path == "/karyotype":
            species_input = params.get('species', [''])[0].strip()
            # Formatea el nombre de la especie para la API (ej. "Homo sapiens" -> "homo_sapiens")
            species_formatted = species_input.replace(" ", "_").lower()
            data = self.get_ensembl_data(f"/info/assembly/{species_formatted}")

            karyotype_list = []
            if data and 'karyotype' in data:
                karyotype_list = data['karyotype']

            if not data or not karyotype_list:
                if wants_json:
                    self.send_response(404)
                    self.send_header('Content-type', 'application/json')
                    self.end_headers()
                    self.wfile.write(json.dumps({"error": "Karyotype not found"}).encode('utf-8'))
                else:
                    self.send_response(404)
                    self.send_header('Content-type', 'text/html')
                    self.end_headers()
                    template = env.get_template("error.html")
                    self.wfile.write(template.render().encode('utf-8'))
            else:
                context = {
                    "species": species_input,
                    "karyotype": karyotype_list
                }
                if wants_json:
                    self.send_response(200)
                    self.send_header('Content-type', 'application/json')
                    self.end_headers()
                    self.wfile.write(json.dumps(context).encode('utf-8'))
                else:
                    self.send_response(200)
                    self.send_header('Content-type', 'text/html')
                    self.end_headers()
                    template = env.get_template("karyotype.html")
                    self.wfile.write(template.render(context).encode('utf-8'))

        # Ruta: Obtener la longitud de un cromosoma específico para una especie
        elif path == "/chromosomeLength":
            species_input = params.get('species', [''])[0].strip()
            chromo_input = params.get('chromo', [''])[0].strip()
            species_formatted = species_input.replace(" ", "_").lower()
            data = self.get_ensembl_data(f"/info/assembly/{species_formatted}")

            length_str = None
            if data and 'top_level_region' in data:
                # Busca a través de las regiones para encontrar el cromosoma solicitado
                for region in data['top_level_region']:
                    if region['name'] == chromo_input:
                        length_str = str(region['length'])
                        break

            if not data or not length_str:
                if wants_json:
                    self.send_response(404)
                    self.send_header('Content-type', 'application/json')
                    self.end_headers()
                    self.wfile.write(json.dumps({"error": "Chromosome not found"}).encode('utf-8'))
                else:
                    self.send_response(404)
                    self.send_header('Content-type', 'text/html')
                    self.end_headers()
                    template = env.get_template("error.html")
                    self.wfile.write(template.render().encode('utf-8'))
            else:
                context = {
                    "species": species_input,
                    "chromosome": chromo_input,
                    "length": length_str
                }
                if wants_json:
                    self.send_response(200)
                    self.send_header('Content-type', 'application/json')
                    self.end_headers()
                    self.wfile.write(json.dumps(context).encode('utf-8'))
                else:
                    self.send_response(200)
                    self.send_header('Content-type', 'text/html')
                    self.end_headers()
                    template = env.get_template("chromosome.html")
                    self.wfile.write(template.render(context).encode('utf-8'))

        # Ruta: Encontrar el ID de Ensembl para un símbolo de gen dado
        elif path == "/geneLookup":
            gene = params.get('gene', [''])[0].strip()
            data = self.get_ensembl_data(f"/lookup/symbol/homo_sapiens/{gene}?expand=0")

            if not data or 'id' not in data:
                if wants_json:
                    self.send_response(404)
                    self.send_header('Content-type', 'application/json')
                    self.end_headers()
                    self.wfile.write(json.dumps({"error": "Gene not found"}).encode('utf-8'))
                else:
                    self.send_response(404)
                    self.send_header('Content-type', 'text/html')
                    self.end_headers()
                    template = env.get_template("error.html")
                    self.wfile.write(template.render().encode('utf-8'))
            else:
                context = {"gene": gene, "gene_id": data['id']}
                if wants_json:
                    self.send_response(200)
                    self.send_header('Content-type', 'application/json')
                    self.end_headers()
                    self.wfile.write(json.dumps(context).encode('utf-8'))
                else:
                    self.send_response(200)
                    self.send_header('Content-type', 'text/html')
                    self.end_headers()
                    template = env.get_template("gene_lookup.html")
                    self.wfile.write(template.render(context).encode('utf-8'))

        # Ruta: Obtener la secuencia completa de ADN de un gen específico
        elif path == "/geneSeq":
            gene = params.get('gene', [''])[0].strip()
            # Paso 1: Obtener primero el ID del gen
            lookup_data = self.get_ensembl_data(f"/lookup/symbol/homo_sapiens/{gene}?expand=0")

            seq_str = None
            if lookup_data and 'id' in lookup_data:
                gene_id = lookup_data['id']
                # Paso 2: Usar el ID para obtener la secuencia
                seq_data = self.get_ensembl_data(f"/sequence/id/{gene_id}")
                if seq_data and 'seq' in seq_data:
                    seq_str = seq_data['seq']

            if not seq_str:
                if wants_json:
                    self.send_response(404)
                    self.send_header('Content-type', 'application/json')
                    self.end_headers()
                    self.wfile.write(json.dumps({"error": "Sequence not found"}).encode('utf-8'))
                else:
                    self.send_response(404)
                    self.send_header('Content-type', 'text/html')
                    self.end_headers()
                    template = env.get_template("error.html")
                    self.wfile.write(template.render().encode('utf-8'))
            else:
                context = {"gene": gene, "sequence": seq_str}
                if wants_json:
                    self.send_response(200)
                    self.send_header('Content-type', 'application/json')
                    self.end_headers()
                    self.wfile.write(json.dumps(context).encode('utf-8'))
                else:
                    self.send_response(200)
                    self.send_header('Content-type', 'text/html')
                    self.end_headers()
                    template = env.get_template("gene_seq.html")
                    self.wfile.write(template.render(context).encode('utf-8'))

        # Ruta: Obtener información detallada de ubicación (inicio, fin, cromosoma) para un gen
        elif path == "/geneInfo":
            gene = params.get('gene', [''])[0].strip()
            data = self.get_ensembl_data(f"/lookup/symbol/homo_sapiens/{gene}?expand=0")

            if not data or 'id' not in data:
                if wants_json:
                    self.send_response(404)
                    self.send_header('Content-type', 'application/json')
                    self.end_headers()
                    self.wfile.write(json.dumps({"error": "Gene info not found"}).encode('utf-8'))
                else:
                    self.send_response(404)
                    self.send_header('Content-type', 'text/html')
                    self.end_headers()
                    template = env.get_template("error.html")
                    self.wfile.write(template.render().encode('utf-8'))
            else:
                # Calcula la longitud exacta usando las coordenadas de inicio y fin
                length = data['end'] - data['start'] + 1
                context = {
                    "gene": gene,
                    "gene_id": data['id'],
                    "start": data['start'],
                    "end": data['end'],
                    "length": length,
                    "chromosome": data['seq_region_name']
                }
                if wants_json:
                    self.send_response(200)
                    self.send_header('Content-type', 'application/json')
                    self.end_headers()
                    self.wfile.write(json.dumps(context).encode('utf-8'))
                else:
                    self.send_response(200)
                    self.send_header('Content-type', 'text/html')
                    self.end_headers()
                    template = env.get_template("gene_info.html")
                    self.wfile.write(template.render(context).encode('utf-8'))

        # Ruta: Calcular porcentajes de nucleótidos usando la clase personalizada Seq
        elif path == "/geneCalc":
            gene = params.get('gene', [''])[0].strip()
            # Paso 1: Buscar el ID
            lookup_data = self.get_ensembl_data(f"/lookup/symbol/homo_sapiens/{gene}?expand=0")

            seq_obj = None
            if lookup_data and 'id' in lookup_data:
                gene_id = lookup_data['id']
                # Paso 2: Obtener la secuencia
                seq_data = self.get_ensembl_data(f"/sequence/id/{gene_id}")
                if seq_data and 'seq' in seq_data:
                    # Paso 3: Instanciar la clase Seq para realizar los cálculos
                    seq_obj = Seq(seq_data['seq'])

            if not seq_obj:
                if wants_json:
                    self.send_response(404)
                    self.send_header('Content-type', 'application/json')
                    self.end_headers()
                    self.wfile.write(json.dumps({"error": "Calculations failed"}).encode('utf-8'))
                else:
                    self.send_response(404)
                    self.send_header('Content-type', 'text/html')
                    self.end_headers()
                    template = env.get_template("error.html")
                    self.wfile.write(template.render().encode('utf-8'))
            else:
                context = {
                    "gene": gene,
                    "total_length": seq_obj.get_length(),
                    "percentages": seq_obj.get_percentages() # Devuelve el diccionario con A,C,G,T
                }
                if wants_json:
                    self.send_response(200)
                    self.send_header('Content-type', 'application/json')
                    self.end_headers()
                    self.wfile.write(json.dumps(context).encode('utf-8'))
                else:
                    self.send_response(200)
                    self.send_header('Content-type', 'text/html')
                    self.end_headers()
                    template = env.get_template("gene_calc.html")
                    self.wfile.write(template.render(context).encode('utf-8'))

        # Ruta: Listar todos los genes dentro de una región cromosómica específica
        elif path == "/geneList":
            chromo = params.get('chromo', [''])[0].strip()
            start = params.get('start', [''])[0].strip()
            end = params.get('end', [''])[0].strip()

            data = self.get_ensembl_data(f"/overlap/region/homo_sapiens/{chromo}:{start}-{end}?feature=gene")

            if data is None:
                if wants_json:
                    self.send_response(404)
                    self.send_header('Content-type', 'application/json')
                    self.end_headers()
                    self.wfile.write(json.dumps({"error": "Region not found"}).encode('utf-8'))
                else:
                    self.send_response(404)
                    self.send_header('Content-type', 'text/html')
                    self.end_headers()
                    template = env.get_template("error.html")
                    self.wfile.write(template.render().encode('utf-8'))
            else:
                # Extrae nombres externos (o IDs si los nombres no están disponibles)
                gene_names = []
                for g in data:
                    if 'external_name' in g:
                        gene_names.append(g['external_name'])
                    elif 'id' in g:
                        gene_names.append(g['id'])

                context = {
                    "chromosome": chromo,
                    "start": start,
                    "end": end,
                    "genes": gene_names
                }
                if wants_json:
                    self.send_response(200)
                    self.send_header('Content-type', 'application/json')
                    self.end_headers()
                    self.wfile.write(json.dumps(context).encode('utf-8'))
                else:
                    self.send_response(200)
                    self.send_header('Content-type', 'text/html')
                    self.end_headers()
                    template = env.get_template("gene_list.html")
                    self.wfile.write(template.render(context).encode('utf-8'))

        # Ruta de respaldo: Manejar cualquier URL desconocida (404 No Encontrado)
        else:
            if wants_json:
                self.send_response(404)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({"error": "Endpoint not found"}).encode('utf-8'))
            else:
                self.send_response(404)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                template = env.get_template("error.html")
                self.wfile.write(template.render().encode('utf-8'))


# Bloque de ejecución principal: Iniciar el servidor y mantenerlo en ejecución
with socketserver.TCPServer(("", PORT), FinalProjectHandler) as httpd:
    print(f"Server is running at http://localhost:{PORT}")
    try:
        httpd.serve_forever() # Mantiene al servidor escuchando peticiones
    except KeyboardInterrupt:
        # Maneja el apagado limpio cuando el usuario presiona Ctrl+C
        print("\nServer stopped.")
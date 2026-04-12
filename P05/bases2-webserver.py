import http.server
import socketserver
import termcolor
import os

# Define the server's port
PORT = 8080

socketserver.TCPServer.allow_reuse_address = True


class TestHandler(http.server.BaseHTTPRequestHandler):

    def do_GET(self):
        """This method is called whenever the client invokes the GET method"""

        # Print the request line in the console
        termcolor.cprint(self.requestline, 'green')

        # 1. Handle the default route
        if self.path == "/":
            self.path = "/index.html"

        # 2. Construct the local file path by prepending "html" to the requested path
        # Example: "/info/A.html" becomes "html/info/A.html"
        filepath = "html" + self.path

        # 3. Check if the file exists in the file system
        if os.path.exists(filepath) and os.path.isfile(filepath):
            status_code = 200
            file_to_open = filepath
        else:
            status_code = 404  # Not found
            file_to_open = "html/error.html"

        # 4. Read the content of the selected file
        try:
            with open(file_to_open, "r", encoding="utf-8") as file:
                contents = file.read()
        except FileNotFoundError:
            # Fallback in case even the error.html is missing
            contents = "<html><body><h1>Critical Error: error.html not found</h1></body></html>"
            status_code = 500

        # 5. Generate and send the response message
        self.send_response(status_code)
        self.send_header('Content-Type', 'text/html')
        self.send_header('Content-Length', str(len(contents.encode('utf-8'))))
        self.end_headers()

        # 6. Send the payload (the HTML content)
        self.wfile.write(contents.encode('utf-8'))

        return

# Server MAIN program

Handler = TestHandler

with socketserver.TCPServer(("", PORT), Handler) as httpd:
    print("Serving at PORT", PORT)

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nStopped by the user")
        httpd.server_close()
from http.server import BaseHTTPRequestHandler, HTTPServer

# --- Configuration ---
IP = "127.0.0.1"
PORT = 8080


# --- Server Logic ---
class SimpleWebHandler(BaseHTTPRequestHandler):

    # This method automatically handles all GET requests from the browser
    def do_GET(self):
        # 1. Check if the requested path is exactly "/info/A"
        if self.path == "/info/A":
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()

            # Read the HTML file and send it
            try:
                with open("A.html", "rb") as file:
                    self.wfile.write(file.read())
            except FileNotFoundError:
                self.wfile.write(b"Error: A.html not found.")

        # 2. For any other resource, send a blank response
        else:
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(b"")  # Sending an empty byte string creates a blank page


# --- Start the Server ---
server = HTTPServer((IP, PORT), SimpleWebHandler)
print(f"Server is up and running.")
print(f"Waiting for connections at http://{IP}:{PORT}")

# Keep the server running infinitely
server.serve_forever()
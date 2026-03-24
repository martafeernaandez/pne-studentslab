import socket

PORT = 8080
HTML_FILE_PATH = "html/info/A.html"

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind(('127.0.0.1', PORT))
server_socket.listen(1)

print(f"Servidor activo. Ve a http://127.0.0.1:{PORT}/info/A")

while True:
    client_conn, addr = server_socket.accept()

    request = client_conn.recv(1024).decode()

    if "GET /info/A" in request:
        try:
            with open(HTML_FILE_PATH, "r", encoding="utf-8") as f:
                content = f.read()

            response = "HTTP/1.1 200 OK\nContent-Type: text/html\n\n" + content
        except FileNotFoundError:
            response = "HTTP/1.1 404 Not Found\n\nError: No encuentro el archivo en html/info/A.html"
    else:
        response = "HTTP/1.1 200 OK\nContent-Type: text/html\n\n "

    client_conn.sendall(response.encode("utf-8"))
    client_conn.close()
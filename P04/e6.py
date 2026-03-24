import socket

PORT = 8080
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind(('127.0.0.1', PORT))
server.listen(1)

print("http://127.0.0.1:8080/")

while True:
    conn, addr = server.accept()
    request = conn.recv(1024).decode()

    if not request:
        conn.close()
        continue

    first_line = request.split('\n')[0]

    if "GET / " in first_line:
        with open("html/index.html", "r", encoding="utf-8") as f:
            contenido = f.read()

    elif "/info/A" in first_line:
        with open("html/info/A.html", "r", encoding="utf-8") as f:
            contenido = f.read()
    elif "/info/C" in first_line:
        with open("html/info/C.html", "r", encoding="utf-8") as f:
            contenido = f.read()
    elif "/info/G" in first_line:
        with open("html/info/G.html", "r", encoding="utf-8") as f:
            contenido = f.read()
    elif "/info/T" in first_line:
        with open("html/info/T.html", "r", encoding="utf-8") as f:
            contenido = f.read()

    else:
        with open("html/error.html", "r", encoding="utf-8") as f:
            contenido = f.read()

    respuesta = "HTTP/1.1 200 OK\nContent-Type: text/html\n\n" + contenido
    conn.sendall(respuesta.encode("utf-8"))
    conn.close()
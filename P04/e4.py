import socket

PORT = 8080
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind(('127.0.0.1', PORT))
server.listen(1)

print("http://127.0.0.1:8080/info/A ; http://127.0.0.1:8080/info/C ; http://127.0.0.1:8080/info/G ; http://127.0.0.1:8080/info/T")

while True:
    conn, addr = server.accept()
    request = conn.recv(1024).decode()

    if "/info/A" in request:
        with open("html/info/A.html", "r", encoding="utf-8") as f:
            contenido = f.read()
    elif "/info/C" in request:
        with open("html/info/C.html", "r", encoding="utf-8") as f:
            contenido = f.read()
    elif "/info/G" in request:
        with open("html/info/G.html", "r", encoding="utf-8") as f:
            contenido = f.read()
    elif "/info/T" in request:
        with open("html/info/T.html", "r", encoding="utf-8") as f:
            contenido = f.read()
    else:
        contenido = ""

    respuesta = "HTTP/1.1 200 OK\nContent-Type: text/html\n\n" + contenido
    conn.sendall(respuesta.encode("utf-8"))
    conn.close()
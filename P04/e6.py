import socket

PORT = 8080
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind(('127.0.0.1', PORT))
server.listen(1)

print("Servidor final listo.")
print("Página principal: http://127.0.0.1:8080/")

while True:
    conn, addr = server.accept()
    request = conn.recv(1024).decode()

    if not request:
        conn.close()
        continue

    # Extraemos la primera línea para saber qué ruta pide el usuario
    # Ejemplo: "GET / HTTP/1.1" o "GET /info/A HTTP/1.1"
    first_line = request.split('\n')[0]

    # --- LÓGICA DE RUTAS ---

    # 1. Si pide la raíz (página principal)
    if "GET / " in first_line:
        with open("html/index.html", "r", encoding="utf-8") as f:
            contenido = f.read()

    # 2. Si pide las bases específicas
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

    # 3. Si pide cualquier otra cosa (Error)
    else:
        with open("html/error.html", "r", encoding="utf-8") as f:
            contenido = f.read()

    # Enviamos la respuesta
    respuesta = "HTTP/1.1 200 OK\nContent-Type: text/html\n\n" + contenido
    conn.sendall(respuesta.encode("utf-8"))
    conn.close()
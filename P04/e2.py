import socket
import termcolor

# -- Server network parameters
IP = "127.0.0.1"
PORT = 8080


def process_client(s):
    # -- Receive the request message
    req_raw = s.recv(2000)
    req = req_raw.decode()

    # -- Split the request messages into lines
    lines = req.split('\n')
    req_line = lines[0]

    print("Request line: ", end="")
    termcolor.cprint(req_line, "green")

    # --- MODIFICACIÓN PARA TU EJERCICIO ---
    # Si la línea de petición contiene /info/A, abrimos tu archivo
    if "/info/A" in req_line:
        # Abrimos el archivo que está en tu carpeta html/info/
        f = open("html/info/A.html", "r")
        body = f.read()
        f.close()
    else:
        # Si pide otra cosa, cuerpo vacío como pide el ejercicio
        body = ""
    # ---------------------------------------

    # -- Status line
    status_line = "HTTP/1.1 200 OK\n"
    # -- Add the Content-Type header
    header = "Content-Type: text/html\n"
    # -- Add the Content-Length
    header += f"Content-Length: {len(body)}\n"

    # -- Build the message
    response_msg = status_line + header + "\n" + body
    s.send(response_msg.encode())


# -------------- MAIN PROGRAM
ls = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ls.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
ls.bind((IP, PORT))
ls.listen()

print("Green server configured!")

while True:
    print("Waiting for clients....")
    try:
        (cs, client_ip_port) = ls.accept()
    except KeyboardInterrupt:
        print("Server stopped!")
        ls.close()
        exit()
    else:
        process_client(cs)
        cs.close()
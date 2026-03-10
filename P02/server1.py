import socket

IP = "192.168.1.45"
PORT = 8080

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((IP, PORT))
s.listen(1)

while True:
    print(f"Waiting for connections at {IP}, {PORT}")

    (client_s, client_addr) = s.accept()
    print(f"CONNECTION: 1. From the IP: {client_addr}")

    msg = client_s.recv(2048).decode("utf-8")
    print(f"Message from client: {msg}")

    response = "Hello from the teacher's server"
    client_s.send(str.encode(response))
    client_s.close()
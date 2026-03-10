import socket


class client:
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port

    def __str__(self):
        return f"Connection to SERVER at {self.ip}, PORT: {self.port}"

    def ping(self):
        print("OK")

    def talk(self, msg):
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        try:
            client_socket.connect((self.ip, self.port))

            client_socket.sendall(msg.encode('utf-8'))

            response = client_socket.recv(1024).decode('utf-8')

            return response

        except Exception as e:
            return f"Error: {e}"

        finally:
            client_socket.close()
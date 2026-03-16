import socket

class client:
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port

    def __str__(self):
        return "Connection to SERVER at " + str(self.ip) + ", PORT: " + str(self.port)

    def ping(self):
        print("OK!")

    def talk(self, msg):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((self.ip, self.port))
        s.send(str.encode(msg))

        response = s.recv(2048).decode("utf-8")
        s.close()
        return response


print("-----| Practice 3, Exercise 7 |------")

IP = "127.0.0.1"
PORT = 8080
c = client(IP, PORT)


print(c)


print("* Testing PING...")
print(c.talk("PING").strip())

print("* Testing GET...")
for n in range(5):
    anwser = c.talk("GET " + str(n)).strip()
    print("GET " + str(n) + ": " + anwser)

sequence0 = c.talk("GET 0").strip()

print("* Testing INFO...")
anwser_info = c.talk("INFO " + sequence0).strip()
print(anwser_info)

print("* Testing COMP...")
print("COMP " + sequence0)
anwser_complete = c.talk("COMP " + sequence0).strip()
print(anwser_complete)

print("* Testing REV...")
print("REV " + sequence0)
anwser_rev = c.talk("REV " + sequence0).strip()
print(anwser_rev)

print("* Testing GENE...")
genes = ["U5", "ADA", "FRAT1", "FXN", "RNU6_269P"]

for gen in genes:
    print("GENE " + gen)
    awnser_gen = c.talk("GENE " + gen).strip()
    print(awnser_gen)
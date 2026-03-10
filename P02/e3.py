from client0 import client

PRACTICE = 2
EXERCISE = 3

print(f"-----| Practice {PRACTICE}, Exercise {EXERCISE} |------")

IP = "192.168.1.45"
PORT = 8080

c = client(IP, PORT)
print(c)

print("Sending a message to the server...")
response = c.talk("Testing!!!")

print(f"Response: {response}")
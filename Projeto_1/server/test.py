import socket

server = ("127.0.0.1", 4242)

try:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print("Socket successfully created...\n")
except socket.error as err:
    print(err)

print("Connecting....\n")
try:
    sock.connect(server)
    print("Connection OK...\n")
    
    #sock.send('profiles#0'.encode())
    sock.send('pv_10kw'.encode())

    rec = sock.recv(1024).decode("utf-8")
    print(rec)

except socket.error as err:
    print(err)
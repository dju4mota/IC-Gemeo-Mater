import socket
import time

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((socket.gethostname(), 1234))

s.send((bytes("i-------", "utf-8")))
s.send((bytes("r-------", "utf-8")))


def move_peca():
    print("movendo")
    time.sleep(3)
    print("peca movida")
    s.send((bytes("r-------", "utf-8")))


while True:
    msg = s.recv(8)
    print(msg)
    if msg == bytes("p-------", "utf-8"):
        move_peca()

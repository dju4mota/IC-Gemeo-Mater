import socket
import time

# server
# con init (i)-> conexão iniciada
# pos (p) 00.00 00.00
# pos not (n) -> peça não encontrada
# (f) -> fecha coenxao

# client
# con init (i)
# ready (r) -> pronto para receber peça
# mov to pos (m) -> movendo para peça
# (f)


socket_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM ) # af_init = ipv4 | sockstream = tcp
socket_server.bind((socket.gethostname(), 1234))

socket_server.listen(5)  # limite de fila ?


#while True:
client_socket, address = socket_server.accept()
print(f"Connection from {address} has been established!")
client_socket.send(bytes("i-------", "utf-8"))


def calcula_nova_posicao():
    print("calculando ...")
    time.sleep(3)
    print("posicao calculada")
    client_socket.send(bytes("p-------", "utf-8"))


while True:
    msg = client_socket.recv(8)
    print(msg)
    if msg == bytes("r-------", "utf-8"):
        calcula_nova_posicao()

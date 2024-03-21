import socket

# server
# con init -> conexão iniciada
# pos 00.00 00.00
# pos not -> peça não encontrada

# client
# con init
# ready -> pronto para receber peça
# mov to pos -> movendo para peça


socket_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM ) # af_init = ipv4 | sockstream = tcp
socket_server.bind((socket.gethostname(), 1234))

socket_server.listen(5) # limite de fila ?

while True:
    client_socket, address = socket_server.accept()
    print(f"Connection from {address} has been established!")
    client_socket.send(bytes("welcome", "utf-8"))
    client_socket.close()



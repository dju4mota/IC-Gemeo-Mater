import socket

host = '192.168.0.240'
port = 7772


class Client:
    def __init__(self, host=host, port=port):
        self.host = host
        self.port = port
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connect_to_server()

    def connect_to_server(self):
        try:
            self.client_socket.connect((self.host, self.port))
            print("Conexão estabelecida com sucesso!")
        except socket.error as e:
            print(f"Erro de socket ao conectar: {e}")

    def send_message(self, message):
        try:
            encoded_message = message.encode()
            self.client_socket.send(encoded_message)
            print(f"Mensagem enviada: {message}")
        except socket.error as e:
            print(f"Erro de socket ao enviar mensagem: {e}")

    def close_connection(self):
        self.client_socket.close()
        print("Conexão encerrada.")


# # Uso da classe Client
# if __name__ == '__main__':
#     client = Client()
#     # client.send_message("GGuilherme e guilherme")
#     client.send_message("G")
#     client.close_connection()

# import socket

# # Configuração do cliente
# host = '192.168.0.240'
# port = 7772
# #FISICO: J205

# # Criando o socket
# client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# try:
#     # Tentativa de conexão
#     client_socket.connect((host, port))
#     print("Conexão estabelecida com sucesso!")

#     # Enviando uma mensagem
#     mensagem =str("GGuilherme e guilherme").encode()
#     client_socket.send(mensagem)
#     print(mensagem)

# except socket.error as e:
#     # Trata erros de conexão, envio e recepção de dados
#     print(f"Erro de socket: {e}")
# finally:
#     # Fechando a conexão, independentemente de sucesso ou falha
#     client_socket.close()
#     print("Conexão encerrada.")

# # ler a mensagem recebida sioGet()
# # verificar se na mensagem o 1o caractere é igual a G
# # caso seja, roda um for para atribuir a variavel string os bytes da mensagem recebida chr(msg[n])
# # printa a mensagem montada
# # limpa a mensagem: =""
# # limpa a variavel do sioGet: for, atribuindo cada uma das posições do array a 0



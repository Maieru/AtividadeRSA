from rsa import RSA
import socket
import time
import concurrent.futures
from comunicationConstants import server_ip, port

def format_message(message): 
    return ''.join([char.upper() if char.isalpha() else char for char in message])

keySize = 512

with concurrent.futures.ThreadPoolExecutor() as executor:
    future_p = executor.submit(RSA.generate_prime_number, keySize)
    future_q = executor.submit(RSA.generate_prime_number, keySize)
    p = future_p.result()
    q = future_q.result()

n = RSA.getN(p, q)
totientN = RSA.totient(p, q)
e = RSA.getE(totientN)
d = RSA.getD(e, totientN)

print("Servidor está pronto com as chaves públicas e privadas")

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((server_ip, port))
server.listen(5)

print("Servidor escutando na porta: ", port)

while True:
    client_socket, addr = server.accept()
    print("Conexão aceita de: ", addr)

    #Envia a chave pública para o cliente
    client_socket.send(RSA.format_public_key(e, n).encode("utf-8"))
    received_public_key = client_socket.recv(65336)

    clientE, clientN = RSA.get_public_key(received_public_key.decode("utf-8"))

    received_encrypted_message = client_socket.recv(65336)
    decrypted_message = RSA.decrypt(received_encrypted_message.decode("utf-8"), d, n)

    print("Mensagem recebida: ", decrypted_message)
    formated_message = format_message(decrypted_message)
    encrypted_message = RSA.encrypt(formated_message, clientE, clientN)
    client_socket.send(encrypted_message.encode("utf-8"))
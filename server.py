from rsa import RSA
import socket
import time
import concurrent.futures
from comunicationConstants import server_ip, port

def format_message(message):
    """
    Formata a mensagem convertendo todos os caracteres alfabéticos para maiúsculas.
    
    Args:
        message (str): A mensagem a ser formatada.

    Returns:
        str: A mensagem formatada.
    """
    return ''.join([char.upper() if char.isalpha() else char for char in message])

# Tamanho da chave RSA
keySize = 2048

# Usa um ThreadPoolExecutor para gerar dois números primos em paralelo
with concurrent.futures.ThreadPoolExecutor() as executor:
    future_p = executor.submit(RSA.generate_prime_number, keySize)
    future_q = executor.submit(RSA.generate_prime_number, keySize)
    p = future_p.result()
    q = future_q.result()

# Calcula n, o produto dos dois números primos
n = RSA.getN(p, q)

# Calcula a função totiente de Euler para p e q
totientN = RSA.totient(p, q)

# Encontra um valor para e que seja coprimo com o totient
e = RSA.getE(totientN)

# Calcula o valor de d, o inverso multiplicativo de e mod totient
d = RSA.getD(e, totientN)

print("Servidor está pronto com as chaves públicas e privadas")

# Cria um socket TCP/IP
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Associa o socket ao endereço IP e porta especificados
server.bind((server_ip, port))

# Coloca o servidor em modo de escuta, permitindo até 5 conexões pendentes
server.listen(5)

print("Servidor escutando na porta: ", port)

while True:
    # Aceita uma nova conexão
    client_socket, addr = server.accept()
    print("Conexão aceita de: ", addr)

    # Envia a chave pública para o cliente
    client_socket.send(RSA.format_public_key(e, n).encode("utf-8"))

    # Recebe a chave pública do cliente
    received_public_key = client_socket.recv(65336)
    clientE, clientN = RSA.get_public_key(received_public_key.decode("utf-8"))

    # Recebe a mensagem criptografada do cliente
    received_encrypted_message = client_socket.recv(65336)

    # Descriptografa a mensagem usando a chave privada do servidor
    decrypted_message = RSA.decrypt(received_encrypted_message.decode("utf-8"), d, n)
    print("Mensagem recebida: ", decrypted_message)

    # Formata a mensagem recebida
    formated_message = format_message(decrypted_message)

    # Criptografa a mensagem formatada usando a chave pública do cliente
    encrypted_message = RSA.encrypt(formated_message, clientE, clientN)

    # Envia a mensagem criptografada de volta para o cliente
    client_socket.send(encrypted_message.encode("utf-8"))
from rsa import RSA
import time
import concurrent.futures
import socket
from comunicationConstants import server_ip, port

# Tamanho da chave RSA
keySize = 2048

# Mensagem a ser enviada
messageToSend = "The information security is of significant importance to ensure the privacy of communications"

# Marca o início do tempo para medir a geração dos números primos
start_time = time.time()

# Usa um ThreadPoolExecutor para gerar dois números primos em paralelo
with concurrent.futures.ThreadPoolExecutor() as executor:
    future_p = executor.submit(RSA.generate_prime_number, keySize)
    future_q = executor.submit(RSA.generate_prime_number, keySize)
    p = future_p.result()
    q = future_q.result()

# Marca o fim do tempo e imprime o tempo gasto para gerar os números primos
finish_time = time.time()
print("Tempo para gerar os números primos: ", finish_time - start_time)

# Calcula n, o produto dos dois números primos
n = RSA.getN(p, q)

# Calcula a função totiente de Euler para p e q
totientN = RSA.totient(p, q)

# Encontra um valor para e que seja coprimo com o totient
e = RSA.getE(totientN)

# Calcula o valor de d, o inverso multiplicativo de e mod totient
d = RSA.getD(e, totientN)

print("Cliente está pronto com as chaves públicas e privadas")
input("Pressione qualquer tecla para continuar")

# Cria um buffer para receber dados
buffer = bytearray(65336)

# Cria um socket TCP/IP
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Conecta ao servidor
client.connect((server_ip, port))

# Recebe a chave pública do servidor
receivedPublicKey = client.recv(65336)

# Converte a chave pública recebida de volta para uma tupla de inteiros (e, n)
serverE, serverN = RSA.get_public_key(receivedPublicKey.decode("utf-8"))

# Envia a chave pública do cliente para o servidor
client.send(RSA.format_public_key(e, n).encode("utf-8"))

# Criptografa a mensagem usando a chave pública do servidor
encryptedMessage = RSA.encrypt(messageToSend, serverE, serverN)

# Envia a mensagem criptografada para o servidor
client.send(encryptedMessage.encode("utf-8"))

# Recebe a resposta criptografada do servidor
encrypted_response = client.recv(65336)

# Descriptografa a resposta usando a chave privada do cliente
decrypted_response = RSA.decrypt(encrypted_response.decode("utf-8"), d, n)

# Imprime a resposta descriptografada
print("Resposta recebida: ", decrypted_response)
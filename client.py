from rsa import RSA
import time
import concurrent.futures
import socket
from comunicationConstants import server_ip, port

keySize = 512
messageToSend = "The information security is of significant importance to ensure the privacy of communications"

with concurrent.futures.ThreadPoolExecutor() as executor:
    future_p = executor.submit(RSA.generate_prime_number, keySize)
    future_q = executor.submit(RSA.generate_prime_number, keySize)
    p = future_p.result()
    q = future_q.result()

n = RSA.getN(p, q)
totientN = RSA.totient(p, q)
e = RSA.getE(totientN)
d = RSA.getD(e, totientN)

print("Cliente está pronto com as chaves públicas e privadas")
input("Pressione qualquer tecla para continuar")

buffer = bytearray(65336)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((server_ip, port))
receivedPublicKey = client.recv(65336)

serverE, serverN = RSA.get_public_key(receivedPublicKey.decode("utf-8"))

client.send(RSA.format_public_key(e, n).encode("utf-8"))

encryptedMessage = RSA.encrypt(messageToSend, serverE, serverN)

client.send(encryptedMessage.encode("utf-8"))

encrypted_response = client.recv(65336)
decrypted_response = RSA.decrypt(encrypted_response.decode("utf-8"), d, n)

print("Resposta recebida: ", decrypted_response)
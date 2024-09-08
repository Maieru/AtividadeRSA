import math
from random import randrange, getrandbits
from sympy import isprime
from concurrent.futures import ThreadPoolExecutor

class RSA:
    @staticmethod
    def generate_prime_number(length=1024):
        def check_prime():
            numero = getrandbits(length)
            return numero if isprime(numero) else None

        with ThreadPoolExecutor(max_workers=1000) as executor:
            while True:
                future = executor.submit(check_prime)
                prime = future.result()
                if prime:
                    return prime

    @staticmethod
    def getN(p, q):
        return p * q

    @staticmethod
    def totient(p, q):
        return (p - 1) * (q - 1)

    @staticmethod
    def getE(totient):
        e = 65537  # Valor comum para e
        if RSA.gcd(e, totient) == 1:
            return e
        else:
            # Encontrar um e alternativo
            for i in range(3, totient, 2):
                if RSA.gcd(i, totient) == 1:
                    return i

    @staticmethod
    def getD(e, totient):
        return pow(e, -1, totient)

    @staticmethod
    def gcd(a, b):
        while b:
            a, b = b, a % b
        return a

    @staticmethod
    def encrypt(message, e, n):
        cipher = []
        for char in message:
            cipher.append(str(pow(ord(char), e, n)))
        return ",".join(cipher)

    @staticmethod
    def decrypt(cipher, d, n):
        decrypted = []
        cipherCharacters = [i.strip() for i in cipher.split(",") if i.strip()]
        for encrypted in cipherCharacters:
            encryptedInt = int(encrypted)
            decrypted.append(chr(pow(encryptedInt, d, n)))
        return "".join(decrypted)

    @staticmethod
    def format_public_key(e, n):
        return f"{e},{n}"

    @staticmethod
    def get_public_key(formated_public_key):
        e, n = formated_public_key.split(",")
        return int(e), int(n)

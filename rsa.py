import math
from random import getrandbits
from sympy import isprime

class RSA:
    @staticmethod
    def generate_prime_number(length=1024):
        """
        Gera um número primo de um determinado comprimento de bits.
        """
        while True:
            numero = getrandbits(length)
            if isprime(numero):
                return numero

    @staticmethod
    def getN(p, q):
        """
        Calcula o produto de dois números primos p e q.
        """
        return p * q

    @staticmethod
    def totient(p, q):
        """
        Calcula a função totiente de Euler para dois números primos p e q.
        """
        return (p - 1) * (q - 1)

    @staticmethod
    def getE(totient):
        """
        Encontra um valor para e que seja coprimo com o totient.
        """
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
        """
        Calcula o valor de d, o inverso multiplicativo de e mod totient.
        """
        return pow(e, -1, totient)

    @staticmethod
    def gcd(a, b):
        """
        Calcula o máximo divisor comum (GCD) de a e b usando o algoritmo de Euclides.
        """
        while b:
            a, b = b, a % b
        return a

    @staticmethod
    def encrypt(message, e, n):
        """
        Criptografa uma mensagem usando a chave pública (e, n) com preenchimento PKCS#1 v1.5.
        
        Args:
            message (str): A mensagem a ser criptografada.
            e (int): O expoente público.
            n (int): O módulo.

        Returns:
            str: A mensagem criptografada, com valores separados por vírgulas.
        """
        # Converte a mensagem para bytes
        message_bytes = message.encode('utf-8')
        k = (n.bit_length() + 7) // 8  # Tamanho em bytes do módulo n
        padding_length = k - len(message_bytes) - 3
        if padding_length < 8:
            raise ValueError("Mensagem muito longa")

        # Gera o preenchimento
        padding = b'\x00' + b'\x02' + getrandbits(8 * padding_length).to_bytes(padding_length, 'big').replace(b'\x00', b'\x01') + b'\x00' + message_bytes

        # Converte o preenchimento para um inteiro e criptografa
        m = int.from_bytes(padding, 'big')
        c = pow(m, e, n)
        return str(c)

    @staticmethod
    def decrypt(cipher, d, n):
        """
        Descriptografa uma mensagem cifrada usando a chave privada (d, n) com preenchimento PKCS#1 v1.5.
        
        Args:
            cipher (str): A mensagem cifrada, com valores separados por vírgulas.
            d (int): O expoente privado.
            n (int): O módulo.

        Returns:
            str: A mensagem descriptografada.
        """
        # Converte a mensagem cifrada para um inteiro
        c = int(cipher)
        m = pow(c, d, n)

        # Converte o inteiro descriptografado para bytes
        message_bytes = m.to_bytes((m.bit_length() + 7) // 8, 'big')
        
        # Remove o preenchimento PKCS#1 v1.5
        if message_bytes[0:1] != b'\x02':
            raise ValueError("Erro de preenchimento")
        message_bytes = message_bytes[2:]
        message_bytes = message_bytes[message_bytes.index(b'\x00') + 1:]

        # Converte os bytes de volta para uma string
        return message_bytes.decode('utf-8')

    @staticmethod
    def format_public_key(e, n):
        """
        Formata a chave pública (e, n) como uma string.
        
        Args:
            e (int): O expoente público.
            n (int): O módulo.

        Returns:
            str: A chave pública formatada como uma string.
        """
        return f"{e},{n}"

    @staticmethod
    def get_public_key(formatted_public_key):
        """
        Converte uma chave pública formatada de volta para uma tupla de inteiros (e, n).
        
        Args:
            formatted_public_key (str): A chave pública formatada como uma string.

        Returns:
            tuple: A chave pública como uma tupla de inteiros (e, n).
        """
        e, n = formatted_public_key.split(',')
        return int(e), int(n)
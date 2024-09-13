import math
from random import randrange, getrandbits
from sympy import isprime
from concurrent.futures import ThreadPoolExecutor
from multiprocessing import Pool, cpu_count


class RSA:
    @staticmethod
    def generate_prime_number(length=1024):
        """
        Gera um número primo de um determinado comprimento de bits.
        Utiliza múltiplas threads para verificar números aleatórios em paralelo.
        """
        def check_prime():
            """
            Gera um número aleatório e verifica se é primo.
            """
            numero = getrandbits(length)
            return numero if isprime(numero) else None

        with ThreadPoolExecutor(max_workers=cpu_count()) as executor:
            while True:
                # Submete 100 tarefas para verificar números primos em paralelo
                futures = [executor.submit(check_prime) for _ in range(100)]
                for future in futures:
                    result = future.result()
                    if result is not None:
                        return result

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
        Encontra um valor para e que seja coprimo com o totiente.
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
        Criptografa uma mensagem usando a chave pública (e, n).
        
        Args:
            message (str): A mensagem a ser criptografada.
            e (int): O expoente público.
            n (int): O módulo.

        Returns:
            str: A mensagem criptografada, com valores separados por vírgulas.
        """
        cipher = []
        for char in message:
            # Converte o caractere para seu valor ASCII, eleva à potência e módulo n
            cipher.append(str(pow(ord(char), e, n)))
        # Junta os valores criptografados em uma string, separados por vírgulas
        return ",".join(cipher)

    @staticmethod
    def decrypt(cipher, d, n):
        """
        Descriptografa uma mensagem cifrada usando a chave privada (d, n).
        
        Args:
            cipher (str): A mensagem cifrada, com valores separados por vírgulas.
            d (int): O expoente privado.
            n (int): O módulo.

        Returns:
            str: A mensagem descriptografada.
        """
        decrypted = []
        # Divide a mensagem cifrada em caracteres individuais e remove espaços em branco
        cipherCharacters = [i.strip() for i in cipher.split(",") if i.strip()]
        for encrypted in cipherCharacters:
            encryptedInt = int(encrypted)  # Converte o caractere cifrado para inteiro
            # Descriptografa o caractere usando a chave privada (d, n)
            decrypted.append(chr(pow(encryptedInt, d, n)))
        return "".join(decrypted)  # Junta os caracteres descriptografados em uma string

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
    def get_public_key(formated_public_key):
        """
        Converte uma chave pública formatada de volta para uma tupla de inteiros (e, n).
        
        Args:
            formated_public_key (str): A chave pública formatada como uma string.

        Returns:
            tuple: A chave pública como uma tupla de inteiros (e, n).
        """
        e, n = formated_public_key.split(",")
        return int(e), int(n)
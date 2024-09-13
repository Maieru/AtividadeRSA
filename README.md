# RSA Encryption/Decryption Project

Este projeto implementa um sistema de criptografia e descriptografia RSA, incluindo a geração de chaves públicas e privadas, criptografia de mensagens e descriptografia de mensagens. O projeto também inclui um cliente e um servidor para comunicação segura.

## Visão Geral

O RSA é um algoritmo de criptografia assimétrica amplamente utilizado para proteger dados. Ele utiliza um par de chaves: uma chave pública para criptografar dados e uma chave privada para descriptografar dados.

## Funcionalidades

- Geração de números primos grandes
- Geração de chaves públicas e privadas
- Criptografia de mensagens usando a chave pública
- Descriptografia de mensagens usando a chave privada
- Comunicação segura entre cliente e servidor

## Estrutura do Projeto

- `rsa.py`: Implementa as funções principais do algoritmo RSA, incluindo geração de chaves, criptografia e descriptografia.
- `client.py`: Implementa o cliente que se comunica com o servidor, enviando mensagens criptografadas e recebendo respostas criptografadas.
- `server.py`: Implementa o servidor que se comunica com o cliente, recebendo mensagens criptografadas, descriptografando-as, processando-as e enviando respostas criptografadas.
- `comunicationConstants.py`: Contém constantes de configuração para a comunicação entre cliente e servidor, como o endereço IP do servidor e a porta.

## Requisitos

- Python 3.x
- Bibliotecas: `sympy`, `concurrent.futures`, `socket`

## Instalação

1. Clone o repositório:
   ```sh
   git clone https://github.com/seu-usuario/seu-repositorio.git
   cd seu-repositorio

2. Instale as dependências:
    pip install sympy

## Uso

### Executando o Cliente
Em outro terminal, inicie o cliente:

Exemplo de Uso
1. O servidor gera um par de chaves RSA e aguarda conexões de clientes.
2. O cliente gera seu próprio par de chaves RSA e se conecta ao servidor.
3. O cliente e o servidor trocam chaves públicas.
4. O cliente criptografa uma mensagem usando a chave pública do servidor e envia a mensagem criptografada.
5. O servidor descriptografa a mensagem usando sua chave privada, processa a mensagem e envia uma resposta criptografada de volta ao cliente.
6. O cliente descriptografa a resposta usando sua chave privada.
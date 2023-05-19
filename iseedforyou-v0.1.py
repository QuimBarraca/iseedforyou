import hashlib
import binascii
import time
import subprocess
import secrets

# ---------------------------------------------------------------------------------------------------------------------
print("")
print("ESTE UTILITARIO GRATUITO PODE SER COPIADO, DISTRIBUIDO E MODIFICADO LIVREMENTE E NÃO OFERECE QUALQUER ")
print("GARANTIA. OS SCRIPTS [rolls.py] [rolls12.py] https://coldcard.com/docs/verifying-dice-roll-math ")
print("SÃO PROPRIEDADE DA COINKITE INC https://coinkite.com/ ")
print("")
print("[ DOAÇÕES PELA LIGHTNING NETWORK: ]")
print("matureprice28@walletofsatoshi.com")
print("")
print(" ------------------ ")
print("[ ISEEDFORYOU V0.1 ]")
print(" ------------------ ")
print("")
# mensagem ------------------------------------------------------------------------------------------------------------

print("[ A T E N Ç Ã O ]")
print("A QUALIDADE DA ENTROPIA DEPENDE MUITO DA QUALIDADE DA PASSWORD, SALT E DO N. DE ITERAÇÕES ")
print("CASO OPTE POR SALT ALEATORIO, TOME NOTA DA [PASSWORD - SALT - N. DE ITERAÇÕES] CASO PRETENDA RECRIAR ")
print("A MESMA SEED NO FUTURO. COMO SEGURANÇA ADICIONAL, ADICIONE PASSPHRASE À SUA SEED, [ 25 WORD ]")
print("")

# password input ------------------------------------------------------------------------------------------------------

password = ""
while not password:
    password = input("[Digite a sua PASSWORD:] ")
    if not password:
        print("A PASSWORD não pode estar em branco!!!")

# salt input ----------------------------------------------------------------------------------------------------------

salt_choice = input("[Deseja que eu crie um SALT aleatorio? (S/N):] ")

if salt_choice.lower() == 's':
    salt = secrets.token_hex(32).encode('utf-8')
    use_key1 = True
    print("[O salt aleatorio e:] ", salt.decode())
else:
    salt = ""
    while not salt:
        salt = input("[Digite o seu SALT:] ")
        if not salt:
            print("O SALT não pode estar em branco !!!")
    use_key1 = False

# iterations ----------------------------------------------------------------------------------------------------------
while True:
    iterations_input = input("[Digite o N. iterações por ex. 100000:] ")
    try:
        iterations = int(iterations_input)
        if iterations > 0:
            break
        else:
            print("Entrada Inválida. Digite um N. Superior a 0.")
    except ValueError:
        print("Valor inválido. Digite um N. Superior a 0.")

if use_key1:
    tic = time.perf_counter()
    key1 = hashlib.pbkdf2_hmac('sha512', password.encode('utf-8'), salt, iterations, dklen=64)
    toc = time.perf_counter()
    print(f"[A entropia 512bits foi criada em  {toc - tic:0.4f} segundos]", "[", binascii.hexlify(key1).decode(), "]")
    with open("entropia.txt", "w") as f:
        f.write(binascii.hexlify(key1).decode())
else:
    tic = time.perf_counter()
    key2 = hashlib.pbkdf2_hmac('sha512', password.encode('utf-8'), salt.encode('utf-8'), iterations, dklen=64)
    toc = time.perf_counter()
    print(f"[A entropia 512bits foi criada em  {toc - tic:0.4f} segundos]", "[", binascii.hexlify(key2).decode(), "]")
    with open("entropia.txt", "w") as f:
        f.write(binascii.hexlify(key2).decode())


# MENU
opcoes = ["SEED 12 Palavras", "SEED 24 Palavras"]
opcao_selecionada = None
print()
print("[ Escolha uma das seguintes opções: ]")
print()
for i, opcao in enumerate(opcoes):
    print(f"{i + 1}. {opcao}")

while opcao_selecionada is None:
    escolha = input("Opção escolhida: ")
    try:
        escolha_int = int(escolha)
        if escolha_int < 1 or escolha_int > len(opcoes):
            print("Opção inválida. Tente novamente.")
        else:
            opcao_selecionada = opcoes[escolha_int - 1]
    except ValueError:
        print("Opção inválida. Tente novamente.")

if opcao_selecionada == "SEED 12 Palavras":
    comando = "cat entropia.txt | python3 rolls12.py && rm entropia.txt"
    resultado = subprocess.run(comando, stdout=subprocess.PIPE, shell=True, text=True)
    print()
    print(resultado.stdout)
elif opcao_selecionada == "SEED 24 Palavras":
    comando = "cat entropia.txt | python3 rolls.py && rm entropia.txt"
    resultado = subprocess.run(comando, stdout=subprocess.PIPE, shell=True, text=True)
    print()
    print(resultado.stdout)
else:
    print(f"Você escolheu a opção '{opcao_selecionada}'.")

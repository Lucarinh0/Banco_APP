from datetime import datetime

Limite = 500
Opcao = 0
cpf = 0
Numero_de_contas = 1
Numero = 0

Usuarios = {
    00000000000: {"Nome": "Adm", "Idade": 18, "Endereco": "logradouro, nro, bairro - cidade/sigla", "Senha": 0000},
}

Contas = {
    1: {
        "Usuario": "Adm",
        "Agencia": "0001",
        "Saldo": 0,
        "Depositos": [],
        "Saques": [],
        "Limite_De_Transacao": 0,
        "Numero_De_Saque": 0
    }
}

def Menu_Login():
    global Opcao
    Titulo = "Bem vindo"
    Menuzinho_Login = """[1] Login
[2] Registrar-se
[3] Sair
"""
    print(Titulo.center(25, "-"))
    print(Menuzinho_Login)
    Opcao = int(input("Ação desejada: "))
    return Opcao

def Menu_Contas():
    global Opcao, cpf
    nome = Usuarios[cpf]["Nome"]
    Titulo = f"Bem vindo {nome}"
    Menuzinho_Login = """[1] Entrar em conta
[2] Registrar nova conta
[3] Sair
"""
    print(Titulo.center(25, "-"))
    print(Menuzinho_Login)
    Opcao = int(input("Ação desejada: "))
    return Opcao

def Entrar_Conta():
    global Numero, Contas, cpf
    nome_logado = Usuarios[cpf]["Nome"]
    contas_do_usuario = {numero: conta for numero, conta in Contas.items() if conta["Usuario"] == nome_logado}
    
    if not contas_do_usuario:
        print("Você não possui contas registradas.\n")
        return

    print("Suas contas disponíveis:")
    for numero, conta in contas_do_usuario.items():
        print(f"Número da conta: {numero} - Agência: {conta['Agencia']} - Saldo: R${conta['Saldo']:.2f}")

    Numero = int(input("Qual conta deseja entrar? "))
    print(f"Login na conta de número {Numero}\n")

    while True:
            opcao = Menu()
            if opcao == 1:
                valor = float(input("Valor para depósito: "))
                Acao_Deposito(valor)
            elif opcao == 2:
                valor = float(input("Valor para saque: "))
                Acao_Saque(valor)
            elif opcao == 3:
                Extrato()
            elif opcao == 4:
                break
            else:
                print("Opção inválida.")
    else:
        print("Número de conta inválido!")

def Registrar_Conta():
    global Contas, cpf, Numero_de_contas
    nome = Usuarios[cpf]["Nome"]
    print('''Criar nova conta? 
[1] Sim
[2] Não''')
    opcao = int(input("Insira ação desejada: "))
    if opcao == 1:
        Numero_de_contas += 1
        Contas[Numero_de_contas] = {
            "Usuario": nome,
            "Agencia": "0001",
            "Saldo": 0,
            "Depositos": [],
            "Saques": [],
            "Limite_De_Transacao": 0,
            "Numero_De_Saque": 0
        }
        print("Conta registrada com sucesso.\n")
    else:
        print("Conta não registrada.\n")

def Menu():
    global Opcao, cpf, Numero
    nome = Usuarios[cpf]["Nome"]
    Titulo_menu = f"Bem vindo {nome} à conta número {Numero}"
    Menuzinho = """[1] Depositar
[2] Sacar
[3] Extrato
[4] Sair
"""
    print(Titulo_menu.center(25, "-"))
    print(Menuzinho)
    Opcao = int(input("Ação desejada: "))
    return Opcao

def Login():
    global Usuarios, cpf
    cpf = int(input("Insira seu CPF: "))
    if cpf in Usuarios:
        senha = int(input("Insira sua senha: "))
        if senha == Usuarios[cpf]["Senha"]:
            nome = Usuarios[cpf]["Nome"]
            print(f"Bem vindo {nome}\n")
            Tela_2()
        else:
            print("Senha incorreta.\n")
    else:
        print("CPF inválido.\n")

def Acao_Deposito(valor_depositado):
    global Numero
    conta = Contas[Numero]
    if valor_depositado > 0 and conta["Limite_De_Transacao"] < 10:
        conta["Saldo"] += valor_depositado
        data = datetime.now().strftime("%H:%M:%S da data %d/%m/%Y")
        conta["Limite_De_Transacao"] += 1
        conta["Depositos"].append(f'R${valor_depositado:.2f} às {data}')
        print("Saldo depositado com sucesso!\n")
    elif valor_depositado <= 0:
        print("Depósito inválido\n")

    else:
        print("Limite de transação diario atingido \n")

def Acao_Saque(valor_sacado):
    global Numero
    conta = Contas[Numero]
    if valor_sacado <= conta["Saldo"] and valor_sacado <= Limite and conta["Numero_De_Saque"] < 3 and conta["Limite_De_Transacao"] < 10:
        conta["Saldo"] -= valor_sacado
        conta["Numero_De_Saque"] += 1
        conta["Limite_De_Transacao"] += 1
        data = datetime.now().strftime("%H:%M:%S da data %d/%m/%Y")
        conta["Saques"].append(f'R${valor_sacado:.2f} às {data}')
        print("Valor sacado com sucesso!")
        print("Retire o seu dinheiro na boca do caixa\n")
    elif valor_sacado > conta["Saldo"]:
        print("Saldo insuficiente.\n")
    elif conta["Numero_De_Saque"] >= 3:
        print("Limite de saques diário atingido.\n")
    elif conta["Limite_De_Transacao"] >= 10:
        print("Limite de transações diário atingido.\n")
    else:
        print("Valor acima do limite permitido (R$500).\n")

def Extrato():
    global Numero
    conta = Contas[Numero]
    print("------- Extrato -------")
    print("Depósitos realizados:")
    for deposito in conta["Depositos"]:
        print(deposito)
    print("\nSaques realizados:")
    for saque in conta["Saques"]:
        print(saque)
    print(f"\nSaldo atual: R${conta['Saldo']:.2f}")
    print("------------------------\n")

def Registrar_Clientes():
    global Usuarios, cpf
    cpf = int(input("Insira seu CPF: "))
    if cpf in Usuarios:
        print("CPF já registrado.\n")
    else:
        Usuarios[cpf] = {
            "Nome": input("Insira seu nome: "),
            "Idade": int(input("Insira sua idade: ")),
            "Endereco": input("Insira seu endereço: "),
            "Senha": int(input("Insira a senha desejada: "))
        }
        print("Cliente registrado com sucesso!\n")

def inicio():
    while True:
        Menu_Login()
        if Opcao == 1:
            Login()
        elif Opcao == 2:
            Registrar_Clientes()
        elif Opcao == 3:
            exit()
        else:
            print("Opção inválida.\n")

def Tela_2():
    while True:
        opcao = Menu_Contas()
        if opcao == 1:
            Entrar_Conta()
        elif opcao == 2:
            Registrar_Conta()
        elif opcao == 3:
            inicio()
        else:
            print("Opção inválida.\n")

inicio()

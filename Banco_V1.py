Saldo = float(0)
Saques = ([])
Depositos = ([])
Valor_Depositado = float(0)
Valor_Sacado = float(0)
Numero_de_Saque = 0
Limite = float(500)

while True:
    Titulo_menu = "Bem vindo"
    Menu = """[1] Depositar
[2] Sacar
[3] Extrato
[4] Sair
    """
    print(Titulo_menu.center(14, "-"))
    print(Menu)

    opcao = int(input("ação: "))

    if opcao == 1:
        Valor_Depositado = float(input("Valor a ser depositado: "))
        if Valor_Depositado <= 0:
            print("Valor de deposito invalido")

        else:
            Saldo += Valor_Depositado
            Depositos.append(f'R$: {Valor_Depositado: .2f}')
            print("Saldo depositado com sucesso")

    elif opcao == 2:
        Valor_Sacado = float(input("Valor a ser sacado: "))
        if Valor_Sacado <= Saldo and Valor_Sacado <= Limite and Numero_de_Saque < 3:
                Saldo -= Valor_Sacado
                Numero_de_Saque += 1
                Saques.append(f'R$: {Valor_Sacado: .2f}')
                print("Valor sacado com sucesso")
                print("Retire o seu dinheiro na boca do caixa")

        elif Valor_Sacado > Saldo:
            print("Valor informado, acima do saldo da sua conta")

        elif Numero_de_Saque >= 3:
            print("Limite de saque diario atingido")

        else:
            print("Valor informado, acima do limite de 500R$")

    elif opcao == 3:
        D = 0
        S = 0
        print("-------Extrato-------")
        print("Depositos realizados: ")
        while D < len(Depositos):
            print(Depositos[D])
            D = D + 1
        print("Saques realizados: ")
        while S < len(Saques):
            print(Saques[S])
            S = S + 1
        print(f"Saldo: R$:{Saldo: .2f}")
        print("---------------------")

    elif opcao == 4:
        print("Obrigado pela preferencia!\nTenha um bom dia")
        break

    else:
        print("Ação invalida")

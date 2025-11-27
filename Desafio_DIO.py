menu = """

[d] Depositar
[s] Sacar
[e] Extrato
[q] Sair

=> """

saldo = 0
limite = 500
extrato = ""
numero_saques = 0
LIMITE_SAQUES = 3

while True:

    opcao = input(menu)

    if opcao == "d":
        valor = float(input("Informe o valor do depósito: "))

        if valor > 0:
            saldo += valor
            extrato += f"Depósito: R$ {valor:.2f}\n"

        else:
            print("Operação falhou! O valor informado é inválido.")

    elif opcao == "s":
        valor = float(input("Informe o valor do saque: "))

        excedeu_saldo = valor > saldo

        excedeu_limite = valor > limite

        excedeu_saques = numero_saques >= LIMITE_SAQUES

        if excedeu_saldo:
            print("Operação falhou! Você não tem saldo suficiente.")

        elif excedeu_limite:
            print("Operação falhou! O valor do saque excede o limite.")

        elif excedeu_saques:
            print("Operação falhou! Número máximo de saques excedido.")

        elif valor > 0:
            saldo -= valor
            extrato += f"Saque: R$ {valor:.2f}\n"
            numero_saques += 1

        else:
            print("Operação falhou! O valor informado é inválido.")

    elif opcao == "e":
        print("\n================ EXTRATO ================")
        print("Não foram realizadas movimentações." if not extrato else extrato)
        print(f"\nSaldo: R$ {saldo:.2f}")
        print("==========================================")

    elif opcao == "q":
        break

    else:
        print("Operação inválida, por favor selecione novamente a operação desejada.")

        #Descrição do Desafio:
        # Contribuição no projeto do professor Gustavo Guanabara, com a criação de duas novas funções do sistema bancário:
        # Primeira: Criação de novo usario com nome e CPF.
        # Segunda: Consulta de saldo e extrato por usuário logado.
        # Terceira: criar conta corrente vinculada ao usuário.

        
        #📄 Transcrição do Conteúdo
        # Função Depósito
        # A função depósito deve receber os argumentos apenas por posição (positional only). 
        # Sugestão de argumentos: saldo, valor, extrato. Sugestão de retorno: saldo e extrato.

        # Função Extrato
        # A função extrato deve receber os argumentos por posição e nome (positional only e keyword only). 
        # Argumentos posicionais: saldo, argumentos nomeados: extrato.

        # Novas funções
        # Precisamos criar duas novas funções: 
        # criar usuário e criar conta corrente. 
        # Fique a vontade para adicionar mais funções, exemplo: listar contas.
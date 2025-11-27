import json
import os

# --- Constantes e Configurações ---
ARQUIVO_USUARIOS = "usuarios.json"
ARQUIVO_CONTAS = "contas.json"  
AGENCIA = "0001" 
LIMITE_CONTAS_POR_USUARIO = 10
LIMITE_SAQUES = 3
LIMITE_VALOR_SAQUE = 500 

# --- Funções de Persistência de Dados (Usuarios) ---

def carregar_usuarios():
    """Carrega a lista de usuários do arquivo JSON, tratando UnicodeError e JSONDecodeError."""
    if os.path.exists(ARQUIVO_USUARIOS):
        try:
            # Tenta abrir e ler o arquivo
            with open(ARQUIVO_USUARIOS, 'r', encoding='utf-8') as f:
                conteudo = f.read()
                # Verifica se o conteúdo está vazio antes de tentar decodificar (JSONDecodeError)
                return json.loads(conteudo) if conteudo else []
        except (UnicodeDecodeError, json.JSONDecodeError) as e:
            print(f"\n⚠️ ERRO DE LEITURA DO ARQUIVO {ARQUIVO_USUARIOS}: {e}")
            print("O arquivo será sobrescrito se novos usuários forem cadastrados.")
            # Se der erro de decodificação ou JSON inválido, retorna uma lista vazia
            return []
    return []

def salvar_usuarios(usuarios):
    """Salva a lista de usuários no arquivo JSON."""
    with open(ARQUIVO_USUARIOS, 'w', encoding='utf-8') as f:
        json.dump(usuarios, f, indent=4)

# --- Funções de Persistência de Dados (Contas) ---

def carregar_contas(usuarios):
    """Carrega a lista de contas do arquivo JSON, tratando erros."""
    if os.path.exists(ARQUIVO_CONTAS):
        try:
            with open(ARQUIVO_CONTAS, 'r', encoding='utf-8') as f:
                conteudo = f.read()
                if not conteudo:
                    return []
                
                contas_serializadas = json.loads(conteudo)
                
                # Reconstrói a referência do usuário no dicionário da conta
                contas_reconstruidas = []
                for conta_s in contas_serializadas:
                    cpf = conta_s.get("cpf_usuario") 
                    usuario_vinculado = filtrar_usuario(cpf, usuarios)
                    
                    if usuario_vinculado:
                        del conta_s["cpf_usuario"] 
                        conta_s["usuario"] = usuario_vinculado 
                        contas_reconstruidas.append(conta_s)
                        
                return contas_reconstruidas
        except (UnicodeDecodeError, json.JSONDecodeError) as e:
            print(f"\n⚠️ ERRO DE LEITURA DO ARQUIVO {ARQUIVO_CONTAS}: {e}")
            print("As contas serão descartadas na inicialização.")
            return []
    return []

def salvar_contas(contas):
    """Salva a lista de contas no arquivo JSON."""
    contas_serializaveis = []
    for conta in contas:
        conta_s = conta.copy() 
        conta_s["cpf_usuario"] = conta_s["usuario"]["cpf"] 
        del conta_s["usuario"] 
        contas_serializaveis.append(conta_s)
    
    with open(ARQUIVO_CONTAS, 'w', encoding='utf-8') as f:
        json.dump(contas_serializaveis, f, indent=4)
        
# --- Funções Auxiliares (Mantidas) ---

def filtrar_usuario(cpf, usuarios):
    """Retorna o dicionário do usuário encontrado."""
    usuarios_filtrados = [usuario for usuario in usuarios if usuario["cpf"] == cpf]
    return usuarios_filtrados[0] if usuarios_filtrados else None

def recuperar_conta_usuario(usuario, contas):
    """Busca e retorna a primeira conta vinculada a um usuário (dicionário)."""
    contas_usuario = [conta for conta in contas if conta["usuario"]["cpf"] == usuario["cpf"]]
    return contas_usuario[0] if contas_usuario else None

# --- Funções de Operação (Mantidas) ---

def depositar(saldo, valor, extrato, contas, /): 
    """Realiza a operação de depósito na conta e salva."""
    if valor > 0:
        saldo += valor
        extrato += f"Depósito: R$ {valor:.2f}\n"
        print("\n✅ Depósito realizado com sucesso!")
        salvar_contas(contas) 
    else:
        print("\n❌ Operação falhou! O valor informado é inválido.")
    
    return saldo, extrato

def sacar(*, saldo, valor, extrato, limite, numero_saques, limite_saques, contas): 
    """Realiza a operação de saque na conta e salva."""

    excedeu_saldo = valor > saldo
    excedeu_limite = valor > limite
    excedeu_saques = numero_saques >= limite_saques

    if excedeu_saldo:
        print("\n❌ Operação falhou! Você não tem saldo suficiente.")
    elif excedeu_limite:
        print("\n❌ Operação falhou! O valor do saque excede o limite.")
    elif excedeu_saques:
        print("\n❌ Operação falhou! Número máximo de saques excedido.")
    elif valor > 0:
        saldo -= valor
        extrato += f"Saque: R$ {valor:.2f}\n"
        numero_saques += 1
        print("\n✅ Saque realizado com sucesso!")
        salvar_contas(contas) 
    else:
        print("\n❌ Operação falhou! O valor informado é inválido.")
        
    return saldo, extrato, numero_saques

# --- Funções de Cadastro (Mantidas) ---

def criar_usuario(usuarios):
    """Cadastra um novo usuário e salva."""
    cpf = input("Informe o CPF (somente números): ")
    if filtrar_usuario(cpf, usuarios):
        print("\n❌ ERRO: Já existe usuário com este CPF!")
        return
    
    nome = input("Informe o nome completo: ")
    data_nascimento = input("Informe a data de nascimento (dd-mm-aaaa): ")
    logradouro = input("Informe o logradouro (ex: Rua Brasil): ")
    numero = input("Informe o número: ")
    bairro = input("Informe o bairro: ")
    cidade = input("Informe a cidade: ")
    estado = input("Informe a sigla do estado (ex: PR): ")
    endereco = f"{logradouro}, {numero} - {bairro} - {cidade}/{estado}"

    usuarios.append({"nome": nome, "data_nascimento": data_nascimento, "cpf": cpf, "endereco": endereco})
    salvar_usuarios(usuarios) 
    print("\n✅ Usuário cadastrado com sucesso e salvo!")

def criar_conta(agencia, numero_conta, usuarios, contas):
    """Cria uma nova conta corrente vinculada a um usuário existente e salva."""
    cpf = input("Informe o CPF do usuário (somente números): ")
    usuario = filtrar_usuario(cpf, usuarios)

    if not usuario:
        print("\n❌ ERRO: Usuário não encontrado, o cadastro da conta não foi realizado!")
        return
    
    contas_do_usuario = [c for c in contas if c["usuario"]["cpf"] == cpf]
    if len(contas_do_usuario) >= LIMITE_CONTAS_POR_USUARIO:
        print(f"\n❌ ERRO: Usuário já possui o limite de {LIMITE_CONTAS_POR_USUARIO} contas cadastradas.")
        return

    contas.append({
        "agencia": agencia,
        "numero_conta": numero_conta,
        "saldo": 0,               
        "limite": LIMITE_VALOR_SAQUE, 
        "extrato": "",            
        "numero_saques": 0,       
        "usuario": usuario 
    })
    
    salvar_contas(contas) 
    print("\n✅ Conta criada com sucesso e salva!")


def listar_contas(contas):
    """Exibe todas as contas correntes cadastradas no sistema."""
    if not contas:
        print("\n⚠️ Nenhuma conta cadastrada.")
        return

    print("\n============== LISTA DE CONTAS ==============")
    for conta in contas:
        linha = f"""
            Agência:\t{conta['agencia']}
            C/C:\t\t{conta['numero_conta']}
            Titular:\t{conta['usuario']['nome']}
            Saldo:\t\tR$ {conta['saldo']:.2f}
        """
        print("=" * 45)
        print(linha.strip())
    print("=============================================")


# --- Variáveis Globais e Inicialização ---
menu = f"""
[d] Depositar
[s] Sacar
[e] Extrato
[n] Novo Usuário
[nc] Nova Conta
[lc] Listar Contas
[q] Sair

=> """

# Carregamento: Agora mais robusto contra erros de codificação e arquivos vazios
USUARIOS = carregar_usuarios() 
CONTAS = carregar_contas(USUARIOS) 

# --- Loop Principal (Mantido) ---
while True:

    opcao = input(menu)
    
    if opcao in ("d", "s", "e"):
        
        cpf_operacao = input("Informe o CPF do cliente para acessar a conta: ")
        usuario = filtrar_usuario(cpf_operacao, USUARIOS)
        if not usuario:
            print("\n❌ ERRO: Cliente não encontrado.")
            continue
            
        conta = recuperar_conta_usuario(usuario, CONTAS)
        if not conta:
            print(f"\n❌ ERRO: Usuário {usuario['nome']} não possui conta cadastrada.")
            continue
            
        if opcao == "d":
            valor = float(input("Informe o valor do depósito: "))
            conta['saldo'], conta['extrato'] = depositar(conta['saldo'], valor, conta['extrato'], CONTAS)

        elif opcao == "s":
            valor = float(input("Informe o valor do saque: "))
            conta['saldo'], conta['extrato'], conta['numero_saques'] = sacar(
                saldo=conta['saldo'], 
                valor=valor, 
                extrato=conta['extrato'], 
                limite=conta['limite'], 
                numero_saques=conta['numero_saques'], 
                limite_saques=LIMITE_SAQUES,
                contas=CONTAS
            )

        elif opcao == "e":
            print("\n================ EXTRATO ================")
            print(f"Conta: {conta['agencia']}-{conta['numero_conta']} | Cliente: {conta['usuario']['nome']}")
            print("-----------------------------------------")
            print("Não foram realizadas movimentações." if not conta['extrato'] else conta['extrato'])
            print(f"\nSaldo Atual: R$ {conta['saldo']:.2f}")
            print("==========================================")
            
    elif opcao == "n":
        criar_usuario(USUARIOS)

    elif opcao == "nc": 
        numero_conta = len(CONTAS) + 1
        criar_conta(AGENCIA, numero_conta, USUARIOS, CONTAS)

    elif opcao == "lc": 
        listar_contas(CONTAS)

    elif opcao == "q":
        break

    else:
        print("Operação inválida, por favor selecione novamente a operação desejada.")
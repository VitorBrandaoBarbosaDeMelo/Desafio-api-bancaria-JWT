"""
Script de teste para a API Bancária
Exemplos de como fazer requisições à API usando a biblioteca requests
"""

import requests
import json
from typing import Optional

# Configuração
BASE_URL = "http://localhost:8000"
API_V1 = f"{BASE_URL}/api/v1"

# Variáveis globais para armazenar token e CPF
current_token = None
current_cpf = None

class Cores:
    """Classe para colorir o output do terminal"""
    VERDE = '\033[92m'
    VERMELHO = '\033[91m'
    AMARELO = '\033[93m'
    AZUL = '\033[94m'
    RESET = '\033[0m'
    NEGRITO = '\033[1m'

def print_header(titulo):
    """Imprime um header formatado"""
    print(f"\n{Cores.NEGRITO}{Cores.AZUL}{'='*60}{Cores.RESET}")
    print(f"{Cores.NEGRITO}{Cores.AZUL}{titulo:^60}{Cores.RESET}")
    print(f"{Cores.NEGRITO}{Cores.AZUL}{'='*60}{Cores.RESET}\n")

def print_sucesso(mensagem):
    """Imprime mensagem de sucesso"""
    print(f"{Cores.VERDE}✓ {mensagem}{Cores.RESET}")

def print_erro(mensagem):
    """Imprime mensagem de erro"""
    print(f"{Cores.VERMELHO}✗ {mensagem}{Cores.RESET}")

def print_info(mensagem):
    """Imprime mensagem informativa"""
    print(f"{Cores.AMARELO}ℹ {mensagem}{Cores.RESET}")

def print_response(response):
    """Imprime resposta formatada"""
    try:
        print(json.dumps(response.json(), indent=2, ensure_ascii=False))
    except:
        print(response.text)

def get_headers():
    """Retorna headers com token JWT se disponível"""
    headers = {"Content-Type": "application/json"}
    if current_token:
        headers["Authorization"] = f"Bearer {current_token}"
    return headers

# ============================================================================
# TESTES DOS ENDPOINTS
# ============================================================================

def test_health_check():
    """Testa health check da API"""
    print_header("🏥 HEALTH CHECK")
    
    try:
        response = requests.get(f"{API_V1}/health")
        if response.status_code == 200:
            print_sucesso("API está online!")
            print_response(response)
        else:
            print_erro(f"Status {response.status_code}")
            print_response(response)
    except Exception as e:
        print_erro(f"Erro ao conectar à API: {e}")

def test_registrar_usuario(nome, cpf, data_nascimento, endereco, senha):
    """Testa registro de novo usuário"""
    print_header(f"👤 REGISTRAR USUÁRIO - {nome}")
    
    dados = {
        "nome": nome,
        "cpf": cpf,
        "data_nascimento": data_nascimento,
        "endereco": endereco,
        "senha": senha
    }
    
    try:
        response = requests.post(
            f"{API_V1}/usuarios/registrar",
            json=dados,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            print_sucesso(f"Usuário registrado com sucesso!")
            print_response(response)
            return True
        else:
            print_erro(f"Erro ao registrar: {response.status_code}")
            print_response(response)
            return False
    except Exception as e:
        print_erro(f"Erro: {e}")
        return False

def test_login(cpf, senha):
    """Testa login e obtém token JWT"""
    global current_token, current_cpf
    
    print_header(f"🔐 LOGIN - CPF: {cpf}")
    
    dados = {
        "cpf": cpf,
        "senha": senha
    }
    
    try:
        response = requests.post(
            f"{API_V1}/auth/login",
            json=dados,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            resultado = response.json()
            current_token = resultado['access_token']
            current_cpf = cpf
            print_sucesso(f"Login realizado com sucesso!")
            print_info(f"Token obtido (primeiros 50 caracteres): {current_token[:50]}...")
            print(f"Tempo de expiração: {resultado['expires_in']} segundos")
            return True
        else:
            print_erro(f"Erro ao fazer login: {response.status_code}")
            print_response(response)
            return False
    except Exception as e:
        print_erro(f"Erro: {e}")
        return False

def test_obter_saldo():
    """Testa obtenção do saldo"""
    if not current_token:
        print_erro("Você precisa fazer login primeiro!")
        return
    
    print_header("💰 OBTER SALDO")
    
    try:
        response = requests.get(
            f"{API_V1}/conta/saldo",
            headers=get_headers()
        )
        
        if response.status_code == 200:
            print_sucesso("Saldo obtido com sucesso!")
            dados = response.json()
            print(f"\n{Cores.NEGRITO}Informações da Conta:{Cores.RESET}")
            print(f"  Agência: {dados['agencia']}")
            print(f"  Número da Conta: {dados['numero_conta']}")
            print(f"  Titular: {dados['titular']}")
            print(f"  Saldo: R$ {dados['saldo']:.2f}")
            print(f"  Limite: R$ {dados['limite']:.2f}")
        else:
            print_erro(f"Erro: {response.status_code}")
            print_response(response)
    except Exception as e:
        print_erro(f"Erro: {e}")

def test_depositar(valor):
    """Testa realização de depósito"""
    if not current_token:
        print_erro("Você precisa fazer login primeiro!")
        return
    
    print_header(f"💵 DEPOSITAR - R$ {valor:.2f}")
    
    dados = {"valor": valor}
    
    try:
        response = requests.post(
            f"{API_V1}/transacoes/depositar",
            json=dados,
            headers=get_headers()
        )
        
        if response.status_code == 200:
            resultado = response.json()
            print_sucesso(resultado['mensagem'])
            print(f"\n{Cores.NEGRITO}Detalhes da Transação:{Cores.RESET}")
            print(f"  Valor: R$ {resultado['valor']:.2f}")
            print(f"  Saldo Anterior: R$ {resultado['saldo_anterior']:.2f}")
            print(f"  Saldo Atual: R$ {resultado['saldo_atual']:.2f}")
            print(f"  Data/Hora: {resultado['data']}")
        else:
            print_erro(f"Erro ao depositar: {response.status_code}")
            print_response(response)
    except Exception as e:
        print_erro(f"Erro: {e}")

def test_sacar(valor):
    """Testa realização de saque"""
    if not current_token:
        print_erro("Você precisa fazer login primeiro!")
        return
    
    print_header(f"💸 SACAR - R$ {valor:.2f}")
    
    dados = {"valor": valor}
    
    try:
        response = requests.post(
            f"{API_V1}/transacoes/sacar",
            json=dados,
            headers=get_headers()
        )
        
        if response.status_code == 200:
            resultado = response.json()
            print_sucesso(resultado['mensagem'])
            print(f"\n{Cores.NEGRITO}Detalhes da Transação:{Cores.RESET}")
            print(f"  Valor: R$ {resultado['valor']:.2f}")
            print(f"  Saldo Anterior: R$ {resultado['saldo_anterior']:.2f}")
            print(f"  Saldo Atual: R$ {resultado['saldo_atual']:.2f}")
            print(f"  Saques Restantes: {resultado['saques_restantes']}")
            print(f"  Data/Hora: {resultado['data']}")
        else:
            print_erro(f"Erro ao sacar: {response.status_code}")
            print_response(response)
    except Exception as e:
        print_erro(f"Erro: {e}")

def test_obter_extrato():
    """Testa obtenção do extrato completo"""
    if not current_token:
        print_erro("Você precisa fazer login primeiro!")
        return
    
    print_header("📊 EXTRATO")
    
    try:
        response = requests.get(
            f"{API_V1}/extrato",
            headers=get_headers()
        )
        
        if response.status_code == 200:
            dados = response.json()
            print_sucesso("Extrato obtido com sucesso!")
            print(f"\n{Cores.NEGRITO}Informações da Conta:{Cores.RESET}")
            print(f"  Agência: {dados['agencia']}")
            print(f"  Número: {dados['numero_conta']}")
            print(f"  Titular: {dados['titular']}")
            print(f"  Saldo: R$ {dados['saldo']:.2f}")
            
            if dados['transacoes']:
                print(f"\n{Cores.NEGRITO}Transações:{Cores.RESET}")
                for i, transacao in enumerate(dados['transacoes'], 1):
                    print(f"\n  {i}. {transacao['tipo']}")
                    print(f"     Valor: R$ {transacao['valor']:.2f}")
                    print(f"     Data: {transacao['data']}")
            else:
                print_info("Nenhuma transação realizada")
        else:
            print_erro(f"Erro: {response.status_code}")
            print_response(response)
    except Exception as e:
        print_erro(f"Erro: {e}")

def test_obter_perfil():
    """Testa obtenção do perfil do usuário"""
    if not current_token:
        print_erro("Você precisa fazer login primeiro!")
        return
    
    print_header("👥 PERFIL DO USUÁRIO")
    
    try:
        response = requests.get(
            f"{API_V1}/usuarios/perfil",
            headers=get_headers()
        )
        
        if response.status_code == 200:
            print_sucesso("Perfil obtido com sucesso!")
            print_response(response)
        else:
            print_erro(f"Erro: {response.status_code}")
            print_response(response)
    except Exception as e:
        print_erro(f"Erro: {e}")

# ============================================================================
# SCRIPT DE TESTE AUTOMÁTICO
# ============================================================================

def executar_teste_completo():
    """Executa um teste completo de todos os endpoints"""
    print(f"\n{Cores.NEGRITO}{Cores.VERDE}")
    print("=" * 60)
    print("TESTE COMPLETO DA API BANCÁRIA DIO")
    print("=" * 60)
    print(f"{Cores.RESET}\n")
    
    # 1. Health Check
    test_health_check()
    
    # 2. Registrar Usuário
    print_info("Registrando novo usuário...")
    if test_registrar_usuario(
        nome="João Silva",
        cpf="12345678901",
        data_nascimento="15-03-1990",
        endereco="Rua A, 123 - Centro - São Paulo/SP",
        senha="senha123"
    ):
        # 3. Login
        print_info("Fazendo login...")
        if test_login("12345678901", "senha123"):
            # 4. Obter Saldo
            test_obter_saldo()
            
            # 5. Depositar
            test_depositar(1000.00)
            
            # 6. Obter Saldo após depósito
            test_obter_saldo()
            
            # 7. Sacar
            test_sacar(250.00)
            
            # 8. Obter Saldo após saque
            test_obter_saldo()
            
            # 9. Outro saque
            test_sacar(150.00)
            
            # 10. Obter Extrato
            test_obter_extrato()
            
            # 11. Obter Perfil
            test_obter_perfil()
            
            print_header("✅ TESTE COMPLETO FINALIZADO COM SUCESSO!")
        else:
            print_erro("Falha ao fazer login")
    else:
        print_erro("Falha ao registrar usuário")

if __name__ == "__main__":
    print(f"\n{Cores.NEGRITO}{Cores.AZUL}Certifique-se de que a API está rodando em http://localhost:8000{Cores.RESET}\n")
    
    try:
        # Tentar conexão rápida
        requests.get(f"{BASE_URL}/", timeout=2)
        executar_teste_completo()
    except requests.exceptions.ConnectionError:
        print_erro("Não foi possível conectar à API!")
        print_info("Inicie o servidor com: python -m uvicorn api:app --reload")
    except Exception as e:
        print_erro(f"Erro: {e}")

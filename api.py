"""
API Bancária com FastAPI e JWT
"""

import os
import json
from datetime import datetime, timedelta, timezone
from typing import Optional, List

from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import HTTPBearer
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
import jwt

# --- Configurações ---
ARQUIVO_USUARIOS = "usuarios.json"
ARQUIVO_CONTAS = "contas.json"
SECRET_KEY = "sua-chave-secreta-super-segura"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
AGENCIA = "0001"
LIMITE_VALOR_SAQUE = 500
LIMITE_SAQUES = 3

# --- Modelos ---

class UsuarioRegistro(BaseModel):
    nome: str = Field(..., min_length=3)
    cpf: str = Field(..., min_length=11, max_length=11)
    data_nascimento: str
    endereco: str = Field(..., min_length=5)
    senha: str = Field(..., min_length=6)

class UsuarioLogin(BaseModel):
    cpf: str
    senha: str

class TransacaoRequest(BaseModel):
    valor: float = Field(..., gt=0)

class TransacaoResponse(BaseModel):
    tipo: str
    valor: float
    data: str

class ExtratoResponse(BaseModel):
    numero_conta: str
    agencia: str
    titular: str
    saldo: float
    transacoes: List[TransacaoResponse]

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int

# --- Persistência ---

def carregar_usuarios():
    if not os.path.exists(ARQUIVO_USUARIOS):
        return {}
    try:
        with open(ARQUIVO_USUARIOS, 'r', encoding='utf-8') as f:
            dados = json.load(f)
            return dados if isinstance(dados, dict) else {}
    except:
        return {}

def salvar_usuarios(usuarios):
    with open(ARQUIVO_USUARIOS, 'w', encoding='utf-8') as f:
        json.dump(usuarios, f, indent=4, ensure_ascii=False)

def carregar_contas():
    if not os.path.exists(ARQUIVO_CONTAS):
        return {}
    try:
        with open(ARQUIVO_CONTAS, 'r', encoding='utf-8') as f:
            dados = json.load(f)
            return dados if isinstance(dados, dict) else {}
    except:
        return {}

def salvar_contas(contas):
    with open(ARQUIVO_CONTAS, 'w', encoding='utf-8') as f:
        json.dump(contas, f, indent=4, ensure_ascii=False)

# --- Autenticação ---

def criar_token(cpf: str):
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    payload = {"sub": cpf, "exp": expire}
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

def verificar_token(credentials) -> str:
    try:
        payload = jwt.decode(credentials.credentials, SECRET_KEY, algorithms=[ALGORITHM])
        cpf = payload.get("sub")
        if not cpf:
            raise HTTPException(status_code=401, detail="Token inválido")
        return cpf
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expirado")
    except:
        raise HTTPException(status_code=401, detail="Token inválido")

def contar_saques_dia(cpf: str, contas: dict):
    if cpf not in contas:
        return 0
    conta = contas[cpf]
    hoje = datetime.now().strftime("%d-%m-%Y")
    return sum(1 for t in conta.get('historico_transacoes', [])
               if t['tipo'] == 'Saque' and t['data'].startswith(hoje))

# --- API ---

app = FastAPI(
    title="API Bancária DIO",
    description="""
## API Bancária RESTful Assíncrona

Uma API moderna para gerenciamento de operações bancárias com autenticação JWT segura.

### Funcionalidades

- Registro de Usuários - Criar novas contas bancárias
- Autenticação JWT - Login seguro com tokens
- Depósitos - Transferir dinheiro para a conta
- Saques - Retirar dinheiro com limites e validações
- Extrato - Ver histórico completo de transações
- Consulta de Saldo - Verificar saldo da conta
- Perfil - Visualizar dados do usuário

### Validações Implementadas

- Valores sempre positivos
- Saldo suficiente para saques
- Limite de R$ 500 por saque
- Máximo de 3 saques por dia
- CPF único por usuário
- Senha mínimo 6 caracteres

### Dados Persistidos

- **usuarios.json** - Dados dos usuários
- **contas.json** - Contas e transações

Desenvolvido como parte do **Desafio DIO**
""",
    version="1.0.0",
    openapi_tags=[
        {
            "name": "Sistema",
            "description": "Endpoints gerais e saúde da API"
        },
        {
            "name": "Autenticação",
            "description": "Registro e autenticação de usuários"
        },
        {
            "name": "Conta",
            "description": "Operações e consultas de conta"
        },
        {
            "name": "Transações",
            "description": "Depósitos, saques e extratos"
        },
        {
            "name": "Usuários",
            "description": "Informações do perfil do usuário"
        }
    ]
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Endpoints Públicos ---

@app.get("/", tags=["Sistema"])
async def root():
    return {"mensagem": "API Bancária", "status": "online"}

@app.post("/api/v1/usuarios/registrar", tags=["Autenticação"])
async def registrar(usuario: UsuarioRegistro):
    try:
        usuarios = carregar_usuarios()
        
        if usuario.cpf in usuarios:
            raise HTTPException(status_code=400, detail="CPF já existe")
        
        usuarios[usuario.cpf] = {
            "nome": usuario.nome,
            "cpf": usuario.cpf,
            "data_nascimento": usuario.data_nascimento,
            "endereco": usuario.endereco,
            "senha": usuario.senha,
            "data_criacao": datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        }
        salvar_usuarios(usuarios)
        
        contas = carregar_contas()
        numero_conta = f"{len(contas) + 1:06d}"
        contas[usuario.cpf] = {
            "numero": numero_conta,
            "agencia": AGENCIA,
            "saldo": 0.0,
            "cpf_cliente": usuario.cpf,
            "limite": LIMITE_VALOR_SAQUE,
            "limite_saques": LIMITE_SAQUES,
            "historico_transacoes": [],
            "tipo_conta": "ContaCorrente"
        }
        salvar_contas(contas)
        
        return {
            "mensagem": "Usuário registrado com sucesso",
            "cpf": usuario.cpf,
            "nome": usuario.nome,
            "numero_conta": numero_conta
        }
    except HTTPException:
        raise
    except Exception as e:
        print(f"ERRO: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/v1/auth/login", response_model=TokenResponse, tags=["Autenticação"])
async def login(credenciais: UsuarioLogin):
    usuarios = carregar_usuarios()
    
    if credenciais.cpf not in usuarios:
        raise HTTPException(status_code=401, detail="CPF ou senha incorretos")
    
    usuario = usuarios[credenciais.cpf]
    
    if usuario['senha'] != credenciais.senha:
        raise HTTPException(status_code=401, detail="CPF ou senha incorretos")
    
    token = criar_token(credenciais.cpf)
    
    return {
        "access_token": token,
        "token_type": "bearer",
        "expires_in": ACCESS_TOKEN_EXPIRE_MINUTES * 60
    }

@app.get("/api/v1/health", tags=["Sistema"])
async def health():
    return {"status": "healthy"}

# --- Endpoints Protegidos ---

@app.get("/api/v1/conta/saldo", tags=["Conta"])
async def obter_saldo(credentials = Depends(HTTPBearer())):
    cpf = verificar_token(credentials)
    contas = carregar_contas()
    usuarios = carregar_usuarios()
    
    if cpf not in contas:
        raise HTTPException(status_code=404, detail="Conta não encontrada")
    
    conta = contas[cpf]
    usuario = usuarios.get(cpf, {})
    
    return {
        "agencia": conta['agencia'],
        "numero_conta": conta['numero'],
        "titular": usuario.get('nome', 'N/A'),
        "saldo": conta['saldo'],
        "limite": conta.get('limite', LIMITE_VALOR_SAQUE)
    }

@app.post("/api/v1/transacoes/depositar", tags=["Transações"])
async def depositar(transacao: TransacaoRequest, credentials = Depends(HTTPBearer())):
    cpf = verificar_token(credentials)
    contas = carregar_contas()
    
    if cpf not in contas:
        raise HTTPException(status_code=404, detail="Conta não encontrada")
    
    if transacao.valor <= 0:
        raise HTTPException(status_code=400, detail="Valor deve ser maior que zero")
    
    conta = contas[cpf]
    saldo_anterior = conta['saldo']
    conta['saldo'] += transacao.valor
    
    conta['historico_transacoes'].append({
        "tipo": "Deposito",
        "valor": transacao.valor,
        "data": datetime.now().strftime("%d-%m-%Y %H:%M:%S")
    })
    
    salvar_contas(contas)
    
    return {
        "mensagem": "Depósito realizado com sucesso",
        "valor": transacao.valor,
        "saldo_anterior": saldo_anterior,
        "saldo_atual": conta['saldo'],
        "data": datetime.now().strftime("%d-%m-%Y %H:%M:%S")
    }

@app.post("/api/v1/transacoes/sacar", tags=["Transações"])
async def sacar(transacao: TransacaoRequest, credentials = Depends(HTTPBearer())):
    cpf = verificar_token(credentials)
    contas = carregar_contas()
    
    if cpf not in contas:
        raise HTTPException(status_code=404, detail="Conta não encontrada")
    
    if transacao.valor <= 0:
        raise HTTPException(status_code=400, detail="Valor deve ser maior que zero")
    
    conta = contas[cpf]
    
    if conta['saldo'] < transacao.valor:
        raise HTTPException(
            status_code=400,
            detail=f"Saldo insuficiente. Disponível: R$ {conta['saldo']:.2f}"
        )
    
    if transacao.valor > conta['limite']:
        raise HTTPException(
            status_code=400,
            detail=f"Valor excede limite de R$ {conta['limite']:.2f}"
        )
    
    saques_hoje = contar_saques_dia(cpf, contas)
    if saques_hoje >= conta['limite_saques']:
        raise HTTPException(
            status_code=400,
            detail=f"Limite de {conta['limite_saques']} saques por dia excedido"
        )
    
    saldo_anterior = conta['saldo']
    conta['saldo'] -= transacao.valor
    
    conta['historico_transacoes'].append({
        "tipo": "Saque",
        "valor": transacao.valor,
        "data": datetime.now().strftime("%d-%m-%Y %H:%M:%S")
    })
    
    salvar_contas(contas)
    
    return {
        "mensagem": "Saque realizado com sucesso",
        "valor": transacao.valor,
        "saldo_anterior": saldo_anterior,
        "saldo_atual": conta['saldo'],
        "saques_restantes": conta['limite_saques'] - saques_hoje - 1,
        "data": datetime.now().strftime("%d-%m-%Y %H:%M:%S")
    }

@app.get("/api/v1/extrato", response_model=ExtratoResponse, tags=["Transações"])
async def obter_extrato(credentials = Depends(HTTPBearer())):
    cpf = verificar_token(credentials)
    contas = carregar_contas()
    usuarios = carregar_usuarios()
    
    if cpf not in contas:
        raise HTTPException(status_code=404, detail="Conta não encontrada")
    
    conta = contas[cpf]
    usuario = usuarios.get(cpf, {})
    
    transacoes = [
        TransacaoResponse(**t)
        for t in conta.get('historico_transacoes', [])
    ]
    
    return ExtratoResponse(
        numero_conta=conta['numero'],
        agencia=conta['agencia'],
        titular=usuario.get('nome', 'N/A'),
        saldo=conta['saldo'],
        transacoes=transacoes
    )

@app.get("/api/v1/usuarios/perfil", tags=["Usuários"])
async def obter_perfil(credentials = Depends(HTTPBearer())):
    cpf = verificar_token(credentials)
    usuarios = carregar_usuarios()
    contas = carregar_contas()
    
    if cpf not in usuarios:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    
    usuario = usuarios[cpf]
    conta = contas.get(cpf, {})
    
    return {
        "nome": usuario.get('nome'),
        "cpf": usuario.get('cpf'),
        "endereco": usuario.get('endereco'),
        "data_nascimento": usuario.get('data_nascimento'),
        "data_criacao": usuario.get('data_criacao'),
        "numero_conta": conta.get('numero'),
        "agencia": conta.get('agencia')
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

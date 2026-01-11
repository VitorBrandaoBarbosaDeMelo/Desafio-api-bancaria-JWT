# API Bancária REST com FastAPI e JWT

API moderna para gerenciamento de operações bancárias com autenticação JWT segura.

## Funcionalidades

- Registro de usuários com CPF único
- Autenticação via JWT (tokens de 30 minutos)
- Depósitos sem limite
- Saques com validações (máximo R$500, 3 por dia)
- Consulta de saldo
- Extrato com histórico de transações
- Perfil do usuário
- Dados persistidos em JSON
- Documentação automática com Swagger UI
<img width="405" height="399" alt="3-Swagger pronto" src="https://github.com/user-attachments/assets/cf10d4da-7044-4c33-8b09-6733a5dd0333" />


### Iniciar a API

```bash
python api.py
```

Acesse em: **http://localhost:8000/docs** (Swagger UI)

## Exemplos de Uso

### 1. Registrar usuário

```bash
curl -X POST 'http://localhost:8000/api/v1/usuarios/registrar' \
  -H 'Content-Type: application/json' \
  -d '{
    "nome": "João Silva",
    "cpf": "12345678901",
    "data_nascimento": "15-03-1990",
    "endereco": "Rua A, 123",
    "senha": "senha123"
  }'
```

### 2. Fazer login (obter token JWT)

```bash
curl -X POST 'http://localhost:8000/api/v1/auth/login' \
  -H 'Content-Type: application/json' \
  -d '{
    "cpf": "12345678901",
    "senha": "senha123"
  }'
```

**Resposta:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIs...",
  "token_type": "bearer",
  "expires_in": 1800
}
```

### 3. Fazer depósito (protegido por JWT)

```bash
curl -X POST 'http://localhost:8000/api/v1/transacoes/depositar' \
  -H 'Authorization: Bearer eyJhbGciOiJIUzI1NiIs...' \
  -H 'Content-Type: application/json' \
  -d '{
    "valor": 100.00
  }'
```

### 4. Fazer saque (protegido por JWT)

```bash
curl -X POST 'http://localhost:8000/api/v1/transacoes/sacar' \
  -H 'Authorization: Bearer eyJhbGciOiJIUzI1NiIs...' \
  -H 'Content-Type: application/json' \
  -d '{
    "valor": 50.00
  }'
```

### 5. Verificar saldo

```bash
curl -X GET 'http://localhost:8000/api/v1/conta/saldo' \
  -H 'Authorization: Bearer eyJhbGciOiJIUzI1NiIs...'
```

### 6. Ver extrato

```bash
curl -X GET 'http://localhost:8000/api/v1/extrato' \
  -H 'Authorization: Bearer eyJhbGciOiJIUzI1NiIs...'
```

## Usuários de Teste

Use estas credenciais para testar a API:

| CPF | Senha |
|-----|-------|
| 12345678901 | senha123 |
| 98765432109 | maria456 |
| 11122233344 | pedro789 |
| 55544433322 | ana321 |
| 77788899900 | carlos654 |

## Endpoints Disponíveis

| Método | Rota | Descrição | Requer Token |
|--------|------|-----------|--------------|
| POST | `/api/v1/usuarios/registrar` | Registrar novo usuário | ✗ |
| POST | `/api/v1/auth/login` | Fazer login e obter JWT | ✗ |
| GET | `/api/v1/conta/saldo` | Consultar saldo | ✓ |
| POST | `/api/v1/transacoes/depositar` | Realizar depósito | ✓ |
| POST | `/api/v1/transacoes/sacar` | Realizar saque | ✓ |
| GET | `/api/v1/extrato` | Ver histórico de transações | ✓ |
| GET | `/api/v1/usuarios/perfil` | Ver dados do usuário | ✓ |
| GET | `/api/v1/health` | Verificar status da API | ✗ |

## Regras de Negócio

- **Saque máximo**: R$ 500.00 por transação
- **Limite diário**: Máximo 3 saques por dia
- **Saldo**: Saque não permitido sem saldo suficiente
- **CPF único**: Cada CPF pode registrar apenas uma conta
- **Senha**: Mínimo de 6 caracteres
- **Token**: Válido por 30 minutos

## Estrutura de Arquivos

```
├── api.py                    # Aplicação principal (FastAPI)
├── usuarios.json             # Base de dados de usuários
├── contas.json               # Base de dados de contas
├── requirements.txt          # Dependências Python
├── run_api.py               # Script para executar API
├── test_api.py              # Testes automatizados
└── README.md                # Documentação
```

## Tecnologias Utilizadas

- **FastAPI** 0.128.0 - Framework web REST
- **Uvicorn** 0.40.0 - Servidor ASGI
- **PyJWT** 2.8.1 - Autenticação JWT
- **Pydantic** 2.12.5 - Validação de dados
- **Python** 3.13.2 - Linguagem
- **JSON** - Persistência de dados

## Como Usar no Swagger UI

1. Acesse http://localhost:8000/docs
2. Clique em "POST /api/v1/auth/login"
3. Registre um usuário ou use as credenciais de teste
4. Copie o `access_token` retornado
5. Clique no botão **"Authorize"** (ícone de cadeado)
6. Cole o token e clique em "Login"
7. Agora você pode testar todos os endpoints protegidos

## Desafio DIO

Projeto desenvolvido por: Vitor Brandão Barbosa de Melo, como parte do Bootcamp Luizalabs - Back-end com Python (Desafio DIO) - Guilherme Carvalho
Creditos e codigo inicial de desenvolvimento: Guilherme Carvalho


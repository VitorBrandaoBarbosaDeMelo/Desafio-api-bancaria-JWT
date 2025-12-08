  Entrega do Projeto Bootcamp DIO: Luizalabs - Back-end com Python
  Desafio: Otimizando o Sistema Bancário simples com Funções Python
  
   
Este é um projeto simples de sistema bancário desenvolvido em Python, para concluir o desafio DIO: Luizalabs - Back-end com Python, focado em demonstrar o uso de funções, parâmetros especiais (positional-only e keyword-only), e persistência de dados (JSON). 
O sistema opera via interface de linha de comando (CLI).


  Funcionalidades Principais:
  
Cadastro de Clientes (Usuários): Permite cadastrar novos clientes (usuários) com nome, CPF, data de nascimento e endereço. 
O CPF deve ser armazenado somente com números e é garantida a unicidade.

Contas Correntes: Permite criar contas correntes vinculadas a usuário. 

As contas possuem agência e número sequencial.

Operações Bancárias:

Depósito: Implementado usando parâmetros positional-only (apenas por posição: saldo, valor, extrato, /).

Saque: Implementado usando parâmetros keyword-only (apenas por nome: *, saldo, valor, extrato, limite, ...).
Extrato: Exibe o histórico de movimentações e o saldo da conta.

Vinculação por Conta: Todas as operações são vinculadas a uma conta específica, garantindo que cada conta tenha seu próprio saldo, extrato e limite de saque isolados.


 Arquitetura e Persistência de Dados
O projeto utiliza o módulo json do Python para garantir que os dados de usuários e contas não sejam perdidos ao fechar o programa.

Persistência de Usuários: Os dados de clientes são salvos no arquivo usuarios.json.

Persistência de Contas: Os dados das contas (incluindo saldo e extrato) são salvos no arquivo contas.json.

Parâmetros Especiais: Funções utilizam marcadores especiais (/ e *) para restringir como os argumentos devem ser passados, promovendo clareza e segurança na interface da função.

RESUMO:
# Titulo: Sistema bancário que combina a estrutura de Programação Orientada a Objetos (POO) 
   # com a persistência de dados (JSON) para criar um sistema bancário modular.

###funcionalidades e estruturas do código ###
    # Funcionalidades:
    # - Criação e gerenciamento de clientes e contas bancárias.
    # - Realização de transações como depósitos e saques.
    # - Geração de extratos detalhados das contas.
    # - Persistência de dados usando arquivos JSON para armazenar informações de clientes e contas.
    
    # Estruturas do código:
    # - Classes para modelar clientes, contas, transações e histórico.
    # - Funções para carregar e salvar dados em arquivos JSON.
    # - Funções de serviço para interagir com o usuário e executar operações bancárias.
    # - Uma função principal que orquestra o fluxo do programa, apresentando um menu interativo ao usuário.

Os próximos passos seriam:

Criar uma interface grafica, importando algumas bibliotecas, provavelmente: import tkinter e import customtkinter.
Executar como .exe e atribuir um atalho para acesso rápido...

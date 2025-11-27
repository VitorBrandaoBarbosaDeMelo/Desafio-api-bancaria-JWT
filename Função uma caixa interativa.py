import tkinter as tk
from tkinter import messagebox

# Variáveis globais para armazenar os dados e controlar o estado
dados_usuario = {}
etapa_atual = 0

# Lista de perguntas a serem feitas
perguntas = [
    {"chave": "nome", "texto": "Digite seu nome:"},
    {"chave": "idade", "texto": "Digite sua idade:"}
]

# --- 1. Funções de Controle de Fluxo ---

def verificar_e_avancar():
    """Valida a entrada atual, registra os dados e avança para a próxima etapa."""
    global etapa_atual

    # Pega o valor da caixa de entrada
    entrada = entry_input.get()

    if not entrada:
        messagebox.showwarning("Aviso", "O campo não pode ser vazio.")
        return

    chave_atual = perguntas[etapa_atual]["chave"]

    # 1. Validação Específica para a Idade
    if chave_atual == "idade":
        try:
            dados_usuario[chave_atual] = int(entrada)
        except ValueError:
            messagebox.showerror("Erro", "A idade deve ser um número inteiro válido.")
            return
    else:
        # Armazena outros dados como string (ex: Nome)
        dados_usuario[chave_atual] = entrada

    # Limpa a caixa de entrada
    entry_input.delete(0, tk.END)

    # 2. Verifica se há mais perguntas
    if etapa_atual < len(perguntas) - 1:
        # Avança para a próxima pergunta
        etapa_atual += 1
        atualizar_interface()
    else:
        # Fim das perguntas: Mostra o resultado final
        mostrar_resultado_final()

def atualizar_interface():
    """Atualiza o Label com a próxima pergunta."""
    if etapa_atual < len(perguntas):
        nova_pergunta = perguntas[etapa_atual]["texto"]
        label_pergunta.config(text=nova_pergunta)
        
        # Foca automaticamente na caixa de entrada
        entry_input.focus_set()

def mostrar_resultado_final():
    """Esconde os campos de input e mostra o resultado da lógica."""
    
    # Esconde os widgets de input
    label_pergunta.pack_forget()
    entry_input.pack_forget()
    btn_proximo.pack_forget()

    # --- Lógica de Resultado ---
    nome = dados_usuario.get("nome", "Participante")
    idade = dados_usuario.get("idade", 0)

    if idade >= 18:
        resultado = "Maior de idade"
    else:
        resultado = "Menor de idade"
    # ---------------------------
    
    # Exibe o resultado na caixa de texto
    output_text.delete("1.0", tk.END)
    output_text.insert(tk.END, f"Resultado: {resultado}\n\n")
    output_text.insert(tk.END, f"Idade digitada: {idade}\n")
    output_text.insert(tk.END, f"Obrigado por participar, {nome}!")


# --- 2. Configuração da Janela Principal ---

janela = tk.Tk()
janela.title("Questionário Dinâmico")
janela.geometry("400x350")
janela.resizable(False, False) # Impede redimensionamento

# --- Elementos da Interface ---

# Label da Pergunta (Será atualizado)
label_pergunta = tk.Label(janela, text="", font=('Arial', 12))
label_pergunta.pack(pady=20)

# Caixa de Entrada Única
entry_input = tk.Entry(janela, width=40)
# Associa a tecla 'Enter' para chamar a função verificar_e_avancar
entry_input.bind("<Return>", lambda event: verificar_e_avancar()) 
entry_input.pack(pady=10)

# Botão de Ação
btn_proximo = tk.Button(janela, text="Próximo", command=verificar_e_avancar)
btn_proximo.pack(pady=10)

# Separador visual
tk.Label(janela, text="--- Resultado ---").pack(pady=10)

# Saída de Interação (Onde o resultado final será mostrado)
output_text = tk.Text(janela, height=7, width=40)
output_text.pack(pady=5)

# 3. Inicia o Questionário
atualizar_interface()

# 4. Loop Principal
janela.mainloop()
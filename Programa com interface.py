import tkinter as tk
from tkinter import messagebox

# 1. Função que executa a lógica do seu programa
def verificar_idade():
    try:
        # Pega os valores das caixas de entrada
        nome = entry_nome.get()
        idade_str = entry_idade.get()

        if not nome or not idade_str:
            messagebox.showwarning("Aviso", "Por favor, preencha todos os campos.")
            return

        # Converte a idade para inteiro (resolvendo o antigo TypeError)
        idade = int(idade_str)

        # Limpa o campo de saída anterior
        output_text.delete("1.0", tk.END)

        # Lógica de verificação
        if idade >= 18:
            resultado = "Maior de idade"
        else:
            resultado = "Menor de idade"

        # Exibe as saídas na caixa de texto
        output_text.insert(tk.END, f"Resultado: {resultado}\n")
        output_text.insert(tk.END, f"Idade digitada: {idade}\n")
        output_text.insert(tk.END, f"Obrigado por participar, {nome}")

    except ValueError:
        # Trata o caso em que o usuário digita texto na caixa de idade
        messagebox.showerror("Erro de Entrada", "A idade deve ser um número inteiro válido.")

# 2. Configuração da Janela Principal
janela = tk.Tk()
janela.title("Verificação de Idade e Nome")
janela.geometry("400x300") # Define o tamanho da janela

# --- Entrada de Nome ---
label_nome = tk.Label(janela, text="Digite seu nome:")
label_nome.pack(pady=5)
entry_nome = tk.Entry(janela, width=40)
entry_nome.pack(pady=2)

# --- Entrada de Idade ---
label_idade = tk.Label(janela, text="Digite sua idade:")
label_idade.pack(pady=5)
entry_idade = tk.Entry(janela, width=40)
entry_idade.pack(pady=2)

# --- Botão de Ação ---
btn_verificar = tk.Button(janela, text="Verificar", command=verificar_idade)
btn_verificar.pack(pady=10)

# --- Saída de Interação ---
label_output = tk.Label(janela, text="Saída:")
label_output.pack(pady=5)
output_text = tk.Text(janela, height=5, width=40)
output_text.pack(pady=5)

# 3. Inicia o Loop Principal da Interface
janela.mainloop()
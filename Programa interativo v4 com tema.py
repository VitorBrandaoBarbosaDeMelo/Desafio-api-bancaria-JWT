import tkinter as tk  # <-- CORREÇÃO: Importa o Tkinter com o alias 'tk'
import customtkinter as ctk
from tkinter import messagebox

# --- ESTILOS ---
COR_FUNDO_JANELA = "#1C2B36"
COR_TEXTO = "white"
COR_DESTAQUE = "#7BB840"

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("green")

FONTE_PERGUNTA = ('Arial', 16, 'bold')
FONTE_GERAL = ('Arial', 15)

# --- Variáveis de Controle ---
dados_usuario = {}
etapa_atual = 0
perguntas = [
    {"chave": "nome", "texto": "Qual é o seu nome completo?"},
    {"chave": "idade", "texto": "Qual a sua idade (em números)?"}
]

# --- Funções de Controle de Fluxo ---

def verificar_e_avancar():
    """Valida a entrada atual, registra os dados e avança para a próxima etapa."""
    global etapa_atual

    entrada = entry_input.get()

    if not entrada:
        messagebox.showwarning("Aviso", "O campo não pode ser vazio.")
        return

    chave_atual = perguntas[etapa_atual]["chave"]

    if chave_atual == "idade":
        try:
            dados_usuario[chave_atual] = int(entrada)
        except ValueError:
            messagebox.showerror("Erro", "A idade deve ser um número inteiro válido.")
            return
    else:
        dados_usuario[chave_atual] = entrada

    entry_input.delete(0, ctk.END)

    if etapa_atual < len(perguntas) - 1:
        etapa_atual += 1
        atualizar_interface()
    else:
        mostrar_resultado_final()

def atualizar_interface():
    """Atualiza o Label com a próxima pergunta."""
    if etapa_atual < len(perguntas):
        nova_pergunta = perguntas[etapa_atual]["texto"]
        label_pergunta.configure(text=nova_pergunta)
        entry_input.focus_set()

def mostrar_resultado_final():
    """Esconde os campos de input e mostra o resultado da lógica."""

    # Oculta os widgets
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

    # Exibe o resultado na caixa de texto (Usando ctk.END do CustomTkinter)
    output_text.delete("1.0", ctk.END)
    output_text.insert(ctk.END, f"Resultado: {resultado}\n\n")
    output_text.insert(ctk.END, f"Idade: {idade}\n")
    output_text.insert(ctk.END, f"Obrigado por participar, {nome}!")

# --- 4. Configuração da Janela Principal ---

janela = ctk.CTk()
janela.title("Questionário Estilizado - CTk")
janela.geometry("450x400")
janela.resizable(False, False)
janela.configure(bg=COR_FUNDO_JANELA)

# --- Elementos da Interface ---

# Label da Pergunta
label_pergunta = ctk.CTkLabel(janela, text="",
                              font=FONTE_PERGUNTA,
                              text_color=COR_TEXTO)
label_pergunta.pack(pady=20, padx=20)

# Caixa de Entrada Única
entry_input = ctk.CTkEntry(janela, width=250, height=35,
                           font=FONTE_GERAL,
                           placeholder_text="Digite aqui...",
                           fg_color="gray20",
                           text_color=COR_TEXTO,
                           border_color=COR_DESTAQUE,
                           corner_radius=10)
entry_input.bind("<Return>", lambda event: verificar_e_avancar())
entry_input.pack(pady=10)

# Botão de Ação
btn_proximo = ctk.CTkButton(janela, text="Próximo",
                            command=verificar_e_avancar,
                            font=FONTE_GERAL,
                            fg_color=COR_DESTAQUE,
                            hover_color="#5A942F",
                            corner_radius=10)
btn_proximo.pack(pady=15)

# Separador visual
ctk.CTkLabel(janela, text="--- RESULTADO ---",
             font=('Arial', 10, 'bold'),
             text_color=COR_TEXTO).pack(pady=10)

# Saída de Interação
output_text = ctk.CTkTextbox(janela, height=150, width=300,
                             bg_color=COR_FUNDO_JANELA,
                             fg_color="#2E4053",
                             text_color=COR_TEXTO,
                             font=FONTE_GERAL,
                             corner_radius=10)
output_text.pack(pady=5)

# 5. Inicia o Questionário
atualizar_interface()

# 6. Loop Principal
janela.mainloop()



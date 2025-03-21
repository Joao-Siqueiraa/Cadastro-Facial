import tkinter as tk
from tkinter import messagebox
from cadastro import cadastrar_usuario
from reconhecimento import reconhecer_usuario  # Se a função estiver realmente definida no cadastro.py
from database import obter_historico  # Corrigido para obter_historico


COR_FUNDO = "#121212"  # Preto carvão  
COR_COMPONENTE = "#1E1E1E"  # Cinza bem escuro  
COR_TEXTO = "#E0E0E0"  # Cinza quase branco  
COR_TEXTO_SECUNDARIO = "#B0B0B0"  # Cinza médio  
COR_DESTAQUE = "#007ACC"  # Azul vibrante  


def criar_interface():
    def cadastrar():
        nome = entry_nome.get()
        if nome:
            cadastrar_usuario(nome)
        else:
            messagebox.showwarning("Atenção", "Digite o nome para cadastrar!")

    def reconhecer():
        reconhecer_usuario()

    # Função para abrir o histórico
    def abrir_historico():
        historico = obter_historico()  # Corrigido para chamar a função obter_historico
        if not historico:
            messagebox.showinfo("Histórico", "Não há registros de login.")
            return
    
        historico_janela = tk.Toplevel()
        historico_janela.title("Histórico de Logins")
    
        historico_texto = tk.Text(historico_janela, wrap=tk.WORD, width=50, height=20)
        historico_texto.pack(padx=10, pady=10)
    
        for nome, data_hora in historico:
            historico_texto.insert(tk.END, f"{data_hora} - {nome}\n")
    
        historico_texto.config(state=tk.DISABLED)

    # Criar a janela principal
    root = tk.Tk()
    root.title("Cadastro Facial")
    root.geometry("400x300")
    root.configure(bg=COR_FUNDO)
    root.iconbitmap(default="icone/icone.ico")

    # Título
    titulo = tk.Label(root, text='Cadastro Facial', font=("arial", 14), bg=COR_FUNDO, fg=COR_TEXTO)
    titulo.pack(pady=10)

    # Labels e campos de entrada
    label_nome = tk.Label(root, text="Digite seu nome:", bg=COR_FUNDO, fg=COR_TEXTO)
    label_nome.pack(pady=10)

    entry_nome = tk.Entry(root)
    entry_nome.pack(pady=10)

    # Botões de cadastrar, reconhecer e ver histórico
    button_cadastrar = tk.Button(root, text="Cadastrar", bg=COR_DESTAQUE, fg="white", font=("Arial", 14), command=cadastrar)
    button_cadastrar.pack(pady=10)

    button_reconhecer = tk.Button(root, text="Reconhecer", bg=COR_COMPONENTE, fg=COR_TEXTO, font=("Arial", 14), command=reconhecer)
    button_reconhecer.pack(pady=10)

    button_historico = tk.Button(root, text="Ver Histórico", bg=COR_DESTAQUE, fg="white", font=("Arial", 14), command=abrir_historico)
    button_historico.pack(pady=10)

    # Iniciar a interface
    root.mainloop()

if __name__ == "__main__":
    criar_interface()

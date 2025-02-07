from database import criar_tabelas
from cadastro import cadastrar_usuario
from reconhecimento import reconhecer_usuario
from historico import exibir_historico

# Criar tabelas ao iniciar
criar_tabelas()

while True:
    print("\n1. Cadastrar Usuário")
    print("2. Reconhecer Usuário")
    print("3. Exibir Histórico de Logins")
    print("4. Sair")

    opcao = input("Escolha uma opção: ")

    if opcao == "1":
        nome = input("Digite seu nome: ")
        cadastrar_usuario(nome)
    elif opcao == "2":
        reconhecer_usuario()
    elif opcao == "3":
        exibir_historico()
    elif opcao == "4":
        print("Saindo...")
        break
    else:
        print("Opção inválida!")

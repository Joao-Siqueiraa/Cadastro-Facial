from database import criar_tabelas, obter_historico  # Corrigido para obter_historico
from cadastro import cadastrar_usuario
from reconhecimento import reconhecer_usuario
from historico import exibir_historico
from interface import criar_interface

# Criar tabelas ao iniciar
criar_tabelas()

# Chama a função que cria a interface
criar_interface()

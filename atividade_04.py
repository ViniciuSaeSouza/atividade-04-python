import oracledb
import os
from dotenv import load_dotenv


# VARIÁVEIS GLOBAIS
cliente = {}

# RECUPERANDO VARIÁVEIS DE AMBIENTE (USER, PASSWORD, DSN) DO ARQUIVO .ENV PARA MANTER MAIOR PRIVACIDADE DOS DADOS
load_dotenv()
user_env = os.getenv("user")
password_env = os.getenv("password")
dsn_env = os.getenv("dsn")
# -----------------------------------------------------------------------
conexao = False

try:
	conn = oracledb.connect(user=user_env, password=password_env, dsn=dsn_env)
	instr_create = conn.cursor()
	instr_read = conn.cursor()
	instr_update = conn.cursor()
	instr_delete = conn.cursor()
	conexao = True
except Exception as e:
	print(e)


# SUB-ALGORITMOS E FUNÇÕES

# Limpa o terminal de comando com 'cls' ou 'clear' dependendo dos Sistema Operacional
# 'cls' -> Windows ('nt')
# 'clear' -> Mac & Linux
def clear() -> None:
    return os.system('cls' if os.name == 'nt' else 'clear')

# Recupera conexão com o Banco de Dados Oracle utilizando as {variáveis de ambiente} 
# Varáveis:
# user_env / password_env / dsn_env

def verifica_registro(pk:str) -> bool:
    sql = f"SELECT * FROM assinantes WHERE cpf = {pk}"
    instr_read.execute(sql)
    result = instr_read.fetchall()        
    cliente['cpf'] = result[0][0]
    cliente['nome'] = result[0][1]
    cliente['plano'] = result[0][2]
    cliente['mensalidade'] = result[0][3]
    cliente['ativo'] = result[0][4]
    if result:
        return True
    else:
        return False


#
def assinar_plano():
    cpf = input("CPF (xxxxxxxxxxx): ")
    if verifica_registro(cpf):
        print("Já temos um usuário cadastrado com este cpf!")
        print(cliente)
        
# LAÇO PRINCIPAL
while conexao:
    # clear()
    print(" -- POTATO FLIX --")
    print("""\n0 - Sair
1 - Assinar plano
2 - Editar assinatura
3 - Listar assinantes
4 - Listar todos os clientes
5 - Excluir assinatura
""")
    escolha = input("Escolha: ")
    match escolha:
        case "0":
            print("Fechando sistema....")
            exit()
        case "1":
            print(assinar_plano())
        case "2":
            # editar_assinatura()
            ...
        case "3":
            # listar_assinantes()
            ...
        case "4":
            # listar_todos_cliente()
            ...
        case "5":
            # cancelar_assinatura()
            ...
        case "6":
            # reativar_assinatura()
            ...
        case   _:
            print("ERRO. Opção inválida!")
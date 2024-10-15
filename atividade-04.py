#RM: 555678 --- NOME: João Victor Michaeli --- 1TDSPK
#RM: 554456 --- NOME: Vinicius Saes de Souza --- 1TDSPK
#RM: 558062 --- NOME: Henrique Francisco Garcia --- 1TDSPK

import oracledb  # Importa a biblioteca para conectar ao banco de dados Oracle
import os  # Importa módulo para operações do sistema
from dotenv import load_dotenv  # Importa para carregar variáveis de ambiente

# VARIÁVEIS GLOBAIS
cliente = {}  # Dicionário para armazenar informações do cliente
colunas = [  # Lista de colunas que serão usadas no banco de dados
    'cpf',
    'nome',
    'plano',
    'mensalidade',
    'ativo',
]
planos = {  # Dicionário que contém os planos disponíveis e seus valores
    "base": 14.90,
    "plus": 24.90,
    "premium": 34.90
}

# RECUPERANDO VARIÁVEIS DE AMBIENTE (USER, PASSWORD, DSN) DO ARQUIVO .ENV
load_dotenv()  # Carrega as variáveis de ambiente do arquivo .env
user_env = os.getenv("user")  # Obtém o usuário
password_env = os.getenv("password")  # Obtém a senha
dsn_env = os.getenv("dsn")  # Obtém o DSN

conexao = False  # Inicializa a variável de controle de conexão como False

# Tenta conectar ao banco de dados Oracle
try:
    conn = oracledb.connect(user=user_env, password=password_env, dsn=dsn_env)  # Conecta ao banco
    instr_create = conn.cursor()  # Cria um cursor para executar comandos SQL
    instr_read = conn.cursor()  # Cria um cursor para leitura de dados
    instr_update = conn.cursor()  # Cria um cursor para atualização de dados
    instr_delete = conn.cursor()  # Cria um cursor para deletar dados
    conexao = True  # Define que a conexão foi estabelecida
except Exception as e:
    print(e)  # Imprime erro caso a conexão falhe

# FUNÇÕES

# Função para limpar o terminal, dependendo do sistema operacional
def clear() -> None:
    return os.system('cls' if os.name == 'nt' else 'clear')

# Função para verificar se um registro já existe no banco de dados
def verifica_registro(pk: str) -> bool:
    sql = f"SELECT * FROM assinantes WHERE cpf = {pk}"  # Consulta SQL para verificar CPF
    instr_read.execute(sql)  # Executa a consulta
    result = instr_read.fetchall()  # Obtém todos os resultados
    if result:  # Se resultados forem encontrados
        # Armazena as informações do cliente no dicionário
        cliente['cpf'] = result[0][0]
        cliente['nome'] = result[0][1]
        cliente['plano'] = result[0][2]
        cliente['mensalidade'] = result[0][3]
        cliente['ativo'] = result[0][4]
        return True  # Registro encontrado
    else:
        return False  # Registro não encontrado

# Função para verificar se a entrada do usuário não está vazia
def verifica_vazio(texto: str) -> str:
    while True:  # Loop até obter uma entrada válida
        temp = input(texto).lower()  # Solicita entrada e converte para minúsculas
        if not temp:  # Se a entrada estiver vazia
            print("Parece que não digitou nenhum valor!")  # Informa ao usuário
            continue  # Continua solicitando entrada
        return temp  # Retorna a entrada válida

# Função para assinar um plano
def assinar_plano() -> None:
    cpf = verifica_vazio("CPF (xxxxxxxxxxx): ")  # Solicita o CPF do usuário
    if verifica_registro(cpf):  # Verifica se o CPF já está cadastrado
        if cliente["ativo"] == 'TRUE':  # Se o cliente estiver ativo
            while True:  # Loop para opções do cliente
                clear()  # Limpa o terminal
                escolha = input(f""" -- Já temos um cadastro no CPF ({cpf}) --
1 - Editar assinatura
2 - Cancelar assinatura
3 - Menu
Escolha: """)
                match escolha:  # Verifica a escolha do usuário
                    case "1":
                        editar_assinatura()  # Chama função para editar assinatura
                    case "2":
                        cancelar_assinatura()  # Chama função para cancelar assinatura
                    case "3":
                        break  # Sai do loop
                    case _:
                        print("ERRO! Opção inválida.")  # Informa opção inválida

        elif cliente["ativo"] == "FALSE":  # Se o cliente estiver inativo
            while True:  # Loop para opções do cliente
                escolha = input(f""" -- Bem vindo(a) novamente {cliente["nome"]}! --
1 - Re-ativar assinatura
2 - Menu
Escolha: """)
                match escolha:  # Verifica a escolha do usuário
                    case "1":
                        reativar_assinatura()  # Chama função para reativar assinatura
                    case "2":
                        break  # Sai do loop
    else:  # Se o CPF não estiver cadastrado
        clear()  # Limpa o terminal
        flag = True  # Inicializa a flag
        while flag:  # Loop para cadastro do cliente
            print("Seja bem vindo(a)! Vamos nos cadastrar...")
            while flag:  # Loop para entrada do nome
                nome = verifica_vazio("Primeiro nome: ")  # Solicita o primeiro nome
                sobrenome = verifica_vazio("Sobrenome: ")  # Solicita o sobrenome
                print(f"\nPrazer {nome.capitalize()}! Agora vamos escolher o seu plano...\n")  # Mensagem de boas-vindas
                i = 0  # Inicializa contador
                for plano, valor in planos.items():  # Loop pelos planos disponíveis
                    print(f"{i + 1} - {plano} (R${valor})")  # Mostra plano e valor
                    i += 1  # Incrementa contador
                plano = verifica_vazio("Plano: ")  # Solicita o plano
                match plano:  # Verifica a escolha do plano
                    case "1":
                        plano = "base"  # Define plano como base
                    case "2":
                        plano = "plus"  # Define plano como plus
                    case "3":
                        plano = "premium"  # Define plano como premium
                # Monta lista com dados do cliente
                aux = [cpf, f"{nome.capitalize()} {sobrenome.capitalize()}", plano.capitalize(), planos[plano], "TRUE"]
                
                # Preenche o dicionário cliente com os dados
                for i, chave in enumerate(colunas):
                    cliente[chave] = aux[i]
                
                # Comando SQL para inserir o cliente no banco de dados
                sql = f"INSERT INTO assinantes (cpf, nome, plano, mensalidade, ativo) VALUES ('{cliente['cpf']}', '{cliente['nome']}', '{cliente['plano']}', '{cliente['mensalidade']}', '{cliente['ativo']}')"
                instr_create.execute(sql)  # Executa o comando SQL
                conn.commit()  # Confirma a transação
                print("Cliente cadastrado com sucesso!")  # Mensagem de sucesso
                input("Pressione qualquer tecla para voltar ao menu: ")  # Espera o usuário
                flag = False  # Sai do loop

# Função para editar assinatura
def editar_assinatura() -> None:
    planos = {"base": 14.90,
              "plus": 24.90,
              "premium": 34.90}  # Planos disponíveis
  
    cpf = verifica_vazio("CPF (xxxxxxxxxxx): ")  # Solicita CPF
    if verifica_registro(cpf):  # Verifica se o CPF está cadastrado
        if cliente["ativo"] == 'TRUE':  # Se o cliente estiver ativo
            print("----------------------------------------------------------------------------------------------------------------------------")
            print(f"""Olá {cliente['nome'].capitalize()}, está é a aba de edição da sua assinatura. O Seu plano atual é = {cliente['plano']}.""")  # Mensagem de boas-vindas
            while True:  # Loop para seleção do plano
                escolhe = input(f""" 
Digite de 1 a 3 para alterar seu plano:
1 - Base
2 - Plus
3 - Premium	
Escolha : """)
                print("----------------------------------------------------------------------------------------------------------------------------")
                match escolhe:  # Verifica a escolha do plano
                    case "1":
                        plano = "base"  # Define plano como base
                    case "2":
                        plano = "plus"  # Define plano como plus
                    case "3":
                        plano = "premium"  # Define plano como premium
                    case _:
                        print("ERRO! Opção inválida.")  # Informa opção inválida	
                        continue  # Continua no loop 
                
                # Comando SQL para atualizar a assinatura no banco de dados
                instr_update.execute(f"""UPDATE assinantes SET plano='{plano}', mensalidade={planos[plano]} WHERE cpf='{cliente['cpf']}'""")  # Executa a atualização
                conn.commit()  # Confirma a transação
                print("Assinatura editada com sucesso!")  # Mensagem de sucesso
                break  # Sai do loop
        else:  # Se o cliente não estiver ativo
            print(f"""Olá {cliente['nome'].capitalize()}, você não está ativo, reative sua assinatura para fazer alterações.""")  # Mensagem de erro
    else:  # Se o CPF não estiver cadastrado
        print("Este CPF não está cadastrado.")  # Informa que o CPF não foi encontrado

# Função para cancelar assinatura
def cancelar_assinatura() -> None:
    cpf = verifica_vazio("CPF (xxxxxxxxxxx): ")  # Solicita CPF
    if verifica_registro(cpf):  # Verifica se o CPF está cadastrado
        if cliente["ativo"] == 'TRUE':  # Se o cliente estiver ativo
            print(f"""Olá {cliente['nome'].capitalize()}, você deseja cancelar sua assinatura?""")  # Mensagem de confirmação
            escolha = verifica_vazio("Digite sim ou não: ").lower()  # Solicita confirmação
            match escolha:  # Verifica a escolha do usuário
                case "sim":  # Se o usuário quiser cancelar
                    # Comando SQL para cancelar a assinatura no banco de dados
                    instr_update.execute(f"""UPDATE assinantes SET ativo='FALSE' WHERE cpf='{cliente['cpf']}'""")  # Executa a atualização
                    conn.commit()  # Confirma a transação
                    print("Assinatura cancelada com sucesso!")  # Mensagem de sucesso
                case "não":  # Se o usuário não quiser cancelar
                    print("Operação cancelada.")  # Mensagem de cancelamento
                case _:
                    print("Opção inválida.")  # Informa que a opção foi inválida
        else:  # Se o cliente não estiver ativo
            print(f"""Olá {cliente['nome'].capitalize()}, você já não está ativo.""")  # Mensagem de erro
    else:  # Se o CPF não estiver cadastrado
        print("Este CPF não está cadastrado.")  # Informa que o CPF não foi encontrado

# Função para reativar assinatura
def reativar_assinatura() -> None:
    cpf = verifica_vazio("CPF (xxxxxxxxxxx): ")  # Solicita CPF
    if verifica_registro(cpf):  # Verifica se o CPF está cadastrado
        if cliente["ativo"] == 'FALSE':  # Se o cliente estiver inativo
            print(f"""Olá {cliente['nome'].capitalize()}, você deseja reativar sua assinatura?""")  # Mensagem de confirmação
            escolha = verifica_vazio("Digite sim ou não: ").lower()  # Solicita confirmação
            match escolha:  # Verifica a escolha do usuário
                case "sim":  # Se o usuário quiser reativar
                    # Comando SQL para reativar a assinatura no banco de dados
                    instr_update.execute(f"""UPDATE assinantes SET ativo='TRUE' WHERE cpf='{cliente['cpf']}'""")  # Executa a atualização
                    conn.commit()  # Confirma a transação
                    print("Assinatura reativada com sucesso!")  # Mensagem de sucesso
                case "não":  # Se o usuário não quiser reativar
                    print("Operação cancelada.")  # Mensagem de cancelamento
                case _:
                    print("Opção inválida.")  # Informa que a opção foi inválida
        else:  # Se o cliente estiver ativo
            print(f"""Olá {cliente['nome'].capitalize()}, você já está ativo.""")  # Mensagem de erro
    else:  # Se o CPF não estiver cadastrado
        print("Este CPF não está cadastrado.")  # Informa que o CPF não foi encontrado

# Função principal para execução do programa
def main() -> None:
    while True:  # Loop principal do programa
        clear()  # Limpa o terminal
        print("----------------------------------------------------------------------------------------------------------------------------")
        escolha = input("""
--- Bem-vindo ao sistema de gerenciamento de assinaturas ---
1 - Assinar plano
2 - Editar assinatura
3 - Cancelar assinatura
4 - Reativar assinatura
5 - Sair
Escolha: """)  # Menu de opções
        print("----------------------------------------------------------------------------------------------------------------------------")
        match escolha:  # Verifica a escolha do usuário
            case "1":
                assinar_plano()  # Chama função para assinar plano
            case "2":
                editar_assinatura()  # Chama função para editar assinatura
            case "3":
                cancelar_assinatura()  # Chama função para cancelar assinatura
            case "4":
                reativar_assinatura()  # Chama função para reativar assinatura
            case "5":
                print("Saindo do sistema...")  # Mensagem de saída
                break  # Sai do loop
            case _:
                print("ERRO! Opção inválida.")  # Informa opção inválida

# Chama a função principal para iniciar o programa
if __name__ == "__main__":
    main()  # Executa a função principal

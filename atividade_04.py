#RM: 555678 --- NOME: João Victor Michaeli --- 1TDSPK
#RM: 554456 --- NOME: Vinicius Saes de Souza --- 1TDSPK
#RM: 558062 --- NOME: Henrique Francisco Garcia --- 1TDSPK


import oracledb
import os
from dotenv import load_dotenv


# VARIÁVEIS GLOBAIS
cliente = {}
colunas = [
	'cpf',
	'nome',
	'plano',
	'mensalidade',
	'ativo',
]
planos = {
	"base" : 14.90,
	"plus" : 24.90,
	"premium" : 34.90
}

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
	if result:
		cliente['cpf'] = result[0][0]
		cliente['nome'] = result[0][1]
		cliente['plano'] = result[0][2]
		cliente['mensalidade'] = result[0][3]
		cliente['ativo'] = result[0][4]
		return True
	else:
		return False


def verifica_vazio(texto:str) -> str:
	while True:
		temp = input(texto).lower()
		if not temp:
			print("Parece que não digitou nenhum valor!")
			continue
		return temp


#Realiza o cadrastro do usuário
#
#
def assinar_plano() -> None:
    
	cpf = verifica_vazio("CPF (xxxxxxxxxxx): ")
	if verifica_registro(cpf):
		if cliente["ativo"] == 'TRUE':
			while True:
				clear()
				escolha = input(f""" -- Já temos um cadastro no CPF ({cpf}) --
1 - Editar assinatura
2 - Cancelar assinatura
3 - Menu
Escolha: """)
				match escolha:
					case "1":
						# editar_assinatura()
						...
					case "2":
						# cancelar_assinatura()
						...
					case "3":
						break
					case _:
						print("ERRO! Opção inválida.")

		elif cliente["ativo"] == "FALSE":
			while True:
				escolha = input(f""" -- Bem vindo(a) novamente {cliente["nome"]}! --
	1 - Re-ativar assinatura
	2 - Menu
	Escolha: """)
				match escolha:
					case "1":
						# reativar_assinatura()
						...
					case "2":
						break
	else:
		clear()
		flag = True
		while flag:
			print("Seja bem vindo(a)! Vamos nos cadastrar...")
			while flag:
				nome = verifica_vazio("Primeiro nome: ")
				sobrenome = verifica_vazio("Sobrenome: ")
				print(f"\nPrazer {nome.capitalize()}! Agora vamos escolher o seu plano...\n")
				i = 0
				for plano, valor in planos.items():
					print(f"{i+1} - {plano} (R${valor})")
					i += 1
				plano = verifica_vazio("Plano: ")
				match plano:
					case "1":
						plano = "base"
					case "2":
						plano = "plus"
					case "3":
						plano = "premium"
				aux = [cpf, f"{nome.capitalize()} {sobrenome.capitalize()}", plano.capitalize(), planos[plano], "TRUE"]
				
				for i, chave in enumerate(colunas):
					cliente[chave] = aux[i]
				
				sql = f"INSERT INTO assinantes (cpf, nome, plano, mensalidade, ativo) VALUES ('{cliente['cpf']}', '{cliente['nome']}', '{cliente['plano']}', '{cliente['mensalidade']}', '{cliente['ativo']}')"
				instr_create.execute(sql)
				conn.commit()
				print("Cliente cadastrado com sucesso!")
				input("Pressione qualquer telca para voltar ao menu: ")
				flag = False


def editar_assinatura() -> None:
	planos = {"base":14.90,
			"plus":24.90,
			"premium":34.90}
  
	cpf = verifica_vazio("CPF (xxxxxxxxxxx): ")
  
	if verifica_registro(cpf):
		if cliente["ativo"] == 'TRUE':
			print("----------------------------------------------------------------------------------------------------------------------------")
			print(f"""Olá {cliente['nome'].capitalize()}, está é a aba de edição da sua assinatura. O Seu plano atual é = {cliente['plano']}.""")
			while True:
				escolhe = input(f""" 
Digite de 1 a 3 para alterar seu plano:
1 - Base
2 - Plus
3 - Premium	
Escolha : """)
				print("----------------------------------------------------------------------------------------------------------------------------")
				match escolhe:
					case"1":
						plano = "base"
					case"2":
						plano = "plus"
					case"3":
						plano = "premium"
					case _:
						print("ERRO! Opção inválida.")	
						continue 
					
				sql = f"UPDATE assinantes SET plano = '{plano.capitalize()}' WHERE cpf = {cpf}"
				print (f'''Sua conta foi atualizada, agora seu plano é {plano.capitalize()}''')
				try:
					instr_update.execute(sql)
					conn.commit()
					return True
				except Exception as e:
					print(e)
					return False
		else:
			print("CPF inativo, não consta no sistema!!")

def listar_assinantes() -> None:
	while True:
		sql = f"SELECT * FROM assinantes WHERE ativo = 'TRUE'"
		try:
			instr_read.execute(sql)
			result = instr_read.fetchall()
		except Exception as e:
			print(e)
		print("--------------------------------------------------------------------")
		print("Esta é a lista de todos os registros em nosso sistema")
		print("CPF -------------- NOME ----------- CONTA ----- VALOR ------- ATIVO")
		for row in result:
			cpf, nome, conta, valor, ativo = row
			print(f"{cpf:<17} {nome:<17} {conta:<12} {valor:<12} {ativo}")
		print("--------------------------------------------------------------------")
		break

def listar_todos_cliente() -> None:
	while True:
		sql = f"SELECT * FROM assinantes"
		try:
			instr_read.execute(sql)
			result = instr_read.fetchall()
		except Exception as e:
			print(e)
		print("--------------------------------------------------------------------")
		print("Esta é a lista de todos os registros em nosso sistema")
		print("CPF -------------- NOME ----------- CONTA ----- VALOR ------- ATIVO")
		for row in result:
			cpf, nome, conta, valor, ativo = row
			print(f"{cpf:<17} {nome:<17} {conta:<12} {valor:<12} {ativo}")
		print("--------------------------------------------------------------------")
		break





def cancelar_assinatura() -> None:
	clear()
	print(" -- CANCELAMENTO DE ASSINATURA -- ")
	if not cliente.items():
		cpf = verifica_vazio("CPF (xxxxxxxxxxx): ")
		if verifica_registro(cpf):
			if cliente['ativo'] == "TRUE":
				confirmar_cancelamento(cpf)
			else:
				print("\nSua assinatura já está cancelada!")
				input("\nPressione qualquer tecla para voltar ao menu: ")
	else:
		if cliente['ativo'] == "TRUE":
			confirmar_cancelamento(cliente['cpf'])
		else:
			print("Sua assinatura já está cancelada!")
			input("Pressione qualquer tecla para voltar ao menu: ")
  
def confirmar_cancelamento(cpf:str) -> None:
	clear()
	print(" -- CANCELAMENTO DE ASSINATURA -- ")
	while True:
		print(f"""
Nome: {cliente['nome']}
Plano: {cliente['plano']}
Mensalidade: {planos[cliente['plano'].lower()]:.2f}
-----
Confirmar cancelamento:
1 - Sim
2 - Não
""")
		escolha = input("Escolha: ")
		match escolha:
			case "1":
				sql = f"UPDATE assinantes SET ativo = 'FALSE' WHERE cpf = {cpf}"
				try:
					instr_delete.execute(sql)
					conn.commit()
					print("Assinatura cancelada com sucesso!")
					input("Pressione qualquer tecla para voltar ao menu: ")
				except Exception as e:
					print(e)
			case "2":
				print("Assinatura não foi cancelada!")
				input("Pressione qualquer tecla para voltar ao menu: ")
				break
			case _:
				clear()
				print("Opção inválida!")


  
def confirmar_cancelamento(cpf:str) -> None:
	clear()
	print(" -- CANCELAMENTO DE ASSINATURA -- ")
	while True:
		print(f"""
Nome: {cliente['nome']}
Plano: {cliente['plano']}
Mensalidade: {planos[cliente['plano'].lower()]:.2f}
-----
Confirmar cancelamento:
1 - Sim
2 - Não
""")
		escolha = input("Escolha: ")
		match escolha:
			case "1":
				sql = f"UPDATE assinantes SET ativo = 'FALSE' WHERE cpf = {cpf}"
				try:
					instr_delete.execute(sql)
					conn.commit()
					print("Assinatura cancelada com sucesso!")
					input("Pressione qualquer tecla para voltar ao menu: ")
				except Exception as e:
					print(e)
			case "2":
				print("Assinatura não foi cancelada!")
				input("Pressione qualquer tecla para voltar ao menu: ")
				break
			case _:
				clear()
				print("Opção inválida!")
     				
def reativar_assinatura() -> None:
	clear()
	print(" -- RE-ATIVAÇÃO DE ASSINATURA -- ")
	if not cliente.items():
		cpf = verifica_vazio("CPF (xxxxxxxxxxx): ")
		if verifica_registro(cpf):
			
			if cliente['ativo'] == "FALSE":
				confirmar_ativacao(cpf)
			else:
				print("\nSua assinatura já está cancelada!")
				input("\nPressione qualquer tecla para voltar ao menu: ")
	else:
		if cliente['ativo'] == "FALSE":
			confirmar_ativacao(cliente['cpf'])
		else:
			print("Sua assinatura já está cancelada!")
			input("Pressione qualquer tecla para voltar ao menu: ")
   
   
def confirmar_ativacao(cpf:str) -> None:
	clear()
	print(" -- RE-ATIVAÇÃO DE ASSINATURA -- ")
	print("\nConta encontrada!")
	while True:
		plano = verifica_vazio(f"""
Confirmar novo plano:
1 - Base
2 - Plus
3 - Premium
Plano: """)
		break

	while True:
		print(f"""
Nome: {cliente['nome']}
Plano: {cliente['plano']}
Mensalidade: {planos[cliente['plano'].lower()]:.2f}
-----
Confirmar re-ativação:
1 - Sim
2 - Não
""")
		escolha = verifica_vazio("Escolha: ")
		match escolha:
			case "1":
				sql = f"UPDATE assinantes SET ativo = 'TRUE' WHERE cpf = {cpf}"
				try:
					instr_delete.execute(sql)
					conn.commit()
					print("Assinatura ativada com sucesso!")
					input("Pressione qualquer tecla para voltar ao menu: ")
					break
				except Exception as e:
					print(e)
			case "2":
				print("Assinatura não foi ativada!")
				input("Pressione qualquer tecla para voltar ao menu: ")
				break
			case _:
				clear()
				print("Opção inválida!")
    

# LAÇO PRINCIPAL
while conexao:
    clear()
    print(" -- POTATO FLIX --")
    print("""\n0 - Sair
1 - Assinar plano
2 - Editar assinatura
3 - Listar assinantes
4 - Listar todos os clientes
5 - Cancelar assinatura
6 - Re-ativar assinatura
""")
	
    escolha = input("Escolha: ")
    match escolha:
        case "0":
            print("Fechando sistema....")
            exit()
        case "1":
            assinar_plano()
        case "2":
            editar_assinatura()
        case "3":
            listar_assinantes()
        case "4":
            listar_todos_cliente()
        case "5":
            cancelar_assinatura()
        case "6":
            reativar_assinatura() 
        case   _:
            print("ERRO. Opção inválida!")
from atividade_04 import *




def assinar_plano():
    
	cpf = input("CPF (xxxxxxxxxxx): ")
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
		
		while True:
			print("Seja bem vindo(a)! Vamos nos cadastrar...")
			nome = input("Nome: ")
			sobrenome = input("Sobrenome: ")
			for i, plano, valor in enumerate(planos.items()):
				print(f"{i+1} - {plano} (R${valor})")
			
			plano = input("Escolha: ")
   
   
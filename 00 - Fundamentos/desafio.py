#-----------------------------------------------variaveis globais-----------------------------------------------#

saldo = 0
limite = 500
extrato = ''
numero_saques = 0
LIMITE_SAQUES = 3
idade_emprestimo = 18
SERASA = False
cadastrar_usuario = []
contas = []




#------------------------------------------------------home------------------------------------------------------#
#inicio

def home1(txt):
    print('-' * 50)
    print(txt)
    print('-' * 50)

home1('Seja bem vindo, digite o seu cpf para continuar')





#------------------------------------------------------login------------------------------------------------------#
#Cpf

def digite_cpf():
    while True:

        cpf = input('Digite o seu cpf: ')

        if cpf == '123':
            print('\n', 'Cpf ok\n')
            break

        else:
            print('\n', 'cpf invalido')

digite_cpf()




#-------------------------------------------------------login-------------------------------------------------------#
#Senha

def senha_digitada():

    tentativa = 0
    while True:

        senha = input('Digite a sua senha')

        if senha == '123':
            print('\n', '========= Login efetuado com sucesso =========')
            print('\n')
            break


        else:
            print('\n', '=== senha inválida ===')
            tentativa += 1


        if tentativa == 1:
            print('Restam 2 tentativas')

        elif tentativa == 2:
            print('Resta 1 tentativa')

        elif tentativa == 3:
            print('Acesso bloqueado')
            break

senha_digitada()





#-------------------------------------------------------opcao-------------------------------------------------------#
#Menu de opções

def opt():
    while True:

        print('__________'.center(70))
        print('\n', '[1] Depositar'.center(48))
        print('[2] Sacar'.center(45))
        print('[3] Extrato'.center(47))
        print('[4] Usuarios ativos'.center(55))
        print('[5] Novo usuario'.center(52))
        print('[6] Nova conta'.center(49))
        print('[7] Emprestimo'.center(50))
        print('[8] Sair'.center(43))
        print('__________'.center(20))
        print('\n')
        opcao = input('\nSelecione uma das opções: ')

        if opcao == '1':
            depositar()

        elif opcao == '2':
            sacar()

        elif opcao == '3':
            ver_extrato()
        
        elif opcao == '4':
            usuario_ativos()
        
        elif opcao == '5':
            novo_usuario()

        elif opcao == '6':
            conta_nova()
        
        elif opcao == '7':
            emprestimo()

        elif opcao == '8':
            print('==='.center(10))
            print('------ Até logo ------'.center(45))
            print('==='.center(90))
            quit()
            break
        else:
            print('Opção inválida')





#---------------------------------------------------funçõesdeopcao---------------------------------------------------#
#Depositar

def depositar():
    global saldo, extrato

    valor = float(input('Informe o valor que você deseja depositar: '))

    if valor > 0:
        saldo += valor
        extrato += f'Depósito: R$ {valor:.2f}\n'
        print('=====================================')
        print('Depósito realizado com sucesso')
        ver_extrato()

    else:
        print('Valor para deposito invalido')





#---------------------------------------------------funçõesdeopcao---------------------------------------------------#
#Sacar

def sacar():
    global saldo, limite, numero_saques, extrato

    print('=============================================')
    valor = float(input('Informe um valor para saque: '))
    print('=============================================')

    if numero_saques >= LIMITE_SAQUES:
        print('=============================================')
        print('Você atingiu o número de saques'.center(20))
        print('=============================================')
    
    elif valor > saldo:
        print('\n')
        print('Saldo insuficiente')
        print('\n')

    elif valor > limite:
        print('\n')
        print('Limite insuficiente')
        print('\n')

    else:
        saldo -= valor
        numero_saques += 1
        extrato += f'Saque: R$ {valor:.2f}\n'
        print('\n''-------------------------------------------')
        print(f'\nSaque realizado com sucesso. R${valor:.2f}')
        print(f'\nSaldo atual. R${saldo:.2f}')
        print('\n''-------------------------------------------')





#---------------------------------------------------funçõesdeopcao---------------------------------------------------#
#Extrato

def ver_extrato():
    global saldo, extrato, numero_saques

    if not extrato:
        print('\n=============================Extrato=============================')
        print('\nNão há movimentação')
        print('=============================')
        opcao2()

    else:
        print('=======================================')
        print('\n')
        print(f'Saldo: R$ {saldo:.2f}'.center(35))
        print('\n')
        print('=======================================')
        opcao2()





#--------------------------------------------------funçõesdeopcao2--------------------------------------------------#
#Extrato "sair" retornar ao menu e sair

def opcao2():
    while True:

        print('\n')
        print('__________'.center(80))
        print('[1] Retornar ao menu'.center(54))
        print('[2] Sair'.center(41))
        print('__________'.center(20))
        print('\n')
        opcao2 = input('Digite uma das opções: ')

        if opcao2 == '1':
            opt()
    
        elif opcao2 == '2':
            print('\n================================================\n')
            print('Até logo 🔚'.center(45))
            print('\n================================================')
            quit()

        else:
            print('\nOpção invalida')





#--------------------------------------------------funçõesdeopcao--------------------------------------------------#
#Usuarios ativos
#def usuario_ativos

def usuario_ativos():
    global cadastrar_usuario, contas
    while True:
        print('=============================================')
        print('\n[1] Consultar todos os usuários ativos')
        print('[2] Consultar um cpf')
        print('[3] Sair')
        print('\n_____________________________________________')
        opt = input('\nSelecione uma das opções ')

        if opt == '1':
            ativos_all()
        
        elif opt == '2':
            ativos()
        
        elif opt == '3':
            return


#================================================================================================================


#Todos usuários

def ativos_all():
    if not cadastrar_usuario:
        print('----------------------------')
        print('Não existe usuários ativos')
        print('-----------------------------')
        return

    for usuario in cadastrar_usuario:
        print(usuario)

        encontrou_conta = False
        for conta in contas:
            if conta['cpf_titular'] == usuario['cpf']:
                print(conta)
                encontrou_conta = True
        
        if not encontrou_conta:
            print('\n-------------------------------------')
            print('Este usuário ainda não possui conta')
            print('\n--------------------------------------')
        print('---')


#===================================================================================================================


#usuario especifico

def ativos():
    global cadastrar_usuario, contas

    print('\n=========================================================')
    consultar_usuario = int(input('Digite o cpf do usuário que deseja consultar: '))
    print('\n__________________________________________________________')

    for usuario in cadastrar_usuario:
        if usuario['cpf'] == consultar_usuario:
            print(usuario)
    
            for conta in contas:
                if conta['cpf_titular'] == consultar_usuario:
                     print(conta)
            break

    else:
        print('\nCadastro não encontrado')





#--------------------------------------------------funçõesdeopcao--------------------------------------------------#
#Novo usuario

def novo_usuario():
    global cadastrar_usuario
    
    cpf = int(input('Digite somente o número do seu cpf: '))
    nome = input('Qual é o seu nome completo: ')
    data_nc = input('Qual a sua data de nascimento dia/mês/ano - xx/xx/xxxx: ')
    rua_av = input('Qual o nome da rua ou av que você mora: ')
    numero = int(input('Número: '))
    bairro = input('Bairro: ')
    cidade = input('Cidade: ')
    estado = input('Digite a sigla do estado: ')

    endereço = f'{rua_av}, {numero}, {bairro}, {cidade}, {estado}' 

    usuario = {
        'nome': nome,
        'cpf': cpf,
        'endereço': endereço
    }

    #a função append é para salva o dado que será guardado na variável dicionário
    cadastrar_usuario.append(usuario)

    print('------------------------------------------')
    print(f'\nUsuário {nome} cadastrado com sucesso!')
    print('------------------------------------------')

    #O endereço é uma string com o formato: logradouro, nro - bairro - cidade/sigla estado. 





#-------------------------------------------------------opcao-------------------------------------------------------#
#criar nova conta

def conta_nova():
    global contas, cadastrar_usuario
    usuario_encontrado = False

    print('\n=========================================================')
    dig_cpf = int(input('Qual cpf será cadastrado na nova conta: '))
    print('\n__________________________________________________________')

    for usuario in cadastrar_usuario:
        if usuario['cpf'] == dig_cpf:
            usuario_encontrado = True            

            nova_conta = {
                    'agência': '0001',
                    'numero_conta': len (contas) +1 ,
                    'cpf_titular': dig_cpf
             }

    #fixar mentalmente que toda função que grava um dicionário é .append
        contas.append(nova_conta)

        print('Conta criada com sucesso, acesse todos os dados no menu usuario ativos')
        break
    
    if not usuario_encontrado:
        print('Usuario não encontrado, crie um usuário e volte para criar a conta')





#--------------------------------------------------funçõesdeopcao--------------------------------------------------#
#Empréstimo

def emprestimo():
    global idade_emprestimo, SERASA

    idade = int(input('\nQual a sua idade? '))
    resposta = input('\nVoce tem alguma restrição no SERASA s/n? ')

    SERASA = True if resposta.lower() == 's' else False

    if idade >= idade_emprestimo and SERASA == False:
        print(f'Você tem um limite pré aprovado de R$ 1000 reais')
        print('== PARA SEGUIR COM A ANÁLISE DE CREDÍTO VÁ ATÉ A AGÊNCIA MAIS PRÓXIMA ==')
        opcao2()
    
    elif idade >= idade_emprestimo and SERASA == True:
        print('\n========================================================')
        print('Nesse momento não temos condições disponíveis para você')
        print('\n=========================================================')
        opcao2()

    elif idade < idade_emprestimo:
        print('\n===========================================================')
        print('\nNesse momento não temos condições disponíveis para você')
        print('\n===========================================================')
        opcao2()




#-------------------------------------------------------opcao-------------------------------------------------------#
#Menu de opções
#Fechamento do menu de opções
opt()

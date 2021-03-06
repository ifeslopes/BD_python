import pymysql.cursors
import os
import matplotlib.pyplot as plt
conexao = pymysql.connect(
    host='localhost',
    user = 'root',
    password = input('Entre com senho do BD: '),
    db = 'erp',
    charset ='utf8mb4',
    cursorclass = pymysql.cursors.DictCursor
)
os.system('clear') or None

autentico = False

def logarCadastrar():
    usuarioExistente = 0 
    autenticado = False
    ussuarioMaster = False

    if decisao == 1:
        nome = input('Digite seu nome: ')
        senha = input('Digite sua senha: ')

        for  linha in resultado:
            if nome == linha['nome'] and senha == linha['senha']:
                if linha['nivel'] == 1:
                    ussuarioMaster = False
                if linha['nivel'] == 2:
                    ussuarioMaster = True
                autenticado = True
                print(f"Bem vindo {linha['nome']} seu nivel é {linha['nivel']}")
                break
            else:
                autenticado = False
        if  not autenticado:
            print('Nome ou senha invalido!')

    elif decisao == 2:
        print('Faça seu  cadastro')
        nome = input('Digite seu nome: ')
        senha = input('Digite sua senha: ')

        for linha in resultado:
            if nome == linha['nome'] and senha == linha['senha']:
                usuarioExistente = 1
        
        if usuarioExistente == 1:
            print('Usuári já cadastrado tente nome ou senha diferente')
        
        elif usuarioExistente == 0:
            try:
                with conexao.cursor() as cursor:
                    cursor.execute('insert into cadastros(nome, senha, nivel ) values(%s, %s, %s )',(nome, senha, 1))
                    conexao.commit()
                print('Usuário cadastrado com  sucesso')
            except:
                print('Erro ao inserrir os dados no banco')
    return autenticado, ussuarioMaster
                

def cadastrarProduto():
    nome = input('Digite nome do produto: ')
    ingredientes = input('Digite os igredientes do produto: ')
    grupo = input('Digite o grupo pertencente a esse produto: ')
    preco = float (input('Digite o preço do produto: '))

    try:
        with conexao.cursor() as cursor:
            cursor.execute('insert into produtos(nome, ingredientes, grupo, preco ) values(%s, %s, %s, %s)',(nome, ingredientes,grupo,preco ))
            conexao.commit()
            print('Produto cadastrado com sucesso!!')

    except:
        print('Erro ao cadastra o produto no banco de dados')

def listarProdotos():
    produtos =[]
    try:
        with conexao.cursor() as cursor:
            cursor.execute('select * from produtos')
            produtosCadastrados = cursor.fetchall()
            
    except:
        print('Erro ao Lista os produtos do banco')
    for i in produtosCadastrados:
        produtos.append(i)
    if len(produtos) != 0:
        for  i in range(0, len(produtos)):
            print(produtos[i])
    else:
        print('Nem um produto cadastrado')

def execluirProdutos():
    iddeletar = int(input('digite ID referente ao produto que deseja apagar: '))
    try:
        with conexao.cursor() as cursor:
            cursor.execute(f'delete from produtos where id ={iddeletar} ')
            print('Protudo excluido com sucesso!!')
    except:
        print('Erro ao execluir o prduto')

def listarPedidos():
    pedidos = []
    decission = 0

    while decission != 2:
        pedidos.clear()

        try:
            with conexao.cursor() as cursor:
                cursor.execute('select * from pedidos')
                listaPedidos =cursor.fetchall()
        except:
            print('Erro nos pedido no banco de dados')
        for i in listaPedidos:
            pedidos.append(i)
        if len(pedidos) != 0:
            for i in range(0, len(pedidos)):
                print(pedidos[i])
        else:
            print('Nem um pedido foi feito')

        decission = int(input('digite 1 para dar un produto como entregue e 2 para voltar'))
        if decission == 1:
            idDeletar = int(input('Digite o id  do pedido entregue'))
            try:
                with conexao.cursor() as cursor:
                    cursor.execute(f'delete from pedidos where id ={idDeletar}')
                    print('Produdo dado como entregue!')
            except:
                print('Erro ao dar produto como entregue')

def gerarEstatistica():
    nomeProdutos = []
    nomeProdutos.clear

    try:
        with conexao.cursor() as cursor:
            cursor.execute('select * from produtos')
            produtos = cursor.fetchall()
    except:
        print('Erro ao consultar ao banco de dados!')
    
    try:
        with conexao.cursor() as cursor:
            cursor.execute('select * from estatisticaVendido')
            vendido = cursor.fetchall()
    except:
        print('Erro ao consultar Estatistica')
    
    estado = int (input('Digite 0 para sair  1 para pesquisar por nome ou 2 para pesquisar por grupo: '))

    if estado == 1:
        decisao3 = int (input('Digite 1 para pesquisar por dinheiro e 2 por quantidade unitaria: '))
        if decisao3 == 1:
            for i in produtos:
                nomeProdutos.append(i['nome'])

            valores = []
            valores.clear()
            for h in range(0, len(nomeProdutos)):
                somaValor  = -1
                for  i in vendido:
                    if i['nome'] == nomeProdutos[h]:
                        somaValor += i['preco']
                if somaValor == -1:
                    valores.append(0)
                elif somaValor > 0:
                    valores.append(somaValor + 1)
            plt.plot(nomeProdutos, valores)
            plt.ylabel('Quantidade  vendida  em  reais')
            plt.xlabel('Produtos')
            plt.show()
        if decisao3 == 2:
            grupoUnico=[]
            grupoUnico.clear()
            try:
                with conexao.cursor() as cursor:
                    cursor.execute('select * from produtos')
                    grupo = cursor.fetchall()
            except:
                print('Erro na consulta!!')
            try: 
                with conexao.cursor() as cursor:
                    cursor.execute('select * from estatisticaVendido')
                    vendidoGrupo = cursor.fetchall()
            except:
                print('Erro na consulta de Grupos')
            
            for i in grupo:
                grupoUnico.append(i['nome'])
            grupoUnico = sorted(set(grupoUnico))
            qtfFinal = []
            qtfFinal.clear()

            for h in range(0, len(grupoUnico)):
                qtfUnitaria = 0
                for i in vendidoGrupo:
                    if grupoUnico[h] == i['nome']:
                        qtfUnitaria += 1 
                qtfFinal.append(qtfUnitaria)
            plt.plot(grupoUnico, qtfFinal)
            plt.ylabel('Qunatidade unitaria vendida')
            plt.xlabel('Produto')
            plt.show()

    elif estado == 2:
        decisao3 = int (input('Digite 1 para pesquisar por dinheiro e 2 por quantidade unitaria: '))
        if decisao3 == 1:
            for i in produtos:
                nomeProdutos.append(i['grupo'])

            valores = []
            valores.clear()
            for h in range(0, len(nomeProdutos)):
                somaValor  = -1
                for  i in vendido:
                    if i['grupo'] == nomeProdutos[h]:
                        somaValor += i['preco']
                if somaValor == -1:
                    valores.append(0)
                elif somaValor > 0:
                    valores.append(somaValor + 1)
            plt.plot(nomeProdutos, valores)
            plt.ylabel('Quantidade  vendida  em  reais')
            plt.xlabel('Produtos')
            plt.show()
        if decisao3 == 2:
            grupoUnico=[]
            grupoUnico.clear()
            try:
                with conexao.cursor() as cursor:
                    cursor.execute('select * from produtos')
                    grupo = cursor.fetchall()
            except:
                print('Erro na consulta!!')
            try: 
                with conexao.cursor() as cursor:
                    cursor.execute('select * from estatisticaVendido')
                    vendidoGrupo = cursor.fetchall()
            except:
                print('Erro na consulta de Grupos')
            
            for i in grupo:
                grupoUnico.append(i['grupo'])
            grupoUnico = sorted(set(grupoUnico))
            qtfFinal = []
            qtfFinal.clear()

            for h in range(0, len(grupoUnico)):
                qtfUnitaria = 0
                for i in vendidoGrupo:
                    if grupoUnico[h] == i['grupo']:
                        qtfUnitaria += 1 
                qtfFinal.append(qtfUnitaria)
            plt.plot(grupoUnico, qtfFinal)
            plt.ylabel('Qunatidade unitaria vendida')
            plt.xlabel('Produto')
            plt.show()



        
while not autentico:
    decisao = int(input('Digite 1 para logar  ou 2 para cadastrar:'))

    try:
        with conexao.cursor() as cursor:
            cursor.execute('select * from cadastros')
            resultado = cursor.fetchall()
            
    except:
        print('Erro ao conectar ao banco de dados')
    
    autentico, usuarioSupremo = logarCadastrar()

if autentico:
    if usuarioSupremo == True:

        decisaoUsuario = 1

        while decisaoUsuario != 0:
            decisaoUsuario = int(input('Digete 0 pra sair  e 1 para cadastra o produtos 2 para lista produtos 3 para lista produtos 4 para gerar graficos: '))
            if decisaoUsuario == 1:
                cadastrarProduto()
            elif decisaoUsuario == 2:
                listarProdotos()

                deleta = int(input('digite 1 para execluir  ou 2 para sair'))
                if  deleta ==1:
                    execluirProdutos()

            elif decisaoUsuario == 3:
                listarPedidos()
            
            elif decisaoUsuario == 4:
                gerarEstatistica()
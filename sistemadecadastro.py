from sqlite3.dbapi2 import Cursor, PrepareProtocol, connect
from typing import Text
from PyQt5 import  uic,QtWidgets
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout
from PyQt5.QtCore import Qt
import sqlite3
import io


cpf_id= 0
def tela_principal():
    login1.infor.setText("")
    nome_usuario = login1.uselog.text()
    senha = login1.senhalog.text()
    banco = sqlite3.connect('banco_cadastro_usuario.db')
    Cursor = banco.cursor()
    try:
        Cursor.execute("SELECT senha FROM cadastro WHERE login ='{}'".format(nome_usuario))
        senha_bd = Cursor.fetchall()
        print(senha_bd[0][0])
        banco.close()    
    except:
        print("Erro ao validar o login")
   
    if senha == senha_bd[0][0]: 
        login1.close()
        telaprincipal.move(380, 50)
        telaprincipal.show()



def fechar_backup():
    abrir_backup.close()
    telaprincipal.move(380, 50)
    telaprincipal.show()


def fechar_telapricipal():
    telaprincipal.close()
    login1.move(380, 50)
    login1.show()


def fechar_cadastro():
    cadastro.close()
    telaprincipal.move(380, 50)
    telaprincipal.show()

def tela_backup():
    telaprincipal.close()
    abrir_backup.move(380, 50)
    abrir_backup.show()


def busca():
    buscar_pedido.close()
    telaprincipal.move(380, 50)
    telaprincipal.show()
    

#salva os dados num arquivo externo através do método write, e o método iterdump(), biblioteca io
""" def backup():
    conn = sqlite3.connect('cadastro_pedidos.db')
    with io.open('Backup_cadastro_pedidos.sql', 'w') as f:
        for linha in conn.iterdump():
            f.write('%s\n' % linha)

    print('Backup realizado com sucesso.')
    print('Salvo como clientes_dump.sql')
    conn.close() 
 """
# Recuper dados do banco que foi feito o backup
""" def recuperar_backup():
    conn = sqlite3.connect('banco_cadastro_usuario.db')
    cursor = conn.cursor()
    f = io.open('banco_cadastro_usuario_dump.sql', 'r')
    sql = f.read()
    cursor.executescript(sql)
    print('Banco de dados recuperado com sucesso.')
    print('Salvo como clientes_recuperado.db')
    conn.close()  """
    
    

def Abrir_cadastro_usuario():
    login1.close()
    tela_cadastro.move(380, 50)
    tela_cadastro.show() 


def cadastrar_usuario():
   
    nome = tela_cadastro.lineEdit.text()
    login = tela_cadastro.lineEdit_2.text()
    senha = tela_cadastro.lineEdit_3.text()
    c_senha = tela_cadastro.lineEdit_4.text()

    if (senha == c_senha):
        try:
            banco = sqlite3.connect('banco_cadastro_usuario.db')
            Cursor = banco.cursor()
            Cursor.execute("CREATE TABLE IF NOT EXISTS cadastro (none text, login text, senha text)")
            Cursor.execute("INSERT INTO cadastro VALUES('"+nome+"','"+login+"','"+senha+"')")

            banco.commit()
            banco.close()
            tela_cadastro.errosenha.setText("Usuario Cadastrado com Sucesso")
            tela_cadastro.close()
            login1.move(400, 50)
            login1.show()

        except sqlite3.Error as erro:
            print("Erro ao inserir os dados:", erro)
    else:
        tela_cadastro.errosenha.setText("As senhas digitadas estão diferentes")

def cadastro_pedidos():
    telaprincipal.close()
    cadastro.move(380, 50)
    cadastro.show()





def adicionar_pedidos():
    funcionario = cadastro.imputnomefunc.text()
    cliente =cadastro.imputnomecliente.text()
    Cpf =cadastro.cpf.text()
    endereco = cadastro.imputend.text()
    telefone = cadastro.imputtel.text()
    pedidos = cadastro.imputpedido.text()
    preco = cadastro.imputpreco.text()


    banco = sqlite3.connect('banco_cadastro_usuario.db')
    Cursor = banco.cursor()
    Cursor.execute("CREATE TABLE IF NOT EXISTS pedidos (funcionario text, cliente text, Cpf integer primary key, endereço text, telefone text, pedidos text, preço text)")
    Cursor.execute("INSERT INTO pedidos VALUES('"+funcionario+"','"+cliente+"','"+Cpf+"','"+endereco+"','"+telefone+"','"+pedidos+"','"+preco+"')")

    banco.commit()
    cadastro.imputnomefunc.setText("")
    cadastro.imputnomecliente.setText("")
    cadastro.cpf.setText("")
    cadastro.imputend.setText("")
    cadastro.imputtel.setText("")
    cadastro.imputpedido.setText("")
    cadastro.imputpreco.setText("")
    banco.close()


def editar_pedidos():
    global cpf_id
    banco = sqlite3.connect('banco_cadastro_usuario.db') 
    linha = buscar_pedido.tableWidget.currentRow()
    
    cursor = banco.cursor()
    cursor.execute("SELECT Cpf FROM pedidos")
    dados_lidos = cursor.fetchall()
    valor_cpf = dados_lidos[linha][0]
    cursor.execute("SELECT * FROM pedidos WHERE Cpf="+ str(valor_cpf))
    pedido = cursor.fetchall()
    editar_pedido.move(380, 50)
    editar_pedido.show()
    

    
    editar_pedido.imputnomefunc.setText(str(pedido[0][0]))
    editar_pedido.imputnomecliente.setText(str(pedido[0][1]))
    editar_pedido.cpf.setText(str(pedido[0][2]))
    editar_pedido.imputend.setText(str(pedido[0][3]))
    editar_pedido.imputtel.setText(str(pedido[0][4]))
    editar_pedido.imputpedido.setText(str(pedido[0][5]))
    editar_pedido.imputpreco.setText(str(pedido[0][6]))
    
    cpf_id = valor_cpf

    banco.close()
    
def salvar_edicao():
    global cpf_id
    banco = sqlite3.connect('banco_cadastro_usuario.db') 
    funcionario = editar_pedido.imputnomefunc.text()
    cliente = editar_pedido.imputnomecliente.text()
    Cpf = editar_pedido.cpf.text()
    endereco = editar_pedido.imputend.text()
    telefone = editar_pedido.imputtel.text()
    pedido = editar_pedido.imputpedido.text()
    preco = editar_pedido.imputpreco.text()
    
    # atualizar os dados no banco
    cursor = banco.cursor()
    cursor.execute("UPDATE pedidos SET funcionario = '{}', cliente = '{}', endereço = '{}', telefone ='{}', pedidos = '{}',preço = '{}' WHERE Cpf = {}".format(funcionario,cliente ,endereco,telefone,pedido,preco,Cpf))
    banco.commit()
    editar_pedido.close()
    buscar_pedido.close()
    telaprincipal.move(380, 50)
    telaprincipal.show()

 

    

def excluir_pedido():

    banco = sqlite3.connect('banco_cadastro_usuario.db')  
    linha = buscar_pedido.tableWidget.currentRow()
    buscar_pedido.tableWidget.removeRow(linha)

    cursor = banco.cursor()
    cursor.execute("SELECT Cpf FROM pedidos")
    dados_lidos = cursor.fetchall()
    valor_id = dados_lidos[linha][0]
    cursor.execute("DELETE FROM pedidos WHERE Cpf="+ str(valor_id))
    banco.commit()
    banco.close()


def busca_completa(): 
    buscar_pedido.move(380, 50)
    buscar_pedido.show()
    telaprincipal.close()
    banco = sqlite3.connect('banco_cadastro_usuario.db') 
    cursor = banco.cursor()
    cursor.execute("select * from pedidos")
    resultados = cursor.fetchall()
    buscar_pedido.tableWidget.setRowCount(len(resultados))
    buscar_pedido.tableWidget.setColumnCount(7)

    for i in range(0, len(resultados)):
        for j in range(0, 7):
            buscar_pedido.tableWidget.setItem(i, j, QtWidgets.QTableWidgetItem(str(resultados[i][j])))
    banco.close()    



app=QtWidgets.QApplication([])
login1=uic.loadUi("login1.ui")
telaprincipal = uic.loadUi("tela_principal.ui")
cadastro = uic.loadUi("cadastro.ui")
tela_cadastro = uic.loadUi("cadastrar_usuario.ui")
editar_pedido = uic.loadUi("editar_pedidos.ui")
buscar_pedido = uic.loadUi("buscar_pedidos.ui")
abrir_backup = uic.loadUi("backup.ui")


login1.btnentrar.clicked.connect(tela_principal)
login1.senhalog.setEchoMode(QtWidgets.QLineEdit.Password)
login1.usecadastrar.clicked.connect(Abrir_cadastro_usuario)
tela_cadastro.cadastaruse.clicked.connect(cadastrar_usuario)
telaprincipal.cpedido.clicked.connect(cadastro_pedidos)
buscar_pedido.editar.clicked.connect(editar_pedidos)
cadastro.btncadastrar.clicked.connect(adicionar_pedidos)
editar_pedido.salvar.clicked.connect(salvar_edicao)
telaprincipal.bpedidos.clicked.connect(busca_completa)
#telaprincipal.backup.clicked.connect(tela_backup)
#abrir_backup.salvar.clicked.connect(backup)
#abrir_backup.sair.clicked.connect(fechar_backup)
telaprincipal.pushButton.clicked.connect(fechar_telapricipal)
cadastro.voltar.clicked.connect(fechar_cadastro)
buscar_pedido.sair.clicked.connect(busca)
buscar_pedido.excluir.clicked.connect(excluir_pedido)
#abrir_backup.recuperar.clicked.connect(recuperar_backup)
login1.show()
app.exec()
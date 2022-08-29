
from flask_mysqldb import MySQL
from flask import Flask, render_template, url_for, request, redirect, flash, jsonify
from sqlalchemy.exc import IntegrityError
import json
from config import app, mysql, cursor, conn

def queryprodutos():
    query = '''SELECT * FROM tb_produto ORDER BY nome'''
    cursor.execute(query)
    res = cursor.fetchall()
    produtos = []
    content = {}
    for result in res:
        content = {'ID': result[0], 'id_tipo': result[1],'nome': result[2], 'descricao': result[3],'qtd_estoque': result[4], 'qtd_minima': result[5],'valor_compra': result[6], 'valor_venda': result[7], 'ativo': result[8]}
        produtos.append(content)
        content={}
    return produtos



@app.route('/')
def index():
    return render_template('index.html')


@app.route('/produtos')
def produtos():
    produtos = queryprodutos()
    return render_template('produtos.html', produtos=produtos)


@app.route('/produtos_faltando')
def produtos_faltando():

    listaprodutos=queryprodutos()
    produtos = cursor.execute('SELECT * FROM tb_produto ORDER BY nome')
    #produtos = Estoque.query.order_by(Estoque.nome).all()
    produtos_em_falta = []

    for produto in listaprodutos:
        if int(produto['qtd_estoque']) < int(produto['qtd_minima']):
            produtos_em_falta.append(produto)
        #if int(produto.qtd_estoque) < int(produto.qtd_minima):
        #    produtos_em_falta.append(produto)

    return render_template('produtos_faltando.html', produtos=produtos_em_falta)


@app.route('/novo_produto/<erro_nome>', methods=['GET'])
def novo_produto(erro_nome):
    if erro_nome == 'sim':
        #TODO ALERT
        print('sim')
    return render_template('novo_produto.html')


@app.route('/criar_produto', methods=['POST'])
def criar_produto():

    id_tipo=request.form['tipo']
    nome = request.form['nome']
    descricao=request.form['descricao']
    valor_compra = request.form['valor_compra']
    valor_venda = request.form['valor_venda']
    qtd_estoque = request.form['qtd_estoque']
    qtd_minima = request.form['qtd_minima']
    disponivel= request.form['ativo']
    if(disponivel=="on"):
        disponivel ="1"
    else:
        disponivel ="0"

    try:
        
        cursor.execute(f'''INSERT INTO tb_produto (id_tipo, nome, descricao, qtd_estoque, qtd_minima, valor_compra, valor_venda, disponivel)
    VALUES ({id_tipo},"{nome}","{descricao}",{qtd_estoque},{qtd_minima},{valor_compra},{valor_venda},{disponivel}) ''')
        conn.commit()
    except IntegrityError:
        return redirect(url_for('novo_produto', erro_nome='sim'))
    produtos = queryprodutos()
    return render_template('produtos.html', produtos=produtos)

@app.route('/alterar_produto/<id>')
def alterar_produto(id):
    
    query = f'''SELECT * FROM tb_produto WHERE id_produto = {id}'''
    cursor.execute(query)
    res = cursor.fetchall()
   
    produto_para_modificar = []
    content = {}
    for result in res:
        content = {'ID': result[0], 'id_tipo': result[1],'nome': result[2], 'descricao': result[3],'qtd_estoque': result[4], 'qtd_minima': result[5],'valor_compra': result[6], 'valor_venda': result[7], 'ativo': result[8]}
        produto_para_modificar.append(content)
        content={}
    print(produto_para_modificar)
    return render_template('alterar_produto.html', produto=produto_para_modificar)
    #produto_para_modificar = cursor.execute(f'''SELECT * FROM produtos WHERE id = {id}''')
    #return render_template('alterar_produto.html', produto=produto_para_modificar)

@app.route('/modificar', methods=['POST'])
def modificar():
    id_produto = int(request.form['id_produto'])
   
    id_tipo = int(request.form['tipo'])
   
    nome = request.form['nome']
  
    descricao = request.form['descricao']
    
    qtd_estoque = int(request.form['qtd_estoque'])
    
    qtd_minima = int(request.form['qtd_minima']) 
       
    valor_compra = float(request.form['valor_compra'])
    
    valor_venda = float(request.form['valor_venda'])
    
    disponivel=(request.form['ativo'])
    if(disponivel=="on"):
        disponivel ="1"
    else:
        disponivel ="0"
    query=f'''UPDATE tb_produto SET id_tipo = {id_tipo}, nome = "{nome}", descricao = "{descricao}",  qtd_estoque = {qtd_estoque}, qtd_minima = {qtd_minima}, valor_compra = {valor_compra}, valor_venda = {valor_venda}, disponivel = {disponivel} WHERE id_produto = {id_produto};'''
    cursor.execute(query)
    conn.commit()
    return redirect(url_for('produtos'))



@app.route('/excluir_produto/<id>')
def excluir_produto(id):
    cursor.execute(f'DELETE FROM tb_produto WHERE id_produto = {id}')
    conn.commit()
    return redirect(url_for('produtos'))

@app.route('/venda')
def venda():
    produtos = queryprodutos()
    return render_template('venda.html', produtos=produtos)


@app.route('/reestoque')
def reestoque():
    produtos = queryprodutos()
    return render_template('reestoque.html', produtos=produtos)


if __name__ == '__main__':
    app.run(host='localhost',debug=True, port=8080)
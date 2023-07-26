import time
from flask import Flask, render_template, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy
from bs4 import BeautifulSoup
import requests

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///login_data.db'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)

def obter_login_payload():
    user = User.query.first()  # Obtém o primeiro usuário do banco de dados (pode ser ajustado conforme necessário)
    if user:
        return {"username": user.username, "password": user.password}
    else:
        return None

def contar_palavras_chave(soup, login_payload):
    print('... Iniciando código ...')
    global resultados, palavras_chave  # usar as variáveis globais
    resultados = {}

    print('... Abriu lista... e iniciando FOR ...')
    for palavra in palavras_chave:
        resultados[palavra] = 0
    print("... passou for ...")

    while True:
        print('... Iniciando FOR ...')
        elementos = soup.select('#main_principal')
        time.sleep(4)
        for elemento in elementos:
            conteudo_elemento = elemento.get_text()
            for palavra in palavras_chave:
                resultados[palavra] += conteudo_elemento.count(palavra)
                print('... While TRY ...')
        
        print('... Proxima página ...')
        proxima_pagina = soup.select('html body main form div div:nth-child(2) div div ul li:nth-child(6)')
        time.sleep(3)

        if len(proxima_pagina) == 0 or "disable" in proxima_pagina[0]['class']:
            break
            print("... Len DISABLE ...")
        proxima_pagina[0].click()

    # Atualizar a exibição dos resultados na página
    print('... Atualizando Resultados ...')
    resultados = {palavra: int(quantidade) for palavra, quantidade in resultados.items()}
    total_palavras = sum(resultados.values())

    print('... Return Resultados ...')
    return resultados, total_palavras

@app.route('/')
def index():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    user = User(username=username, password=password)
    db.session.add(user)
    db.session.commit()
    return redirect(url_for('exibir_resultados'))

@app.route('/exibir_resultados')
def exibir_resultados():
    global palavras_chave, resultados  # usar as variáveis globais
    palavras_chave = ["TOTAL EXP", "DATO TESTE", "AG AMINTAS"," AG LAMANHA","OLIST RETIRA", "AG ANGELO", "ENTREGA OSVALDO", "JAD", "TRANSPORTADORA", "ESM", "LATAM","AZUL", "GOL", "ANDREIA SSA", "BIT HOME", "RETIRA", "BLING", "AMPLO"]

    username = obter_login_payload()["username"]
    password = obter_login_payload()["password"]

    if username is None or password is None:
        return redirect(url_for('index'))

    url = "https://amplo.eship.com.br/"
    login_payload = obter_login_payload()
    headers = {"User-Agent": "Mozilla/5.0"}

    with requests.Session() as session:
        # Realizar login
        session.post(url, data=login_payload, headers=headers)
        time.sleep(3)
        print("... Logado ...")

        # Navegar para a página desejada
        lista_url = "https://amplo.eship.com.br/lista_de_itens"
        response = session.get(lista_url, headers=headers)
        soup = BeautifulSoup(response.content, "html.parser")
        resultados, total_palavras = contar_palavras_chave(soup, login_payload)

    # Remover palavras-chave com valor zero
    palavras_chave = [palavra for palavra in palavras_chave if resultados.get(palavra, 0) != 0]
    resultados = {palavra: quantidade for palavra, quantidade in resultados.items() if quantidade != 0}

    return render_template('index.html', resultados=resultados, total_palavras=total_palavras)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run()

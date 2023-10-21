from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

senha_correta = "dato123"  # Senha correta
nome_correto = "Dato"

@app.route('/')
def login():
    return render_template('login.html', mensagem_erro="")

@app.route('/verificar_senha', methods=['POST'])
def verificar_senha():
    nome_inserido = request.form['nome']
    senha_inserida = request.form['senha']
    
    if nome_inserido == nome_correto and senha_inserida == senha_correta:
        # Nome e senha corretos, redirecionar para a página principal ou outra rota
        return redirect(url_for('pagina_principal'))
    else:
        # Nome ou senha incorretos, exibir uma mensagem de erro
        mensagem_erro = "Nome ou senha incorretos. Tente novamente."
        return render_template('login.html', mensagem_erro=mensagem_erro)

@app.route('/pagina_principal')
def pagina_principal():
    return "Bem-vindo à página principal!"

if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)

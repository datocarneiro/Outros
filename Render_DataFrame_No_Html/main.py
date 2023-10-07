# Importa a classe Flask e a função render_template do módulo Flask
from flask import Flask, render_template
# Importa o módulo pandas com o alias 'pd'
import pandas as pd

# Cria uma instância do aplicativo Flask
app = Flask(__name__)

# Define uma rota raiz ("/") e associa a função resultado a ela
@app.route('/')
def resultado():
    # Chama a função criar_dataframe para criar um DataFrame pandas chamado 'df'
    df = criar_dataframe()
    # Converte o DataFrame 'df' em uma representação HTML e define classes CSS para a tabela HTML
    # ou seja transforma todos os dados do DataFrame, no formato de Tag html.
    table_html = df.to_html(classes='table table-bordered', index=False)
    print(table_html)
    # Renderiza um modelo HTML chamado 'resultado.html' e passa a variável 'table_html' para ele
    return render_template('resultado.html', table_html=table_html)

# Define a função criar_dataframe que cria um DataFrame pandas
def criar_dataframe():
    # Define uma lista de dicionários com dados fictícios
    dados = [{'NOME': 'Dato', 'SOBRENOME': "Carneiro", 'POSIÇÃO': "Atacante", "NÍVEL": 10},
             {'NOME': 'Dato', 'SOBRENOME': "Santos", 'POSIÇÃO': "Meio-campo", "NÍVEL": 10}]
    # Cria um DataFrame pandas a partir da lista de dicionários
    df = pd.DataFrame(dados)
    # Retorna o DataFrame criado
    return df

# Verifica se o script está sendo executado como um programa principal
if __name__ == '__main__':
    # Inicia o servidor web Flask na máquina local, escutando em todas as interfaces de rede na porta 8080
    app.run(host="0.0.0.0", port=8080)

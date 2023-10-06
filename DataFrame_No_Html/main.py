# main.py

from flask import Flask, render_template
from app import criar_dataframe  # Importa a função do arquivo app.py

app = Flask(__name__)

@app.route('/')
def resultado():
    df = criar_dataframe()  # Chama a função para criar o DataFrame
    table_html = df.to_html(classes='table table-bordered', index=False)
    return render_template('resultado.html', table_html=table_html)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080)
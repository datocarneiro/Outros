from flask import Flask, render_template, send_file
import pandas as pd
import io
from main import *

app = Flask(__name__)

@app.route('/tabela')
def index():
    df = tabela()  # Call the tabela function to get the DataFrame
    table_html = df.to_html(index=False)
    return render_template('index.html', table_html=table_html)

def tabela(df):
    dados = df
    planilha = pd.DataFrame(dados)
    print(df)
    return df

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080)

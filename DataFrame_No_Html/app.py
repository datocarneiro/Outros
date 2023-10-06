from flask import Flask, render_template, send_file
import pandas as pd
import io

app = Flask(__name__)

@app.route('/')
def index():
    df = tabela()  # Call the tabela function to get the DataFrame
    table_html = df.to_html(index=False)
    return render_template('index.html', table_html=table_html)

@app.route('/download')
def download():
    df = tabela()
    output = io.BytesIO()
    writer = pd.ExcelWriter(output, engine='xlsxwriter')
    df.to_excel(writer, sheet_name='Sheet1', index=False)
    writer.save()
    output.seek(0)
    return send_file(output, attachment_filename='tabela.xlsx', as_attachment=True)

def tabela():
    dados = [{'awb': 123, 'status': "entregue", 'data': "10/10/2023"},
             {'awb': 456, 'status': "rota", 'data': "2/2/2023"}]
    df = pd.DataFrame(dados)
    return df

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080)

from openpyxl import Workbook, load_workbook
import time
import os
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import pandas as pd
import tkinter as tk
from tkinter import filedialog
from flask import Flask, render_template, request
from werkzeug.utils import secure_filename

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/', methods=['POST'])
def process_form():
    file = request.files['file']
    
    # Solicitar ao usuário que escolha o nome e diretório de saída
    arquivo_saida = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Arquivos Excel", "*.xlsx")])

    # Salvar arquivo Excel enviado pelo usuário
    filename = secure_filename(file.filename)
    file.save(filename)

    if not filename.endswith('.xlsx'):
        return "Por favor, selecione um arquivo Excel (.xlsx)"

    # Carregar planilha
    planilha = load_workbook(filename)
    aba_ativa = planilha.active

    # LER A PLANILHA, E CRIAR UMA LISTA SOMENTE COM AS ENTREGAS DIFERENTE DE "ENTREGUE"
    lista = []

    for coluna_a, coluna_c, coluna_d in zip(aba_ativa["A"][1:], aba_ativa["C"][1:], aba_ativa["D"][1:]):
        # se os dados da coluna "D(status)" forem diferente de "Entregue", adicione(append) à lista os dados da coluna "C(AWB)".
        if coluna_d.value != 'ENTREGUE':
            if coluna_c.value is not None:
                lista.append(coluna_c.value)

    print("="*150)
    print(f'As pendente de entrega são: {lista}')
    print("="*150)

    servico = Service(ChromeDriverManager().install())

    # ABRI NAVEGADOR
    opcoes = Options()
    opcoes.headless = True  # modo off ou não
    driver = webdriver.Chrome(service=servico, options=opcoes)

    tabela = {}

    # FUNÇÃO PARA CONSULTAR STATUS DE RASTREAMENTO NO SITE DA LATAM
    def captura_status(awb):
        driver.get(f"https://www.latamcargo.com/en/trackshipment?docNumber={awb}&docPrefix=957&soType=SO")
        
        # Aguarde até que o elemento esteja visível
        wait = WebDriverWait(driver, 10)

        status_evento = wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="statusTable"]/tbody/tr[1]/td[1]')))
        status = status_evento.text 

        data_evento = wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="statusTable"]/tbody/tr[1]/td[6]')))
        data = data_evento.text 

        print(f'dados capturados: | AWB: {awb} | STATUS:{status} | DATA_EVENTO: {data} |')

        return [status, data]

    dados_rastreamento = []
    for awb in lista:
        status, data = captura_status(awb)
        dados_rastreamento.append({'AWB': awb, 'STATUS': status, 'DATA_EVENTO': data})

    df_rastreamento = pd.DataFrame(dados_rastreamento)
    print(df_rastreamento)

    # Salvar o DataFrame modificado em um arquivo Excel com o nome escolhido pelo usuário
    df_rastreamento.to_excel(arquivo_saida, index=False)

    print(f"Arquivo Excel '{arquivo_saida}' criado com sucesso.")

    return "Consulta de rastreamento realizada com sucesso!"

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)

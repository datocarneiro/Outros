import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from flask import Flask, render_template, request
from openpyxl import load_workbook
from werkzeug.utils import secure_filename
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from pathlib import Path
import xlsxwriter
import os

options = Options()
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.headless = False  # Executar o Chrome de forma oculta
driver = webdriver.Chrome(options=options) # replit

# Inicialização do aplicativo Flask
app = Flask(__name__)

lista_pendentes = [] # Variável global para armazenar a lista

# FUNÇÃO PARA CONSULTAR STATUS DE RASTREAMENTO NO SITE DA LATAM
def captura_status(awb):
    driver.get(f"https://www.latamcargo.com/en/trackshipment?docNumber={awb}&docPrefix=957&soType=SO")

    wait = WebDriverWait(driver, 10)

    status_evento = wait.until(
        EC.visibility_of_element_located((By.XPATH, '//*[@id="statusTable"]/tbody/tr[1]/td[1]')))
    status = status_evento.text

    data_evento = wait.until(
        EC.visibility_of_element_located((By.XPATH, '//*[@id="statusTable"]/tbody/tr[1]/td[6]')))
    data = data_evento.text

    captura = f'dados capturados: | AWB: {awb} | STATUS:{status} | DATA_EVENTO: {data} |'
    print(captura)
    print("="*150)

    return status, data, captura

def capturar_status_pendentes():
    dados_rastreamento = []
    statuses = []  # Lista para armazenar os valores de status
    datas = []  # Lista para armazenar os valores de data

    for awb in lista_pendentes:
        status, data, _ = captura_status(awb)  # Descartar o valor da captura
        dados_rastreamento.append({'AWB': awb, 'STATUS': status, 'DATA_EVENTO': data})
        statuses.append(status)  # Adicionar o status à lista
        datas.append(data)  # Adicionar a data à lista

    df_rastreamento = pd.DataFrame(dados_rastreamento)
    print(df_rastreamento)

    return df_rastreamento

@app.route('/', methods=['POST'])
def preparar_dados_planilha():
    global lista_pendentes # Acessando a variável global
    file = request.files['file']
    
    if not file.filename.endswith('.xlsx'):
        return "Por favor, selecione um arquivo Excel (.xlsx)"

    # Carregar planilha
    planilha = load_workbook(file)
    aba_ativa = planilha.active

    # LER A PLANILHA, E CRIAR UMA LISTA SOMENTE COM AS ENTREGAS DIFERENTE DE "ENTREGUE"
    lista_pendentes = [coluna_c.value for coluna_a, coluna_c, coluna_d in zip(aba_ativa["A"][1:], aba_ativa["C"][1:], aba_ativa["D"][1:]) if coluna_d.value != 'ENTREGUE' and coluna_c.value is not None]

    print("=" * 150)
    print(f'As pendente de entrega são: {lista_pendentes}')
    print("=" * 150)

    df_rastreamento = capturar_status_pendentes()
    statuses = df_rastreamento['STATUS']
    datas = df_rastreamento['DATA_EVENTO']

    # Salvar o DataFrame em um arquivo Excel na pasta "Downloads"
    nome_arquivo = 'rastreamento.xlsx'
    caminho_arquivo = os.path.join(os.path.expanduser("~"), "C:/Downloads", nome_arquivo)
    df_rastreamento.to_excel(caminho_arquivo, index=False)

    return render_template('index.html', pendentes=lista_pendentes, statuses=statuses, datas=datas)

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080)

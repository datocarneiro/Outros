import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from flask import Flask, render_template, request, redirect, url_for
from openpyxl import load_workbook
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from webdriver_manager.chrome import ChromeDriverManager

# Inicializa o aplicativo Flask
app = Flask(__name__)

# Variáveis globais
lista_pendentes = []
tabela = None  # Inicializa a tabela como None


# Inicializa o ChromeDriver com opções
servico = Service(ChromeDriverManager().install())
opcoes = webdriver.ChromeOptions()
opcoes.headless = True  # Defina como True para o modo headless
driver = webdriver.Chrome(service=servico, options=opcoes)

# Define rotas
@app.route('/')
def index():
    if tabela is not None:
        return render_template('index.html', pendentes=lista_pendentes, tabela=tabela.to_html(classes='data'))
    else:
        return render_template('index.html', pendentes=lista_pendentes, tabela=None)

# @app.route('/resultados')
#def mostrar_tabela():
#   return render_template('resultados.html', tabela=tabela.to_html(classes='data'))

@app.route('/', methods=['POST'])
def preparar_dados_planilha():
    global lista_pendentes
    global tabela

    file = request.files['file']

    if not file.filename.endswith('.xlsx'):
        return "Por favor, selecione um arquivo Excel (.xlsx)"

    planilha = load_workbook(file)
    aba_ativa = planilha.active

    lista_pendentes = []
    for coluna_a, coluna_c, coluna_d in zip(aba_ativa["A"][1:],
                                            aba_ativa["C"][1:],
                                            aba_ativa["D"][1:]):
        if coluna_d.value != 'ENTREGUE':
            if coluna_c.value is not None:
                lista_pendentes.append(coluna_c.value)

    statuses, datas = capturar_status_pendentes()
    capturas = []

    for awb, status, data in zip(lista_pendentes, statuses, datas):
        captura = f'{awb}    ,{status}    ,{data}'
        capturas.append(captura)

    # Atualizar a tabela global
    tabela = pd.DataFrame({
        'AWB': lista_pendentes,
        'STATUS': statuses,
        'DATA_EVENTO': datas
    })


    return render_template('index.html',
                           pendentes=lista_pendentes,
                           statuses=statuses,
                           datas=datas,
                           capturas=capturas)

# Função para capturar status de rastreamento no site da LATAM Cargo
def captura_status(awb):
    driver.get(f"https://www.latamcargo.com/en/trackshipment?docNumber={awb}&docPrefix=957&soType=SO")

    wait = WebDriverWait(driver, 30)

    try:
        status_evento = wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="statusTable"]/tbody/tr[1]/td[1]')))
        status = status_evento.text

        data_evento = wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="statusTable"]/tbody/tr[1]/td[6]')))
        data = data_evento.text

        captura = f'dados capturados,AWB,{awb},STATUS,{status},DATA_EVENTO,{data}'
        print(captura)

        return status, data
    except TimeoutException:
        status = "Erro de tempo limite"
        data = "Erro de tempo limite"
        print("Erro de tempo limite ao capturar os dados")
        return status, data

# Função para capturar status de rastreamento das encomendas pendentes
def capturar_status_pendentes():
    dados_rastreamento = []
    statuses = []
    datas = []

    for awb in lista_pendentes:
        status, data = captura_status(awb)
        dados_rastreamento.append({
            'AWB': awb,
            'STATUS': status,
            'DATA_EVENTO': data
        })
        statuses.append(status)
        datas.append(data)

    return statuses, datas

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080)
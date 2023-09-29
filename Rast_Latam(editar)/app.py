from openpyxl import load_workbook
import os
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import pandas as pd
from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
import pathlib


app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/', methods=['POST'])
def process_form():
    file = request.files['file']
    
    # Solicitar ao usuário que escolha o nome de saída para o arquivo DataFrame
    arquivo_saida = secure_filename(file.filename).replace('.xlsx', '_modificado.xlsx')

    if not file.filename.endswith('.xlsx'):
        return "Por favor, selecione um arquivo Excel (.xlsx)"

    # Carregar planilha
    planilha = load_workbook(file)
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
    opcoes.headless = False  # modo off ou não
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

  
    # Obter o diretório da pasta de downloads do sistema operacional
    diretorio_downloads = str(pathlib.Path.home() / "Downloads")

    # Caminho completo para o arquivo de saída na pasta de downloads
    caminho_saida = os.path.join(diretorio_downloads, arquivo_saida)

    # Salvar o DataFrame modificado em um arquivo Excel na pasta de downloads
    df_rastreamento.to_excel(caminho_saida, index=False)


    print(f"Arquivo Excel '{arquivo_saida}' criado com sucesso.")

    # return "Consulta de rastreamento realizada com sucesso!"
    # Renderizar a página HTML e passar a variável resultado como argumento
    
    #resultado = f'A última consulta de rastreamento retornou: | AWB: {awb} | STATUS:{status} | DATA_EVENTO: {data} |'
    #return render_template('index.html', resultado=resultado)
    resultado = "Todas as consultas foram realizadas com sucesso"
    return render_template('index.html', resultado=resultado, pendentes=lista)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)

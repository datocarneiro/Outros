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

diretorio_atual = os.path.dirname(os.path.abspath(__file__))
arquivo = os.path.join(diretorio_atual, 'rastreamento.xlsx')

# Carregar planilha
planilha = load_workbook(arquivo)
aba_ativa = planilha.active

# LER A PLANILHA, E CRIAR UMA LISTA SOMENTE COM AS ENTREGAS DIFERENTE DE "ENTREGUE"
lista = []

for coluna_a, coluna_c, coluna_d in zip(aba_ativa["A"][1:], aba_ativa["C"][1:], aba_ativa["D"][1:]):
    '''
    # PRINTAR NO TERMINAL TODOS OS STATUS 
    print(f'Franquia: {coluna_a.value}')
    print(f'AWB: {coluna_c.value}')
    print(f'Status: {coluna_d.value}')
    '''

    # se os dados da coluna "D(status)" forem diferente de "Entregue", adicione(append) à lista os dados da coluna "C(AWB)".
    if coluna_d.value != 'ENTREGUE' or 'entregue':
        lista.append(coluna_c.value)

# FORMATANDO O CODIGO AWB, RETIRANDO OS 3 PRIMEIROS DIGITOS
lista_awb_formatada = []
for i in lista:
    awb_formatada = int(str(i)[3:])
    lista_awb_formatada.append(awb_formatada)
    
# EXIBIR SOMENTE AS PENDENTE DE ENTREGA
print("-"*40)
print(f' As pendente de entrega são: {lista_awb_formatada}')
print("-"*40)
 
servico = Service(ChromeDriverManager().install())

# FUNÇÃO PARA CONSULTAR STATUS DE RASTREAMENTO NO SITE DA LATAM
def captura_status(awb):
    opcoes = Options()
    opcoes.headless = False  # modo off ou não
    driver = webdriver.Chrome(service=servico, options=opcoes)

    # https://www.latamcargo.com/en/trackshipment?docNumber=12801530&docPrefix=957&soType=SO
    # 13127026 TRANSFERENCIA , 13128710 EM ROTA, 13034092 EM ROTA 

    driver.get(f"https://www.latamcargo.com/en/trackshipment?docNumber={awb}&docPrefix=957&soType=SO")
    
    # Aguarde até que o elemento esteja visível
    wait = WebDriverWait(driver, 10)

    status_evento = wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="statusTable"]/tbody/tr[1]/td[1]')))

    status = status_evento.text 
    print(status)

    data_evento = wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="statusTable"]/tbody/tr[1]/td[6]')))
    data = data_evento.text 
    print(data)

    return [status, data]



dicionario = {}
for awb in lista_awb_formatada:
    dicionario[awb] = captura_status(awb)
print(dicionario)
    
time.sleep(5)

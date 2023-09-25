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
from selenium.common.exceptions import NoSuchElementException

diretorio_atual = os.path.dirname(os.path.abspath(__file__))
arquivo = os.path.join(diretorio_atual, 'rastreamento.xlsx')

# Carregar planilha
planilha = load_workbook(arquivo)
aba_ativa = planilha.active


# consultar a planilha, e criar uma lista somente com as que forem diferente de "ENTREGUE"
lista = []
dicionario = {}
for coluna_a, coluna_c, coluna_d in zip(aba_ativa["A"][1:], aba_ativa["C"][1:], aba_ativa["D"][1:]):
    print(f'Franquia: {coluna_a.value}')
    print(f'AWB: {coluna_c.value}')
    print(f'Status: {coluna_d.value}')
    #se os dados da coluna "D(status)" forem diferente de "Entregue", adicione(append) à lista os dados da coluna "C(AWB)".
    if coluna_d.value != 'ENTREGUE':
        lista.append(coluna_c.value)
        print('-'*50)
    else:
        print('não adicionar')
        print('-'*50)
print(f'Lista das pendencias: {lista[:]}')

print('-'*50)

lista_awb_formatada = []

for i in lista:
    awb_formatado = int(str(i)[3:])  # Cortar os 3 primeiros números e converter de volta para inteiro
    lista_awb_formatada.append(awb_formatado)
print(lista_awb_formatada)

servico = Service(ChromeDriverManager().install())

lista_awb_formatada = [12801530, 13102972]
for i in lista_awb_formatada:
    print(i)

    print('-'*50)
  
    opcoes = Options()
    opcoes.headless = False  # modo off ou não
    driver = webdriver.Chrome(service=servico, options=opcoes)

    print('... ENTRANDO NO SITE DA LATAM, AGUARDE, "vai pegar um café apressado(a)!" ...')
    # https://www.latamcargo.com/en/trackshipment?docNumber=12801530&docPrefix=957&soType=SO
    # 13127026 TRANSFERENCIA , 13128710 EM ROTA, 13034092 EM ROTA 


    link = driver.get(f"https://www.latamcargo.com/en/trackshipment?docNumber={i}&docPrefix=957&soType=SO")
    print("... horas depoiS, O SITE FOI CARREGADO")

    # movimentacoes = driver.find_element(By.XPATH, '#statusTable > tbody > tr:nth-child(1) > td.Event')
    movimentacoes = driver.find_element(By.XPATH, '//*[@id="statusTable"]/tbody/tr[1]/td[2]/text()').click()
      

    print('passou XPATH ........................................')


    lista_movimentacoes = []
    lista_movimentacoes = lista_movimentacoes.append(movimentacoes.text)

    driver.quit()
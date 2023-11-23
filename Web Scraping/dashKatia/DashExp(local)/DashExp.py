import time #teste
import os
from flask import Flask, render_template
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException

servico = Service(ChromeDriverManager().install())

app = Flask(__name__)

def contar_palavras_chave():
    print('... Iniciando código ...')
    global resultados, palavras_chave  # usar as variáveis globais
    resultados = {}

    opcoes = Options()
    opcoes.headless = True  # modo off ou não
    navegador = webdriver.Chrome(service=servico, options=opcoes)
    
    print('... Logando ...')
    navegador.get("https://amplo.eship.com.br/")
    navegador.find_element(By.XPATH, '//*[@id="login"]').send_keys("dato@amplologistica.com.br")
    navegador.find_element(By.XPATH, '//*[@id="senha"]').send_keys("D@sh4123")
    navegador.find_element(By.XPATH, '//*[@id="Entrar"]/span').click()
    time.sleep(5)
    print("... Logado ...")

    navegador.find_element(By.XPATH, '//*[@id="FormListarOrdem"]/ul/li[2]/div/a[3]/div').click()
    print('... Abriu lista para 100... e iniciando FOR ...')
    time.sleep(5)
    for palavra in palavras_chave:
        resultados[palavra] = 0
    print("... passou for ...")

    while True:
        print('... Iniciando FOR ...')
        try:
            elementos = navegador.find_elements(By.XPATH, '//*[@id="FormListarOrdem"]')
            time.sleep(5)
            for elemento in elementos:
                conteudo_elemento = elemento.text
                for palavra in palavras_chave:
                    resultados[palavra] += conteudo_elemento.count(palavra)
                    print(f'... Palavra {palavra} encontrada ...')
        except NoSuchElementException:
            break
            print("... While except ...")
        
        print('... Proxima página ...')
        proxima_pagina = navegador.find_elements(By.XPATH, '/html/body/main/form/div[1]/div[2]/div/div[2]/div/ul/li[6]')
        time.sleep(5)

        if len(proxima_pagina) == 0 or "disable" in proxima_pagina[0].get_attribute("class"):
            break
            print("... Len DISABLE ...")
        proxima_pagina[0].click()

    # Atualizar a exibição dos resultados na página
    print('... Atualizando Resultados ...')
    resultados = {palavra: int(quantidade) for palavra, quantidade in resultados.items()}
    total_palavras = sum(resultados.values())

    print('... Return Resultados ...')
    return resultados, total_palavras
 
@app.route('/') 
def exibir_resultados():
    global palavras_chave, resultados  # usar as variáveis globais
    palavras_chave = ["TOTAL EXP",
                        "FM",
                        "DATO TESTE",
                        "AG AMINTAS",
                        "AG LAMENHA",
                        "OLIST RETIRA",
                        "AG ANGELO",
                        "ENTREGA OSVALDO",
                        "JAD", "TRANSPORTADORA",
                        "ESM",
                        "LATAM",
                        "AZUL",
                        "GOL",
                        "ANDREIA SSA",
                        "BIT HOME",
                        "RETIRA",
                        "BLING",
                        "SUBWAY - AMPLO"]
    resultados, total_palavras = contar_palavras_chave()

    # Remover palavras-chave com valor zero
    palavras_chave = [palavra for palavra in palavras_chave if resultados.get(palavra, 0) != 0]
    resultados = {palavra: quantidade for palavra, quantidade in resultados.items() if quantidade != 0}

    return render_template('index.html', resultados=resultados, total_palavras=total_palavras)

if __name__ == '__main__':
    app.run()


# precisa trocar o --hidden-import=tkinter para as bibliotecas que estou utilizando, e atualizar o diretorio da pasta 

# criar uma pasta virtual 
# python -m venv "nome da pasta"
# cria o codigo dentro 
# bibliotecas
# fazer o deplay

''' FAZER DEPLOY EXECUTAVEL
pip install pyinstaller
pyinstaller --onefile --hidden-import=flask --hidden-import=selenium --hidden-import=time  --noconsole d:/Repositorio/Python/YoutubeTools/nome do programa.py
'''

# onfile -> irá criar o execultavel 
# noconsole -> irá rodar o terminal em segundo plano para o usuario
import time
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
    global resultados, palavras_chave  # usar as variáveis globais
    resultados = {}

    opcoes = Options()
    opcoes.headless = True  # modo off ou não
    navegador = webdriver.Chrome(service=servico, options=opcoes)

    navegador.get("https://amplo.eship.com.br/")
    navegador.find_element(By.XPATH, '//*[@id="login"]').send_keys("dashboard3")
    navegador.find_element(By.XPATH, '//*[@id="senha"]').send_keys("12341234")
    navegador.find_element(By.XPATH, '//*[@id="Entrar"]/span').click()
    time.sleep(3)
    print("Buscando...")

    navegador.find_element(By.XPATH, '//*[@id="FormListarRemessas"]/ul/li[2]/div/a[3]/div').click()

    for palavra in palavras_chave:
        resultados[palavra] = 0
    print("passou for...")

    while True:
        try:
            elementos = navegador.find_elements(By.XPATH, '//*[@id="main_principal"]')
            time.sleep(4)
            for elemento in elementos:
                conteudo_elemento = elemento.text
                for palavra in palavras_chave:
                    resultados[palavra] += conteudo_elemento.count(palavra)
        except NoSuchElementException:
            break

        print("passou While except...")
        proxima_pagina = navegador.find_elements(By.XPATH, '/html/body/main/form/div[1]/div[2]/div/div[2]/div/ul/li[6]')
        time.sleep(3)

        if len(proxima_pagina) == 0 or "disable" in proxima_pagina[0].get_attribute("class"):
            break
        print("passou if...")
        proxima_pagina[0].click()

    # Atualizar a exibição dos resultados na página
    resultados = {palavra: int(quantidade) for palavra, quantidade in resultados.items()}
    total_palavras = sum(resultados.values())

    return resultados, total_palavras
    print("passou return...")

@app.route('/') 
def exibir_resultados():
    global palavras_chave, resultados  # usar as variáveis globais
    palavras_chave = ["TESTE", "BLING", "AMPLO", "DATO", "TOTAL EXP", "AG AMINTAS", "JAD", "TRANSPORTADORA", "ESM", "LATAM", "BIT HOME", "RETIRA"]
    resultados, total_palavras = contar_palavras_chave()

    # Remover palavras-chave com valor zero
    palavras_chave = [palavra for palavra in palavras_chave if resultados.get(palavra, 0) != 0]
    resultados = {palavra: quantidade for palavra, quantidade in resultados.items() if quantidade != 0}

    return render_template('index.html', resultados=resultados, total_palavras=total_palavras)

if __name__ == '__main__':
    app.run()

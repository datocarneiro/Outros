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

    while True:
        opcoes = Options()
        opcoes.add_argument("--headless")
        navegador = webdriver.Chrome(service=servico, options=opcoes)

        navegador.get("https://amplo.eship.com.br/")
        navegador.find_element(By.XPATH, '//*[@id="login"]').send_keys("dashboard3")
        navegador.find_element(By.XPATH, '//*[@id="senha"]').send_keys("12341234")
        navegador.find_element(By.XPATH, '//*[@id="Entrar"]/span').click()

        time.sleep(5)

        navegador.find_element(By.XPATH, '//*[@id="FormListarRemessas"]/ul/li[2]/div/a[3]/div').click()
        time.sleep(1)

        for palavra in palavras_chave:
            resultados[palavra] = 0

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

            proxima_pagina = navegador.find_elements(By.XPATH, '/html/body/main/form/div[1]/div[2]/div/div[2]/div/ul/li[6]')
            
            if len(proxima_pagina) == 0 or "disable" in proxima_pagina[0].get_attribute("class"):
                break

            proxima_pagina[0].click()

        navegador.quit()
        break

@app.route('/')
def exibir_resultados():
    global palavras_chave, resultados  # usar as variáveis globais
    palavras_chave = ["TOTAL EXP", "AG AMINTAS", "JAD", "TRANSPORTADORA", "ESM", "BIT HOME", "RETIRA", "LATAM"]
    contar_palavras_chave()

    # Converter os valores para inteiros antes de calcular a soma
    resultados = {palavra: int(quantidade) for palavra, quantidade in resultados.items()}

    total_palavras = sum(resultados.values())

    return render_template('index.html', resultados=resultados, total_palavras=total_palavras)


if __name__ == '__main__':
    app.run()

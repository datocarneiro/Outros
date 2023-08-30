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
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager

#pip show selenium (verifica a versão do selenium)

servico = Service(ChromeDriverManager().install())
app = Flask(__name__)

def get_driver(browser):
    if browser == "chrome":
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")  # Executar o navegador em modo oculto
        options.add_argument("--window-size=1920x1080")  # Especificar uma resolução de tela para o modo headless
        options.add_argument("--disable-gpu")
        navegador = webdriver.Chrome(service=servico, options=webdriver.))  # Desativar aceleração de GPU

    elif browser == "firefox":
        options = FirefoxOptions()
        options.headless = True  # Executar o navegador de forma oculta

        return webdriver.Firefox(executable_path=GeckoDriverManager().install(), options=options)
    elif browser == "edge":
        return webdriver.Edge(EdgeChromiumDriverManager().install())
    else:
        raise ValueError("Navegador não suportado")


def login_to_external_site(navegador):
    print('Realizando login no site externo...')
    navegador.get("https:.com.br/")
    time.sleep(2)
    username_field = navegador.find_element(By.XPATH, '//*[@id="login"]')
    password_field = navegador.find_element(By.XPATH, '//*[@id="senha"]')
    login_button = navegador.find_element(By.XPATH, '//*[@id="Entrar"]/span')

    username_field.send_keys("xxxxxxxx")
    password_field.send_keys("xxxxxxxx")
    login_button.click()
    time.sleep(5)
    print("Preenchendo campos de login e senha...")

def contar_palavras_chave():
    print('... Iniciando código ...')
    navegador = get_driver("chrome")
    global resultados, palavras_chave  # usar as variáveis globais
    resultados = {}

    # Obtendo o driver do Chrome
    navegador = get_driver("chrome")

    print('... Logando ...')
    login_to_external_site(navegador)
    time.sleep(3)
    print("... Login realizado ...")

    navegador.find_element(By.XPATH, '//*[@id="FormListarRemessas"]/ul/li[2]/div/a[3]/div').click()
    time.sleep(3)
    print('... Abriu lista... e iniciando FOR ...')
    for palavra in palavras_chave:
        resultados[palavra] = 0
    print("... passou for ...")

    while True:
        print('... Iniciando FOR ...')
        try:
            elementos = navegador.find_elements(By.XPATH, '//*[@id="main_principal"]')
            time.sleep(4)
            for elemento in elementos:
                conteudo_elemento = elemento.text
                for palavra in palavras_chave:
                    resultados[palavra] += conteudo_elemento.count(palavra)
                    print('... PALAVRA ENCONTRADA ...')
        except NoSuchElementException:
            break
            print("... While except ...")
        
        print('... Proxima página ...')
        proxima_pagina = navegador.find_elements(By.XPATH, '/html/body/main/form/div[1]/div[2]/div/div[2]/div/ul/li[6]')
        time.sleep(3)

        if len(proxima_pagina) == 0 or "disable" in proxima_pagina[0].get_attribute("class"):
            break
            print("... Len DISABLE ...")
        proxima_pagina[0].click()

    # Fechar o navegador após a automação
    navegador.quit()

    # Atualizar a exibição dos resultados na página
    print('... Atualizando Resultados ...')
    resultados = {palavra: int(quantidade) for palavra, quantidade in resultados.items()}
    total_palavras = sum(resultados.values())
    print()
    print('"... RETURN - TODOS OS RESULTADOS ..."')
    # Exibir os resultados como uma lista
    print("Resultados:")
    for palavra, quantidade in resultados.items():
        print(f"{palavra}: {quantidade}")

    return resultados, total_palavras
 
@app.route('/') 
def exibir_resultados():
    global palavras_chave, resultados  # usar as variáveis globais
    palavras_chave = ["TOTAL EXP", "DATO TESTE", "AG AMINTAS"," AG LAMANHA","OLIST RETIRA", "AG ANGELO", "ENTREGA OSVALDO", "JAD", "TRANSPORTADORA", "ESM", "LATAM","AZUL", "GOL", "ANDREIA SSA", "BIT HOME", "RETIRA", "BLING", "AMPLO"]
    resultados, total_palavras = contar_palavras_chave()

    # Remover palavras-chave com valor zero
    palavras_chave = [palavra for palavra in palavras_chave if resultados.get(palavra, 0) != 0]
    resultados = {palavra: quantidade for palavra, quantidade in resultados.items() if quantidade != 0}
    print()
    print("... RETURN - SOMENTE RESULTADOS > 0 ...")
    # Exibir os resultados como uma lista
    print("Resultados:")
    for palavra, quantidade in resultados.items():
        print(f"{palavra}: {quantidade}")
    print()
    return render_template('index.html', resultados=resultados, total_palavras=total_palavras)

if __name__ == '__main__':
    app.run()
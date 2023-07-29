import time
from flask import Flask, render_template, jsonify
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options as ChromeOptions
from bs4 import BeautifulSoup
import threading


app = Flask(__name__)

def get_driver():
    options = ChromeOptions()
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--headless")
    return webdriver.Chrome(options=options)

def login_to_external_site(navegador):
    print('Realizando login no site externo...')
    navegador.get("https://amplo.eship.com.br/")
    time.sleep(2)
    username_field = navegador.find_element(By.XPATH, '//*[@id="login"]')
    password_field = navegador.find_element(By.XPATH, '//*[@id="senha"]')
    login_button = navegador.find_element(By.XPATH, '//*[@id="Entrar"]/span')

    username_field.send_keys("dashboard3")
    password_field.send_keys("12341234")
    login_button.click()
    time.sleep(5)
    print("Preenchendo campos de login e senha...")

def get_page_content(navegador):
    page_content = navegador.page_source
    soup = BeautifulSoup(page_content, "html.parser")
    return soup

def consultar_palavras_chave(navegador):
    print('... Iniciando código ...')
    global resultados, palavras_chave
    resultados = {}
    print('... Logando ...')
    login_to_external_site(navegador)
    time.sleep(3)
    print("... Logado ...")

    navegador.find_element(By.XPATH, '//*[@id="FormListarRemessas"]/ul/li[2]/div/a[3]/div').click()
    time.sleep(3)
    print('... Abriu lista... e iniciando FOR ...')
    for palavra in palavras_chave:
        resultados[palavra] = 0
    print("... passou for ...")

    while True:
        print('... Iniciando FOR ...')
        try:
            soup = get_page_content(navegador)
            elementos = soup.select("#main_principal")
            time.sleep(4)
            for elemento in elementos:
                conteudo_elemento = elemento.get_text()
                for palavra in palavras_chave:
                    resultados[palavra] += conteudo_elemento.count(palavra)
                    resultados[palavra] /= 2  # Dividindo a quantidade por 2
                    print(f'... PALAVRA {palavra} ENCONTRADA ...')
        except NoSuchElementException:
            break

        print('... Proxima página ...')
        proxima_pagina = navegador.find_elements(By.XPATH, '/html/body/main/form/div[1]/div[2]/div/div[2]/div/ul/li[6]')
        time.sleep(3)
        if len(proxima_pagina) == 0 or "disable" in proxima_pagina[0].get_attribute("class"):
            break
            print("... Len DISABLE ...")
        proxima_pagina[0].click()
    print('... Atualizando Resultados ...')
    resultados = {palavra: int(quantidade) for palavra, quantidade in resultados.items()}
    total_palavras = sum(resultados.values())
    print("Resultados:")
    for palavra, quantidade in resultados.items():
        print(f"{palavra}: {quantidade}")
    return resultados, total_palavras
 
@app.route('/') 
def exibir_resultados():
    global palavras_chave, resultados  # usar as variáveis globais
    palavras_chave = ["TOTAL EXP", "DATO TESTE", "AG AMINTAS"," AG LAMANHA","OLIST RETIRA", "AG ANGELO", "ENTREGA OSVALDO", "JAD", "TRANSPORTADORA", "ESM", "LATAM","AZUL", "GOL", "ANDREIA SSA", "BIT HOME", "RETIRA", "BLING", "AMPLO"]
    resultados, total_palavras = consultar_palavras_chave(get_driver())
    palavras_chave = [palavra for palavra in palavras_chave if resultados.get(palavra, 0) != 0]
    resultados = {palavra: quantidade for palavra, quantidade in resultados.items() if quantidade != 0}
    print()
    print("... RETURN - SOMENTE RESULTADOS > 0 ...")
    print("Resultados:")
    for palavra, quantidade in resultados.items():
        print(f"{palavra}: {quantidade}")
    print()
    return render_template('resultados.html', resultados=resultados, total_palavras=total_palavras)

@app.route('/api/resultados')
def obter_resultados():
    global palavras_chave, resultados
    palavras_chave = [  "TOTAL EXP",
                        "DATO TESTE",
                        "AG AMINTAS",
                        "AG LAMANHA",
                        "OLIST RETIRA",
                        "AG ANGELO",
                        "ENTREGA OSVALDO",
                        "JAD",
                        "TRANSPORTADORA",
                        "ESM",
                        "LATAM",
                        "AZUL",
                        "GOL",
                        "ANDREIA SSA",
                        "BIT HOME",
                        "RETIRA",
                        "BLING",
                        "AMPLO"]
                        
    resultados, total_palavras = consultar_palavras_chave(get_driver())
    palavras_chave = [palavra for palavra in palavras_chave if resultados.get(palavra, 0) != 0]
    resultados = {palavra: quantidade for palavra, quantidade in resultados.items() if quantidade != 0}
    print()
    print("... RETURN - SOMENTE RESULTADOS > 0 ...")
    print("Resultados:")
    print("Use /api/resultados em seu navegador ou cliente HTTP, receberá os resultados em formato JSON.")
    for palavra, quantidade in resultados.items():
        print(f"{palavra}: {quantidade}")
    print()

    # Retornar os resultados como JSON
    return jsonify(resultados=resultados, total_palavras=total_palavras)

def atualizar_resultados_periodicamente(intervalo=60):
    while True:
        atualizar_resultados()
        time.sleep(intervalo)


def atualizar_resultados():
    global palavras_chave, resultados
    palavras_chave = ["TOTAL EXP", "DATO TESTE", "AG AMINTAS", "AG LAMENHA", "OLIST RETIRA", "AG ANGELO", "ENTREGA OSVALDO", "JAD", "TRANSPORTADORA", "ESM", "LATAM", "AZUL", "GOL", "ANDREIA SSA", "BIT HOME", "RETIRA", "BLING", "AMPLO"]
    resultados, total_palavras = consultar_palavras_chave(get_driver())
    palavras_chave = [palavra for palavra in palavras_chave if resultados.get(palavra, 0) != 0]
    resultados = {palavra: quantidade for palavra, quantidade in resultados.items() if quantidade != 0}
    print()
    print("... RETORNO - SOMENTE RESULTADOS > 0 ...")
    print("Resultados:")
    print("Acesse /api/resultados no seu navegador ou cliente HTTP para receber os resultados em formato JSON.")
    for palavra, quantidade in resultados.items():
        print(f"{palavra}: {quantidade}")
    print()

if __name__ == '__main__':
    # Iniciar a thread para atualização dos resultados
    thread_atualizacao = threading.Thread(target=atualizar_resultados_periodicamente, args=(60,))
    thread_atualizacao.daemon = True  # Isso permite encerrar a thread quando o programa principal (o app Flask) terminar
    thread_atualizacao.start()

    # Iniciar o aplicativo Flask
    app.run(host="0.0.0.0", port=5000)

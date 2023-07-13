import time
import os
from flask import Flask, render_template, request  # Importar 'request'
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

resultados = {}
def contar_palavras_chave(usuario, senha):
   
    global resultados, palavras_chave
    
    opcoes = Options()
    opcoes.add_argument("--headless")
    navegador = webdriver.Chrome(service=servico, options=opcoes)

    navegador.get("https://amplo.eship.com.br/")
    navegador.find_element(By.XPATH, '//*[@id="login"]').send_keys(usuario)
    navegador.find_element(By.XPATH, '//*[@id="senha"]').send_keys(senha)
    navegador.find_element(By.XPATH, '//*[@id="Entrar"]/span').click()

    time.sleep(5)
    
    # abre a lista pra 100
    navegador.find_element(By.XPATH, '//*[@id="FormListarRemessas"]/ul/li[2]/div/a[3]/div').click()
    time.sleep(1)

    for palavra in palavras_chave:
        resultados[palavra] = 0

    while True:
        try: # Quando um erro ocorre dentro do bloco "try", o código dentro do bloco "except" é executado, a exceção nesse caso é: NoSuchElementException:
            elementos = navegador.find_elements(By.XPATH, '//*[@id="main_principal"]') 

            time.sleep(4)
            for elemento in elementos:
                conteudo_elemento = elemento.text
                for palavra in palavras_chave:
                    resultados[palavra] += conteudo_elemento.count(palavra)

        except NoSuchElementException:
            break

        # Avança para a proxima página
        proxima_pagina = navegador.find_elements(By.XPATH, '/html/body/main/form/div[1]/div[2]/div/div[2]/div/ul/li[6]')
            
        if len(proxima_pagina) == 0 or "disable" in proxima_pagina[0].get_attribute("class"):
            break

        proxima_pagina[0].click()

    # navegador.quit()

    # Atualizar a exibição dos resultados na página
    resultados = {palavra: int(quantidade) for palavra, quantidade in resultados.items()}
    total_palavras = sum(resultados.values())
    
    return render_template('index.html', resultados=resultados, total_palavras=total_palavras)


    @app.route('/', methods=['GET', 'POST'])
    def exibir_resultados():
        global palavras_chave, resultados
        palavras_chave = ["TESTE", "TOTAL EXP", "AG AMINTAS", "JAD", "TRANSPORTADORA", "ESM", "BIT HOME", "RETIRA", "LATAM"]
        if request.method == 'POST':
            usuario = request.form['usuario']
            senha = request.form['senha']
       
            return contar_palavras_chave(usuario, senha)

        total_palavras = sum(resultados.values())
        
        return render_template('index.html', resultados=resultados, total_palavras=total_palavras)


if __name__ == '__main__':
    app.run()
import time
from flask import Flask, render_template
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
import os

app = Flask(__name__, template_folder=os.path.abspath('templates'))

servico = Service(ChromeDriverManager().install())

def contar_palavras_chave():
    global resultados, palavras_chave  # usar as variáveis globais
    resultados = {} # dicionario vazio, usado para armnazenar as contagem das palavras_chave

    opcoes = Options()
    opcoes.headless = True  # sendo True execulta navegador em modo off
    navegador = webdriver.Chrome(service=servico, options=opcoes)

    navegador.get("https://amplo.eship.com.br/")
    navegador.find_element(By.XPATH, '//*[@id="login"]').send_keys("dashboard3")
    navegador.find_element(By.XPATH, '//*[@id="senha"]').send_keys("12341234")
    navegador.find_element(By.XPATH, '//*[@id="Entrar"]/span').click()
    time.sleep(3)
    print("Buscando...")

    # Abre para listar 100 remessas
    navegador.find_element(By.XPATH, '//*[@id="FormListarRemessas"]/ul/li[2]/div/a[3]/div').click()

    for palavra in palavras_chave: # Um loop for é iniciado para percorrer todas as palavras-chave na lista palavras_chave
        resultados[palavra] = 0 # Para cada palavra-chave, uma entrada correspondente é adicionada ao dicionário resultados
    print("passou for...")

    while True: # É iniciado um loop while True, que continua indefinidamente até ser interrompido
        try:
            # Dentro do loop, o navegador encontra o elementos avnaçar paginana página com o XPath 
            elementos = navegador.find_elements(By.XPATH, '//*[@id="main_principal"]') 
            time.sleep(4)
            for elemento in elementos: #Para cada elemento encontrado, seu conteúdo de texto é extraído e armazenado na variável conteudo_elemento
                conteudo_elemento = elemento.text
                
                # Para cada palavra-chave, a função count() é usada para contar o número de ocorrências da palavra-chave no conteúdo do elemento atual,
                # e o resultado é adicionado à contagem existente no dicionário resultados(linha 34).
                for palavra in palavras_chave: 
                    resultados[palavra] = resultados.get(palavra, 0) + conteudo_elemento.count(palavra)
        except NoSuchElementException: #Se ocorrer uma exceção do tipo NoSuchElementException, o loop é interrompido usando o comando break.
            break

        print("passou While except...")
        proxima_pagina = navegador.find_elements(By.XPATH, '/html/body/main/form/div[1]/div[2]/div/div[2]/div/ul/li[6]')
        time.sleep(3)

        # Se não houver elementos de próxima página 
        # ou se o atributo "class" do primeiro elemento indicar "disable", o loop é interrompido usando break.
        if len(proxima_pagina) == 0 or "disable" in proxima_pagina[0].get_attribute("class"):
            break
        print("passou if...")
        proxima_pagina[0].click() # O primeiro elemento da lista proxima_pagina é clicado.

    # Após sair do loop, a função atualiza a exibição dos resultados convertendo os valores do dicionário resultados 
    # para inteiros e armazenando o resultado em resultados. 
    # Além disso, a função calcula a soma total das contagens das palavras-chave e a armazena em total_palavras.
    resultados = {palavra: int(quantidade) for palavra, quantidade in resultados.items()}
    total_palavras = sum(resultados.values())

    # Por fim, a função retorna os valores resultados e total_palavras
    return resultados, total_palavras

@app.route('/')
def exibir_resultados():
    global palavras_chave, resultados  # variavel global, usando as variais da primeira função. 
    palavras_chave = ["TESTE", "BLING", "AMPLO", "DATO", "TOTAL EXP", "AG AMINTAS", "JAD", "TRANSPORTADORA", "ESM", "LATAM", "BIT HOME", "RETIRA"]

    resultados, total_palavras = contar_palavras_chave() # Chamando a função contar_palavras_chaves da linha 15

    return render_template('index.html', resultados=resultados, total_palavras=total_palavras)

if __name__ == '__main__':
    app.run(debug=True)
    # A condição if __name__ == '__main__': verifica se o módulo está sendo executado diretamente
    # (ou seja, não foi importado como um módulo em outro lugar).
    # Se for o caso, o aplicativo Flask é executado em modo de depuração (debug=True). 
    # Isso geralmente é usado para facilitar o desenvolvimento e depuração de um aplicativo web Flask.

import time #teste
import os
from flask import Flask, render_template, request, redirect, url_for
from markupsafe import Markup
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
import concurrent.futures

'''
versão 1.2 = tela de login, tela de espera (teste ) 
'''

app = Flask(__name__)

nome_correto = "amplo"
senha_correta = "3033"  # Senha correta
palavras_chave = [] 

@app.route('/')
def login():
    return render_template('login.html', mensagem_erro="")

@app.route('/verificar_senha', methods=['POST'])
def verificar_senha():
    nome_inserido = request.form['nome']
    senha_inserida = request.form['senha']
    
    if nome_inserido == nome_correto and senha_inserida == senha_correta:
        # Nome e senha corretos, redirecionar para a página principal ou outra rota
        return redirect(url_for('login_passou'))
    else:
        # Nome ou senha incorretos, exibir uma mensagem de erro
        mensagem_erro = "Nome ou senha incorretos. Tente novamente."
        return render_template('login.html', mensagem_erro=mensagem_erro)
    
@app.route('/login_passou')
def login_passou(): 
    # Adiciona estilos embutidos para estilizar a mensagem
    estilos = '<style>.conteudo-gerado { font-size: 50px; color: blue; }</style>'
    
    # Renderiza o template e envia a página para o cliente
    rendered_template = render_template('gerando_dados.html')
    
    # Adiciona estilos e script JavaScript ao HTML
    rendered_template = Markup(estilos + rendered_template)
    script = Markup('<script>setTimeout(function() { window.location.href = "/executar_contar_palavras_chave"; }, 1000);</script>')
    rendered_template += script
    
    return rendered_template

def aguardar_elemento_xpath(driver, xpath, tempo_limite=10):
    try:
        elemento = WebDriverWait(driver, tempo_limite).until(
            EC.presence_of_element_located((By.XPATH, xpath))
        )
        return elemento
    except:
        raise Exception(f"Elemento XPath {xpath} não encontrado após {tempo_limite} segundos")


def contar_palavras_chave_async():
    print('... Iniciando código ...')
    global resultados, palavras_chave  # usar as variáveis globais
    resultados = {}



    ########################################################################## 
    servico = Service(ChromeDriverManager().install())

    opcoes = Options()
    opcoes.headless = True  # modo off ou não
    navegador = webdriver.Chrome(service=servico, options=opcoes)
    ##########################################################################

    # para rodar no replit usar essas configuraçõa
    # options = Options()
    # options.add_argument("--no-sandbox")
    # options.add_argument("--disable-dev-shm-usage")
    # options.headless = True  # Executar o Chrome de forma oculta

    # print('Antes de iniciar o WebDriver')
    # navegador = webdriver.Chrome(options=options)
    # print('Após iniciar o WebDriver')
    #############################################################################

    print('... Logando ...')
    navegador.get("https://amplo.eship.com.br/")
    aguardar_elemento_xpath(navegador, '//*[@id="login"]', tempo_limite=10).send_keys("dato@amplologistica.com.br")
    aguardar_elemento_xpath(navegador, '//*[@id="senha"]', tempo_limite=10).send_keys("D@sh4123")
    aguardar_elemento_xpath(navegador, '//*[@id="Entrar"]/span', tempo_limite=10).click()

    aguardar_elemento_xpath(navegador, '//*[@id="FormListarOrdem"]/ul/li[2]/div/a[3]/div').click()


    print('... Abriu lista para 100... e iniciando FOR ...')
    time.sleep(5)
    for palavra in palavras_chave:
        resultados[palavra] = 0
   
    while True:
        try:
            aguardar_elemento_xpath(navegador, '//*[@id="FormListarOrdem"]')
            elementos = navegador.find_elements(By.XPATH, '//*[@id="FormListarOrdem"]')
            
            for elemento in elementos:
                conteudo_elemento = elemento.text
                for palavra in palavras_chave:
                    resultados[palavra] += conteudo_elemento.count(palavra)
        except NoSuchElementException:
            print("... While except ...")
            break
            
        print('... Proxima página ...')
    # Substitua time.sleep(5) por aguardar_elemento_xpath(navegador, 'XPath do elemento', tempo_limite)
        proxima_pagina = aguardar_elemento_xpath(navegador, '/html/body/main/form/div[1]/div[2]/div/div[2]/div/ul/li[6]', tempo_limite=10)
    
        # Correção aqui: remova o uso de len() e ajuste a condição
        if not proxima_pagina or "disable" in proxima_pagina.get_attribute("class"):
            print("... Len DISABLE ...")
            break
        proxima_pagina[0].click()


    # Atualizar a exibição dos resultados na página
    resultados = {palavra: int(quantidade) for palavra, quantidade in resultados.items()}
    total_palavras = sum(resultados.values())
    print('... Exuibindo resultado (função contar_palavras_chaves_sync)...')

    return resultados, total_palavras

@app.route('/executar_contar_palavras_chave')
def executar_contar_palavras_chave():
    global palavras_chave, resultados  # usar as variáveis globais
    with concurrent.futures.ThreadPoolExecutor() as executor:
        resultados, total_palavras = contar_palavras_chave_async()
        palavras_chave = ["TOTAL EXP",
                    "FM",
                    "DATO TESTE",
                    "AG AMINTAS",
                    "AG LAMENHA",
                    "OLIST RETIRA",
                    "AG ANGELO",
                    "ENTREGA OSVALDO",
                    "JAD",
                    "ESM",
                    "LATAM",
                    "AZUL",
                    "GOL",
                    "ANDREIA SSA",
                    "BIT HOME",
                    "RETIRA",
                    "BLING",
                    "SUBWAY - AMPLO",
                    "BRASPRESS",
                    "MULHERES",
                    "RODONAVES",
                    "PAULISTANA",
                    "ADW",
                    "TECMAR",
                    "MAEX",
                    "BEMOL",
                    "DESTAK",
                    "AVANCE",
                    "DOMINIO",
                    "EBTRANS",
                    "RAFAEL BERNAL",
                    "RODOVIASUL",
                    "URANOLOG",
                    "RODOVITOR",
                    "TRANSPO-ALMENARA",
                    "LOGGI",
                    "AGF XAXIM",
                    "AMAZON",
                    ]
        
    resultados, total_palavras = contar_palavras_chave_async()
    # Remover palavras-chave com valor zero
    palavras_chave = [palavra for palavra in palavras_chave if resultados.get(palavra, 0) != 0]
    resultados = {palavra: quantidade for palavra, quantidade in resultados.items() if quantidade != 0}
    return render_template('index.html', resultados=resultados, total_palavras=total_palavras) 


if __name__ == '__main__':
  app.run(host="0.0.0.0", port=9090)
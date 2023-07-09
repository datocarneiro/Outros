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
from selenium.common.exceptions import StaleElementReferenceException

# Configuração das opções do Chrome

# Executar em modo headless (sem abrir janela do navegador)
servico = Service(ChromeDriverManager().install()) # atualizar versão do selenium automaticamente
opcoes = Options()
opcoes.add_argument("--headless")    

'''
# habilitar se quiser visualizar as ações na tela 
servico = Service(ChromeDriverManager().install()) # atualizar o selenium automaticamente oara a ultima versão
'''

# Obter o caminho absoluto do diretório atual
diretorio_atual = os.path.dirname(os.path.abspath(__file__))

while True:
    # modo de execução
    navegador = webdriver.Chrome(service=servico, options=opcoes) # habilitar comando para execultar em modo off, ver linha 16
    # navegador = webdriver.Chrome(service=servico) # habilitar comando para visualizar a tela, ver linha 23

    # Criar uma instância do WebDriver e acessar a página de login
    navegador.get("https://amplo.eship.com.br/")
    navegador.find_element(By.XPATH, '//*[@id="login"]').send_keys("dashboard3")
    navegador.find_element(By.XPATH, '//*[@id="senha"]').send_keys("12341234")
    navegador.find_element(By.XPATH, '//*[@id="Entrar"]/span').click()

    # Aguardar o carregamento da página
    time.sleep(5)

    # Abrir visualização para lista de 100
    navegador.find_element(By.XPATH, '//*[@id="FormListarRemessas"]/ul/li[2]/div/a[3]/div').click()
    time.sleep(1)

    # Palavras-chave a serem contadas
    palavras_chave = ["TOTAL EXP", "AG AMINTAS", "JAD", "TRANSPORTADORA"]
    contador_palavras_chave = {palavra: 0 for palavra in palavras_chave}

    while True:
        try:
            # Obter elementos com a soma das palavras-chave
            elementos = navegador.find_elements(By.XPATH, '//*[@id="main_principal"]')

            time.sleep(4)
            # Contagem das palavras-chave nos elementos da página atual
            for elemento in elementos:
                conteudo_elemento = elemento.text
                for palavra in palavras_chave:
                    contador_palavras_chave[palavra] += conteudo_elemento.count(palavra)

        except NoSuchElementException:
            # XPath não corresponde a nenhum elemento na página
            break

        proxima_pagina = navegador.find_elements(By.XPATH, '/html/body/main/form/div[1]/div[2]/div/div[2]/div/ul/li[6]')

        if len(proxima_pagina) == 0 or "disable" in proxima_pagina[0].get_attribute("class"):
            break  # Não há próxima página, sair do loop

        # Ir para a próxima página
        proxima_pagina[0].click()

    # Preencher os resultados no arquivo HTML

    resultado_html = ""
    for palavra, contador in contador_palavras_chave.items():
        resultado_html += f"""
            <tr>
                <td>{palavra}</td>
                <td>{contador}</td>
            </tr>
        """
    navegador = webdriver.Chrome(service=servico) # abrir o navegador para apresentar o resultado
    with open(os.path.join(diretorio_atual, "resultado.html"), "r") as arquivo:
        html = arquivo.read()

    # Inserir os resultados no arquivo HTML
    html = html.replace("<!-- Os resultados das palavras-chave serão preenchidos aqui -->", resultado_html)

    with open(os.path.join(diretorio_atual, "resultado.html"), "w") as arquivo:
        arquivo.write(html)

    # Abrir o arquivo no navegador
    navegador.get("file://" + os.path.join(diretorio_atual, "resultado.html"))

    # Fechar o navegador
    # navegador.quit()

    # Aguardar antes de repetir o ciclo
    time.sleep(30)
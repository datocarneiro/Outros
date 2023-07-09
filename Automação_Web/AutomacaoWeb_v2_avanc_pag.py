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

'''
# Executar em modo headless (sem abrir janela do navegador)
servico = Service(ChromeDriverManager().install()) # atualizar versão do selenium automaticamente
opcoes = Options()
opcoes.add_argument("--headless")    
navegador = webdriver.Chrome(service=servico, options=opcoes) 
'''

# habilitar se quiser visualizar as ações na tela 
servico = Service(ChromeDriverManager().install())
navegador = webdriver.Chrome(service=servico) # caso não funcione habilitar esse comando para atualizar o webdrive 

while True:
    # Criar uma instância do WebDriver
    # Acessar a página de login
    navegador.get("https://amplo.eship.com.br/")
    navegador.find_element(By.XPATH, '//*[@id="login"]').send_keys("dashboard3")
    navegador.find_element(By.XPATH, '//*[@id="senha"]').send_keys("12341234")
    navegador.find_element(By.XPATH, '//*[@id="Entrar"]/span').click()

    # Aguardar o carregamento da página
    time.sleep(5)

    # Abrir visualização para lista de 100
    navegador.find_element(By.XPATH, '//*[@id="FormListarRemessas"]/ul/li[2]/div/a[3]/div').click()
    time.sleep(5)

    # Palavras-chave a serem contadas
    palavras_chave = ["TOTAL EXP", "AG AMINTAS", "JAD", "TRANSPORTADORA"]
    contador_palavras_chave = {palavra: 0 for palavra in palavras_chave}

    while True:
        try:
            # Obter elementos com a soma das palavras-chave
            elementos = navegador.find_elements(By.XPATH, '//*[@id="main_principal"]') 
            #//*[@id="FormListarRemessas"]/table
            #//*[@id="FormListarRemessas"]
            #//*[@id="main_principal"]

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

    # Exibir resultados
    for palavra, contador in contador_palavras_chave.items():
        print(f"'{palavra}' {contador} envios pendentes.")

    # Fechar o navegador
    navegador.quit()

    # Aguardar antes de repetir o ciclo
    time.sleep(30)
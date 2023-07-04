'''
Certifique-se de ter instalado a biblioteca msedge-selenium-tools usando o comando 
pip install selenium
pip install msedge-selenium-tools
Lembre-se de substituir as configurações usuario, senha, url_login e arquivo_saida pelo seu próprio nome de usuário, senha,
 URL de login e nome de arquivo desejado.
O código acima usará o navegador Edge para fazer o download do relatório a cada 30 minutos.
 Certifique-se de ter configurado corretamente o Microsoft Edge WebDriver no seu ambiente.
'''


import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from msedge.selenium_tools import EdgeOptions, Edge

# Configurações iniciais
usuario = "dashboard3"
senha = "12341234"
url_login = "https://amplo.eship.com.br"
arquivo_saida = "dashexp.xlsx"

# Função para fazer o download do relatório

def baixar_relatorio():
    driver_options = EdgeOptions()
    driver_options.use_chromium = True
    
    driver = Edge(options=driver_options)
    
    driver.get(url_login)
    
    # Preencher campos de login
    campo_usuario = driver.find_element(By.ID, "campoUsuario")
    campo_senha = driver.find_element(By.ID, "campoSenha")
    campo_usuario.send_keys(usuario)
    campo_senha.send_keys(senha)
    
    # Fazer login
    botao_login = driver.find_element(By.ID, "btnEntrar")
    botao_login.click()
    
    time.sleep(5)  # Aguardar o login ser concluído
    
    # Clicar no botão "Exportar"
    botao_exportar = driver.find_element(By.ID, "cFuncaoListarRemessas_Exportar")
    botao_exportar.click()
    
    time.sleep(10)  # Aguardar o download ser concluído
    
    # Salvar o arquivo
    with open(arquivo_saida, "wb") as file:
        file.write(driver.page_source.encode("utf-8"))
    
    driver.quit()

# Loop principal
while True:
    baixar_relatorio()
    time.sleep(1800)  # Aguardar 30 minutos (em segundos) antes de baixar novamente

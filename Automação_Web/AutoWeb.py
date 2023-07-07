'''
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import service

servico = service(ChromeDriverManager().install())

navegador = webdriver.Chrome(service=servico)
'''
# selenium 4
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))

# Definir informações de login
usuario = "dashboard3"
senha = "12341234"

# Função para fazer o download do relatório
def fazer_download_relatorio():
    # Acessar o site
    driver.get("https://amplo.eship.com.br")

    # Preencher campos de usuário e senha
    input_usuario = driver.find_element_by_id("login")
    input_senha = driver.find_element_by_id("senha")
    input_usuario.send_keys("dashboard3")
    input_senha.send_keys("12341234")

    # Fazer login
    input_senha.send_keys(Keys.RETURN)

    # Aguardar o carregamento da página
    time.sleep(5)

    # Selecionar a codificação em ISO-8859-1
    select_codificacao = Select(driver.find_element_by_id("codificacao"))
    select_codificacao.select_by_value("ISO-8859-1")

    # Marcar os campos para exportação do serviço de transporte
    checkbox_servico_transporte = driver.find_element_by_id("servico_transporte")
    checkbox_servico_transporte.click()

    # Clicar no botão exportar
    botao_exportar = driver.find_element_by_id("exportar")
    botao_exportar.click()

    # Aguardar o download ser concluído
    time.sleep(10)

    # Fechar o navegador
    driver.quit()

# Executar a função de download do relatório a cada 30 minutos
while True:
    fazer_download_relatorio()
    time.sleep(1800)  # Esperar 30 minutos (1800 segundos) antes de realizar o próximo download


print(input("deseja sair:(s/n)"))
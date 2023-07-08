import time
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.select import Select

servico = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=servico)

driver.get("https://amplo.eship.com.br/")
driver.find_element(By.XPATH, '//*[@id="login"]').send_keys("dashboard3")
driver.find_element(By.XPATH, '//*[@id="senha"]').send_keys("12341234")
driver.find_element(By.XPATH, '//*[@id="Entrar"]/span').click()

# Aguardar o carregamento da página
time.sleep(5)

# Selecionar a codificação em ISO-8859-1
driver.find_element(By.XPATH, '//*[@id="formulario"]/div[1]/div[2]/div/div[1]/div/div/div[2]/div[2]/div[1]/div/div[2]/div[1]/div/div[2]/div[2]/label').click()

# Marcar os campos para exportação
driver.find_element(By.XPATH, '//*[@id="formulario"]/div[1]/div[2]/div/div[1]/div/div/div[2]/div[2]/div[1]/div/div[2]/div[2]/div/div[2]/div[6]/label').click()

# Clicar no botão exportar
driver.find_element(By.XPATH, '//*[@id="cFuncaoListarRemessas_Exportar"]/span').click()


# Aguardar o download ser concluído
time.sleep(30)

# Fechar o navegador
#driver.quit()
print(input("deseja sair:(s/n)"))

# Executar a função de download do relatório a cada 30 minutos
while True:
    # fazer_download_relatorio()
    time.sleep(1800)  # Esperar 30 minutos (1800 segundos) antes de realizar o próximo download

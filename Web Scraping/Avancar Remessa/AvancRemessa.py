'''
Para executar este código em outra máquina, você precisará ter os seguintes requisitos instalados:
Python, selenium, WebDrive_Manager
Imoportante, navegador google Chrome deve estar atualizado na ultima versão atual.
winget install Python
pip install selenium 
pip install webdriver_manager.
'''
import time
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options as ChromeOptions


# atualiza webdriver automaticamento
servico = Service(ChromeDriverManager().install())


while True:
    # Executar em modo headless (sem abrir janela do navegador)
    opcoes = Options()
    opcoes.add_argument("--headless")    
    navegador = webdriver.Chrome(service=servico, options=opcoes) 

    # habilitar se quiser visualizar as ações na tela 
    # navegador = webdriver.Chrome(options=opcoes) # habilitar comando para visualizar a tela, ver linha 23
  
    # DEFINA AS AÇÕES QUE SERÃO AUTOMATIZADAS 
    # Acessar a página de login
    navegador.get("https:.com.br/")
    navegador.find_element(By.XPATH, '//*[@id="login"]').send_keys("xxxxxxxx") # seu login
    navegador.find_element(By.XPATH, '//*[@id="senha"]').send_keys("xxxxxxxx") # sua senha
    navegador.find_element(By.XPATH, '//*[@id="Entrar"]/span').click()

    # Aguardar o carregamento da página
    time.sleep(5)

    # Abrir visualização para lista de 100
    navegador.find_element(By.XPATH, '//*[@id="FormListarRemessas"]/ul/li[2]/div/a[3]/div').click()
    time.sleep(10)

    # etapa conferidas
    navegador.find_element(By.XPATH, '//*[@id="formulario"]/div[1]/div[1]/ul/li/div[1]').click() # filtro
    time.sleep(10)
    
    # APLICAR filtros
    navegador.find_element(By.XPATH, '//*[@id="formulario"]/div[1]/div[1]/ul/li/div[2]/div/div[1]/div/div[2]/div/fieldset[1]/div/div/div[3]/div[2]/label').click() # conferido
    time.sleep(10)
    navegador.find_element(By.XPATH, '//*[@id="formulario"]/div[1]/div[1]/ul/li/div[2]/div/div[1]/div/div[2]/div/fieldset[1]/div/div/div[3]/div[3]/label').click() # Ag doc                          
    time.sleep(10)

    try:
        filtrar_button = navegador.find_element(By.XPATH, '//*[@id="cFuncaoListarRemessas_Filtrar"]/span')
        filtrar_button.click()
        time.sleep(7)
        
        check_box = navegador.find_element(By.XPATH, '//*[@id="FormListarRemessas"]/table/thead/tr/th[1]/div/label')
        check_box.click()
        time.sleep(3)
        
        avancar_button = navegador.find_element(By.XPATH, '//*[@id="cFuncaoListarRemessas_Avançar"]/span')
        avancar_button.click()
        time.sleep(7)
        
        confirmar_button = navegador.find_element(By.XPATH, '//*[@id="cFuncaoListarRemessas_CheckAvancarRemessa_Confirmar"]/span')
        confirmar_button.click()
        time.sleep(7)

    except NoSuchElementException:
        navegador.quit()  # Fechar o navegador
        time.sleep(180)
        continue  # Reiniciar o loop

    navegador.quit()  # Fechar o navegador

    time.sleep(180)
    continue  # Reiniciar o loop
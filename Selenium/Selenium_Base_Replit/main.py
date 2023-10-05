import time
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

############################################################################

# para rodar no replit usar essas configuraçõa
options = Options()
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.headless = False  # Executar o Chrome de forma oculta

driver = webdriver.Chrome(options=options)

#############################################################################
'''
# para rodar local usar essa configuração aqui
from webdriver_manager.chrome import ChromeDriverManager

servico = Service(ChromeDriverManager().install())

opcoes = Options()
opcoes.headless = True  # modo off ou não
driver = webdriver.Chrome(service=servico, options=opcoes)
'''
#############################################################################
driver.get("https://google.com.br/")
time.sleep(10)

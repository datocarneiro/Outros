Este código utiliza o Selenium para automatizar a interação com o navegador Chrome.
Para garantir seu funcionamento correto no ambiente do Replit,
é importante manter o executável "chromedriver" no mesmo diretório.


############################################################################

para rodar no replit usar essas configurações:

options = Options() 
options.add_argument("--no-sandbox") 
options.add_argument("--disable-dev-shm-usage")
options.headless = False # Executar o Chrome de forma oculta
driver = webdriver.Chrome(options=options)

#############################################################################

para rodar local usar essa configuração aqui:

from webdriver_manager.chrome import ChromeDriverManager
servico = Service(ChromeDriverManager().install())
opcoes = Options() 
opcoes.headless = True # modo off ou não 
driver = webdriver.Chrome(service=servico, options=opcoes)

############################################################################# 

05/10/2023, 20:48:18 - Dato






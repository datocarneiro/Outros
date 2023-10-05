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

navegador = webdriver.Chrome(options=options)
#############################################################################

# para rodar local usar essa configuração aqui 
from webdriver_manager.chrome import ChromeDriverManager
servico = Service(ChromeDriverManager().install())

opcoes = Options()
opcoes.headless = True  # modo off ou não
navegador = webdriver.Chrome(service=servico, options=opcoes)

#############################################################################


# Inicialização do aplicativo Flask
app = Flask(__name__)

def abrir_navegador():
    print('... Iniciando código ...')
    resultados = {}
    palavras_chave = []

    print('... Logando ...')
    navegador.get("https://amplo.eship.com.br/")
    print("... abriu página ...")
    time.sleep(15)
    print("... Logado ...")
    
    # Você pode realizar operações no navegador aqui

    # Feche o navegador quando terminar
    navegador.quit()

@app.route('/')
def index():
    abrir_navegador()
    return "Página inicial"

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080)
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from flask import Flask, render_template, request
from selenium.webdriver.common.by import By
import time
from selenium.common.exceptions import NoSuchElementException

app = Flask(__name__)

resultados = {}
palavras_chave = [
  "TESTE", "BLING", "AMPLO", "DATO", "TOTAL EXP", "AG AMINTAS", "JAD",
  "TRANSPORTADORA", "ESM", "LATAM", "BIT HOME", "RETIRA"
]

# Global variables to store login credentials
username = None
password = None


def contar_palavras_chave():
  global resultados, username, password

  print('iniciando - ciclo.........')
  options = Options()
  options.add_argument("--no-sandbox")
  options.add_argument("--disable-dev-shm-usage")
  options.headless = True  # Executar o Chrome de forma oculta
  navegador = webdriver.Chrome(options=options)
  navegador.execute_script("document.body.style.zoom = '25%'")
  navegador.get("https://amplo.eship.com.br/")
  time.sleep(15)

  # Use the stored login credentials
  navegador.find_element(By.XPATH, '//*[@id="login"]').send_keys(username)
  time.sleep(3)
  navegador.find_element(By.XPATH, '//*[@id="senha"]').send_keys(password)
  time.sleep(3)
  navegador.find_element(By.XPATH, '//*[@id="Entrar"]/span').click()
  print("logando - sleep 5...")
  time.sleep(7)

  navegador.find_element(
    By.XPATH, '//*[@id="FormListarRemessas"]/ul/li[2]/div/a[3]/div').click()
  print('lista de 100... sleep 3')
  time.sleep(15)

  for palavra in palavras_chave:
    resultados[palavra] = 0
  print("passou for...")

  while True:
    try:
      print('loop while true ...... ')
      elementos = navegador.find_elements(By.XPATH,
                                          '//*[@id="main_principal"]')
      time.sleep(15)
      for elemento in elementos:
        conteudo_elemento = elemento.text
        for palavra in palavras_chave:
          resultados[palavra] += conteudo_elemento.count(palavra)
          print('elemento MAIN PRINCIPAL = TRY')
    except NoSuchElementException:
      break
    print("elemento MAIN PRINCIPAL = EXCEPT...")

    proxima_pagina = navegador.find_elements(
      By.XPATH, '/html/body/main/form/div[1]/div[2]/div/div[2]/div/ul/li[6]')
    print('Avançando pagina...sleep 3')
    time.sleep(15)

    if len(proxima_pagina
           ) == 0 or "disable" in proxima_pagina[0].get_attribute("class"):
      break
      print("avançar = DISABLE...")
    proxima_pagina[0].click()

  print('ATUALIZANDO RESULTADOS')
  resultados = {
    palavra: int(quantidade)
    for palavra, quantidade in resultados.items()
  }
  total_palavras = sum(resultados.values())

  navegador.quit()
  print('RESULTADOS RUN....')
  return resultados, total_palavras

@app.route('/', methods=['GET', 'POST'])
def exibir_resultados():
  global resultados, username, password

  # Handle form submission
  if request.method == 'POST':
    username = request.form['username']
    password = request.form['password']

  # Check if login credentials are available
  if not username or not password:
    return render_template('index.html')

  resultados, total_palavras = contar_palavras_chave()

  palavras_chave_atualizadas = [
    palavra for palavra in palavras_chave if resultados.get(palavra, 0) != 0
  ]
  resultados_atualizados = {
    palavra: quantidade
    for palavra, quantidade in resultados.items() if quantidade != 0
  }

  return render_template('results.html',
                         resultados=resultados_atualizados,
                         total_palavras=total_palavras)


if __name__ == '__main__':
  app.run(host='0.0.0.0', port=80)

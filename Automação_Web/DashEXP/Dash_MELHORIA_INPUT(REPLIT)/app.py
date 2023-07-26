from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from flask import Flask, render_template
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import time

app = Flask(__name__)

resultados = {}
palavras_chave = [
  "TESTE", "BLING", "AMPLO", "DATO", "TOTAL EXP", "AG AMINTAS", "JAD",
  "TRANSPORTADORA", "ESM", "LATAM", "BIT HOME", "RETIRA"
]


def contar_palavras_chave():
  global resultados
  print('iniciando - ciclo.........')
  options = Options()
  options.add_argument("--no-sandbox")
  options.add_argument("--disable-dev-shm-usage")
  webdriver_service = Service(ChromeDriverManager().install())
  navegador = webdriver.Chrome(service=webdriver_service, options=options)
  navegador.get("https://amplo.eship.com.br/")
  time.sleep(15)

  navegador.find_element(By.XPATH, '//*[@id="login"]').send_keys("dashboard3")
  time.sleep(3)
  navegador.find_element(By.XPATH, '//*[@id="senha"]').send_keys("12341234")
  time.sleep(3)
  navegador.find_element(By.XPATH, '//*[@id="Entrar"]/span').click()
  print("logando - sleep 5...")
  time.sleep(7)

  navegador.find_element(
    By.XPATH, '//*[@id="FormListarRemessas"]/ul/li[2]/div/a[3]/div').click()
  print('lista de 100... sleep 3')
  time.sleep(10)
  for palavra in palavras_chave:
    resultados[palavra] = 0
  print("passou for...")

  while True:
    try:
      print('loop while true ...... ')
      elementos = navegador.find_elements(By.XPATH,
                                          '//*[@id="main_principal"]')
      time.sleep(5)
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
    time.sleep(10)

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


@app.route('/')
def exibir_resultados():
  global resultados
  resultados, total_palavras = contar_palavras_chave()

  palavras_chave_atualizadas = [
    palavra for palavra in palavras_chave if resultados.get(palavra, 0) != 0
  ]
  resultados_atualizados = {
    palavra: quantidade
    for palavra, quantidade in resultados.items() if quantidade != 0
  }

  return render_template('index.html',
                         resultados=resultados_atualizados,
                         total_palavras=total_palavras)


if __name__ == '__main__':
  app.run(host='0.0.0.0', port=8080)

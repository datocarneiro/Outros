from flask import Flask, render_template, request, jsonify
import datetime
import json
import os

app = Flask(__name__)

# Caminho para o arquivo de dados
DATA_FILE_PATH = 'reservas_data.txt'


# Função para carregar os dados de reservas do arquivo (se existir)
def load_reservas():
  if os.path.exists(DATA_FILE_PATH):
    with open(DATA_FILE_PATH, 'r') as file:
      return json.load(file)
  return {}


# Carregar os dados de reservas na inicialização do aplicativo
reservas = load_reservas()


def generate_dates():
  start_date = datetime.date(2023, 7, 31)
  end_date = datetime.date(2023, 8, 10)
  dates = []
  current_date = start_date
  while current_date <= end_date:
    dates.append(
        current_date.strftime("%d/%m/%Y"))  # Modifique o formato da data aqui
    current_date += datetime.timedelta(days=1)
  return dates


def save_reservas():
  # Criar um novo dicionário para armazenar as datas formatadas
  reservas_formatted = {}
  for data_reserva, reserva_info in reservas.items():
    # Converter a data de "dd/mm/aaaa" para "aaaa-mm-dd" antes de salvar
    data_reserva_formatted = datetime.datetime.strptime(
        data_reserva, '%d/%m/%Y').strftime('%Y-%m-%d')
    reservas_formatted[data_reserva_formatted] = reserva_info

  # Salvar os dados de reservas formatados no arquivo
  with open(DATA_FILE_PATH, 'w') as file:
    json.dump(reservas_formatted, file)


def sort_reservas_by_date(reservas):
  return dict(sorted(reservas.items()))


def find_reserva_by_date(data_reserva):
  return reservas.get(data_reserva)


@app.context_processor
def utility_processor():

  def formatDate(dateString):
    date = datetime.datetime.strptime(dateString, '%Y-%m-%d')
    return date.strftime('%d/%m/%Y')

  return dict(formatDate=formatDate)


@app.route('/', methods=['GET', 'POST'])
def index():
  if request.method == 'POST':
    # Restante do código...

    # Salvar os dados de reservas no arquivo
    save_reservas()

    # Retornar uma resposta JSON para a solicitação POST
    return jsonify({'success': True})

  dates = generate_dates()

  # Modificar a linha abaixo para ordenar as reservas por data
  sorted_reservas = sort_reservas_by_date(reservas)

  # Formatando as datas antes de exibir as reservas
  formatted_reservas = {
      formatDate(dateString): reserva_info
      for dateString, reserva_info in sorted_reservas.items()
  }

  # Retornar a resposta renderizada para a solicitação GET
  return render_template('index.html',
                         dates=dates,
                         reservas=formatted_reservas)


if __name__ == '__main__':
  # Carregar os dados de reservas do arquivo antes de iniciar o servidor Flask
  reservas = load_reservas()

  app.run(host='0.0.0.0', port=5050)

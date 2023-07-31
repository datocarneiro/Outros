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
        dates.append(current_date.strftime("%d/%m/%Y"))  # Modifique o formato da data aqui
        current_date += datetime.timedelta(days=1) 
    return dates


def save_reservas():
    with open(DATA_FILE_PATH, 'w') as file:
        json.dump(reservas, file)


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
        nome = request.form['nome']
        data_reserva = request.form['data_reserva']
        periodo = request.form['periodo']

        reserva = find_reserva_by_date(data_reserva)
        if reserva:
            # If the reservation already exists, update the existing reservation
            reserva['nome'] = nome
            reserva['periodo'] = periodo
        else:
            # If the reservation does not exist, add a new one
            reservas[data_reserva] = {'nome': nome, 'periodo': periodo}

        # Salvar os dados de reservas no arquivo
        save_reservas()

        return jsonify({'success': True})

    dates = generate_dates()

    # Modifique a linha abaixo para ordenar as reservas por data
    sorted_reservas = sort_reservas_by_date(reservas)

    return render_template('index.html', dates=dates, reservas=sorted_reservas)


if __name__ == '__main__':
    # Carregar os dados de reservas do arquivo antes de iniciar o servidor Flask
    reservas = load_reservas()
    
    app.run(host='0.0.0.0', port=5050)
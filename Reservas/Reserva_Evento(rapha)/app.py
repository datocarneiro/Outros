from flask import Flask, render_template, request, jsonify
import datetime
import os
import json

app = Flask(__name__)

# Caminho para o arquivo de dados
DATA_FILE_PATH = 'dados.txt'


# Função para carregar os dados de reservas do arquivo (se existir)
def load_reservas():
    if os.path.exists(DATA_FILE_PATH):
        with open(DATA_FILE_PATH, 'r') as file:
            return json.load(file)
    return {}


# Função para salvar os dados de reservas no arquivo
def save_reservas(reservas):
    # Salvar os dados de reservas no arquivo
    with open(DATA_FILE_PATH, 'w') as file:
        json.dump(reservas, file)


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


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        data_reserva = request.form['data_reserva']
        reserva_info = request.form['reserva_info']

        # Carregar as reservas existentes
        reservas = load_reservas()

        # Check if the selected date already exists in the data
        if data_reserva in reservas:
            return jsonify({'success': False, 'message': 'A reserva para essa data já foi cadastrada!'})

        # Adicionar a nova reserva
        reservas[data_reserva] = reserva_info

        # Salvar as reservas atualizadas
        save_reservas(reservas)

        # Retornar uma resposta JSON para a solicitação POST
        return jsonify({'success': True, 'reservas': reservas})

    dates = generate_dates()

    # Carregar as reservas existentes
    reservas = load_reservas()

    # Retornar a resposta renderizada para a solicitação GET
    return render_template('index.html',
                           dates=dates,
                           reservas=reservas)


@app.route('/delete', methods=['POST'])
def delete_reserva():
    if request.method == 'POST':
        data_reserva = request.form['data_reserva']

        # Carregar as reservas existentes
        reservas = load_reservas()

        # Remover a reserva com base na data_reserva
        if data_reserva in reservas:
            del reservas[data_reserva]

            # Salvar as reservas atualizadas
            save_reservas(reservas)

            # Retornar uma resposta JSON para a solicitação POST
            return jsonify({'success': True, 'reservas': reservas})
        else:
            return jsonify({'success': False, 'message': 'A reserva para essa data não foi encontrada!'})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5050)
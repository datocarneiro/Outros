from flask import Flask, render_template, request, jsonify
import datetime
import os
import json

app = Flask(__name__)

# Caminho para o arquivo de dados
DATA_FILE_PATH = 'dados.txt'

def load_reservas():
    if os.path.exists(DATA_FILE_PATH):
        with open(DATA_FILE_PATH, 'r') as file:
            return json.load(file)
    return {}

def save_reservas(reservas):
    with open(DATA_FILE_PATH, 'w') as file:
        json.dump(reservas, file, indent=4)

def generate_dates():
    start_date = datetime.date(2023, 7, 31)
    end_date = datetime.date(2023, 8, 10)
    dates = []
    current_date = start_date
    while current_date <= end_date:
        dates.append({
            'date': current_date.strftime("%d/%m/%Y"),
            'periodos': ['MANHÃ', 'NOITE']
        })
        current_date += datetime.timedelta(days=1)
    return dates

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        data_reserva = request.form['data_reserva']
        reserva_info = request.form['reserva_info']
        periodo = request.form['periodo']

        reservas = load_reservas()

        if data_reserva not in reservas:
            reservas[data_reserva] = {'MANHÃ': None, 'NOITE': None}
        if not reservas[data_reserva][periodo]:
            reservas[data_reserva][periodo] = reserva_info
            save_reservas(reservas)
            return jsonify({'success': True, 'reservas': reservas})

        return jsonify({'success': False, 'message': 'A reserva para essa data e período já foi cadastrada!'})

    dates = generate_dates()

    reservas = load_reservas()
    for date in dates:
        date_str = date['date']
        if date_str not in reservas:
            reservas[date_str] = {'MANHÃ': None, 'NOITE': None}

    save_reservas(reservas)

    return render_template('index.html', dates=dates, reservas=reservas)

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

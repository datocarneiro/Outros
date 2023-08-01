from flask import Flask, render_template, request, jsonify
import datetime
import json
import os

app = Flask(__name__)

# Get the directory path of the current script
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Caminho para o arquivo de dados
DATA_FILE_PATH = os.path.join(BASE_DIR, 'reservas_data.txt')


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
    # Carregar as reservas existentes
    reservas = load_reservas()

    # Se não houver reservas, definir uma data inicial e final padrão
    if not reservas:
        start_date = datetime.date(2023, 7, 31)
        end_date = datetime.date(2023, 8, 10)
    else:
        # Verificar o formato das datas e convertê-las para o formato correto (DD/MM/YYYY)
        dates = []
        keys_to_modify = []  # Criar uma lista para armazenar as chaves que precisam ser modificadas
        for date_str in reservas.keys():
            try:
                date_obj = datetime.datetime.strptime(date_str, "%d/%m/%Y").date()
            except ValueError:
                # Se a data não estiver no formato correto, tentar converter para o formato 'YYYY-MM-DD'
                date_obj = datetime.datetime.strptime(date_str, "%Y-%m-%d").date()
                keys_to_modify.append(date_str)  # Adicionar a chave à lista

            dates.append(date_obj)

        for key in keys_to_modify:
            date_obj = datetime.datetime.strptime(key, "%Y-%m-%d").date()
            reservas[date_obj.strftime("%d/%m/%Y")] = reservas.pop(key)

        start_date = min(dates)
        end_date = max(dates)

    # Gerar as datas dentro do intervalo (30 dias a partir da data mais recente ou da data atual)
    current_date = max(end_date, datetime.date.today())
    end_date = current_date + datetime.timedelta(days=30)

    dates = []
    while current_date <= end_date:
        dates.append(current_date.strftime("%d/%m/%Y"))  # Modifique o formato da data aqui
        current_date += datetime.timedelta(days=1)
    return dates


def find_reserva_by_date(data_reserva, reservas):
    return reservas.get(data_reserva)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        nome = request.form['nome']
        data_reserva = request.form['data_reserva']
        periodo = request.form['periodo']

        # Carregar os dados de reservas na inicialização do aplicativo
        reservas = load_reservas()

        reserva = find_reserva_by_date(data_reserva, reservas)

        # Check if the selected date already exists in the data
        if data_reserva in reservas:
            return jsonify({'success': False, 'message': 'A reserva para essa data já foi cadastrada!'})

        if reserva:
            # If the reservation already exists, update the existing reservation
            reserva['nome'] = nome
            reserva['periodo'] = periodo
        else:
            # If the reservation does not exist, add a new one
            reservas[data_reserva] = {'nome': nome, 'periodo': periodo}

        # Salvar os dados de reservas no arquivo
        save_reservas(reservas)

        return jsonify({'success': True})

    dates = generate_dates()

    # Carregar as reservas existentes
    reservas = load_reservas()

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

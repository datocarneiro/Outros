from flask import Flask, render_template, request
from twilio.rest import Client

# Configure o SID da sua conta e o token de autenticação do Twilio
# Preencha seu Account SID e Auth Token do Twilio no arquivo app.py (no campo "SEU_ACCOUNT_SID" e "SEU_AUTH_TOKEN").
account_sid = 'SEU_ACCOUNT_SID'
auth_token = 'SEU_AUTH_TOKEN'
client = Client(account_sid, auth_token)

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/send', methods=['POST'])
def send_message():
    groups = request.form.getlist('groups')
    message = request.form['message']

    for group in groups:
        # Substitua "seu_numero" pelo número do seu WhatsApp no formato: "whatsapp:+55XXXXXXXXX"
        client.messages.create(body=message, from_='whatsapp:seu_numero', to=f'whatsapp:{group}')

    return 'Mensagem enviada com sucesso!'

if __name__ == '__main__':
    app.run()

from flask import Flask, render_template, redirect, url_for, flash
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo
import sqlite3

app = Flask(__name__)
app.config['SECRET_KEY'] = 'teste'  # Use uma chave secreta forte em um ambiente de produção
DATABASE = 'users.db'

# Classe do formulário de registro
class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

# Classe do formulário de login
class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

# Criação da tabela de usuários no banco de dados (SQLite)
def create_users_table():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS users
                      (id INTEGER PRIMARY KEY AUTOINCREMENT,
                       username TEXT NOT NULL,
                       email TEXT NOT NULL,
                       password TEXT NOT NULL)''')
    conn.commit()
    conn.close()

# Rota para a página inicial
@app.route('/')
def home():
    return render_template('base.html')

# Rota para registro de novo usuário
@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        cursor.execute('INSERT INTO users (username, email, password) VALUES (?, ?, ?)',
                       (form.username.data, form.email.data, form.password.data))
        conn.commit()
        conn.close()
        flash('Registration successful. Please log in.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

# Rota para login de usuário
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE username=? AND password=?',
                       (form.username.data, form.password.data))
        user = cursor.fetchone()
        conn.close()
        if user:
            flash('Login successful.', 'success')
            return app.py
        else:
            flash('Login failed. Please check your username and password.', 'danger')
            return render_template('invalid.html')
    return render_template('login.html', form=form)

if __name__ == '__main__':
    create_users_table()
    app.run(debug=True)



from flask import Flask, render_template, redirect, url_for, request
from flask_login import LoginManager, UserMixin, login_user, login_required, current_user, logout_user
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)

login_manager = LoginManager(app)


class Usuario(UserMixin):
    def __init__(self, id, username, password, es_admin:bool):
        self.id = id
        self.username = username
        self.password = password
        self.es_admin = es_admin


class Perros(UserMixin):
    def __init__(self, id, nombre:str, edad:int, raza:str):
        self.id = id
        self.nombre = nombre
        self.edad = edad
        self.raza = raza


users_db = {
    'diana': Usuario(1, 'diana', '123', 1),
    'lina': Usuario(2, 'lina', '123', 0),
    'marcela': Usuario(3, 'marcela', '123', 0)
}


dogs_db = {
    1: Perros(1, 'Kira', 10, "Pitbull"),
    2: Perros(2, 'Keyla', 5, "Chihuahua"),
    3: Perros(3, 'Tokio', 3, "Pastor")
}


@login_manager.user_loader
def load_user(user_id):
    return next((user for user in users_db.values() if user.id == int(user_id)), None)



@app.route('/')
def home():
    return render_template("index.html")


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = users_db.get(username)
        if user and user.password == password:
            login_user(user)
            return redirect(url_for('rutalogueada'))

        return "Username or Password is invalid"

    return render_template("login.html")




@app.route('/rutalogueada')
@login_required
def rutalogueada():
    if current_user.es_admin == 1:

        return render_template("rutalogueada.html", username=current_user.username, users=users_db.values(), dogs=dogs_db.values())
    
    return render_template("rutalogueada.html", username=current_user.username)


@app.route('/logout')
@login_required
def logout():
    logout_user()  
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)

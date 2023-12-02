from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
import os
from pymongo import MongoClient
from bson import ObjectId
from datetime import datetime
from bson import DBRef
import base64
from flask_mail import Mail, Message
from flask_bcrypt import Bcrypt
from datetime import timedelta

app = Flask(__name__)
bcrypt = Bcrypt(app)
app.secret_key = "Utec"

client = MongoClient("mongodb+srv://alexanderastorga:parasyte2134@iot-cognitive.dvor5qx.mongodb.net/")
db = client['ProyectoCognitive']
user_collection = db['users']
sensors_collection = db['sensors']

global id_for_delete

@app.route('/login', methods=['POST', 'GET'])
def login():    
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        #user = user_collection.find_one({'username': username})
        user = user_collection.find_one({'username': username})
        datos = user_collection.find_one({'username': username}, {'_id': 0, 'username': 1, 'password': 1})
        
        if datos and username == datos.get('username') and password == datos.get('password'):
            session['logged_in'] = True
            session['username'] = user['username']
            flash('Bienvenido ' + user['name'])
            return redirect(url_for('clienteTabla'))
        else:
            flash('Usuario o contraseña incorrectos')

    return render_template('login.html')

@app.route("/")   
def clienteTabla():
    data = user_collection.find()
    return render_template("Usuarios.html", users=data)

@app.route("/createUser")   
def createUser():
    return render_template("createUser.html")

@app.route('/create', methods=['POST'])
def create():
    if request.method == 'POST':
        # Obtiene los datos del formulario
        name = request.form['name']
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']

        # Inserta los datos en la colección
        user_collection.insert_one({'name': name, 'username': username, 'password': password, 'email': email})

    return redirect(url_for('clienteTabla'))

@app.route('/update/<string:_id>', methods=['GET', 'POST'])
def update(_id):
    if request.method == 'GET':
        # Obtiene los datos del usuario a actualizar
        user = user_collection.find_one({'_id': _id})
        return render_template('update.html', user=user)

    if request.method == 'POST':
        # Obtiene los nuevos datos del formulario
        new_name = request.form['name']
        new_username = request.form['username']
        new_password = request.form['password']
        new_email = request.form['email']

        # Actualiza los datos en la colección
        user_collection.update_one({'_id': _id}, {'$set': {'name': new_name, 'username': new_username, 'password': new_password, 'email': new_email}})

        return redirect(url_for('index'))

@app.route('/borrar/<string:_id>')
def borrar(_id):
    data = user_collection.find_one({'_id': _id})
    id_for_delete = _id
    return render_template('delete.html', user = data)

@app.route('/delete',  methods = ['POST'])
def delete():
    # Elimina el usuario de la colección
    if request.method == 'POST':
        user_collection.delete_one({'_id': id_for_delete})
    return redirect(url_for('clienteTabla'))

@app.route("/Sensores")   
def vendedorGrafico():
    data = sensors_collection.find()
    return render_template("Sensores.html", sensors = data)

@app.route("/createSensor")   
def createSensor():
    return render_template("createSensor.html")

@app.route('/createS', methods=['POST'])
def createS():
    if request.method == 'POST':
        # Obtiene los datos del formulario
        sensor_id = request.form['sensor_id']
        description = request.form['description']
        location = request.form['location']
        enabled = request.form['enabled']
        type = request.form['type']
        value = request.form['value']

        # Inserta los datos en la colección
        sensors_collection.insert_one({'sensor_id': sensor_id, 'description': description, 'location': location, 'enabled': enabled, 'type': type, 'value': value})    

    return redirect(url_for('vendedorGrafico'))


@app.route("/password")
def password():
    return render_template("password.html")

@app.route("/register")
def register():
    return render_template("register.html")

@app.route('/registerdata', methods=['POST'])
def registerUser():
    if request.method == 'POST':
        # Obtiene los datos del formulario
        name = request.form['name']
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']

        # Inserta los datos en la colección
        user_collection.insert_one({'name': name, 'username': username, 'password': password, 'email': email})    

    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(port=7000, host="0.0.0.0", debug=True)

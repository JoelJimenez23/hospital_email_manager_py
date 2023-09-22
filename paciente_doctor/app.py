from flask import Flask,request,jsonify,abort
from flaskext.mysql import MySQL
from datetime import datetime
import os
import sys
import json
import subprocess
import uuid

app = Flask(__name__)
mysql = MySQL()

app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = '230204'
app.config['MYSQL_DATABASE_DB'] = 'cloud_project'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
app.config['MYSQL_DATABASE_PORT'] = 8005

mysql.init_app(app)

@app.route('/user',methods=['POST'])
def create_user():
    try:
        body = request.json

        connection = mysql.connect()
        cursor = connection.cursor()
        _name = body.get('name')
        _email = body.get('email')
        _password = body.get('password')
        _token = body.get('token')
        
        _uid = str(uuid.uuid4())

        insert_user_cmd = "INSERT INTO users(id,name,email,password,token) VALUES(%s,%s,%s,%s,%s)"
        cursor.execute(insert_user_cmd, (_uid, _name, _email, _password, _token))
        connection.commit()
        
        cursor.close()
        connection.close()

        return jsonify({"success":True,"message":_uid})
    except Exception as e:
        return jsonify({"succes":False,"message":str(e)})


@app.route('/user',methods=['GET'])
def show_user():
    try:
        connection = mysql.connect()
        cursor = connection.cursor()
        cursor.execute("select * from users")
        rows = cursor.fetchall()

        cursor.close()
        connection.close()
        return jsonify({"success":True,"message":rows})
    except Exception as e:
        return jsonify({"success":False,'message':str(e)})


@app.route('/paciente',methods=['POST'])
def create_paciente():
    try: 
        body = request.json

        connection = mysql.connect()
        cursor = connection.cursor()
        _id = body.get('dni')
        _name = body.get('name')
        _apellido = body.get('apellido')
        _email = body.get('email')
        _password = body.get('password')
        _token = body.get('token')

        insert_paciente_cmd = """INSERT INTO pacientes(id,name,apellido,email,password,token)
         VALUES(%s,%s,%s,%s,%s,%s)"""
        cursor.execute(insert_paciente_cmd,(_id, _name, _apellido, _email, _password, _token))
        connection.commit()

        cursor.close()
        connection.close()
        
        return jsonify({"success":True,"message":_id})
    except Exception as e:
        return jsonify({"success":False,"message":str(e)})

@app.route('/paciente',methods=["GET"])
def show_paciente():
    try:
        connection = mysql.connect()
        cursor = connection.cursor()
        cursor.execute("select * from pacientes")
        rows = cursor.fetchall()
        cursor.close()
        connection.close()
        return jsonify({"success":True,"pacientes":rows})
    except Exception as e:
        return jsonify({"success":False,"message":str(e)})


@app.route('/doctor',methods=['POST'])
def create_doctor():
    try: 
        body = request.json

        connection = mysql.connect()
        cursor = connection.cursor()
        _id = body.get('dni')
        _name = body.get('name')
        _apellido = body.get('apellido')
        _email = body.get('email')
        _password = body.get('password')
        _token = body.get('token')
        _codigo_doctor = body.get('codigo_doctor')
        _especialidad = body.get('especialidad')

        insert_doctor_cmd = """INSERT INTO doctores(id,name,apellido,email,password,token,codigo_doctor,especialidad)
         VALUES(%s,%s,%s,%s,%s,%s,%s,%s)"""
        cursor.execute(insert_doctor_cmd,(_id, _name, _apellido, _email, _password, _token, _codigo_doctor, _especialidad))
        connection.commit()

        cursor.close()
        connection.close()
        
        return jsonify({"success":True,"message":_id})
    except Exception as e:
        return jsonify({"success":False,"message":str(e)})




@app.route('/doctor',methods=["GET"])
def show_doctor():
    try:
        connection = mysql.connect()
        cursor = connection.cursor()
        cursor.execute("select * from doctores")
        rows = cursor.fetchall()
        cursor.close()
        connection.close()
        return jsonify({"success":True,"pacientes":rows})
    except Exception as e:
        return jsonify({"success":False,"message":str(e)})



if __name__ == "__main__":
    app.run(host='0.0.0.0',port=8000,debug=False)





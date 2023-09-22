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

admin_id = '73641477'

mysql.init_app(app)

@app.route('/cita',methods=['POST'])
def create_cita():
    try:
        body = request.json
        
        connection = mysql.connect()
        cursor = connection.cursor()

        _id_paciente = body.get('id_paciente')
        _id_doctor = body.get('id_doctor')
        _motivo = body.get('motivo')
        _year = body.get('year')
        _month = body.get('month')
        _day = body.get('day')
        _hour = body.get('hour')
        _minute = body.get('minute')

        date = datetime(int(_year),int(_month),int(_day),
                        int(_hour),int(_minute))
        date_str = date.isoformat()
        _uid = str(uuid.uuid4())
        
        insert_cita_cmd = """INSERT INTO cita(id,id_paciente,
        id_doctor,date,motivo) VALUES(%s,%s,%s,%s,%s)"""
        
        cursor.execute(insert_cita_cmd, (_uid,_id_paciente,
        _id_doctor,date_str,_motivo))
        connection.commit()

        cursor.execute('select email from doctores where id = %s',(_id_doctor,))
        doc_email = cursor.fetchone()[0]
        print("docmail ",doc_email)

        cursor.execute('select email from pacientes where id = %s',(_id_paciente,))
        paciente_email = cursor.fetchone()[0]
        print("pacientemail",paciente_email)

        cursor.close()
        connection.close()
        
        new_hour = str(int(_hour) - 1)


        url = "http://localhost:8015/email"  # Note the 'http://' prefix for the URL

        # Create Python dictionaries
        doc_data = {
            "id_sender": admin_id,
            "receiver": doc_email,
            "subject": "cita en consultorio",
            "message": "tiene cita con el estupido de su paciente",
            "year": _year,
            "month": _month,
            "day": _day,
            "hour": new_hour,
            "minute": _minute
        }

        pac_data = {
            "id_sender": admin_id,
            "receiver": paciente_email,
            "subject": "clinica barata",
            "message": "no olvidar que tiene cita en una hora con el doctor matasanos",
            "year": _year,
            "month": _month,
            "day": _day,
            "hour": new_hour,
            "minute": _minute
        }

        # Convert Python dictionaries to JSON strings
        json_doc = json.dumps(doc_data)
        json_pac = json.dumps(pac_data)

        # Print the JSON strings (for debugging)
        print(json_doc)
        print('\n')
        print(json_pac)

        # Send POST requests using curl
        subprocess.Popen(['curl', '-X', 'POST', '-H', 'Content-Type: application/json', '-d', json_doc, url])
        subprocess.Popen(['curl', '-X', 'POST', '-H', 'Content-Type: application/json', '-d', json_pac, url])

        # Rest of your code...


        return jsonify({"success":True,"message":_uid})
    except Exception as e:
        return jsonify({'success':False,"message":str(e)})

@app.route('/cita',methods=['GET'])
def show_cita():
    try:
        connection = mysql.connect()
        cursor = connection.cursor()
        cursor.execute('select * from cita')
        rows = cursor.fetchall()

        cursor.close()
        connection.close()
        return jsonify({"success":True,"message":rows})
    except Exception as e:
        return jsonify({"success":False,"message":str(e)})

@app.route('/receta',methods=["POST"])
def create_receta():
    try:
        body = request.json
        connection = mysql.connect()
        cursor = connection.cursor()
        
        _indicaciones = body.get('indicaciones')
        _medicamentos = body.get('medicamentos')
        _id_cita = body.get('id_cita')
        _uid = str(uuid.uuid4())

        insert_receta_cmd = """INSERT INTO receta(id,
        indicaciones,medicamentos,id_cita) VALUES(%s,%s,%s,
        %s)"""

        cursor.execute(insert_receta_cmd, (_uid,_indicaciones
        ,_medicamentos,_id_cita))
       
        connection.commit()

        cursor.execute('select id_paciente from cita where id = %s',(_id_cita,))
        id_paciente = cursor.fetchone()[0]
        cursor.execute("select email from pacientes where id = %s",(id_paciente,))
        paciente_email = cursor.fetchone()[0]

        cursor.close()
        connection.close()

        curl = "curk -X POST -H 'Content-Type: application/json' -d"
        url = "localhost:8015/email"
        date = datetime.now()

        json_pac = {"id_sender": 73641477 ,
                    "receiver": paciente_email ,
                    'subject': "clinica barata",
                    'message': f"Indicaciones: {_indicaciones}\nMedicinas: {_medicamentos}" ,
                    "year":date.year,"month":date.month, 
                    "day":date.day ,"hour": date.hour,
                    "minute":date.minute
                    }
        data = json.dumps(json_pac)
       
        subprocess.Popen(['curl', '-X', 'POST', '-H', 'Content-Type: application/json', '-d', data , url])

        return jsonify({"success":True,"message":_uid})
    except Exception as e:
        return jsonify({"success":False,"message":str(e)})

@app.route('/receta',methods=['GET'])
def show_receta():
    try:
        connection = mysql.connect()
        cursor = connection.cursor()
        cursor.execute('select * from receta')
        rows = cursor.fetchall()
        cursor.close()
        connection.close()

        return jsonify({"success":True,"receta":rows})
    except Exception as e:
        return jsonify({"success":False,"message":str(e)})


if __name__ == "__main__":
    app.run(host='0.0.0.0',port=8010,debug=False)

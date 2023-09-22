from flask import Flask,request,jsonify,abort
from flaskext.mysql import MySQL
from datetime import datetime
import os
import sys
import json
import uuid
import subprocess


app = Flask(__name__)
mysql = MySQL()

app.config["MYSQL_DATABASE_USER"] = 'root'
app.config["MYSQL_DATABASE_PASSWORD"] = '230204'
app.config["MYSQL_DATABASE_DB"] = 'cloud_project'
app.config["MYSQL_DATABASE_HOST"] = 'localhost'
app.config["MYSQL_DATABASE_PORT"] = 8005

mysql.init_app(app)

@app.route('/email',methods=['POST'])
def create_email():
    try:
        body = request.json

        connection = mysql.connect()
        cursor = connection.cursor()

        _id_sender = body.get('id_sender')
        _receiver = body.get('receiver')
        _subject = body.get('subject')
        _message = body.get('message')
        
        _year = body.get('year')
        _month = body.get('month')
        _day = body.get("day")
        _hour = body.get('hour')
        _minute = body.get('minute')

        _uid = str(uuid.uuid4())
        date = datetime(int(_year),int(_month),int(_day),int(_hour),int(_minute))
        date_str = datetime.isoformat(date)

        insert_email_cmd = """INSERT INTO email(id,id_sender,receiver,subject,message,date) 
         VALUES(%s,%s,%s,%s,%s,%s)"""

        cursor.execute(insert_email_cmd,(_uid,_id_sender,_receiver,_subject,_message,date_str))
        connection.commit()

        cursor.close()
        connection.close()
        print(date_str,'\t',_uid)
        
        
        subprocess.Popen(["python3",'mailscript.py','--date_str',date_str,'--email_id',_uid],stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True)

        return jsonify({"success":True,"message":_uid})
    except Exception as e:
        return jsonify({"success":False,"message":str(e)})

@app.route("/email",methods=["GET"])
def show_email():
    try:
        connection = mysql.connect()
        cursor = connection.cursor()
        cursor.execute('select * from email')
        rows = cursor.fetchall()

        cursor.close()
        connection.close()

        return jsonify({"success":True,"message":rows})
    except Exception as e:
        return jsonify({"success":False,"message":str(e)})


if __name__ == "__main__":
    app.run(host='0.0.0.0',port=8015,debug=False)

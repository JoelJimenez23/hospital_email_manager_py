import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import argparse
import psycopg2
import pymysql


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--email_id',type=str)
    args = parser.parse_args()

    connection = pymysql.connect(host='localhost',user='root',password='230204',database='cloud_project',port=8005)
    cursor = connection.cursor()
    cursor.execute('select * from email where id = %s',(args.email_id,))
    email_data = cursor.fetchone()
    user_id = email_data[1]

    cursor.execute('select * from doctores where id = %s',(user_id,))
    user_data = cursor.fetchone()
    
    connection.close()
    cursor.close()


    email = user_data[3]
    token = user_data[5]
    receiver = email_data[2]
    subject = email_data[3]
    message = email_data[4]

    msg = MIMEMultipart()
    msg['From'] = email
    msg['To'] = receiver
    msg['Subject'] = subject

    msg.attach(MIMEText(message,'plain'))
    smtp_server = 'smtp.gmail.com'
    smtp_port = 587


    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(email, token)

        server.sendmail(email, receiver, msg.as_string())
        print("Correo enviado")
    except Exception as e:
        print("Error al enviar el correo:", str(e))
    finally:
        if server:
            server.quit()  # Asegúrate de que la conexión SMTP se cierre en cualquier caso


if __name__ == '__main__':
    main()



#server = smtplib.SMTP(smtp_server,smtp_port)
#server.starttls()
#server.login(email,token)

#server.sendmail(email,receiver,msg.as_string())
#server.quit()

#print("correo enviado")



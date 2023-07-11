import datetime as dt
import pandas
import random
import smtplib

MY_EMAIL = "tucorreo@mail.com"
# OJO no colocar la contraseña del correo, hay que colocar la contraseña generada en tu correo para SMTP
MY_PASSWORD = "abcd1234"

today_tuple = (dt.datetime.now().month, dt.datetime.now().day)
# Dataframe para crear diccionario posteriormente (comprehension)
data = pandas.read_csv("birthdays.csv")

"""Iteramos las filas del DataFrame y asignamos cada fila a la variable data_row y su índice a la variable index
   luego filtramos los valores de las columnas "month" y "day" de cada fila del data_row
   terminamos con un diccionario donde la clave del diccionario es una tupla (month, day) obtenida de cada fila del 
   DataFrame, y el valor es la colección de datos en data_row"""
birthday_dict = {(data_row["month"], data_row["day"]): data_row for (index, data_row) in data.iterrows()}
if today_tuple in birthday_dict:
    # almacenamos la fila que contenga la tupla con fecha y hora de hoy
    birthday_person = birthday_dict[today_tuple]
    # Creamos un path hacia cualquiera de nuestras txt (random)
    letter_path = f"letter_templates/letter_{random.randint(1, 3)}.txt"
    with open(letter_path) as letter_file:
        email_message_content = letter_file.read()
        # Reemplazamos la variable name de la carta de cumpleaños con el nombre del cumpleañero(a)
        formatted_email_content = email_message_content.replace("[NAME]", birthday_person["name"])
    # Enviamos el mail de felicitaciones
    with smtplib.SMTP("smtp.gmail.com") as connection:
        connection.starttls()
        connection.login(MY_EMAIL, MY_PASSWORD)
        connection.sendmail(
            from_addr=MY_EMAIL,
            to_addrs=birthday_person["email"],
            msg=f"Subject:Feliz Cumpleaños!!!\n\n{formatted_email_content}"
        )
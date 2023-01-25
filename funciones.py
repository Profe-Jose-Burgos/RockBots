import string
import random
import string
import pickle
import re
from string import ascii_letters
from apiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
import sqlite3
from datetime import datetime,timedelta
import pandas as pd
from chatbot_respuesta import *
import qrcode 
from PIL import Image, ImageDraw


#AGENDAR CITAS

credentials=pickle.load(open('token.pkl','rb'))
service=build('calendar','v3',credentials=credentials)

def range_alpha(start_letter, end_letter):
    return ascii_letters[
    ascii_letters.index(start_letter):ascii_letters.index(end_letter) + 1
  ]

def codigo_cita():
    letras=range_alpha('a', 'v')
    characters = letras + string.digits 
    cita_id = ''.join(random.choice(characters) for i in range(8))
    return cita_id+'5'


def mostrarDatos(dictinfo, msgconf):
    print(msgconf,'\n')
    for key in dictinfo.keys():    
        print(key, ':', dictinfo[key])



def verificar_correo(entradaUsuario):
   reCorreo= r"(?:[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*|\"(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*\")@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\[(?:(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9]))\.){3}(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9])|[a-z0-9-]*[a-z0-9]:(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\])"
   correo_verificar= re.match(reCorreo,entradaUsuario) is not none 
  while correo_verificar==True:
    if correo_verificar==True:
      correo=entradaUsuario
    else:
      print('El correo ingresado no es válido, ingrese nuevamente')



def getInfo(msgInicial, listaConsultas, servicio):
    print(msgInicial)
    for i, pregChat in enumerate(listaConsultas):
        print(pregChat)
        entradaUsuario = input()
        if i ==0:
            nombre = entradaUsuario
            
        if i ==1:
            fecha = str(entradaUsuario+' ')
            
        if i ==2:
            hora = str(entradaUsuario+':00')
            fecha= fecha+hora
            start_time= datetime.strptime(fecha, "%d/%m/%Y %H:%M:%S")
            end_time=start_time+timedelta(hours=1)

        if i ==3:
            verificar_correo() 
        if i ==4:
            description = entradaUsuario 

    return {'nombre':nombre, 'descripcion':description, 'hora_de_inicio':start_time, 'hora_finalización':end_time,'correo':correo}
            
msgInicial = "Para consultar disponibilidad indiquenos los siguientes datos:"
listaConsultas = ['por favor indiqueme el nombre','Ingrese fecha en formato *DD/MM/AAAA* ','Ingrese hora en formato de 24 horas *hora:min*','Ingrese su correo electrónico','Porqué está agendando esta cita?']
msgconf = 'Para terminar el proceso de agendar su cita, confirme que los datos ingresados son correctos.'



def crear_evento(nombre,servicio,id_cita,description,start_time,end_time,correo,calendar_id):
    event = { 
        'summary': (nombre + '  servicio: ' + servicio),
        'id':id_cita,
          'location': 'Local NO. 3,Town Center, Costa del Este, Ciudad de Panamá',
          'description': description,
          'start': {
            'dateTime': start_time.strftime('%Y-%m-%dT%H:%M:%S'),
            'timeZone': 'America/Panama',
          },
          'end': {
            'dateTime': end_time.strftime('%Y-%m-%dT%H:%M:%S'),
            'timeZone': 'America/Panama',
          },
          'attendees': [
            {'email': correo}
          ],
          'reminders': {
            'useDefault': False,
            'overrides': [
              {'method': 'email', 'minutes': 24 * 60},
              {'method': 'popup', 'minutes': 10},
            ],
          },
        }
    service.events().insert(calendarId=calendar_id, body=event).execute()


def aggdatos_sql(datos):
    conn = sqlite3.connect('Calendario_citas.db')
    cursor = conn.cursor()
    ingresar= cursor.execute("INSERT INTO Citas VALUES (:id_cita, :calendar_id,:servicio, :nombre,:descripcion,:hora_de_inicio,:hora_finalización,:correo)", infoCita) 
    conn.commit()
    conn.close()
    return ingresar


def confirmar_datos(intencion,infoCita,servicio,calendar_id):
    if intencion=='Afirmación' :
            id_citas= codigo_cita()
            infoCita['id_cita']=id_citas
            infoCita['calendar_id']=calendar_id
            crear_evento(infoCita['nombre'],servicio,id_citas,infoCita['descripcion'],infoCita['hora_de_inicio'],infoCita['hora_finalización'],infoCita['correo'],infoCita['calendar_id'])
            aggdatos_sql(infoCita)
            print('Su cita ha sido agendada con éxito, en que más puedo ayudarte?, su id de cita es: ',id_citas )
    elif intencion=='Negación':
            print('Ok, cita no agendada. En que más puedo ayudarte?')


id_asesoria='longstoryshort51@gmail.com'
id_atencióncliente='1e8f7a6f98f1ef21fe6c91c81f4bf84ea6715d776b3621517fb74a04fec2badd@group.calendar.google.com'

#Los id de calendario depende de la cuenta a ingresar para obtener el token.



def generar_qr(id_cita,infoCita):
    data = info
    img = qrcode.make(data)
    qr_name=str(id_cita)+'.png'
    qr=img.save(qr_name)
    return qr



def citas(intencion_previa,entradaUsuario):
    if intencion_previa=='Agendar Cita' and entradaUsuario == '1':
        msg1='''Para agendar una cita virtual indique el servicio que desea:
                 
                                1. Asesoría de compras
                                2. Atención al cliente'''
        print(msg1)
        entradaUsuario=input()
        modalidad='virtual'
        if  entradaUsuario == '1':
            servicio='Asesoría'
            calendar_id=id_asesoria
            infoCita = getInfo(msgInicial, listaConsultas, servicio)
            infoCita['servicio']=servicio
            infoCita['modalidad']=modalidad
            mostrarDatos(infoCita, msgconf)
            entradaUsuario = input()
            respuesta, intencion = chatbot_respuesta(entradaUsuario)
            confirmar_datos(intencion,infoCita,servicio,calendar_id)
            
        


        elif entradaUsuario == '2':
            servicio='Atención al cliente'
            calendar_id=id_atencióncliente
            infoCita = getInfo(msgInicial, listaConsultas, servicio)
            infoCita['servicio']=servicio
            infoCita['modalidad']=modalidad
            mostrarDatos(infoCita, msgconf)
            entradaUsuario = input()
            respuesta, intencion = chatbot_respuesta(entradaUsuario)
            confirmar_datos(intencion,infoCita,servicio,calendar_id)
            
        else: 
            print('Opción no válida')
            
    if intencion_previa=='Agendar Cita' and entradaUsuario == '2':
        msg1='''Para agendar una cita virtual indique el servicio que desea:
                 
                                1. Asesoría de compras
                                2. Atención al cliente'''
        modalidad='Presencial'                         
        print(msg1)
        entradaUsuario=input()

        if  entradaUsuario == '1':
            locacion='Ciudad de Panamá'
            servicio='Asesoría'
            calendar_id=id_asesoria
            infoCita = getInfo(msgInicial, listaConsultas, servicio)
            infoCita['servicio']=servicio
            infoCita['modalidad']=modalidad
            mostrarDatos(infoCita, msgconf)
            entradaUsuario = input()
            respuesta, intencion = chatbot_respuesta(entradaUsuario)
            confirmar_datos(intencion,infoCita,servicio,calendar_id)
            generar_qr(id_cita,infoCita)


        elif entradaUsuario == '2':
            locacion='Ciudad de Panamá'
            servicio='Atención al cliente'
            calendar_id=id_atencióncliente
            infoCita = getInfo(msgInicial, listaConsultas, servicio)
            infoCita['servicio']=servicio
            infoCita['modalidad']=modalidad
            mostrarDatos(infoCita, msgconf)
            entradaUsuario = input()
            respuesta, intencion = chatbot_respuesta(entradaUsuario)
            confirmar_datos(intencion,infoCita,servicio,calendar_id)
            generar_qr(id_cita,infoCita)

         
        else: 
            print('Opción no válida')
        
    intencion_previa = intencion  
    print(respuesta) 


def modificar_fecha():
  listaConsultas = ['Ingrese fecha en formato *DD/MM/AAAA* ','Ingrese hora en formato de 24 horas *hora:min*']
  entradaUsuario=input()
  for i, pregChat in enumerate(listaConsultas):
          print(pregChat)
          if i ==1:
              fecha = str(entradaUsuario+' ')
              
          if i ==2:
              hora = str(entradaUsuario+':00')
              fecha= fecha+hora
              start_time= datetime.strptime(fecha, "%d/%m/%Y %H:%M:%S")
              end_time=start_time+timedelta(hours=1)

      return start_time,end_time


def cambiar_info(entradaUsuario, id_cita):
    if entradaUsuario=='1':
        print('''Seleccione la opción que necesita:
                 1. Asesoría
                 2. Atención al cliente ''')
        entradaUsuario=input()
        evento = service.events().get(calendarId=calendarId, eventId=id_cita).execute()
        evento['summary'] = entradaUsuario

    elif entradaUsuario=='2':
        print('''Seleccione la modalidad que desea:
                 1. Virtual
                 2. Presencial ''')

        entradaUsuario=input()
        evento = service.events().get(calendarId=calendarId, eventId=id_cita).execute()
        if entradaUsuario=='1':
          evento['location'] = 'Virtual'

        elif entradaUsuario=='1':
          evento['location'] = 'Presencial'

    elif entradaUsuario=='3':
        modificar_fecha()
        evento = service.events().get(calendarId=calendarId, eventId=id_cita).execute()
        evento['start_time'] = start_time.strftime('%Y-%m-%dT%H:%M:%S')
        evento['end_time']= end_time.strftime('%Y-%m-%dT%H:%M:%S')
        
    elif entradaUsuario=='4':
        print('Ingrese su Nombre')
        entradaUsuario=input()
        evento = service.events().get(calendarId=calendarId, eventId=id_cita).execute()
        evento['nombre'] = entradaUsuario
        
    elif entradaUsuario=='5':
        print('Ingrese su correo')
        entradaUsuario=input()
        evento = service.events().get(calendarId=calendarId, eventId=id_cita).execute()
        evento['correo'] = entradaUsuario

    else:
        print('Opción no válida, ingrese nuevamente')


def modificar_citar(id_cita):
    if intencion_previa=='Modificar Cita' and buscar_id(id_cita)== True:
      menu=''''Indique el parametro a modificar (Número):
                  1. Servicio
                  2. Modalidad
                  3. Fecha y hora
                  4. Nombre
                  5. Correo'''
      print(menu)
      entradaUsuario=input()
      cambiar_info(entradaUsuario, id_cita)

    return service.events().update(calendarId='primary', eventId=event['id'], body=event).execute()



def cancelar_cita(id_cita):
      buscar=buscar_id(id_Cita)
      if intencion_previa=='Cancelar Cita' and buscar== True:
         service.events().delete(calendarId=calendar_id, eventId=id_cita).execute()



        


   
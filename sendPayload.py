import datetime
import requests
import json
import os
import boto3
client = boto3.client('events')

from arrayComunas import comunas
from mockPayloadEntrada import payload

#RECORRE LISTA DE COMUMNAS SEGUN POSICION
def itera_comuna(lista,n):
  comunas_json = json.dumps(lista)
  comunas_json_loads = json.loads(comunas_json)
  res = comunas_json_loads[n]["nombre"]
  return res

#REEMPLAZO DE CARACTERES ESPECIALES DE LA COMUNA
def get_cod_comuna_by_nombre_comuna(nombre_comuna):
    nombre_comuna_format = nombre_comuna.replace("á","a")
    nombre_comuna_format = nombre_comuna_format.replace("é","e")
    nombre_comuna_format = nombre_comuna_format.replace("í","i")
    nombre_comuna_format = nombre_comuna_format.replace("ó","o")
    nombre_comuna_format = nombre_comuna_format.replace("ú","u")
    nombre_comuna_format = nombre_comuna_format.replace("ñ","n")
    nombre_comuna_format = nombre_comuna_format.replace(" ","")
    nombre_comuna_format = nombre_comuna_format.replace("Á","a")
    nombre_comuna_format = nombre_comuna_format.replace("É","e")
    nombre_comuna_format = nombre_comuna_format.replace("Í","i")
    nombre_comuna_format = nombre_comuna_format.replace("Ó","o")
    nombre_comuna_format = nombre_comuna_format.replace("Ú","u")
    nombre_comuna_format = nombre_comuna_format.replace("Ñ","n")
    nombre_comuna_format = nombre_comuna_format.replace("'","")
    return nombre_comuna_format

#SE OBTIENE UN RUT ALEATORIO EJ:'19022567-4'
def get_rut():  
  url = "https://hzh5d7pn61.execute-api.us-west-2.amazonaws.com/dev/v1/rut"

  response = requests.get(url)
  res = response.text
  res = json.loads(res)
  rut = res["rutAleatorio"] 
  return rut

#SE OBTIENE EL NUMERO DE RUT  
def obtener_numero_rut(rut_obtenido):
  posicion = len(rut_obtenido)
  if len(rut_obtenido) == 10:
    num_rut = rut_obtenido[posicion-posicion] + rut_obtenido[posicion + 1 -posicion] + rut_obtenido[posicion + 2 -posicion] + rut_obtenido[posicion + 3 -posicion] + rut_obtenido[posicion + 4 -posicion] + rut_obtenido[posicion + 5 -posicion] + rut_obtenido[posicion + 6 -posicion] + rut_obtenido[posicion + 7 -posicion] + rut_obtenido[posicion + 8 -posicion]
  else:
    num_rut = rut_obtenido[posicion-posicion] + rut_obtenido[posicion + 1 -posicion] + rut_obtenido[posicion + 2 -posicion] + rut_obtenido[posicion + 3 -posicion] + rut_obtenido[posicion + 4 -posicion] + rut_obtenido[posicion + 5 -posicion] + rut_obtenido[posicion + 6 -posicion] + rut_obtenido[posicion + 7 -posicion] + rut_obtenido[posicion + 7 -posicion]  
  num_rut = num_rut.replace("-","")
  num_rut = int(num_rut)
  return num_rut
#SE OBTIENE EL DV
def obtener_dv_rut(rut_obtenido):
  posicion = len(rut_obtenido)
  dv_rut = rut_obtenido[posicion-1]
  return dv_rut   

def valida_rut(rut_entrada):
    while len(rut_entrada) < 10:
        rut_entrada = get_rut() 
        return rut_entrada      
i = 0
while i < len(comunas):

    #OBTENCION DE VALORES
    comuna = itera_comuna(comunas,i) # Comuna segun posicion
    rut = get_rut() #Obtiene el rut
    num_rut = int(obtener_numero_rut(rut)) #saco numero de rut
    dv_rut = obtener_dv_rut(rut) #saco dv

    #SE REEMPLAZA VALORES DEL PAYLOAD

    payload["rutContratante"] = num_rut
    payload["rutAsegurado"] = num_rut

    payload["dvContratante"] = dv_rut
    payload["dvAsegurado"] = dv_rut

    payload["comunaContratante"] = comuna
    payload["comunaAsegurado"] = comuna

    payload["token"] = "null"
    payload["terminoVigencia"] = "null"
    payload["numeroPoliza"] = "null"

    payload_dumps = json.dumps(payload)
    #payload_loads = json.loads(payload_dumps)

    arn_qa = 'arn:aws:events:us-east-1:282782924650:event-bus/input-data-poliza-telemarketing'
    arn_dev ='arn:aws:events:us-west-2:533588983801:event-bus/input-data-poliza-telemarketing'
    nombre_bus ='input-data-poliza-telemarketing'

    #por si acaso

    version= "0"
    id = "475f4622-2715-17f8-b17e-2cc22f3d129f"
    detail_type = "New Lead"
    source = "bice.poliza.telemarketing"
    account = "431852759368"
    time = "2022-10-14T12:19:12Z"
    region = "us-east-1"
    resources = []
    detail = payload_dumps

    response = client.put_events(
    Entries=[
        {
            'Time': time,
            'Source': source,
            'Resources': [],
            'DetailType': "New Lead",
            'Detail': payload_dumps,
            'EventBusName': arn_dev
        },
    ])

    #print("EL JSON MODIFICADO ES:")
    print(payload_dumps)



    i += 1

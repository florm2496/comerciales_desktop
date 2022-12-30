import requests
import json


dev = 'http://127.0.0.1:8000/'
prod = 'http://146.190.114.7/'


host = prod

endpoints = {
    'login': host+'logindesktop',
    'prueba':host+'prueba',
    'crearlote':host+'crearlotenuevo',
    'getloteactual':host+'getloteactual',
    'cambiar_estado_lote':host+'cambiarestadolote',
    'getconfigactual': host+'getconfigsactual',
    'getultimolotefinalizado':host+'getultimolotefinalizado',
    'cambiarestadolote':host+'cambiarestadolote',
    'actualizarlote':host+'actualizarlote',
    'crearjuicio':host+'crearjuicio'
}



def get_request(endpoint_name,params):      
    response=requests.get(endpoints[endpoint_name],params)
    return response.json()



def post_request(token,endpoint_name,data):
    headers={'Content-Type':'application/json',
              'Authorization': f'Token {token}'}
    response=requests.post(endpoints[endpoint_name],headers=headers,json=data)
    return response.json()

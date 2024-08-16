import requests
import http.client
import random
import json

def envia_mensagem(fone:str, msg:str) -> str:
    """
    Envia uma mensagem para o número de telefone especificado.
    """
    headers = {
        'content-type': 'application/json',
    } 
    json_data = {
        'apikey': '6bccbf5e-a3e2-4e97-8877-19d3c71725c2',
        'phone_number': '554430237230',
        'contact_phone_number': '55'+fone.replace( ' ', '').replace('(','').replace(')','').replace('-',''),
        'message_custom_id': '999998',
        'message_type': 'text',
        'message_to_group': '0',
        'message_body': msg,
    }
    
    con = requests.post(f"https://app.whatsgw.com.br/api/WhatsGw/Send", headers=headers, json=json_data)
   
    return con.status_code

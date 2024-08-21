from flask import g
from .config import load_config 
import psycopg2
import os

"""os.chdir('C:\prg\change')"""
os.chdir('/home/kuro/change')
def create_connection():
    config = load_config()
    db = psycopg2.connect(**config)
    return db

def create_table_pedido():
     execute('''
        CREATE TABLE IF NOT EXISTS pedido (
            pedido_id           SERIAL PRIMARY KEY,
            pix_id              INTEGER DEFAULT NULL,
            created_date        TEXT ,
            created_time        TEXT ,
            status_pagamento    BOOLEAN DEFAULT FALSE,
            status_carga        BOOLEAN DEFAULT FALSE,
            tiempo_carga        TEXT,
            valor               FLOAT,
            segundo_total       INTEGER,
            fone                TEXT,
            voucher             TEXT 
    ); ''')


          
def execute(sql, values=None):
    try:
        conn = create_connection()
        cur  = conn.cursor()
        cur.execute(sql, values)
        conn.commit()
    except  psycopg2.errors.UndefinedTable as e:

        print(e)
        create_table_pedido()
        create_table_config()


    #return cur.fetchall()[0]
def create_config(codemp,chave,valor):
    sql = '''
    INSERT INTO config(cod, nome, valor)
      VALUES (%s, %s, %s);
    '''
    execute(sql, values=(codemp,chave, valor))


def create_pedido(date, time_c, fomatado, seg, valor, fone, voucher):
    """ Create new pedido in database

    :param
        date::      time zone create pedido
        status::    true pay not pay false
        formatado:: HH:MM:SS
        valor::     valor a pagar
        seg::       total secondss
        fone::      telefone
        voucher::   voucher recarga

    """
    """alterar tabela pedido  criando campos voucher text e fone text"""
    """ alter = '''alter table pedido add column if not exists fone text;
               alter table pedido add column if not exists voucher text;'''
    execute(alter)
    """
    sql = '''
    INSERT INTO pedido(created_date, created_time,  tiempo_carga, segundo_total, valor,fone,voucher)
      VALUES (%s, %s, %s, %s, %s,%s, %s);
        
    '''
    execute(sql, values=(date,time_c, fomatado, seg, valor,fone,voucher))

def add_pix_id(pedido_id ,pix_id):
    """ add pix_id ref in pix 

    :param
        pedido_id::: is identification pedido

    """
    
    sql = f""" UPDATE pedido 
               SET pix_id = {pix_id}
               WHERE pedido_id = {pedido_id}   
    """
    conn = create_connection()
    cur  = conn.cursor()
    cur.execute(sql)
    conn.commit()
    

def update_value(column,value,where):
    """ Update pedido in True status

    :param
        pedido_id::: is identification pedido
        column   ::: is column name updare

    """
    
    sql = f""" UPDATE pedido 
               SET {column} = {value}
               WHERE {where}; 
    """
    print(sql)
    conn = create_connection()
    cur  = conn.cursor()
    cur.execute(sql)
    conn.commit()
    cur.close()
    conn.close()



def check_status():
    """ query pedido by id  
    :param
        pedido_id::: is identification pedido


    :return list[tuple]
    """ 
    regitro_id = ultimo_registro()
   
    return view_pedido(regitro_id)[2]
    
    
def view_pedido(pedido_id):
    """ query pedido by id  
    :param
        pedido_id::: is identification pedido


    :return list[tuple]
    """ 
    sql = f'SELECT * FROM pedido WHERE pedido_id = {pedido_id} '
    conn = create_connection()
    cur = conn.cursor()
    cur.execute(sql)

    return cur.fetchall()[0]


def view_all():

    conn = create_connection()
    cur  = conn.cursor()
    row = cur.fetchone()
    if row:
        return row[0]
    return None



def ultimo_registro():

    sql = '''SELECT pedido_id FROM pedido 
             WHERE  pedido_id = (SELECT MAX(pedido_id)
             FROM   pedido);'''

    conn = create_connection()
    cur = conn.cursor()
    cur.execute(sql)
    row = cur.fetchone()
    if row:
        return row[0]
    return None

def telefone_cadastrado(telefone):
    sql = f"SELECT fone FROM pedido WHERE voucher = '0' and  fone = '{telefone}'"
    conn = create_connection()
    cur = conn.cursor()
    cur.execute(sql)
    row = cur.fetchone()
    if row:
        return row[0]
    return None

def create_table_config():
     execute('''
        CREATE TABLE IF NOT EXISTS config (
            cod      SERIAL PRIMARY KEY,
            nome      TEXT,
            valor     TEXT
    ); ''')
     
def view_config():
    """ query pedido by id  
    :param
        pedido_id::: is identification pedido


    :return list[tuple]
    """ 
    sql = f'SELECT * FROM config order by cod '
    conn = create_connection()
    cur = conn.cursor()
    cur.execute(sql)

    return cur.fetchall()

def empresa_cadastrada(codemp):
    sql = f"SELECT cod FROM config WHERE cod = '{codemp}'"
    conn = create_connection()
    cur = conn.cursor()
    cur.execute(sql)
    row = cur.fetchone()
    if row:
        return row[0]
    return None

def update_config(column,value,where):
    """ Update pedido in True status

    :param
        pedido_id::: is identification pedido
        column   ::: is column name updare

    """
    
    sql = f""" UPDATE config 
               SET {column} = {value}
               WHERE {where}; 
    """
    print(sql)
    conn = create_connection()
    cur  = conn.cursor()
    cur.execute(sql)
    conn.commit()
    cur.close()
    conn.close()
create_table_pedido()

"""
example use
 
date = datetime.now()

date_row = date.strftime('%m/%d/%Y %H:%M:%S')
form     = date.strftime('%H:%M:%S') 
carga    = '00:30:00'
valor    =  45.00
segTotal = '1800'

create_pedido(date_row, False, carga, valor, segTotal)
pay_paedido(ultimo_registro())
print(view_all())

"""


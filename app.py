from flask import Flask, render_template, request, Response, abort, redirect,url_for
from os import path, getcwd, chdir
from libs.pixadd import create_cob, get_cob, delete_pix
from libs.db import *
from dotenv import dotenv_values
from datetime import datetime
from time import sleep
from libs.relay.acrive import *
import math
from subprocess import Popen, PIPE,check_output
#from libs.whats import envia_mensagem


app = Flask(__name__)

chdir('/home/kuro/change')
app.template_folder = getcwd() + r'/tamplante' 
app.static_folder   = getcwd() + r'/static'

#chdir(r"C:\\prg\\change")
#app.template_folder = getcwd() + r'\\tamplante' 
#app.static_folder   = getcwd() + r'\\static'
print(app.static_folder ,
      app.template_folder)

@app.route('/')
def home():
   #verificar se banco virgem
   #abrir tela de codigo empresa
   #senao return telefone
   
   return render_template('fone.html')
@app.route('/tipopagamento')
def tipopagamento():
   telefone = request.args.get('telefone')
   if not telefone:
        telefone ='00 00000-0000'
   

   resultado = ''.join(filter(lambda i: i if i.isdigit() else None, telefone))
 
   date = datetime.now()
  
   # ['%d/%m/%Y,  %H:%M:%S']
   date_row = date.strftime('%d/%m/%Y %H:%M:%S').split(' ')

   hora     = 00
   minutos  = 00
   segundos = 00 
   
   carga = "{:02d}:{:02d}:{:02d}".format(
                          int(hora), int(minutos), int(segundos))

   totalseg = hora * 3600 + minutos * 60 + segundos
   total_pagar = 0
   total_pagar = '%.2f' % float(total_pagar) 
   # save pedido
   if telefone_cadastrado(resultado) == None:
      create_pedido(date_row[0],date_row[1], carga, totalseg, total_pagar,resultado,0)
      
   pedido_id = ultimo_registro()
   print(pedido_id)	
   return render_template('tipopagamento.html', telefone=telefone)

@app.route('/config')
def config():
  # config = view_config()
  # print(config) dffjhfgjhfg
   a = check_output(getcwd() + r'\\atualizar.bat')
   print(a)
  # startfile(getcwd() + r'\\atualizar.bat')
  
   #filepath=getcwd() + r"/libs/atualizar.bat"
   #p = Popen(filepath, shell=True, stdout = PIPE)
   #stdout, stderr = p.communicate()
   #print(stdout)
   #print( p.returncode)
   #with open(getcwd() + r"/libs/atualizar.bat") as f:
   #  code = compile(f.read(), getcwd() + r"/libs/atualizar.bat", 'exec')
   #  exec(code)
   return render_template('config.html')  

@app.route('/salvarconfig')
def salvarconfig():
   codemp = request.args.get('codemp')
   chave = request.args.get('chave')
   valor = request.args.get('valor')
   print('codemp '+codemp)
       
   if codemp != None:
     empresa = empresa_cadastrada(codemp)
     if empresa != None:
       con = update_config('nome',f"\'{chave}\'","cod="+str(codemp))
       con = update_config('valor',f"\'{valor}\'","cod="+str(codemp))
     else: con = create_config(codemp,chave,valor)
     print(con)
   if con =='':
     return redirect('config.html')  
   return redirect('/') 
@app.route('/voucher')
def voucher():
   pedido_id = ultimo_registro()
   print(pedido_id)
   return render_template('voucher.html', 
                                 pedido_id=pedido_id)
@app.route('/tempo')
def tempo():

   pedido_id = ultimo_registro()
   print(pedido_id)
   if pedido_id != None:
      registro = view_pedido(pedido_id) 
      print(registro)
      if registro[-4] == False and registro[-5] == True  :
         return redirect(url_for('timer', 
                                 pedido_id=registro[0],
                                 startauto='true'))
         

   return render_template('tempo.html')


@app.route('/btn')
def button():
   return render_template('btn.html')

@app.route('/carton/<pedido_id>')
def carton(pedido_id):
    pedido = view_pedido(pedido_id)
    total  = str(pedido[-4]).replace(',', '') 
    return render_template('carton.html', total_pagar='%.2f' % float(total)
                           ,  img='nfc.jpg')

@app.route('/deletePix/<pedido_id>')
def deletePix(pedido_id):
   pedido = view_pedido(pedido_id)
   pix_id = pedido[1]
   print(pix_id)
   if pix_id != None:
      if path.exists(".env"):   
         config = dotenv_values(".env")
         appid = config['APP_ID']
         con = delete_pix(appid,pix_id)
         if (con ==200):
           update_value('pix_id','null', "pedido_id = "+str(pedido_id))
           return redirect('/')
         else:
           return render_template('error.html', num= con)
      abort(500)
   abort(404)


@app.route('/timer/<int:pedido_id>')
def timer(pedido_id):
      start = request.args.get('startauto')
      voucher = request.args.get('voucher')
      print(voucher)
      if (voucher !=None):
         tempo = int(voucher[12: 14])
         hora = math.floor((tempo * 10) / 60);
         minutos = (tempo * 10) % 60;
         carga = "{:02d}:{:02d}".format(
                          int(hora), int(minutos))
         update_value('tiempo_carga',f"\'{carga}\'", "pedido_id = "+str(pedido_id))   
         update_value('voucher',f"\'{voucher}\'", "pedido_id = "+str(pedido_id))
      print(start)
      info = view_pedido(pedido_id)
      print(info)
      return render_template('timer.html', Time=info[-5],Fone=info[-2])


@app.route('/cheking')
def show_post():
   date = datetime.now()
   # ['%d/%m/%Y,  %H:%M:%S']
   date_row = date.strftime('%d/%m/%Y %H:%M:%S').split(' ')

   try:
      hora     = int(request.args.get('hours'))
      minutos  = int(request.args.get('min'))
      segundos = int(request.args.get('seg'))
   except TypeError:
      hora     = 00
      minutos  = 00
      segundos = 00 
   
   carga = "{:02d}:{:02d}".format(
                          int(hora), int(minutos))

   totalseg = hora * 3600 + minutos * 60 + segundos
   
   total_pagar = totalseg / 240 # 60 seg valeria 0,25 reales
   total_pagar = '%.2f' % float(total_pagar) 
   # save pedido
   pedido_id = ultimo_registro()
   print(pedido_id)	
   update_value('valor',total_pagar, "pedido_id = "+str(pedido_id))
   update_value('segundo_total',totalseg, "pedido_id = "+str(pedido_id))
   update_value('tiempo_carga',f"\'{carga}\'", "pedido_id = "+str(pedido_id))   
   
   return render_template('cheking.html', 
                             time=carga,
                             total=total_pagar,
                             pedido_id=pedido_id )
   
   abort(404)

@app.route('/pix/<pedido_id>')
def pix(pedido_id):
   pedido = view_pedido(pedido_id)
   total  ="{:.2f}".format(pedido[-4])
   print(total)
   if total != '0.00':
     # if path.exists(".env"):   
     #    config = dotenv_values(".env")
      if path.exists(".env"):   
         config = dotenv_values(".env")
         appid = config['APP_ID']
        
         pix = (0,pedido[1])
         if pix[1] == None:
            pix = create_cob(appid, total.replace('.',''), cometdv='')
            add_pix_id(pedido_id, pix[1])
        
         cob = get_cob(appid, pix[1])
         print(cob)
	
      

         try:
            img = cob['charge']['qrCodeImage']

         except KeyError:
            error = cob
            print(error)
            return  render_template('pix.html', e=error)
         return render_template('pix.html', total_pagar='%.2f' % float(total), 
                              img=img,
                              ID=cob['charge']['correlationID'],
                              pedido_id=pedido_id)
      abort(500)      
   abort(404)

# server APi
@app.route('/pixcheck/<idPix>')
def pixcheck(idPix):
    def generate_data():
        #config = dotenv_values(".env")
        config = dotenv_values(".env")
        appid  = config['APP_ID']
        while True:
            ultima_trastion = get_cob(appid, idPix)
            status = ultima_trastion['charge']['status']  
            if status != 'ACTIVE':
               update_value('status_pagamento',True,f'pix_id = {idPix}')
            yield 'data: {}\n\n'.format(status)
            sleep(2)  # Espera 2 segundo antes de generar el próximo dato

    return Response(generate_data(), mimetype='text/event-stream', headers={'Cache-Control': 'no-cache'})
      

@app.route('/complete')
def completestatus():
   def tiempo_a_segundos(tiempo):
      print(tiempo)
      horas, minutos = tiempo.split(':')
      total_segundos = int(horas) * 3600 + int(minutos) * 60 
      return total_segundos
   
   def formatear_tiempo(segundos):
      horas = segundos // 3600
      minutos = (segundos % 3600) // 60
      
      return "{pad(horas)}:{pad(minutos)}"

   def pad(numero):
      return str(numero).zfill(2)
  
   def generate_data():
      
      while True:
            pedido_id = ultimo_registro()
            registro = view_pedido(pedido_id) 
            temBan =  registro[5]
            print(temBan)
            #fone = registro[-2]
            if temBan == "00:00:00" or temBan =="00:00":
               update_value('status_carga',True, "pedido_id = {pedido_id}")
               control_relay().stop()
            #   if fone != '':
            #     con =envia_mensagem(fone, 'Carga Completa')
            #     print(con)
            else:
               seg = tiempo_a_segundos(temBan)
               timeformat = formatear_tiempo(seg - 60)
               control_relay().stop()
               print(timeformat)
               update_value('tiempo_carga', "\'{timeformat}\'", "pedido_id = "+str(pedido_id))
            print(registro)
            print(pedido_id)

            yield 'data: {}\n\n'.format(pedido_id)
            sleep(60)

   return Response(generate_data(), mimetype='text/event-stream', headers={'Cache-Control': 'no-cache'})


@app.route('/cancel')
def cancelstatus():
   fone = request.args.get('fone')
   pedido_id = ultimo_registro()
   update_value('status_carga',True, f'pedido_id = {pedido_id}')
   
   control_relay().start()
   print(fone)
  # if fone != None:
  #   con =envia_mensagem(fone, 'Carga cancelada')
   
   #if (con !=''):
   return redirect('/')
   #else:
   #   return render_template('error.html', num= con)

# section error

@app.route('/atualizagit')
def atualizagit():
   os.open(getcwd()+ r'\\libs\\atualizar.bat',1)
   return redirect('/')  
# error 
@app.errorhandler(404)
def not_found(e):
  print(e)
  return render_template('error.html', num='2'), 404
  
@app.errorhandler(500)
def internal_server(e):
  print(e)
  return render_template('error.html', num='3'), 500

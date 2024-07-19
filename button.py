Programa: Hat Rele 4 canais para Raspberry Pi
#Autor: Arduino e Cia
# !/usr/bin/python3
from tkinter import *
from tkinter import messagebox
from tkinter import font
# Define biblioteca da GPIO
import RPi.GPIO as GPIO
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(19, GPIO.OUT)
GPIO.setup(26, GPIO.OUT)
GPIO.setup(20, GPIO.OUT)
GPIO.setup(21, GPIO.OUT)
#Pinos em estado alto para desligar os reles
GPIO.output(19, 1)
GPIO.output(26, 1)
GPIO.output(20, 1)
GPIO.output(21, 1)
#Armazena o estado do rele
b1=b2=b3=b4=1
cor_botao1=cor_botao2=cor_botao3=cor_botao4 = 'red'
top = Tk()
top.geometry("330x200+235+140")
top.title("Arduino e Cia")
top.configure(background='grey')
helv36 = font.Font(family='Helvetica', size=16, weight='bold')
def chamada_botao_1():
   global b1
   global cor_botao1
   b1 = not b1
   GPIO.output(19, b1)
   if b1 == 1:
    cor_botao1 = 'red'
   elif b1 == 0:
    cor_botao1 = 'green'
   desenha_botao1()
      
def chamada_botao_2():
   global b2
   global cor_botao2
   b2 = not b2
   GPIO.output(26, b2)
   if b2 == 1:
    cor_botao2 = 'red'
   elif b2 == 0:
    cor_botao2 = 'green'
   desenha_botao2()
   
def chamada_botao_3():
   global b3
   global cor_botao3
   b3 = not b3
   GPIO.output(20, b3)
   if b3 == 1:
    cor_botao3 = 'red'
   elif b3 == 0:
    cor_botao3 = 'green'
   desenha_botao3()
   
def chamada_botao_4():
   global b4
   global cor_botao4
   b4 = not b4
   GPIO.output(21, b4)
   if b4 == 1:
    cor_botao4 = 'red'
   elif b4 == 0:
    cor_botao4 = 'green'
   desenha_botao4()
def desenha_botao1():
   B = Button(top, text = "RELAY 1", command = chamada_botao_1, font = helv36, fg=cor_botao1)
   B.config(width="8",height="2")
   B.place(x = 30,y = 30)
   
def desenha_botao2():
   C = Button(top, text = "RELAY 2", command = chamada_botao_2, font = helv36, fg=cor_botao2)
   C.config(width="8",height="2")
   C.place(x = 180,y = 30)
   
def desenha_botao3():
   D = Button(top, text = "RELAY 3", command = chamada_botao_3, font = helv36, fg=cor_botao3)
   D.config(width="8",height="2")
   D.place(x = 30,y = 110)
   
def desenha_botao4():
   E = Button(top, text = "RELAY 4", command = chamada_botao_4, font = helv36, fg=cor_botao4)
   E.config(width="8",height="2")
   E.place(x = 180,y = 110)
#Desenha botoes
desenha_botao1()
desenha_botao2()
desenha_botao3()
desenha_botao4()
top.mainloop()

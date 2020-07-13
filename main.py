#!/usr/bin/python3

# chmod o+x hora.py                             // Se le dan permisos al archivo
# crontab -e                                    // Ejecutamos el crontab para que se pueda iniciar solo el script al iniciar el sistema
# @reboot python3 /home/pi/asistente/main.py    // Agregamos al crontab esta linea, se guarda y se reinicia, ya deberia funcionar

# sudo rasp-config            // Hay que cambiar la salida del audio ya que por defecto usa la de HDMI, configuramos a plug que es salida analoga


# https://es.stackoverflow.com/questions/150343/c%C3%B3mo-se-hace-en-linux-para-ejecutar-un-archivo-python-al-arrancar-la-m%C3%A1quina
# https://pypi.org/project/SpeechRecognition/3.0.0/
# https://www.raspberrypi-spy.co.uk/2019/06/using-a-usb-audio-device-with-the-raspberry-pi/	 // Cambiar salida de audio

# sudo apt install portaudio19-dev
# sudo apt install mpg321
# sudo apt install flac
# sudo apt install python3-pip
# sudo pip3 install SpeechRecognition
# sudo pip3 install pyaudio
# sudo pip3 install gTTS

# Nuevos, aun no los uso pero van a ser para text_parser
# pip3 install nltk
# pip3 install numpy

import threading
import time
import random

from datetime import datetime
from datetime import date

from servidor import Servidor
from voice_input import Voice_input
from voice_output import Voice_output
#from text_parser import Text_parser
from procesa_comando import Procesa_comando
import raspberry as rpi


def ServidorComandos():
	s = Servidor(3333) # numero de puerto
	global idioma, w
	while(True):
		try:
			msg = s.recibir()
			val, idioma = w.ProcesaComando(msg,idioma)
		except:
			pass

def GpioAutomatico(): # Mantiene el ventilador funcionando cuando es necesario, y agregar funciones de encendido automatico.
	global hora_encendido, hora_apagado
	status_actual = 0
	while True:
		if round(rpi.get_cpu_temp()) >= 42:
			rpi.onPin(12)
		else:
			rpi.offPin(12)

		hora_act = datetime.now().time()
		if (hora_act > hora_encendido) and (hora_act < hora_apagado):
			if status_actual == 0:
				status_actual = 1
				rpi.onRele(11)
		elif (status_actual == 1):
			status_actual = 0
			rpi.offRele(11)

		time.sleep(15)

hiloServidor = threading.Thread(target=ServidorComandos)
hiloServidor.start()

# Configuracion de raspberry
pines = [7,11,12] # Ventilador es el GPIO 12, 11 luz roja
rpi.iniciar(False,"BOARD",pines)
for i in pines:
	rpi.offRele(i)# apagamos todos los pines

hora_encendido = datetime.strptime("20:00:00","%X").time()
hora_apagado = datetime.strptime("22:30:00","%X").time()

hiloGpio = threading.Thread(target=GpioAutomatico)
hiloGpio.start()

s = Voice_output()
v = Voice_input("USB") # Nombre del microfono, 1 para mostrar los micros existentes
w = Procesa_comando(1) # El 1 hace que imprima el comando enviado en consola
idioma = "es"

while(True):
	texto = v.ObtenerRespuestaVoz(idioma)
	val, idioma = w.ProcesaComando(texto,idioma) # val es el retorno de funcion, si es -1 no existe, si es 1 se ejecuto bien y hubo respuesta de voz, 2 se ejecuto sin respuesta de voz, se la brindamos:
	if val == -1:
		if idioma == "en":
			s.RespuestadeVoz("Sorry but i couldn't run the command",idioma)
		else:
			s.RespuestadeVoz("Perdon pero no pude ejecutar el comando",idioma)
	elif val == 2:
		salidas = ["listo","hecho","de acuerdo","sin problema","claro","okey","esta bien"]
		s.RespuestadeVoz(random.choice(salidas),idioma)
	time.sleep(1)

# unused
# v = Voice_input("sysdefault",1)
# #analizar = Text_parser()
# salida.RespuestadeVoz("es","Hola, soy tu asistente de voz, ¿cual es tu nombre?")
# texto = v.ObtenerRespuestaVoz("es")
# nombre = analizar.obtenerNombre(texto)
# salida.RespuestadeVoz("es","Hola David, ¿como quieres llamarme?")
# texto = v.ObtenerRespuestaVoz("es") 
# salida.RespuestadeVoz("es","Muy bien, mi nombre sera Alina, vamos a realizar las primeras configuraciones")
# v = Procesa_comando()
# v.ProcesaComando("idioma")
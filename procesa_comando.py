import random
from datetime import datetime
from datetime import date
from voice_output import Voice_output
import raspberry as rpi

class Procesa_comando():

	def __init__(self,print_cmd = 0):
		self.salida = Voice_output()
		self.print_command = print_cmd

	def ProcesaComando(self,comando,idioma="en"): ###return 1 comando ejecutado con respuesta de voz, return -1 comando no existe, return 2 comando ejecutado sin respuesta de voz.
		if self.print_command:
			print(comando)

		if self.s(comando,"language","lenguaje","idioma"):
			if(idioma == "es"):
				idioma = ("en")
			else:
				idioma = ("es")
			self.salida.PlayAudio("language_changed.mp3",idioma)
			return (1, idioma)

		elif self.s(comando,"spanish","español","espanol"):
			idioma = "es"
			self.salida.PlayAudio("language_changed.mp3",idioma)
			return (1, idioma)

		elif self.s(comando,"english","ingles"):
			idioma = "en"
			self.salida.PlayAudio("language_changed.mp3",idioma)
			return (1, idioma)

		elif self.s(comando,"date","today","time","clock","fecha","hora","hoy"):
			now = datetime.now()
			self.salida.RespuestadeVoz(self.current_date_format(idioma,now),idioma,0)
			return (1, idioma)

		elif self.s(comando,"caracola","mágica","magic","conch"):
			respuestas = ["yes.mp3", "maybe_someday.mp3", "i_do_not_believe_it.mp3", "no.mp3", "try_asking_again.mp3"]
			aleatorio = random.choice(respuestas)
			self.salida.PlayAudio(aleatorio,idioma)
			return (1, idioma)

		elif self.s(comando,"cuánto","es"):
			if (comando.find("es") >= 0):
				text = self.CortarFrase(comando,"es").split()
			if len(text) == 3 :
				if text[1] == "más" or text[1] == "+":
					self.salida.RespuestadeVoz(str(int(text[0]) + int(text[2])),idioma)
				elif text[1] == "por" or text[1] == "*":
					self.salida.RespuestadeVoz(str(int(text[0]) * int(text[2])),idioma)
				elif text[1] == "entre" or text[1] == "/":
					if int(text[2]) != 0:
						self.salida.RespuestadeVoz(str(int(text[0]) / int(text[2])),idioma)
					else:
						self.salida.RespuestadeVoz("Cannot divide by zero",idioma)
				elif text[1] == "menos" or text[1] == "-":
					self.salida.RespuestadeVoz(str(int(text[0]) - int(text[2])),idioma)
			return (1, idioma)

		elif self.s(comando,"di","repite","repeat","say"):
			if (comando.find("mí") >= 0):
				self.salida.RespuestadeVoz(self.CortarFrase(comando,"mí"),idioma)
			elif (comando.find("mi") >= 0):
				self.salida.RespuestadeVoz(self.CortarFrase(comando,"mi"),idioma)
			elif (comando.find("esto") >= 0):
				self.salida.RespuestadeVoz(self.CortarFrase(comando,"esto"),idioma)
			elif (comando.find("me") >= 0):
				self.salida.RespuestadeVoz(self.CortarFrase(comando,"me"),idioma)
			elif (comando.find("this") >= 0):
				self.salida.RespuestadeVoz(self.CortarFrase(comando,"this"),idioma)
			return (1, idioma)

		elif self.s(comando,"gracias","thank"):
			self.salida.PlayAudio("youre_welcome.mp3",idioma)
			return (1, idioma)

		elif self.s(comando,"enciende","prende","encender","on","start"): # Los pines hay que manejarlos en listas cargadas por archivo para poder grabarlos por voz.
			if self.s(comando,"ventilador","aire","air","fan"):
				rpi.onPin(12)
			elif self.s(comando,"red","roja","rojo","secondary"):
				rpi.onRele(11)
			elif self.s(comando,"white","blanca","blanco","primary","luz"):
				rpi.onRele(7)
			return (2, idioma)

		elif self.s(comando,"apaga","quita","cancela","off"):
			if self.s(comando,"ventilador","aire","air","fan"):
				rpi.offPin(12)
			elif self.s(comando,"red","roja","rojo","secondary"):
				rpi.offRele(11)
			elif self.s(comando,"white","blanca","blanco","primary","luz"):
				rpi.offRele(7)
			return (2, idioma)

		elif self.s(comando,"switch","cambia","invierte","change"):
			if self.s(comando,"ventilador","aire","air","fan"):
				rpi.switchPin(12)
			elif self.s(comando,"red","roja","rojo","secondary"):
				rpi.switchPin(11)
			elif self.s(comando,"white","blanca","blanco","primary","luz"):
				rpi.switchPin(7)
			return (2, idioma)

		elif self.s(comando,"temperatura","temperature"):
			if self.s(comando,"server","servidor"):
				print("yes")
				respuesta = ["server temperature is "+str(round(rpi.get_cpu_temp()))+" degrees","La temperatura del servidor es de "+str(round(rpi.get_cpu_temp()))+" grados"]
				print(respuesta[0]+respuesta[1])
				if idioma == "en":
					self.salida.RespuestadeVoz(respuesta[0],idioma)
				else:
					self.salida.RespuestadeVoz(respuesta[1],idioma)
			return (1, idioma)

		return (-1, idioma)


	def s(self,texto,*args):
		for arg in args:
			if(texto.find(arg) >= 0):
				return 1
		return 0

	def current_date_format(self,idioma,date):
		months = ("January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December")
		days = ("Sunday","Monday","Tuesday","Wednesday","Thursday","Friday","Saturday")
		if(idioma == "es"):
			months = ("Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre")
			days = ("Domingo","Lunes","Martes","Miercoles","Jueves","Viernes","Sabado")
		day = days[int(date.strftime("%w"))]
		number_day = date.day
		month = months[date.month - 1]
		year = date.year
		hour = date.strftime('%H:%M')
		messsage = "today is {} {} of {} of {} and the actual time is {}".format(day, number_day, month, year, hour)
		if(idioma == "es"):
			messsage = "hoy es {} {} de {} de {} y la hora es {}".format(day, number_day, month, year, hour)
		return messsage

	def CortarFrase(self,frase,a_partir):
		separado = frase.split(a_partir)
		if(len(separado) > 1):
			return separado[1]
		return separado[0]
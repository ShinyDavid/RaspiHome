#!/usr/bin/python3

# chmod o+x hora.py           // Se le dan permisos al archivo
# crontab -e                  // Ejecutamos el crontab para que se pueda iniciar solo el script al iniciar el sistema
# @reboot /home/pi/hora.py    // Agregamos al crontab esta linea, se guarda y se reinicia, ya deberia funcionar

# sudo rasp-config            // Hay que cambiar la salida del audio ya que por defecto usa la de HDMI, configuramos a plug que es salida analoga


# https://es.stackoverflow.com/questions/150343/c%C3%B3mo-se-hace-en-linux-para-ejecutar-un-archivo-python-al-arrancar-la-m%C3%A1quina
# https://pypi.org/project/SpeechRecognition/3.0.0/
# https://www.raspberrypi-spy.co.uk/2019/06/using-a-usb-audio-device-with-the-raspberry-pi/	 // Cambiar salida de audio

# sudo apt-get install portaudio19-dev
# sudo apt-get install mpg321
# sudo apt install python3-pip
# sudo apt-get install flac
# sudo pip3 install SpeechRecognition
# sudo pip3 install pyaudio
# sudo pip3 install gTTS

import time
import RPi.GPIO as gpio
import threading
import speech_recognition as sr
import socket
import os
import random
from datetime import datetime
from datetime import date
from gtts import gTTS
from pathlib import Path

########################### CONFIGURACION DE SCRIPT ##############################

hora_encendido = datetime.strptime("20:00:00","%X").time()
hora_apagado = datetime.strptime("22:30:00","%X").time()
nombre_microfono_1		= "Logitech"
nombre_microfono_2		= "camera"
path_audios_pregrabados = "sounds_pre" # subcarpetas: en, es, effects, cache [subcarpetas: en, es],
path_musica				= "music"
path_files				= "files"
puerto_conexion			= 3333
idioma					= ("es")

########################### DEFINICION DE FUNCIONES ##############################

def get_cpu_temp(): # Muestra la temperatura en grados centigrados
    tempFile = open( "/sys/class/thermal/thermal_zone0/temp" )
    cpu_temp = tempFile.read()
    tempFile.close()
    return float(cpu_temp)/1000
    #Mostrar temperatura en grados Fahrenheit
    #return float(1.8*cpu_temp)+32

def ServidorComandos():
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.bind(("", puerto_conexion))
	s.listen(20)
	PrintandSave("[Servidor] El servidor de recepcion de comandos fue iniciado correctamente")
	while True:
		connect, addr = s.accept()
		hiloTmpS = threading.Thread(name='clientthread',target=clientthread,args=(connect,addr,))
		hiloTmpS.start()
	connect.close()

def clientthread(connect, addr):
	PrintandSave("[Servidor] Cliente conectado. IP:" + str(addr))
	while True:
		try:
			str_recv, temp = connect.recvfrom(1024)#
			if str_recv:
				print(str_recv)
				Command = EjecutarComando(str(str_recv))
				str_return = "El comando que enviaste fue ejecutado: " + str(str_recv)
				if Command == 0:
					str_return = "Error al ejecutar el comando que enviaste: " + str(str_recv)
				connect.sendto(bytes(str_return, 'utf-8'), addr)
			else:
				remove(connect)
		except:
			break

def ls(ruta = Path.cwd()):
	return [arch.name for arch in Path(ruta).iterdir() if arch.is_file()]

def createVoice(name,text_in_english,texto_en_espanol):
	tts = gTTS(text=text_in_english, lang='en')
	tts.save(path_audios_pregrabados+"/en/" + name)

	tts = gTTS(text=texto_en_espanol, lang='es')
	tts.save(path_audios_pregrabados+"/es/" + name)

def normalize(s):
    replacements = (
        ("á", "a"),
        ("é", "e"),
        ("í", "i"),
        ("ó", "o"),
        ("ú", "u"),
    )
    for a, b in replacements:
        s = s.replace(a, b).replace(a.upper(), b.upper())
    return s

def current_date_format(idioma,date):
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
	

def comprobar_fecha(a, m, d, hora, minuto, sec):
    dias_mes = [31, 28, 31, 30,31, 30, 31, 31, 30, 31, 30, 31]
    if(minuto < 0 or minuto >= 60 or sec < 0 or sec >= 60 or hora < 0 or hora >= 24):
        return False
    if((a%4 == 0 and a%100 != 0) or a%400 == 0):
        dias_mes[1] += 1
    if(m < 1 or m > 12):
        return False
    m -= 1
    if(d <= 0 or d > dias_mes[m]):
        return False
    return True

def EncenderPinRele(pin):
	if gpio.input(pin) == 1:
		gpio.output(pin, False) # Apaga el pin, en el rele actua de forma inversa y lo enciende
		return 1
	return 0
	
def ApagarPinRele(pin):
	if gpio.input(pin) == 0:
		gpio.output(pin, True) #Enciende el pin, en el rele actua de forma inversa y lo apaga
		return 1
	return 0

def SwitchPinRele(pin):
	if ApagarPinRele(pin) != 1:
		EncenderPinRele(pin)

def PrintandSave(text):
	now = datetime.now()
	text = now.strftime('[%d/%m/%Y - %H:%M:%S]') + " " + text
	f = open(path_files+"/log_hora.txt","a")
	f.write(text + '\n')
	f.close()
	print(text)
	
def CortarFrase(frase,a_partir):
	return a_partir[a_partir.find(frase)+len(frase):].lstrip(frase)

def CortarFrase1(frase,a_partir):
	separado = frase.split(a_partir)
	if(len(separado) > 1):
		return separado[1]
	return separado[0]
	
def PlayAudio(lang,audiofile):
	if(lang == "en"):
		os.system("mpg321 " + path_audios_pregrabados + "/en/" + audiofile)
	elif (lang == "es"):
		os.system("mpg321 " + path_audios_pregrabados + "/es/" + audiofile)
		
def PlayEffect(audiofile):
	os.system("mpg321 -g 30 " + path_audios_pregrabados + "/effects/" + audiofile) # -g X es el volumen
	
def PlayEffectForWait(audiofile):
	hiloTmp = threading.Thread(name='PlayEffect',target=PlayEffect,args=(audiofile,))
	hiloTmp.start()
	
def PlaySong(audiofile):
	os.system("mpg321 -g 40 " + path_musica + "/" + "\""+audiofile+"\"") # -g X es el volumen
	
def PlaySongInAnotherThr(song):
	songa = song.replace(" ","")
	lista = ls(path_musica)
	for name in lista:
		nume = name.lower()
		nume = nume.replace(" ","")
		nume = nume.replace(",","")
		nume = nume.replace("'","")
		if (nume.find(songa) >= 0):
			os.system("killall mpg321")
			hiloTmpS = threading.Thread(name='PlaySong',target=PlaySong,args=(name,))
			hiloTmpS.start()
			return 1
	return 0

def MusicaAleatoria(last_song): # reproduce canciones hasta que se acaban todas o se detiene por voz
	lista = ls(path_musica)
	global musica_auto
	while musica_auto == 1 and len(lista) > 1:
		if(last_song != "zero"):
			lista.remove(last_song)
		last_song = random.choice(lista)
		os.system("killall mpg321")
		PlaySong(last_song)

def checkFileExistance(filePath):
    try:
        with open(filePath, 'r') as f:
            return True
    except FileNotFoundError as e:
        return False
    except IOError as e:
        return False

def RespuestadeVoz(idioma,texto_en,texto_es,use_cache = 1): # si texto_es == "null" se ejecutara texto_en en el idioma que venga solamente, hay que verificar que el tamaño del texto sea menor a 225
	if use_cache == 1:	
		if (texto_es == "null" or idioma == "en") and (len(texto_en) > 0):
			if os.path.isfile(path_audios_pregrabados+"/cache/"+idioma+"/" + texto_en + ".mp3"):
				os.system("mpg321 " + path_audios_pregrabados+"/cache/"+idioma+"/" + "\""+ texto_en + "\""+ ".mp3")
			else:
				PlayEffectForWait("mario_coin.mp3")
				tts = gTTS(text=texto_en, lang=idioma)
				tts.save(path_audios_pregrabados+"/cache/"+idioma+"/" + texto_en + ".mp3")
				os.system("mpg321 " + path_audios_pregrabados+"/cache/"+idioma+"/" + "\""+ texto_en + "\""+ ".mp3")
		elif idioma == "es" and (len(texto_es) > 0):
			if os.path.isfile(path_audios_pregrabados+"/cache/es/" + texto_es + ".mp3"):
				os.system("mpg321 " + path_audios_pregrabados+"/cache/es/" + "\""+ texto_es + "\""+ ".mp3")
			else:
				PlayEffectForWait("mario_coin.mp3")
				tts = gTTS(text=texto_es, lang=idioma)
				tts.save(path_audios_pregrabados+"/cache/es/" + texto_es + ".mp3")
				os.system("mpg321 " + path_audios_pregrabados+"/cache/es/" + "\""+ texto_es + "\""+ ".mp3")
	else:
		if (texto_es == "null" or idioma == "en") and (len(texto_en) > 0):
			PlayEffectForWait("mario_coin.mp3")
			tts = gTTS(text=texto_en, lang=idioma)
			tts.save("output.mp3")
			os.system("mpg321 output.mp3")
		elif idioma == "es" and (len(texto_es) > 0):
			PlayEffectForWait("mario_coin.mp3")
			tts = gTTS(text=texto_es, lang=idioma)
			tts.save("output.mp3")
			os.system("mpg321 output.mp3")		

def ObtenerComandoVoz():
	recog = ("zero")
	r = sr.Recognizer()
	global index_microphone, idioma
	speech = sr.Microphone(device_index=index_microphone)
	with speech as source:
		#audio = r.adjust_for_ambient_noise(source) # Hace retardo de 1 segundo para ajustar el ruido del ambiente
		audio = r.listen(source)
	if (idioma == "en"):
		try:
			recog = r.recognize_google(audio, language = 'en-US').lower()
			print("You said: " + recog)
		except sr.UnknownValueError:
			print("Google Speech Recognition could not understand audio [EN]")			
		except sr.RequestError as e:
			print("Could not request results from Google Speech Recognition service; {0}".format(e))
			
	elif (idioma == "es"):
		try:
			recog = r.recognize_google(audio, language = 'es-MX').lower()
			print("Tu dijiste: " + recog)
		except sr.UnknownValueError:
			print("Google Speech Recognition could not understand audio [ES]")			
		except sr.RequestError as e:
			print("Could not request results from Google Speech Recognition service; {0}".format(e))

	return recog

def EjecutarComando(texto):
	global idioma
	if (texto.find("spanish") >= 0) or (texto.find("espanol") >= 0) or (texto.find("español") >= 0):
		idioma = ("es")
		PlayAudio(idioma,"language_changed.mp3")
		return 1

	elif (texto.find("english") >= 0) or (texto.find("ingles") >= 0):
		idioma = ("en")
		PlayAudio(idioma,"language_changed.mp3")
		return 1

	elif (texto.find("language") >= 0) or (texto.find("lenguaje") >= 0) or (texto.find("idioma") >= 0): 
		if(idioma == "es"):
			idioma = ("en")
			PlayAudio(idioma,"language_changed.mp3")
			return 1
		else:
			idioma = ("es")
			PlayAudio(idioma,"language_changed.mp3")
			return 1
			
	elif ((texto.find("fan") >= 0) or (texto.find("ventilador") >= 0) or (texto.find("air") >= 0) or (texto.find("refrigeration") >= 0) or (texto.find("refrigeración") >= 0)):
		global ventilador_auto
		if(ventilador_auto == 1):
			ventilador_auto = 0
			PlayAudio(idioma,"fan_auto_off.mp3")
		else:
			ventilador_auto = 1
			PlayAudio(idioma,"fan_auto_on.mp3")
		return 1
	
	elif (((texto.find("temperatura") >= 0) or (texto.find("temperature") >= 0)) and ((texto.find("server") >= 0) or (texto.find("servidor") >= 0))):
		RespuestadeVoz(idioma,"server temperature is "+str(round(get_cpu_temp()))+" degrees","La temperatura del servidor es de "+str(round(get_cpu_temp()))+" grados")
		return 1

	elif ((texto.find("off") >= 0) and (texto.find("all") >= 0) and (texto.find("pines") >= 0)) or ((texto.find("apaga") >= 0) and (texto.find("todos") >= 0) and (texto.find("pines") >= 0)):
		ApagarPinRele(7)
		ApagarPinRele(11)
		PlayAudio(idioma,"all_pines_off.mp3")
		return 1

	elif ((texto.find("on") >= 0) and (texto.find("all") >= 0) and (texto.find("pines") >= 0)) or ((texto.find("enciende") >= 0) and (texto.find("todos") >= 0) and (texto.find("pines") >= 0)):
		EncenderPinRele(7)
		EncenderPinRele(11)
		PlayAudio(idioma,"all_pines_on.mp3")
		return 1

	elif ((texto.find("all") >= 0) and (texto.find("lights") >= 0)) or ((texto.find("todas") >= 0) and (texto.find("luces") >= 0)):
		SwitchPinRele(7)
		SwitchPinRele(11)
		PlayAudio(idioma,"all_lights_switched.mp3")
		return 1
		
	elif (texto.find("primary") >= 0) or (texto.find("white") >= 0) or (texto.find("blanca") >= 0) or (texto.find("main") >= 0):
		SwitchPinRele(7)
		PlayAudio(idioma,"white_light_switched.mp3")
		return 1

	elif (texto.find("secondary") >= 0) or (texto.find("red") >= 0) or (texto.find("roja") >= 0) or (texto.find("rojo") >= 0):
		SwitchPinRele(11)
		PlayAudio(idioma,"red_light_switched.mp3")
		return 1
		
	elif ((texto.find("change") >= 0) and (texto.find("microphone") >= 0)) or ((texto.find("cambia") >= 0) and (texto.find("micrófono") >= 0)):
		global index_microphone, index_microphone_2
		if(index_microphone_2 != -1 and index_microphone != -1):
			tmp = index_microphone
			index_microphone = index_microphone_2
			index_microphone_2 = tmp
			PlayAudio(idioma,"microphone_has_changed.mp3")
		else:
			PlayAudio(idioma,"microphone_not_changed.mp3")
		return 1

	elif (texto.find("date") >= 0) or (texto.find("today") >= 0) or (texto.find("time") >= 0) or (texto.find("clock") >= 0) or (texto.find("hora") >= 0) or (texto.find("fecha") >= 0):
		now = datetime.now()
		RespuestadeVoz(idioma,current_date_format(idioma,now),"null",0)
		return 1

	elif (texto.find("gracias") >= 0) or (texto.find("thank") >= 0):
		PlayAudio(idioma,"youre_welcome.mp3")
		return 1
		
	elif ((texto.find("much") >= 0) and (texto.find("is") >= 0)) or ((texto.find("cuánto") >= 0) and (texto.find("es") >= 0)):
		if (texto.find("es") >= 0):
			text = CortarFrase1(texto,"es").split()
			if len(text) == 3 :
				if text[1] == "más":
					RespuestadeVoz(idioma,str(int(text[0]) + int(text[2])),"null")
				elif text[1] == "por":
					RespuestadeVoz(idioma,str(int(text[0]) * int(text[2])),"null")
				elif text[1] == "entre":
					if int(text[2]) != 0:
						RespuestadeVoz(idioma,str(int(text[0]) / int(text[2])),"null")
					else:
						RespuestadeVoz(idioma,"Cannot divide by zero","No se puede dividir por cero")
				elif text[1] == "menos":
					RespuestadeVoz(idioma,str(int(text[0]) - int(text[2])),"null")
		return 1
		
	elif (texto.find("di") >= 0) or (texto.find("repite") >= 0) or (texto.find("repeat") >= 0) or (texto.find("say") >= 0):
		if (texto.find("mí") >= 0):
			RespuestadeVoz(idioma,CortarFrase1(texto,"mí"),"null")
		elif (texto.find("mi") >= 0):
			RespuestadeVoz(idioma,CortarFrase1(texto,"mi"),"null")
		elif (texto.find("esto") >= 0):
			RespuestadeVoz(idioma,CortarFrase1(texto,"esto"),"null")
		elif (texto.find("me") >= 0):
			RespuestadeVoz(idioma,CortarFrase1(texto,"me"),"null")
		elif (texto.find("this") >= 0):
			RespuestadeVoz(idioma,CortarFrase1(texto,"this"),"null")
		return 1
			
	elif (texto.find("play") >= 0) or (texto.find("reproduce") >= 0) or (texto.find("pon") >= 0) or (texto.find("rola") >= 0) or (texto.find("music") >= 0) or (texto.find("música") >= 0):
		global musica_auto
		if (texto.find("stop") >= 0) or (texto.find("detén") >= 0) or (texto.find("silenc") >= 0) or (texto.find("para") >= 0):
			os.system("killall mpg321")
			musica_auto = 0

		elif (texto.find("aleatori") >= 0) or (texto.find("random") >= 0):
			musica_auto = 1
			hiloTmpA = threading.Thread(name='MusicaAleatoria',target=MusicaAleatoria,args=("zero",))
			hiloTmpA.start()
			
		elif (texto.find("song") >= 0):
			if(PlaySongInAnotherThr(CortarFrase1(texto,"song")) != 1):
				PlayAudio(idioma,"song_not_in_device.mp3")
			
		elif (texto.find("de") >= 0):
			if(PlaySongInAnotherThr(CortarFrase1(texto,"de")) != 1):
				PlayAudio(idioma,"song_not_in_device.mp3")
			
		elif (texto.find("cancion") >= 0):
			if(PlaySongInAnotherThr(CortarFrase1(texto,"cancion")) != 1):
				PlayAudio(idioma,"song_not_in_device.mp3")
		return 1
		
	elif (texto.find("caracola") >= 0) or (texto.find("mágica") >= 0) or (texto.find("magic") >= 0) or (texto.find("conch") >= 0):
		respuestas = ["yes.mp3", "maybe_someday.mp3", "i_do_not_believe_it.mp3", "no.mp3", "try_asking_again.mp3"]
		aleatorio = random.choice(respuestas)
		PlayAudio(idioma,aleatorio)
		return 1

	elif ((texto.find("add") >= 0) and (texto.find("reminder") >= 0)) or ((texto.find("agregar") >= 0) and (texto.find("recordatorio") >= 0)):
		PlayAudio(idioma,"add_reminder_insert_date.mp3")
		date = ObtenerComandoVoz().split()
		if(date != "zero" and len(date) == 3):
			if(date[0].isdigit() and date[2].isalpha()):
				months = ["january", "february", "march", "april", "may", "june", "july", "august", "september", "october", "november", "december"]
				if(idioma == "es"):
					months = ["enero", "febrero", "marzo", "abril", "mayo", "junio", "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre"]
				number_month = -1
				for i in range(len(months)):
					if months[i] == date[2]:
						number_month = i+1
						break
				if(number_month != -1 and comprobar_fecha(2020, number_month, int(date[0]), 0, 0, 0)):
					PlayAudio(idioma,"add_reminder_insert_text.mp3")
					texto_reminder = ObtenerComandoVoz()
					if(texto_reminder != "zero"):
						text_to_write = ""+date[0]+":"+str(number_month)+":2020:00:00|"+texto_reminder+"\n"
						RespuestadeVoz(idioma,"the reminder to write is: "+date[0]+":"+date[2]+", "+texto_reminder,"el recordatorio a grabar es: "+date[0]+":"+date[2]+", "+texto_reminder,0)
						archivo = open(path_files + "/reminders.txt", "a")
						archivo.write(text_to_write)
						archivo.close()
					else:
						PlayAudio(idioma,"add_reminder_text_not_found.mp3")
				else:
					PlayAudio(idioma,"add_reminder_month_or_day_incorrect.mp3")
			else:
				PlayAudio(idioma,"add_reminder_date_incorrect.mp3")
		else:
			PlayAudio(idioma,"add_reminder_not_have_date.mp3")
		return 1

	elif ((texto.find("buenos") >= 0) and (texto.find("días") >= 0)) or ((texto.find("good") >= 0) and (texto.find("morning") >= 0)):
		#PlayAudio(idioma,"good_morning_intro.mp3")
		now = datetime.now()
		RespuestadeVoz(idioma,"Good morning, "+current_date_format(idioma,now)+ ", you reminder list is: ","Buenos días mi lord, amo y señor, "+current_date_format(idioma,now)+ ", su lista de recordatorios es: ",0)
		recordatorios = 0
		try:
			archivo = open(path_files + "/reminders.txt", "r")
			now = datetime.now()
			tmp = now.strftime("%d:%m:%Y:%H:%M")
			for linea in archivo.readlines():
				linea = linea.rstrip("\r\n")
				nuevo = linea.split("|")
				date = nuevo[0].split(":")
				new_date = datetime(int(date[2]), int(date[1]), int(date[0]), int(date[3]), int(date[4]), 00, 00000)
				now = datetime.now()
				if now.date() == new_date.date():
					#if now.time() <= new_date.time(): # para saber si la hora aun no pasa
					#RespuestadeVoz(idioma,"Today at "+date[3]+":"+date[4]+" have the remember: "+nuevo[1],"Hoy a las "+date[3]+":"+date[4]+" tienes: "+nuevo[1]) # cuando se arregle lo de la hora se puede usar este y borrar la sig linea
					RespuestadeVoz(idioma,"Today have the remember: "+nuevo[1],"Hoy tienes: "+nuevo[1])
					recordatorios += 1
			archivo.close()
		except IOError:
			recordatorios = -1
			PlayAudio(idioma,"not_have_reminders_today.mp3")
		if recordatorios == 0:
			PlayAudio(idioma,"not_have_reminders_today.mp3")
		return 1
			
	else:
		#PlayEffect("super_mario_lose_life.mp3")
		PlayAudio(idioma,"order_not_recived.mp3")
		return 0

def ReconocimientoVoz():
	global index_microphone, index_microphone_2
	for index, name in enumerate(sr.Microphone.list_microphone_names()):
		print("Microphone with name \"{1}\" found for `Microphone(device_index={0})`".format(index, name)) # Muestra una lista con los microfonos conectados al sistema
		if (name.find(nombre_microfono_1) >= 0):
			PrintandSave("[Voz] El microfono si fue detectado [1].")
			index_microphone = index
		elif(name.find(nombre_microfono_2) >= 0):
			PrintandSave("[Voz] El microfono si fue detectado [2].")
			index_microphone_2 = index
		elif(index_microphone != -1 and index_microphone_2 != -1):
			break
			
	if 	index_microphone == -1 and index_microphone_2 != -1:
		index_microphone = index_microphone_2

	if index_microphone != -1:
		PrintandSave("[Voz] El sistema esta escuchando. microfono id: "+str(index_microphone))
		while(1):
			texto = ObtenerComandoVoz()
			if texto != "zero":
				#PrintandSave("[Voz] "+texto) # guarda los comandos que va escuchando
				EjecutarComando(texto)
	else:
		PrintandSave("[Voz] El microfono no fue detectado, y se cancela el reconocimiento de voz.")
	
############################### VARIABLES GLOBALES NECESARIAS ####################################

gpio.setwarnings(False)
gpio.setmode(gpio.BOARD) # enumerados los pines desde el 1 hasta el 40, seguidos o sea 1, 2, 3, 4...
gpio.setup(7, gpio.OUT)
gpio.setup(11, gpio.OUT)
gpio.setup(12, gpio.OUT) #ventilador

musica_auto        = 0
status_actual      = 0
index_microphone   = -1
index_microphone_2 = -1
ventilador_auto    = 1

##################################### INICIO DEL SCRIPT #########################################

hiloVoz = threading.Thread(target=ReconocimientoVoz)
hiloVoz.start()

hiloServidor = threading.Thread(target=ServidorComandos)
hiloServidor.start()

ApagarPinRele(7) # Al encender raspberry se emiten 0 en los pines y los reles se activan, esto los apaga.
ApagarPinRele(11)
PrintandSave("El sistema esta listo.")

############################### ENCENDIDO AUTOMATICO DE LUCES ####################################
while 1:

	hora_act = datetime.now().time()
	
	if (hora_act > hora_encendido) and (hora_act < hora_apagado):
		if status_actual == 0:
			status_actual = 1
			EncenderPinRele(11)
					
	elif (status_actual == 1):
		status_actual = 0
		ApagarPinRele(11)
		
					
	if((round(get_cpu_temp()) > 45 and ventilador_auto == 1) or (round(get_cpu_temp()) >= 58)):
		gpio.output(12, True)
	else:
		gpio.output(12, False)
		
	time.sleep(10)

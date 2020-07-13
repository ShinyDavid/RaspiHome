import os
import threading
from gtts import gTTS

class Voice_output():

	def __init__(self,audio_cache = "cache", audios_pre = "sounds_pre"):
		self.audios_cache = audio_cache
		self.path_audios_pregrabados = audios_pre

	def RespuestadeVoz(self,texto,idioma = "en",use_cache = 1,volumen = 100): # si texto_es == "null" se ejecutara texto_en en el idioma que venga solamente, hay que verificar que el tamaño del texto sea menor a 225
		if use_cache == 1:
			result = self.ClearText(texto)
			if os.path.isfile(self.audios_cache + "/"+ idioma + "_" + result + ".mp3"):
				os.system("mpg321 -g " +str(volumen)+ " " + self.audios_cache + "/"+ idioma + "_\"" + result + "\".mp3")
			else:
				tts = gTTS(text=texto, lang=idioma)
				tts.save(self.audios_cache + "/"+ idioma + "_" + result + ".mp3")
				os.system("mpg321 -g " +str(volumen)+ " " + self.audios_cache + "/"+ idioma + "_\"" + result + "\".mp3")
		else:
			tts = gTTS(text=texto, lang=idioma)
			tts.save("output.mp3")
			os.system("mpg321 -g "+str(volumen)+" output.mp3")

	def ClearText(self,texto): # En este caso estos simbolos se limpian ya que no se pueden escribir en una ruta, si se escriben el programa crashearia.
		caracteres = "¿?¡!"
		for i in range(len(caracteres)):
			texto = texto.replace(caracteres[i],"")
		return texto

	def PlayAudio(self,audiofile,lang = "en"): # Cuidado inverti el lenguaje y el audiofile
		os.system("mpg321 " + self.path_audios_pregrabados + "/" + lang + "/" + audiofile)
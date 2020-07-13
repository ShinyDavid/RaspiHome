import speech_recognition as sr

class Voice_input():

	index_microphone = -1

	def __init__(self,nombre_microfono,print_microphones=0):
		for index, name in enumerate(sr.Microphone.list_microphone_names()):
			if print_microphones == 1:
				print("Microphone with name \"{1}\" found for `Microphone(device_index={0})`".format(index, name)) # Muestra una lista con los microfonos conectados al sistema
			if (name.find(nombre_microfono) >= 0):
				self.index_microphone = index
				break
		if self.index_microphone == -1:
			print("Error: microphone not found")

	def ObtenerRespuestaVoz(self,idioma,print_msgs=0):
		recog = ("NULL") # Con mayuscula debido a que con la funcion lower hace que aunque la diga sera null (minuscula)
		while recog == "NULL":
			r = sr.Recognizer()
			speech = sr.Microphone(device_index=self.index_microphone)
			with speech as source:
				#audio = r.adjust_for_ambient_noise(source) # Hace retardo de 1 segundo para ajustar el ruido del ambiente
				audio = r.listen(source)
			if (idioma == "en"):
				try:
					recog = r.recognize_google(audio, language = 'en-US')
				except sr.UnknownValueError:
					if print_msgs == 1:
						print("Google Speech Recognition could not understand audio [EN]")			
				except sr.RequestError as e:
					if print_msgs == 1:
						print("Could not request results from Google Speech Recognition service; {0}".format(e))
					
			elif (idioma == "es"):
				try:
					recog = r.recognize_google(audio, language = 'es-MX')
				except sr.UnknownValueError:
					if print_msgs == 1:
						print("Google Speech Recognition could not understand audio [ES]")			
				except sr.RequestError as e:
					if print_msgs == 1:
						print("Could not request results from Google Speech Recognition service; {0}".format(e))

		return recog.lower()

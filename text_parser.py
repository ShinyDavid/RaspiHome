# pip3 install nltk
# pip3 install numpy
#import nltk # Muy interesante pero muy extensa, estudiarla mas
# pip3 install nameparser
from nameparser import HumanName # acurracy 5% :()

class Text_parser():

	def __init__(self,download_data = 1): # descargar los archivos necesarios
		print("none")
		#nltk.download('punkt')
		#nltk.download('averaged_perceptron_tagger')
		#nltk.download('maxent_ne_chunker')
		#nltk.download('words')

	def obtenerNombre(self,texto):
		name = HumanName(texto)
		name.string_format = "{first}"
		print(str(name))
		return str(name)
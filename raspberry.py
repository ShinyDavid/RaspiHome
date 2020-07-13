import RPi.GPIO as gpio

def iniciar(warnings,board_type,pines):
	gpio.setwarnings(warnings) 
	if board_type == "BOARD":
		gpio.setmode(gpio.BOARD) # enumerados los pines desde el 1 hasta el 40, seguidos o sea 1, 2, 3, 4...
	else:
		gpio.setmode(gpio.BCM)
	gpio.setup(pines, gpio.OUT)

def onRele(pin):
	try:
		gpio.output(pin, False)
	except:
		pass

def offRele(pin):
	try:
		gpio.output(pin, True)
	except:
		pass

def onPin(pin):
	try:
		gpio.output(pin, True)
	except:
		pass

def offPin(pin):
	try:
		gpio.output(pin, False)
	except:
		pass

def switchPin(pin):
	if gpio.input(pin) == 0:
		gpio.output(pin, True)
	else:
		gpio.output(pin, False)

def get_cpu_temp(): # devuelve la temperatura (del procesador) en grados centigrados
	tempFile = open( "/sys/class/thermal/thermal_zone0/temp" )
	cpu_temp = tempFile.read()
	tempFile.close()
	return float(cpu_temp)/1000

def Oscilar(pin,frecuencia):
	p = gpio.PWM(pin, frecuencia)
	p.start(1)
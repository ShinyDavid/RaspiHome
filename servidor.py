import socket

class Servidor():

	def __init__(self, puerto_conexion=3333, sock=None):
		if sock is None:
			self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		else:
			self.sock = sock
		self.sock.bind(("", puerto_conexion))
		self.sock.listen(20)

	def recibir(self):
		connect, addr = self.sock.accept()
		str_recv = connect.recvfrom(1024)
		connect.close()
		return str_recv[0].decode()
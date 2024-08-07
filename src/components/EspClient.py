import socket
import yaml

class EspClient:
	def __init__(self):
		self.host = 0
		self.port = 0
		self.set_connection_config()
		self.socket = 0
		self.conn = True

	def connect(self):
		self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.socket.connect((self.host, self.port))
		self.conn = True
	
	def send_data(self, msg):
		self.socket.sendall(msg.encode("UTF-8"))
		self.socket.send("\0".encode("UTF-8"))
		self.socket.shutdown(1)

	def receive_data(self, buffSize):
		return self.socket.recv(buffSize).decode('UTF-8')
	
	def close(self):
		self.socket.shutdown(0)
		self.socket.close()
		self.conn = False

	def set_connection_config(self):
		with open('local_conf.yaml', 'r') as file:
			conf = yaml.safe_load(file)
			self.host = conf['client']['host']
			self.port = conf['client']['port']
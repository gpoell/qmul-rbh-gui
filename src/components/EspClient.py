import socket

class EspClient:
	def __init__(self, host, port):
		self.host = host
		self.port = port
		self.socket = 0
		self.conn = True
		self.data = []

	def connect(self):
		self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.socket.connect((self.host, self.port))
		self.conn = True
	
	def send_data(self, msg):
		self.socket.sendall(msg.encode("UTF-8"))
		self.socket.shutdown(1)

	def receive_data(self):
		return self.socket.recv(24).decode('UTF-8')
	
	def close(self):
		self.socket.shutdown(0)
		self.socket.close()
		self.conn = False

	def collect_sensor_data(self, command):
		self.connect()
		self.send_data(command)
		self.receive_data()
		self.close()
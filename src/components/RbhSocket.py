import socket

class RbhSocket:
	def __init__(self, host, port):
		self.host = host
		self.port = port
		self.socket = 0
		self.conn = False
		self.data = []

	def connect(self):
		self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.socket.connect((self.host, self.port))
		self.conn = True
	
	def send_data(self, msg):
		self.socket.sendall(msg.encode("UTF-8"))
		self.socket.shutdown(1)

	def receive_data(self):
		# Decode First Status Byte
		batch = self.socket.recv(64).decode('UTF-8')

		# Receive Data Batches
		while batch != '':
			batch = self.socket.recv(2048).decode("UTF-8")
			self.data.append(batch)
		
		# Remove Terminating Byte
		del self.data[-1]
	
	def close(self):
		self.socket.shutdown(0)
		self.socket.close()
		self.conn = False

	def collect_sensor_data(self, command):
		self.connect()
		self.send_data(command)
		self.receive_data()
		self.close()
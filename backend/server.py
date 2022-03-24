import socket
import threading

# Constants
IP       = "127.0.0.1"
PORT     = 6969
BUFFER   = 1024

class Server:
	def __init__(self, ip, port):
		self.running = True
		self.ip = ip
		self.port = port

		# Holds all the clients connected
		self.client_id = 0
		self.clients = {}
		self.usrname = ""
	
	def __create_sv(self):
		# Socket client
		self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM);
		self.server.bind((self.ip, self.port))

	def __handle_client(self, conn, usrname):
		print(f"{usrname} just connected.")
		while True:
			try:
				audio = conn.recv(BUFFER)
				if not audio:
					break
				
				# Sending the audio data to all the clients except the one who sent it
				for i in self.clients:
					if i != usrname:
						self.clients[i].send(audio)

			except Exception as e:
				print(f"[ERROR] {usrname}: {e}")
				break

		conn.close()
		print(f"{usrname} just disconnected.")
		self.clients.pop(usrname)
	
	def close(self):
		print("[INFO]: Server has been closed.")
	
	def run(self):
		self.__create_sv()

		print(f"[INFO]: Server started on {self.ip}:{self.port}")
		self.server.listen()
		while self.running:
			try:
				conn, addr = self.server.accept()
				self.usrname = conn.recv(BUFFER).decode('utf-8')
				self.usrname = self.usrname + f"#{self.client_id}"

				#updating dictonary
				self.clients.update({self.usrname: conn})
				

				# Thread for new connection
				thread = threading.Thread(target = self.__handle_client, args = (conn, self.usrname))
				thread.start()

				self.client_id += 1

			except KeyboardInterrupt:
				self.running = False
			except Exception as e:
				self.running = False
				print(f"[ERROR]: {e}")

if __name__ == "__main__":
	server = Server(IP, PORT)
	server.run()
	server.close()


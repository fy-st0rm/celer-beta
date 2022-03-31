import socket
import pyaudio
import threading

# Constants
BUFFER   = 1024
FORMAT   = pyaudio.paInt16
CHANNELS = 2
RATE     = 44100

class Client:
	def __init__(self):
		self.ip = ""
		self.port = 0

		self.running = True
		self.mute = False
		self.deafen = False

	def init(self, ip, port):
		self.ip = ip
		self.port = port
		
		res = self.__create_cli()
		if res: print(f"[INFO]: Connected to the {self.ip}:{self.port}")
		res = self.__pyaudio_init()

		return res 
	
	def __create_cli(self):
		try:
			self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			print(f"[INFO] Connecting to {self.ip}:{self.port}")
			self.client.connect((self.ip, self.port))
			return True
		except Exception as e:
			print(f"[ERROR]: {e}")
			return False
	
	def __pyaudio_init(self):
		try:
			self.p_cli = pyaudio.PyAudio()
			self.istream = self.p_cli.open(format = FORMAT, channels = CHANNELS, rate = RATE, input = True, frames_per_buffer = BUFFER)
			self.ostream = self.p_cli.open(format = FORMAT, channels = CHANNELS, rate = RATE, output = True)
			return True
		except Exception as e:
			print(f"[ERROR]: {e}")
			return False

	def __listen(self):
		while self.running:
			if not self.deafen: # If deafen dont receive the audio
				audio = self.client.recv(BUFFER)
				if audio:
					self.ostream.write(audio)

	def send_username(self, name):
		self.client.send(name.encode('utf-8'))
	
	def close(self):
		self.running = False
		self.istream.stop_stream()
		self.istream.close()
		self.ostream.stop_stream()
		self.ostream.close()
		self.p_cli.terminate()

		print("[INFO]: Disconnected from the server.")

	def __record(self):
		while self.running:
			try:
				if not self.mute and not self.deafen: # If mute and deafen is activated ignore the mic input
					audio = self.istream.read(BUFFER)
					if audio:
						self.client.send(audio)
			except KeyboardInterrupt:
				self.running = False
			except Exception as e:
				print(f"[ERROR]: {e}")
				self.running = False
	
	def run(self):
		listen_thread = threading.Thread(target = self.__listen)
		listen_thread.start()

		record_thread = threading.Thread(target = self.__record)
		record_thread.start()

if __name__ == "__main__":
	client = Client()
	client.init("127.0.0.1", 6969)
	client.send_username("Slok")
	client.run()
	running = True
	while running:
		if not client.record(): running = False

from listbox import *
from textbox import *
from curses  import wrapper
import platform
import sys

# Importing the backend client
sys.path.append("../backend")
from client import *

#TODO: [ ] Stop print output 
#TODO: [ ] Maintain ip and port checks and display some errors
#TODO: [ ] A help window
#TODO: [ ] Output log window
#TODO: [X] Connect client backend
#TODO: [X] Voice call window ([ ] mem list, [ ] mute and deafen button, [ ] Disconnect function)


MAX_ROWS = MAX_COLS = 20

#Color index
SELECTED = 1
INFO = 2
ERROR = 3

# ALT LOGO
#█▀▀ █▀▀ █░░ █▀▀ █▀█
#█▄▄ ██▄ █▄▄ ██▄ █▀▄


LOGO = [
" ██████ ███████ ██      ███████ ██████ \n",
"██      ██      ██      ██      ██   ██\n",
"██      █████   ██      █████   ██████ \n",
"██      ██      ██      ██      ██   ██\n",
" ██████ ███████ ███████ ███████ ██   ██\n"
]


"""
[#] MAIN WINDOW
"""
class Celer:
	def __init__(self, surface):
		self.surface = surface
		self.running = True

		self.connected = False
		self.client = Client()
	
	"""
	* Initializing functions
	"""
	def __create_widgets(self):
		self.listbox = ListBox(self.surface, "Servers", 0, 0, 30, 9, SELECTED)
		self.textbox = Textbox(self.surface, 0, 0, 0, 0)

	def __init_colors(self):
		curses.init_pair(SELECTED, curses.COLOR_BLACK, curses.COLOR_YELLOW)
	
	def init(self):
		# Hiding the cursor
		curses.curs_set(0)

		# Setting the terminal size
		rows, cols = self.surface.getmaxyx()
		if platform.system() == "Windows":
			curses.resize_term(rows, cols)
		else:
			curses.resizeterm(rows, cols)

		self.__init_colors()
		self.__create_widgets()
	
	"""
	* Event handleing functions
	"""
	def __resize(self):
		rows, cols = self.surface.getmaxyx()
		# Prevents resizing the curses elements if the rows and cols are smaller than 25
		if rows > MAX_ROWS and cols > MAX_COLS:
			w = int(cols - 20)
			h = int(rows - 10)
			x = int(cols / 2) - int(w / 2)
			y = int(rows / 2) - int(h / 2) + 2
			self.listbox.relocate(x, y, w, h)

			h = 3
			y = rows - 3
			self.textbox.relocate(x, y, w, h)
	
	def __change_focus(self):
		if self.listbox.focus:
			self.listbox.focus = False
			self.textbox.focus = True
		elif self.textbox.focus:
			self.textbox.focus = False
			self.listbox.focus = True
	
	def __event(self):
		key = self.surface.getch()
		
		# 113 = q
		if key == 113:
			self.running = False
			self.client.close()

		# 9 = TAB
		elif key == 9:
			self.__change_focus()
		
		# 10 = ENTER 
		elif key == 10:
			text = self.textbox.get_text().split(":")
			self.textbox.clear()

			if len(text) < 2:
				exit()

			ip = text[0]
			port = int(text[1])
			res = self.client.init(ip, port)
			print(res, ip, port)
			# TODO: Check for the initializing error here!
			if res:
				self.connected = True
				self.client.send_username("Slok")
				scene(self.surface, MainWin)
				self.client.run()


		elif key == curses.KEY_RESIZE:
			self.__resize()

		self.listbox.handle_key(key)
		self.textbox.handle_key(key)

	"""
	* Rendering function
	"""
	def __render(self):
		self.surface.clear()
		self.surface.refresh()
		self.listbox.draw()
		self.textbox.draw()

		# Rendering logo
		rows, cols = self.surface.getmaxyx()
		if rows > MAX_ROWS and cols > MAX_COLS:
			x = int(cols/2) - int(len(LOGO[0])/2)
			y = 1
			for i in LOGO:
				self.surface.addstr(y, x, i)
				y += 1
	
	"""
	* Main loop function
	"""

	def run(self):
		for i in range(10):
			self.listbox.insert(f"Server#{i}")

		while self.running:
			self.__render()
			self.__event()


"""
[*]MAIN WINDOW
"""
class MainWin:
	def __init__(self, surface):
		self.surface = surface
		self.running = True
	"""
	* Initializing functions
	"""
	def __create_widgets(self):
		self.server_clients = ListBox(self.surface, "Clients", 0, 0, 20, 9, SELECTED) 

	def __init_colors(self):
		curses.init_pair(INFO, curses.COLOR_GREEN, curses.COLOR_BLACK)
		curses.init_pair(SELECTED, curses.COLOR_BLACK, curses.COLOR_YELLOW)

	
	def init(self):
		# Hiding the cursor
		curses.curs_set(0)

		# Setting the terminal size
		rows, cols = self.surface.getmaxyx()
		if platform.system() == "Windows":
			curses.resize_term(rows, cols)
		else:
			curses.resizeterm(rows, cols)

		self.__init_colors()
		self.__create_widgets()
	
	"""
	* Event handleing functions
	"""
	def __resize(self):
		rows, cols = self.surface.getmaxyx()
		# Prevents resizing the curses elements if the rows and cols are smaller than 25
		if rows > MAX_ROWS and cols > MAX_COLS:
			w = int(cols - 40)
			h = int(rows - 20)
			x = int(cols / 2) - int(w / 2)
			y = int(rows / 2) - int(h / 2)
			self.server_clients.relocate(x, y, w, h)

	def __change_focus(self):
		if self.server_clients.focus:
			self.server_clients.focus = True

	def __event(self):
		key = self.surface.getch()
		
		# 113 = q
		if key == 113:
			self.running = False

			#switches scene
			scene(self.surface, Celer)
			self.client.close()
		# 9 = TAB
		elif key == 9:
			self.__change_focus()

		elif key == curses.KEY_RESIZE:
			self.__resize()

	"""
	* Rendering function
	"""
	def __render(self):
		self.surface.clear()
		self.surface.refresh()

		self.server_clients.draw()
		rows, cols = self.surface.getmaxyx()
		if rows > MAX_ROWS and cols > MAX_COLS:
			x = int(cols/2) - int(len(LOGO[0])/2)
			y = 1
			for i in LOGO:
				self.surface.addstr(y, x, i)
				y += 1

		if rows > MAX_ROWS and cols > MAX_COLS:
			x = int((rows /2) + 10)
			y = int((rows /2) + 5)
			#INFO STUFF
			self.surface.addstr(y, x,"Currently Connected To: [IP HERE] ",curses.color_pair(INFO))
			self.surface.addstr(y+6,x,"Control Buttons")
			self.surface.addstr(y+8,x,"MUTE[x]  DEAFEN[Z]  DISCONNECT[Q]  ")

	
	"""
	* Main loop function
	"""
	def run(self):
		for i in range(3):
			if i == 2:
				self.server_clients.insert(f"Client{i} [ x][ x]")
			else:
				self.server_clients.insert(f"Client#{i}")
		while self.running:
			self.__render()
			self.__event()

"""
*Scene Change Function
"""
def scene(stdscr, scene):
	scene = scene(stdscr)
	scene.init()
	scene.run()

def main(stdscr):
	scene(stdscr, Celer)

wrapper(main)


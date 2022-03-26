from listbox import *
from textbox import *
from curses  import wrapper
import platform
MAX_ROWS = MAX_COLS = 20

SELECTED = 1

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


class Celer:
	def __init__(self, surface):
		self.surface = surface
		self.running = True
	
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

		# 9 = TAB
		elif key == 9:
			self.__change_focus()
		
		# 10 = ENTER 
		elif key == 10:
			text = self.textbox.get_text()
			self.textbox.clear()

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

def main(stdscr):
	celer = Celer(stdscr)
	celer.init()
	celer.run()

wrapper(main)


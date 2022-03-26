import curses

class Textbox:
	def __init__(self, surface, x, y, w, h):
		self.surface = surface
		self.x = x
		self.y = y
		self.w = w
		self.h = h
		
		self.win = curses.newwin(self.h, self.w, self.y, self.x)
		self.text = ""
		self.focus = True
	
	def relocate(self, x, y, w, h):
		self.x = x
		self.y = y
		self.w = w
		self.h = h
		self.win = curses.newwin(self.h, self.w, self.y, self.x)
	
	def get_text(self):
		return self.text
	
	def clear(self):
		self.text = ""
		self.win.clear()
		self.win.refresh()
	
	def insert(self, char):
		if len(self.text) < self.w - 2:
			self.text += char

	def handle_key(self, key):
		if self.focus:

			# Backspace
			if key == 127: 
				self.text = self.text[:-1]
			
			# All typable characters
			elif 33 <= key <= 126: 
				self.insert(chr(key))

			# Space
			elif key == 32:
				self.insert(" ")

	def __render_text(self):
		self.win.addstr(1, 1, self.text)
		if self.focus:
			self.win.addstr(1, len(self.text) + 1, "█")
		self.win.refresh()

	def draw(self):
		self.win.erase()
		self.win.box()
		self.win.refresh()
		self.__render_text()

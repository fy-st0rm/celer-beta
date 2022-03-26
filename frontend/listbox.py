import curses


class ListBox:
	"""
	* A curses listbox class 
	"""

	def __init__(self, surface, x, y, w, h, selected_color):
		self.surface = surface
		self.x = x
		self.y = y
		self.w = w
		self.h = h
		self.selected_color = curses.color_pair(selected_color)

		self.win = curses.newwin(self.h, self.w, self.y, self.x)

		# listbox items 
		self.items = []
		self.start = 0
		self.end = 0
		self.selected = 0
	
	def select_up(self):
		if self.selected > 0:
			self.selected -= 1
			
			# Scrolling up when we reach the topmost element
			if self.selected == self.start - 1 and self.start:
				self.start -= 1
				self.end -= 1
	
	def select_down(self):
		if self.selected < len(self.items) - 1:
			self.selected += 1

			# When the selected line gets deeper than the window
			if self.selected >= self.h - 2:
				self.start += 1
				self.end += 1
				if self.end >= len(self.items):
					self.end = len(self.items)
	
	def insert(self, value):
		self.items.append(value)

		if len(self.items) >= self.h - 2:
			self.end = self.h - 2
		else:
			self.end = len(self.items)
	
	def draw(self):
		self.win.erase()
		self.win.box()

		x = 1 
		y = 1

		for i in range(self.start, self.end, 1):
			if i == self.selected:
				self.win.addstr(y, x, self.items[i], self.selected_color)
			else:
				self.win.addstr(y, x, self.items[i])
			self.win.refresh()
			y += 1

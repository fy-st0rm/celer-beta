from listbox import *
from curses  import wrapper

SELECTED = 1

def main(stdscr):
	curses.curs_set(0) # Hiding the cursor

	stdscr.clear()
	stdscr.refresh()

	# Initializing the color
	curses.init_pair(SELECTED, curses.COLOR_BLACK, curses.COLOR_YELLOW)

	# Creating listboxes
	listbox = ListBox(stdscr, 0, 0, 30, 9, SELECTED)
	listbox2 = ListBox(stdscr, 40, 0, 30, 9, SELECTED)

	# Inserting value in listbox
	for i in range(10):
		listbox.insert("Hello world" + str(i))

	for i in range(10):
		listbox2.insert("Hello world" + str(i))


	# Main loop
	running = True
	while running:
		stdscr.clear()
		stdscr.refresh()
		listbox.draw()
		listbox2.draw()

		key = stdscr.getkey()
		if key == "KEY_UP":
			listbox.select_up()
			listbox2.select_up()
		elif key == "KEY_DOWN":
			listbox.select_down()
			listbox2.select_down()
		elif key == "q":
			running = False

wrapper(main)

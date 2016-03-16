import time
from unicurses import *	

class timer:
	def __init__(self):
		self.str_time, self.passed_time = 0.0,0.0
	
	def start(self):
		self.str_time = time.time()
		return 1
	
	def stop(self):
		self.passed_time = time.time() - self.str_time
		return 1
	
	def get_time(self):
		return time.time() - self.str_time
	
	def restart(self):
		self.str_time = time.time() - self.passed_time
		return 1
	
	def clock(self, intervals):
		self.period = 1.0 / intervals
		if self.period > self.get_time():
			return True
		else:
			self.start()
			return False
	
	def close(self):
		self.str_time, self.passed_time = NULL, NULL
		return 1

class board:
	def __init__(self, ply):
		self.original_board = [[]]
		self.objects= [pad(1,2,[['|'],['|'],['|'],['|'],['|']]),pad(35,2,[['|'],['|'],['|'],['|'],['|']]),ball(13,13,[['@']])]
		self.players = ply
		self.inputs= [0,0,0]
	
	def create_board(self,wt, ht):
		self.width, self.height = wt, ht
		for h in range(0,self.height):
			self.original_board.append([])
			if h == 0 or h==self.height-1:
				for w in range(0,self.width):
					self.original_board[h].append(" = ")
			else:
				for w in range(0, self.width):
					if w == 0 or w == self.width-1:
						self.original_board[h].append(" | ")
					else:
						self.original_board[h].append(" - ")
	
	def print_board(self):
		for i in range(0,len(self.original_board)):
			mvaddstr(i,0,"".join(self.original_board[i]))
		
	def board_controler(self, inputs):
		if self.players == 2:
			self.inputs[0] = inputs[0]
			self.inputs[1] = inputs[1]
			self.update_objects()
			
		elif self.players == 1:
			self.inputs[0] = inputs[0:1]
			self.inputs[1] = self.computer()
			self.update_objects()
		
		else:
			pass
			
	def update_objects(self):
		c = 0
		for o in self.objects:
			o.update(1)
			self.coord = o.get_coordinates()
			self.image = o.get_image()
			for i in range(len(self.image)): 
				mvaddstr(self.coord[1]+i,self.coord[0]*2+1,"".join(self.image[i][0]))
			c+=1
	
	def computer(self):
		
		return 1
	
class object:
	def __init__(self, x_coordinate, y_coordinate, image):
		self.x,self.y,self.image = x_coordinate, y_coordinate, image
		
	def update(self, direction):
		pass

	def get_coordinates(self):
		return [self.x, self.y]
		
	def get_image(self):
		return self.image


class pad(object):
	def update(self, direction):
		self.velocity = direction
		if self.y != 1 or self.y != 19:
			self.y += self.velocity
		
		
class ball(object):
	def update(self, direction):
		self.flag = False
		self.velocity = [0,0]
		if self.velocity[0]+self.x !=0 or self.velocity[0]+self.x != 25:
			self.x +=self.velocity[0]
			if self.x < 0 or self.x > 25:
				self.flag = True
		else:
			pass
		
		if self.velocity[1]+self.y !=0 or self.velocity[1]+self.y != 25:
			self.y +=self.velocity[1]
		else:
			pass
	
		

game_board = board(1)
game_board.create_board(10,10)

HEIGHT = 50
WIDTH = 50 
key = 0 
stdscr = initscr()
noecho()
clear()
curs_set(0)
game_win = newwin(HEIGHT, WIDTH, 0, 0)
game_board.print_board()
keypad(game_win, True)
refresh()
nodelay(stdscr,True)
system_clock = timer()
system_clock.start()

while True:
	key_state=[0,0]
	
	while system_clock.clock(5):
		key = wgetch(stdscr)
		if key == ord('w'):
			key_state[0]= -1
		elif key == ord('s'):
			key_state[0]=1
		elif key == ord('q'):
			break
	
	clear()
	game_board.print_board()
	game_board.board_controler(key_state)
	refresh()
	
	if key == ord('q'):
		break		


game_board.board_controler(key_state)
refresh()
endwin()
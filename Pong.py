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
		self.positions = [[1,2],[23,2],[13,13]]
		self.objects= [pad(self.positions[0][0],self.positions[0][1],[['|'],['|'],['|'],['|'],['|']]),
					pad(self.positions[1][0],self.positions[1][1],[['|'],['|'],['|'],['|'],['|']]),
					ball(self.positions[2][0],self.positions[2][0],[['@']])]
		self.players = ply
		self.inputs= [[0,0],[0,0],[0,0]]
		
	
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
		clear()
		self.print_board()
		if self.players == 2:
			self.inputs[0][0] = inputs[0]
			self.inputs[1][0] = inputs[1]
			self.update_objects()
			
		elif self.players == 1:
			self.inputs[0][0] = inputs[0]
			self.inputs[1][0] = self.computer()
			self.update_objects()
		
		else:
			pass
		refresh()
		
	def update_objects(self):
		c = 0
		for o in self.objects:
			o.update(self.inputs[c])
			self.positions[c] = o.get_coordinates()
			self.image = o.get_image()
			for i in range(len(self.image)): 
				mvaddstr(self.positions[c][1]+i,self.positions[c][0]*3+1,"".join(self.image[i][0]))
			c+=1
	
	def computer(self):
		
		return 0
	
class object:
	def __init__(self, x_coordinate, y_coordinate, image):
		self.x,self.y,self.image = x_coordinate, y_coordinate, image
		self.velocity = [1,1]
	def update(self, direction):
		pass

	def get_coordinates(self):
		return [self.x, self.y]
		
	def get_image(self):
		return self.image


class pad(object):
	def update(self, direction,  positions=0):
		if self.y + direction[0] >= 1 and self.y + direction[0] <= 19:
			self.y += direction[0]
		
class ball(object):
	def update(self, direction, positions=0):
		
		if self.velocity[0] + self.x > 1 and self.velocity[0]+self.x < 23:
			self.x += self.velocity[0]
			
		else:
			if self.velocity[0] + self.x < 1:
				if self.y in range(1,position[0][1]):
					self.x -= self.velocity[0] + self.x
				
				else:
					pass
				
			elif self.velocity[0] + self.x > 24:
				if self.y in range(1,position[1][1]):
					self.x = 47 - self.velocity[0] + self.x
					
				else:
					pass
					
			self.velocity[0] = - self.velocity[0]				
		
		if self.velocity[1] + self.y > 0 and self.velocity[1] + self.y < 24:
			self.y += self.velocity[1]
		
		else:
			
			if self.velocity[1] + self.y < 0:
				self.y = abs(self.velocity[1] + self.y)
			
			elif self.velocity[1] + self.y > 25:
				self.y = 49 - self.velocity[1] - self.y
				
			self.velocity[1] = -self.velocity[1]
			
	

def main():
	game_board = board(2)
	game_board.create_board(25,25)
	
	HEIGHT = 50
	WIDTH = 50 
	key = 0 
	stdscr = initscr()
	noecho()
	clear()
	curs_set(0)
	game_win = newwin(HEIGHT, WIDTH, 0, 0)
	game_board.print_board()
	keypad(stdscr, True)
	refresh()
	nodelay(stdscr,True)
	system_clock = timer()
	system_clock.start()
	
	while True:
		key_state=[0,0]
		
		while system_clock.clock(10):
			key = wgetch(stdscr)
			if key == ord('a'):
				key_state[0]= -1
			elif key == ord('s'):
				key_state[0]=1
			if key == ord('o'):
				key_state[1]=-1
			elif key == ord('p'):
				key_state[1]=1
			if key == ord('q'):
				break
		game_board.board_controler(key_state)
		
		if key == ord('q'):
			break		
	
	refresh()
	endwin()


if __name__ == "__main__":
	main()

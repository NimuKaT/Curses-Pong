import time
from unicurses import *	
import random

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
		self.positions = [[1,10,[0,0]],[23,10,[0,0]],[13,13,[1,1]]]
		self.objects= [pad(self.positions[0][0],self.positions[0][1],[['|'],['|'],['|'],['|'],['|']]),
					pad(self.positions[1][0],self.positions[1][1],[['|'],['|'],['|'],['|'],['|']]),
					ball(self.positions[2][0],self.positions[2][0],[['@']])]
		self.players = ply
		self.inputs = [[0,0],[0,0],[0,0]]
		self.score = [0,0] 
		
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
			
		mvaddstr(27, 20, str.format("Player 1: {0} || Player 2: {1}",self.score[0], self.score[1] ))
		
	def board_controler(self, inputs):
		clear()
		self.print_board()
		if self.players == 2:
			if self.objects[2].get_flag() == 0:
				self.inputs[0][1] = inputs[0]
				self.inputs[1][1] = inputs[1]
				self.update_objects()
			
			else:
				if self.objects[2].get_flag() == 1:
					self.score[0] += 1
				elif self.objects[2].get_flag() == 2:
					self.score[1] += 1
				self.objects[2].reset_ball()
			
		elif self.players == 1:
			if self.objects[2].get_flag() == 0:
				self.inputs[0][1] = inputs[0]
				self.inputs[1][1] = self.computer(1)
				self.update_objects()
			else:
				if self.objects[2].get_flag() == 1:
					self.score[0] += 1
				elif self.objects[2].get_flag() == 2:
					self.score[1] += 1
				self.objects[2].reset_ball()
			
		elif self.players == 3:
			if self.objects[2].get_flag() == 0:
				self.inputs[0][1] = self.computer(0)
				self.inputs[1][1] = self.computer(1)
				self.update_objects()
			else:
				if self.objects[2].get_flag() == 1:
					self.score[0] += 1
				elif self.objects[2].get_flag() == 2:
					self.score[1] += 1
				self.objects[2].reset_ball() 
		refresh()
		
	def update_objects(self):
		c = 0
		for o in self.objects:
			o.update(self.inputs[c],self.positions)
			self.positions[c] = o.get_coordinates()
			self.image = o.get_image()
			for i in range(len(self.image)): 
				mvaddstr(self.positions[c][1]+i,self.positions[c][0]*3+1,"".join(self.image[i][0]),COLOR_PAIR(c+1))
			c+=1
	
	def computer(self, pn):
		self.result = 0
		if self.positions[2][1] != self.positions[pn][1]+2:
			if self.positions[2][1] > self.positions[pn][1]+2:
				self.result = 1
			
			elif self.positions[2][1] < self.positions[pn][1]+2:
				self.result = -1
			
		return self.result
	
class object:
	def __init__(self, x_coordinate, y_coordinate, image):
		self.x,self.y,self.image = x_coordinate, y_coordinate, image
		self.velocity = [0,0]
		
	def update(self, direction):
		pass

	def get_coordinates(self):
		return [self.x, self.y, self.velocity]
		
	def get_image(self):
		return self.image


class pad(object):
	def update(self, direction,  positions=0):
		if direction[1] == 0:
			if self.velocity[1] != 0:
				self.velocity[1] = 0	
		
		elif abs(self.velocity[1]+direction[1]) <= 3:
			if abs(self.velocity[1]+direction[1]) > abs(self.velocity[1]):
				self.velocity[1] += direction[1]
			else:
				self.velocity[1] = direction[1]
				
		
		if self.y + self.velocity[1] >= 1 and self.y + self.velocity[1] <= 19:
			self.y += self.velocity[1]
		
		elif self.y + self.velocity[1] < 1:
			self.y = 1
			self.velocity[1] = 0
			
		elif self.y + self.velocity[1] > 19:
			self.y = 19
			self.velocity[1] = 0
		
class ball(object):
	def __init__(self, x_coordinate, y_coordinate, image):
		self.x,self.y,self.image = x_coordinate, y_coordinate, image
		self.velocity = [1,1]
		self.flag = 0
	
	def update(self, direction, positions=0):
		
		if self.velocity[1] + self.y > 0 and self.velocity[1] + self.y < 24:
			self.y += self.velocity[1]
		
		else:
			
			if self.velocity[1] + self.y < 0:
				self.y = abs(self.velocity[1] + self.y)
			
			elif self.velocity[1] + self.y > 25:
				self.y = 49 - self.velocity[1] - self.y
				
			self.velocity[1] = -self.velocity[1]
		
		
		if self.velocity[0] + self.x > 1 and self.velocity[0]+self.x < 23:
			self.x += self.velocity[0]
		
		else:
			if self.velocity[0] + self.x <= 1:
				if self.y in range(positions[0][1],positions[0][1]+5):
					if positions[0][2][1] == 0 and self.velocity[0] > -2:
						self.velocity[0] -= 1
					else:
						self.velocity[1] += positions[0][2][1]
					self.x -= self.velocity[0] - self.x + 1
					
				else:
					self.x = 1
					self.flag = 2
					
			elif self.velocity[0] + self.x >= 23:
				if self.y in range(positions[1][1],positions[1][1]+5):
					if positions[1][2][1] == 0 and self.velocity[0] < 2:
						self.velocity[0] += 1
					else:
						self.velocity[1] += positions[1][2][1]
					self.x = 45 - self.velocity[0] - self.x
				
				else:
					self.x = 23
					self.flag = 1
				
			self.velocity[0] = - self.velocity[0]
		
	def get_flag(self):
		return self.flag
	
	def reset_ball(self):
		self.flag = 0
		self.x = 13
		self.y = 13
		self.velocity[0] = -int(self.velocity[0]/abs(self.velocity[0]))
		self.velocity[1] = random.choice([-2,-1,1,2])

def main():
	game_board = board(3)
	game_board.create_board(25,25)
	
	HEIGHT = 50
	WIDTH = 50 
	key = 0 
	stdscr = initscr()
	noecho()
	clear()
	curs_set(0)
	start_color()
	game_win = newwin(HEIGHT, WIDTH, 0, 0)
	game_board.print_board()
	keypad(stdscr, True)
	refresh()
	nodelay(stdscr,True)
	
	init_pair(1, COLOR_RED, COLOR_WHITE)
	init_pair(2, COLOR_GREEN, COLOR_WHITE)
	init_pair(3, COLOR_MAGENTA, COLOR_WHITE)
	init_pair(4, COLOR_BLACK, COLOR_WHITE)
	bkgd(COLOR_PAIR(4))
	
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

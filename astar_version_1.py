import pygame
import math
import queue
import time
from queue import PriorityQueue

WIDTH = 800
WIN = pygame.display.set_mode((WIDTH, WIDTH))  #output window make it a square
pygame.display.set_caption("PATHFINDER VISUALIZER OP")

#colour RGB codes
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (88, 204, 207)
YELLOW = (255, 255, 0)
BLUE = (255, 255, 255)
BLACK = (0, 0, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165 ,0)
GREY = (128, 128, 128)
TURQUOISE = (64, 224, 208)

class Spot:  #tool track the nodes in the grid depending on colour;
	def __init__(self, row, col, width, total_rows):
		self.row = row
		self.col = col
		self.x = row * width  #size of node
		self.y = col * width  #initial colour of grid
		self.color = BLUE
		self.neighbors = []
		self.width = width
		self.total_rows = total_rows

	def get_pos(self):      #access the node using the rows and coloums(int,int)
		return self.row, self.col

	def is_closed(self):
		return self.color == RED  #check colour of closed or already used set of nodes(bool)

	def is_open(self):
		return self.color == GREEN #check colour of open set of nodes(bool)

	def is_barrier(self):
		return self.color == BLACK #check colour of obstacle(bool)

	def is_start(self):
		return self.color == ORANGE #check colour of start node(bool)

	def is_end(self):
		return self.color == TURQUOISE #check colour of end node(bool)

	def reset(self):
		self.color = BLUE #makes all nodes BLUE

	def make_start(self): #makes start node orange
		self.color = ORANGE

	def make_closed(self):  #makes closed node red
		self.color = RED

	def make_open(self):  #makes open node green
		self.color = GREEN

	def make_barrier(self):  #makes wall/barrier node black
		self.color = BLACK

	def make_end(self):  #makes final node turquoise
		self.color = TURQUOISE

	def make_path(self):  #makes final path nodes purple
		self.color = PURPLE

	def draw(self, win):  #draw the cubes on the screen
		pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width)) #etai hocchilo na

	def update_neighbors(self, grid): #append the neighbours of a node into the self.neighbour[] list
		self.neighbors = []           #blank list
		if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].is_barrier(): # DOWN
			self.neighbors.append(grid[self.row + 1][self.col])

		if self.row > 0 and not grid[self.row - 1][self.col].is_barrier(): # UP
			self.neighbors.append(grid[self.row - 1][self.col])

		if self.col < self.total_rows - 1 and not grid[self.row][self.col + 1].is_barrier(): # RIGHT
			self.neighbors.append(grid[self.row][self.col + 1])   #row and col used interchangeably since it's a square grid

		if self.col > 0 and not grid[self.row][self.col - 1].is_barrier(): # LEFT
			self.neighbors.append(grid[self.row][self.col - 1])




def h(p1, p2):  #heuristic function: calc Manhattan distance(no diagonals allowed)
	x1, y1 = p1
	x2, y2 = p2
	return (abs(x1 - x2) + abs(y1 - y2))	#manhattan distance(experimentally proven faster)
	#return math.sqrt(abs((x1 - x2)**2) + abs((y1 - y2)**2))	#eucledian distance 

def reconstruct_path(came_from, current, draw):
	while current in came_from:
		current = came_from[current]
		current.make_path()
		draw()


def a_star(draw, grid, start, end):  #draw variable is used to call the entire draw function
	count = 0
	open_set = PriorityQueue()       #priorityQueue
	open_set.put((0, count, start))  #add to the priority queue
	#0: f score of the start node,
	#start: start node,
	#count: counter to check when the element id added,
	#in case two entries have same f score, count can be compared to check which was inserted first
	
	came_from = {} #this dictionary keeps track of the previously traversed path	
	g_score = {spot: float("inf") for row in grid for spot in row} #g score for nodes is set to inf by default	
	g_score[start] = 0 #g f and h score for start node is 0	
	f_score = {spot: float("inf") for row in grid for spot in row} #f score for nodes is set to inf by default	
	f_score[start] = h(start.get_pos(), end.get_pos())  #heuristic distance of start node to end node

	open_set_hash = {start} #set:to keep track of elements in priority queue
							#since items can be removed from priority queue but we can't check for it's presence in it

	while not open_set.empty():
		for event in pygame.event.get():
			if event.type == pygame.QUIT: #escape door
				pygame.quit()

		current = open_set.get()[2]  #index two is element 3 i.e start node
		open_set_hash.remove(current)

		if current == end:   #destination found
			reconstruct_path(came_from, end, draw)
			end.make_end()
			start.make_start()
			return True

		for neighbor in current.neighbors:
			temp_g_score = g_score[current] + 1

			if temp_g_score < g_score[neighbor]:
				came_from[neighbor] = current
				g_score[neighbor] = temp_g_score
				f_score[neighbor] = temp_g_score + h(neighbor.get_pos(), end.get_pos())
				if neighbor not in open_set_hash:
					count += 1
					open_set.put((f_score[neighbor], count, neighbor))
					open_set_hash.add(neighbor)
					neighbor.make_open()

		draw()

		if current != start:
			current.make_closed()

	return False


"""  def bfa(draw, grid, start, end):
	nums=queue.Queue()
	nums.put("")
	add=""
	draw()
	while not findEnd(draw(),add):
		add=num.get()
		for j in ["L","R","U","D"]:
			put = add+jif valid(maze,pit):
			nums.put(put) """


def make_grid(rows, width): #make the data structure to hold all the nodes(list)
	grid = []   #2D list
	gap = width // rows
	for i in range(rows):
		grid.append([])
		for j in range(rows):
			spot = Spot(i, j, gap, rows) #use the Spot class object
			grid[i].append(spot)

	return grid

#draw the grid(make the separation lines visible)
def draw_grid(win, rows, width): #the window where everything is going to be displayed is passed as argument
	gap = width // rows
	for i in range(rows):   #draw the grid(make the separation lines visible)
		pygame.draw.line(win, GREY, (0, i * gap), (width, i * gap))   #horizontal line
		for j in range(rows):
			pygame.draw.line(win, GREY, (j * gap, 0), (j * gap, width))  #vertical lines

#draw all the stuff
def draw(win, grid, rows, width):
	win.fill(BLUE) #fill the whole window with BLUE per frame(since it's dynamic)

	for row in grid:
		for spot in row:
			spot.draw(win)

	draw_grid(win, rows, width)
	pygame.display.update()

#mouse clicks
def get_clicked_pos(pos, rows, width):  #pos: mouse position(etao problem dicchilo)
	gap = width // rows
	y, x = pos

	row = y // gap
	col = x // gap

	return row, col


def main2(win, width):

	start_t = time.time() #marks the start time of the main function
	c=0 #counter to counter the number of times new set of walls have been formed

	ROWS = 50   #change just this to make the entire window size change change (<=800)
	grid = make_grid(ROWS, width)  #make the grid: list of nodes (2D)

	start = None #default
	end = None #default

	run = True
	while run:
		draw(win, grid, ROWS, width)       #the grid is drawn
		for event in pygame.event.get():   #every event: mouse click, timer runs out, etc
			if event.type == pygame.QUIT:  #top right x
				run = False

			if pygame.mouse.get_pressed()[0]: #LEFT mouse button is pressed
				pos = pygame.mouse.get_pos()
				row, col = get_clicked_pos(pos, ROWS, width) #store the row and col value of he node we clicked
				spot = grid[row][col]
				if not start and spot != end: #if the spot is not the start node and the spot is not the end node make it the strat node
					start = spot
					s=start
					start.make_start()

				elif not end and spot != start: #if the spot is not the end node and the spot is not the start node, make it the end node
					end = spot
					e=end
					end.make_end()

				elif spot != end and spot != start: #spot is not start or end then make it wall
					spot.make_barrier()
					
			elif pygame.mouse.get_pressed()[2]: # RIGHT (here used to reset)
				pos = pygame.mouse.get_pos()
				row, col = get_clicked_pos(pos, ROWS, width)
				spot = grid[row][col]
				spot.reset() #reset to default
				if spot == start:
					start = None 
				elif spot == end:
					end = None

			if event.type == pygame.KEYDOWN: #if type of event is that some key is pressed
				if event.key == pygame.K_SPACE and start and end: #and the key is the space bar
					if(c==0):  #when the first set of walls are drawn(c=0)
						c=c+1
						for row in grid:   
							for spot in row:
								spot.update_neighbors(grid)  #starts within loop the process of updating the neighbours in the list

						a_star(lambda: draw(win, grid, ROWS, width), grid, start, end)  #algo is called outside of looping event after the neighbours of a node is updated
						#lambda is a anonymous function, used so that a variable name can be assigner to it and thus can be called multiple times during the execution of the algo block

						""" bfa(lambda: draw(win, grid, ROWS, width), grid, start, end) """
						
						t = time.time()-start_t #calculate the amount of time taken to reach from the start node to end node for a particular set of walls
						print(c,"th time: ",t)

					elif(c>0):  #when subsequesnt sets of walls are drwan(c>0)
						c=c+1
						for row in grid:   
							for spot in row:
								if spot != end and spot != start and not spot.is_barrier():
									spot.reset() 
						for row in grid:   
							for spot in row:
								spot.update_neighbors(grid)  #starts within loop the process of updating the neighbours in the list
						a_star(lambda: draw(win, grid, ROWS, width), grid, start, end)  #algo is called outside of looping event after the neighbours of a node is updated
						
						t = time.time()-start_t #calculate the amount of time taken to reach from the start node to end node for a particular set of walls
						print(c,"th time: ",t)

				if event.key == pygame.K_c:
					start = None
					end = None
					start_t=0
					t=0
					grid = make_grid(ROWS, width)

	pygame.quit() #exit the pygame window


main2(WIN, WIDTH)


""" if pygame.mouse.get_pressed()[0]: #LEFT mouse button is pressed
		pos = pygame.mouse.get_pos()
		row, col = get_clicked_pos(pos, ROWS, width) #store the row and col value of he node we clicked
		spot = grid[row][col]
	    if spot != end and spot != start: #spot is not start or end then make it wall
		spot.make_barrier() """
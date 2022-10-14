import pygame, sys, random, math
from collections import deque
import time
from tkinter import messagebox, Tk

size = (width, height) = 600, 600
pygame.init()

win = pygame.display.set_mode(size)
pygame.display.set_caption("Dijikstar Algorithm")

cols, rows = 60, 60

w = width//cols
h = height//rows

grid = []
queue, visited = deque(), []
path = []

class Spot:
    def __init__(self, i, j):
        self.x, self.y = i, j
        self.f, self.g, self.h = 0, 0, 0
        self.neighbors = []
        self.prev = None
        self.wall = False
        self.visited = False
        # if random.randint(0, 100) < 20:
        #     self.wall = True
        
    def show(self, win, col, shape= 1):
        if self.wall == True:
            col = (0, 0, 0)
        if shape == 1:
            pygame.draw.rect(win, col, (self.x*w, self.y*h, w-1, h-1))
        else:
            pygame.draw.circle(win, col, (self.x*w+w//2, self.y*h+h//2), w//3)
    
    def add_neighbors(self, grid):
        if self.x < cols - 1:
            self.neighbors.append(grid[self.x+1][self.y])
        if self.x > 0:
            self.neighbors.append(grid[self.x-1][self.y])
        if self.y < rows - 1:
            self.neighbors.append(grid[self.x][self.y+1])
        if self.y > 0:
            self.neighbors.append(grid[self.x][self.y-1])

        """ Add Diagonals """
        """ if self.x < cols - 1 and self.y < rows - 1:
            self.neighbors.append(grid[self.x+1][self.y+1])
        if self.x < cols - 1 and self.y > 0:
            self.neighbors.append(grid[self.x+1][self.y-1])
        if self.x > 0 and self.y < rows - 1:
            self.neighbors.append(grid[self.x-1][self.y+1])
        if self.x > 0 and self.y > 0:
            self.neighbors.append(grid[self.x-1][self.y-1])
 """

def clickWall(pos, state):
    i = pos[0] // w
    j = pos[1] // h
    grid[i][j].wall = state


for i in range(cols):
    arr = []
    for j in range(rows):
        arr.append(Spot(i, j))
    grid.append(arr)

for i in range(cols):
    for j in range(rows):
        grid[i][j].add_neighbors(grid)

def get_clicked_pos(pos, rows, width): 
	gap = width // rows
	y, x = pos

	row = y // gap
	col = x // gap

	return row, col
    

def main():
    flag = False
    noflag = True
    startflag_d = False     #start flag for dijkstar

    start = None
    end = None

    start_t = time.time() 
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            #first double click =  start point
            #second double click = end point
            #keeping left mouse button pressed, move the mouse to make walls
            #keeping right mouse button pressed, move the mouse to delete walls

            if event.type == pygame.MOUSEBUTTONUP:
                if pygame.mouse.get_pressed(0):
                    pos=pygame.mouse.get_pos()
                    row,col=get_clicked_pos(pos,rows,width)
                    s=grid[row][col]
                    if not start and s!=end:
                        start=s
                        queue.append(start)
                        start.visited = True  

                    elif not end and s!=start:
                        end=s
                
                    elif s!=start and s!=end:
                        clickWall(pygame.mouse.get_pos(), True)

            if event.type == pygame.MOUSEMOTION:
                if pygame.mouse.get_pressed()[0]:
                    clickWall(pygame.mouse.get_pos(), True)

                elif pygame.mouse.get_pressed()[2]:
                    clickWall(pygame.mouse.get_pos(), False)

            elif pygame.mouse.get_pressed(2):
                clickWall(pygame.mouse.get_pos(), False) 
                 
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_d:
                    startflag_d = True    
                    
        if startflag_d:
            if len(queue) > 0:
                current = queue.popleft()
                if current == end:
                    temp = current
                    while temp.prev:
                        path.append(temp.prev)
                        temp = temp.prev 
                    if not flag:
                        flag = True
                        t = time.time()-start_t
                        print("Time taken to complete: ",t,"seconds")
                    elif flag:
                        continue
                if flag == False:
                    for i in current.neighbors:
                        if not i.visited and not i.wall:
                            i.visited = True
                            i.prev = current
                            queue.append(i)
            else:
                if noflag and not flag:
                    Tk().wm_withdraw()
                    messagebox.showinfo("No Solution", "There was no solution" )
                    noflag = False
                else:
                    continue


        win.fill((0, 20, 20))
        for i in range(cols):
            for j in range(rows):
                spot = grid[i][j]
                spot.show(win, (44, 62, 80))
                if flag and spot in path:
                    spot.show(win, (192, 57, 43))

                elif spot.visited:
                    spot.show(win, (39, 174, 96))
                if spot in queue:
                    spot.show(win, (44, 62, 80))
                    spot.show(win, (39, 174, 96), 0)

                if spot == start:
                    spot.show(win, (0, 255, 200))
                if spot == end:
                    spot.show(win, (0, 120, 255))

        pygame.display.flip()
    


main()
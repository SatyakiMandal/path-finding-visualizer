import pygame, sys, random, math
from tkinter import messagebox, Tk
import time


size = (width, height) = 600, 600

pygame.init()

win = pygame.display.set_mode(size)
pygame.display.set_caption("A* algoritms")

clock = pygame.time.Clock()

cols, rows = 50, 50


grid = []
openSet, closeSet = [], []
path = []

w = width//cols
h = height//rows

class Spot:
    def __init__(self, i, j):
        self.x, self.y = i, j
        self.f, self.g, self.h = 0, 0, 0
        self.neighbors = []
        self.prev = None
        self.wall = False
        # if random.randint(0, 100) < 20:
        #     self.wall = True
        
    def show(self, win, col, shape=1):
        if self.wall == True:
            col = (0, 0, 0)
        if shape==1:
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
        #Add Diagonals
        if self.x < cols - 1 and self.y < rows - 1:
            self.neighbors.append(grid[self.x+1][self.y+1])
        if self.x < cols - 1 and self.y > 0:
            self.neighbors.append(grid[self.x+1][self.y-1])
        if self.x > 0 and self.y < rows - 1:
            self.neighbors.append(grid[self.x-1][self.y+1])
        if self.x > 0 and self.y > 0:
            self.neighbors.append(grid[self.x-1][self.y-1])


def clickWall(pos, state):
    i = pos[0] // w
    j = pos[1] // h
    grid[i][j].wall = state

            
def heuristics(a, b):       #for a*
    return math.sqrt((a.x - b.x)**2 + abs(a.y - b.y)**2)  #eucledian distance
    #return (abs(a.x - b.x) + abs(a.y - b.y))   #manhattan distance


for i in range(cols):
    arr = []
    for j in range(rows):
        arr.append(Spot(i, j))
    grid.append(arr)

for i in range(cols):
    for j in range(rows):
        grid[i][j].add_neighbors(grid)

def close():
    pygame.quit()
    sys.exit()

def get_clicked_pos(pos, rows, width):  #pos: mouse position(etao problem dicchilo)
	gap = width // rows
	y, x = pos

	row = y // gap
	col = x // gap

	return row, col



def main():
    flag = False
    noflag = True
    startflag_a = False

    start = None
    end = None

    start_t = time.time() 
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()        
            if event.type == pygame.MOUSEBUTTONUP:
                if pygame.mouse.get_pressed(0):
                    pos=pygame.mouse.get_pos()
                    row,col=get_clicked_pos(pos,rows,width)
                    s=grid[row][col]
                    if not start and s!=end:
                        start=s
                        openSet.append(start)
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
                if event.key == pygame.K_a:
                    startflag_a = True 

        if startflag_a:
            if len(openSet) > 0:
                winner = 0
                for i in range(len(openSet)):
                    if openSet[i].f < openSet[winner].f:
                        winner = i

                current = openSet[winner]
                
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
                    openSet.remove(current)
                    closeSet.append(current)

                    for neighbor in current.neighbors:
                        if neighbor in closeSet or neighbor.wall:
                            continue
                        tempG = current.g + 1

                        newPath = False
                        if neighbor in openSet:
                            if tempG < neighbor.g:
                                neighbor.g = tempG
                                newPath = True
                        else:
                            neighbor.g = tempG
                            newPath = True
                            openSet.append(neighbor)
                        
                        if newPath:
                            neighbor.h = heuristics(neighbor, end)
                            neighbor.f = neighbor.g + neighbor.h
                            neighbor.prev = current

            else:
                if noflag:
                    Tk().wm_withdraw()
                    messagebox.showinfo("No Solution", "There was no solution" )
                    noflag = False

        win.fill((0, 20, 20))
        for i in range(cols):
            for j in range(rows):
                spot = grid[j][i]
                spot.show(win, (44, 62, 80))
                if flag and spot in path:
                    spot.show(win, (192, 57, 43))
                elif spot in closeSet:
                    spot.show(win, (39, 174, 96))
                elif spot in openSet:
                    spot.show(win, (44, 62, 80))
                    spot.show(win, (39, 174, 96), 0)
                if spot == start:
                    spot.show(win, (0, 255, 200))
                if spot == end:
                    spot.show(win, (0, 120, 255))
                
        pygame.display.flip()



main()
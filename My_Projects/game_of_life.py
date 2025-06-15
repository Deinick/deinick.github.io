import turtle
import random
import time
import math
                      
def initializeTheCells():
    for i in range(35):
        cells.append([])
        for j in range(35):
            newCell = turtle.Turtle()
            newCell.penup()
            newCell.shape("square")
            newCell.shapesize(stretch_wid = 0.9, stretch_len = 0.9)
            cells[i].append(newCell)
            newCell.state = 0
            newCell.color("gray90") #gray90 almost white



def selectCells(x, y):
    if onClick:
        if x > -350 and x < 350 and y > -350 and y < 350:
            j = math.floor((x + 350)/20)
            i = math.floor((350 - y)/20)
            if cells[i][j].state == 0:
                cells[i][j].state = 1
                cells[i][j].color("gray0") #black
            else:
                cells[i][j].state = 0
                cells[i][j].color("gray90") #gray90 almost white
    wn.update()


def showTheUniverse():
    ycor = 340
    for i in range(35):
        xcor = -340
        for j in range(35):
            cells[i][j].goto(xcor, ycor)
            xcor += 20
        ycor -= 20
    wn.update()

def getNeighbors(i, j):
    count_neighbors = 0
    potential_neighbors = []
    if boundaryCondition==1:
        if i==0 and j==0:
            potential_neighbors=[(i, j + 1),(i + 1, j), (i + 1, j + 1)]
            for x,y in potential_neighbors:
                ni,nj=x,y
                count_neighbors+=cells[ni][nj].state
        elif i==0 and j==34:
            potential_neighbors=[(i, j - 1), (i + 1, j - 1),(i + 1, j)]
            for x,y in potential_neighbors:
                ni,nj=x,y
                count_neighbors+=cells[ni][nj].state
        elif i==34 and j==34:
            potential_neighbors=[(i - 1, j - 1), (i - 1, j), (i, j - 1)]
            for x,y in potential_neighbors:
                ni,nj=x,y
                count_neighbors+=cells[ni][nj].state
        elif i==34 and j==0:
            potential_neighbors=[(i - 1, j), (i - 1, j + 1), (i, j + 1)]
            for x,y in potential_neighbors:
                ni,nj=x,y
                count_neighbors+=cells[ni][nj].state
        elif 0<i<34 and j==0:
            potential_neighbors=[(i - 1, j), (i - 1, j + 1), (i, j + 1), (i + 1, j), (i + 1, j + 1)]
            for x,y in potential_neighbors:
                ni,nj=x,y
                count_neighbors+=cells[ni][nj].state
        elif 0<i<34 and j==34:
            potential_neighbors=[(i - 1, j - 1), (i - 1, j), (i, j - 1), (i + 1, j - 1),(i + 1, j)]
            for x,y in potential_neighbors:
                ni,nj=x,y
                count_neighbors+=cells[ni][nj].state
        elif i==0 and 0<j<34:
            potential_neighbors=[(i, j - 1), (i, j + 1), (i + 1, j - 1),(i + 1, j), (i + 1, j + 1)]
            for x,y in potential_neighbors:
                ni,nj=x,y
                count_neighbors+=cells[ni][nj].state
        elif i==34 and 0<j<34:
            potential_neighbors=[(i - 1, j - 1), (i - 1, j), (i - 1, j + 1), (i, j - 1), (i, j + 1)]
            for x,y in potential_neighbors:
                ni,nj=x,y
                count_neighbors+=cells[ni][nj].state
        else:
            potential_neighbors=[(i - 1, j - 1), (i - 1, j), (i - 1, j + 1), (i, j - 1), (i, j + 1), (i + 1, j - 1),(i + 1, j), (i + 1, j + 1)]
            for x,y in potential_neighbors:
                ni,nj=x,y
                count_neighbors+=cells[ni][nj].state
    if boundaryCondition==2:
        if i==0 and j==0:
            potential_neighbors=[(i+34, j+34), (i+34, j), (i+34, j + 1), (i, j+34), (i, j + 1), (i + 2, j -34),(i + 1, j), (i + 1, j + 1)]
            for x,y in potential_neighbors:
                ni,nj=x,y
                count_neighbors+=cells[ni][nj].state
        elif i==0 and j==34:
            potential_neighbors=[(i +34, j - 1), (i +34, j), (i +34, j -34), (i, j - 1), (i, j -34), (i + 1, j - 1),(i + 1, j), (i + 1, j -34)]
            for x,y in potential_neighbors:
                ni,nj=x,y
                count_neighbors+=cells[ni][nj].state
        elif i==34 and j==0:
            potential_neighbors=[(i - 1, j +34), (i - 1, j), (i - 1, j + 1), (i, j +34), (i, j + 1), (i -34, j +34),(i -34, j), (i -34, j + 1)]
            for x,y in potential_neighbors:
                ni,nj=x,y
                count_neighbors+=cells[ni][nj].state
        elif i==34 and j==34:
            potential_neighbors=[(i - 1, j - 1), (i - 1, j), (i - 1, j -34), (i, j - 1), (i, j -34), (i -34, j - 1),(i -34, j), (i -34, j -34)]
            for x,y in potential_neighbors:
                ni,nj=x,y
                count_neighbors+=cells[ni][nj].state
        elif 0<i<34 and j==0:
            potential_neighbors=[(i-1, j +34), (i - 1, j), (i - 1, j + 1), (i, j+34), (i, j + 1), (i + 1, j +34),(i + 1, j), (i + 1, j + 1)]
            for x,y in potential_neighbors:
                ni,nj=x,y
                count_neighbors+=cells[ni][nj].state
        elif 0<i<34 and j==34:
            potential_neighbors=[(i - 1, j - 1), (i - 1, j), (i - 1, j -34), (i, j - 1), (i, j -34), (i + 1, j - 1),(i + 1, j), (i + 1, j -34)]
            for x,y in potential_neighbors:
                ni,nj=x,y
                count_neighbors+=cells[ni][nj].state
        elif i==0 and 0<j<34:
            potential_neighbors=[(i +34, j - 1), (i +34, j), (i +34, j + 1), (i, j - 1), (i, j + 1), (i + 1, j - 1),(i + 1, j), (i + 1, j + 1)]
            for x,y in potential_neighbors:
                ni,nj=x,y
                count_neighbors+=cells[ni][nj].state
        elif i==34 and 0<j<34:
            potential_neighbors=[(i - 1, j - 1), (i - 1, j), (i - 1, j + 1), (i, j - 1), (i, j + 1), (i -34, j - 1),(i -34, j), (i -34, j + 1)]
            for x,y in potential_neighbors:
                ni,nj=x,y
                count_neighbors+=cells[ni][nj].state
        else:
            potential_neighbors=[(i - 1, j - 1), (i - 1, j), (i - 1, j + 1), (i, j - 1), (i, j + 1), (i + 1, j - 1),(i + 1, j), (i + 1, j + 1)]
            for x,y in potential_neighbors:
                ni,nj=x,y
                count_neighbors+=cells[ni][nj].state

    return count_neighbors
                    
                
                           
def updateCells():
    global cells
    newborn = []
    for i in range(35):
        newborn.append([])
        for j in range(35):
            alive = getNeighbors(i, j)
            state_cell = cells[i][j].state
            if state_cell == 1 and (alive < 2 or alive > 3):
                new_state = 0 
            elif state_cell == 0 and alive == 3:
                new_state = 1  
            else:
                new_state = state_cell            
            newborn[i].append(new_state)
    for i in range(35):
        for j in range(35):
            cells[i][j].state = newborn[i][j]
            if newborn[i][j] == 0:
                cells[i][j].color("gray90")
            else:
                cells[i][j].color("gray0") 
    
def esc():
    global stop
    stop = True

def start():
    global boundaryCondition
    global onClick

    onClick = False
    pen.clear()
    pen.write("Choose the boundary condition in the shell", font=("Verdana", 20, "normal"), align = "center")
    wn.update()
    boundaryCondition = int(input("Boundary Condition? Enter 1 for Constant or 2 for Periodic: "))
    pen.clear()
    pen.write("Press ESC to exit", font=("Verdana", 20, "normal"), align = "center")
    
    while not stop:
        wn.update()
        updateCells()
        time.sleep(0.05)
        
    pen.clear()
    pen.write("Done", font=("Verdana", 20, "normal"), align = "center")
    turtle.done()


 
wn = turtle.Screen()
wn.setup(width = 35*20 + 100, height = 35*20 + 100)
wn.tracer(0)

wn.listen()
wn.onkeypress(esc, "Escape") #Press ESC to exit
wn.onkeypress(start, "Return") #Press Enter to start
wn.onscreenclick(selectCells)

pen = turtle.Turtle()
pen.hideturtle()
pen.penup()
pen.goto(0, 365)
pen.write("Select the cells and then Press Enter to start", font=("Verdana", 20, "normal"), align = "center")

boundaryCondition = None
stop = False
onClick = True
cells = []

initializeTheCells() #Already done for you
showTheUniverse() #Already done for you

turtle.mainloop()

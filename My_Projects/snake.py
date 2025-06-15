import turtle
import time
import random

def moveRight():
    global direction
    global x
    global y
    if direction !='l'and (y<=290 and y>=-290):
        direction = 'r'
    
def moveUp():
    global direction
    global x
    global y
    if direction !='d'and (x<=290 and x>=-290):
        direction = 'u'

def moveLeft():
    global direction
    global x
    global y
    if direction !='r'and (y<=290 and y>=-290):
        direction = 'l'
   
def moveDown():
    global direction
    global x
    global y
    if direction !='u'and (x<=290 and x>=-290):
        direction = 'd'
  
wn = turtle.Screen()
wn.setup(width=600, height=600)
wn.tracer(0)

t=turtle.Turtle()
t.shape('square')
t.penup()
t.speed(0)
t.goto(-300,300)

t.pendown()
count=0
while count<4:
    t.forward(600)
    t.right(90)
    count += 1
t.speed(1)
t.penup()
t.goto(0,0)
t.speed(1)
t.hideturtle()



blist=[]
x=280
while x>=-280:
    y=280
    while y>=-280:
        blist.append([x,y])
        y=y-20
    x=x-20
    
food=turtle.Turtle()
food.color('red')
food.shape('square')
food.penup()

fxcor=random.randint(-13,13)
fycor=random.randint(-13,13)
food.goto(fxcor*20,fycor*20)


alist=[]
i=1
while i<6:
    b=turtle.Turtle()
    b.shape("square")
    b.color("blue")
    b.penup()  
    a = random.randint(0,len(blist)-1)
    b.goto(blist[a])  
    alist.append(blist[a])
    del blist[a]
    i+=1
        


wn.listen()

wn.onkeypress(moveRight,"Right")
wn.onkeypress(moveUp, "Up")
wn.onkeypress(moveLeft,"Left")
wn.onkeypress(moveDown,"Down")

d = random.randint(0,2)
if d==0:
    direction='r'
elif d==1:
    direction='u'
elif d==2:
    direction='d'
x=0
y=0
head=turtle.Turtle()
head.shape('square')
head.penup()
snake=[]
snake.append(head)

count=1
while count<4:
    t=turtle.Turtle()
    t.shape('square')
    t.penup()
    t.goto(-20*count,0)
    snake.append(t)
    blist.remove([-20*count,0])
    count=count+1

flag = True 
while flag:
    wn.update()
    time.sleep(0.1)


    i=len(snake)-1
    blist.append([snake[i].xcor(),snake[i].ycor()])
    while i>0:
        snake[i].goto(snake[i-1].xcor(),snake[i-1].ycor())
        if [snake[i-1].xcor(),snake[i-1].ycor()] in blist:
            blist.remove([snake[i-1].xcor(),snake[i-1].ycor()])
        i=i-1

    #head.goto(head.xcor()+20,head.ycor())
   

    if fxcor*20==x and fycor*20==y:
        fxcor=blist[random.randint(0,len(blist)-1)][0]/20
        fycor=blist[random.randint(0,len(blist)-1)][1]/20
        food.goto(fxcor*20,fycor*20)
        t=turtle.Turtle()
        t.shape('square')
        t.penup()
        t.goto(snake[-1].xcor(), snake[-1].ycor())
      
        snake.append(t)

    

    if direction == 'r':
        x=x+20
        head.goto(x,y)
    elif direction == 'u':
        y=y+20
        head.goto(x,y)
    elif direction == 'l':
        x=x-20
        head.goto(x,y)
    elif direction =='d':
        y=y-20
        head.goto(x,y)
            
        
    if x>=290:
        x = -300
        head.goto(x,y)
    elif x<=-290:
        x = 300
        head.goto(x,y)
    if y>=290:
        y=-300
        head.goto(x,y)
    elif y<=-290:
        y=300
        head.goto(x,y)
    blist.remove([snake[i].xcor(),snake[i].ycor()])
  
    i=len(snake)-1

    while i>0:
        if snake[i].xcor()==x and snake[i].ycor()==y:
            flag = False
            break 
        elif [x,y] in alist:
            flag = False
            break
        i-=1


    
  
        

    


  

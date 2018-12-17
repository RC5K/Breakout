import pygame, time, sys, random
pygame.init()
lives = 3
score = 0
FPS = 60
displaywidth = 800
displayheight = 600
gamedisplay = pygame.display.set_mode((displaywidth,displayheight)) # builds the window and sets size
pygame.display.set_caption("Brickbreaker")# sets the name of the window
clock = pygame.time.Clock()
paddle_height = displayheight/30
paddle_width = (3/16)*displaywidth
ball_height = displayheight/40
ball_width = (3/160)*displaywidth
ball_going_up = True
a = random.randint(0,1)
if a == 1:
    ball_going_right = True
else:
    ball_going_right = False
ball_xchange = displaywidth/200
ball_ychange = displayheight/200
paddle_x = (displaywidth/2)-(paddle_width/2)
paddle_y= (5/6)*displayheight
ball_x = displaywidth/2
ball_y = (4/5)*displayheight
brick_length = 50
brick_width = 100


#colours
red = (200,0,0)
orange = (255,165,0)
yellow = (255,255,0)
green = (0,200,0)
blue = (0,0,200)
indigo = (75,0,130)
violet =(238,130,238)
black = (0,0,0)
white = (255,255,255)
bright_red = (255,0,0)
bright_green = (0,255,0)

def render(text,x,y,font,colour):
    text = font.render(text,True,colour)
    textrect = text.get_rect()
    textrect.center = ((x),(y))
    gamedisplay.blit(text,textrect)

def button(msg,x,y,w,h,tc,ic,ac,action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    if x+w > mouse[0] > x and y+h > mouse[1] > y:
        pygame.draw.rect(gamedisplay, ac,(x,y,w,h))
        if click[0] == 1 and action != None:
            action()
    else:
        pygame.draw.rect(gamedisplay, ic,(x,y,w,h))
    font = pygame.font.SysFont("comicsansms",20)
    render(msg,x+(w/2),y+(h/2),font,tc)

def counter(a,b,x,y):
    font = pygame.font.SysFont("comicsansms",20)
    render(a+str(b),x,y,font,pygame.Color("black"))

def quit():
    pygame.quit()
    sys.exit()

def obj(thingx, thingy, thingw, thingh, color):
    pygame.draw.rect(gamedisplay, color, [thingx, thingy, thingw, thingh])
def flipflop(ball_going_right):
    if ball_going_right == True:
        ball_going_right = False
    elif ball_going_right == False:
        ball_going_right = True
    return ball_going_right
def brick_generator():
    brickxy = []
    for i in range(0,4):
        for a in range(0,9):
            x = (a*brick_width)
            y = 250-(i*brick_length)
            if i == 0:
                colour = red
            elif i == 1:
                colour = orange
            elif i == 2:
                colour = green
            elif i == 3:
                colour = blue
            brickxy.append([x,y,i])
            obj(x,y,brick_width,brick_length,colour)
            pygame.display.update()
    return brickxy
def updatebrick(brickxy):
    for i in range(0,(len(brickxy)-1)):
        temp = brickxy[i][2]
        x = brickxy[i][0]
        y = brickxy[i][1]
        if temp == 0:
            colour = red
        elif temp == 1:
            colour = orange
        elif temp == 2:
            colour = green
        elif temp == 3:
            colour = blue
        obj(x,y,brick_width,brick_length,colour)
def detect(ball_x,ball_y,brickxy,score):
    for i in range(0,(len(brickxy)-1)):
        x = brickxy[i][0]
        y = brickxy[i][1]
        x_left_boundary = x
        y_left_boundary = y
        x_right_boundary = x + brick_width
        y_right_boundary = y + brick_length
        if ball_x <= x_right_boundary and ball_x >= x_left_boundary and ball_y >= y_left_boundary and ball_y <= y_right_boundary:
            brickxy[i][0] = displaywidth
            brickxy[i][1] = displayheight
            score += 1
    updatebrick(brickxy)
    return score
def gameintro():
    intro = True
    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()

        gamedisplay.fill(pygame.Color("black"))
        render("Breakout", displaywidth/2, displayheight/5, pygame.font.SysFont("comicsansms",115), pygame.Color("white"))

        button("Start",displaywidth*(3/16),displayheight*(3/4),displaywidth/6,displayheight/12,black,green,bright_green,gameloop) # creates button
        button("Quit",displaywidth*(11/16),displayheight*(3/4),displaywidth/6,displayheight/12,black,red,bright_red,quit) # creates button

        pygame.display.update()
        clock.tick(15)
def gameloop():
    global paddle_x, paddle_y, ball_x, ball_y, ball_going_right, ball_going_up, FPS, lives, score, paddle_height, paddle_width, ball_xchange, ball_ychange
    gameexit = False
    x_change = 0
    brickxy = brick_generator()
    #pygame.mixer.Sound.play(theme)
    while not gameexit:
        ball_going_righttemp = ball_going_right
        ball_going_uptemp = ball_going_up
        scoretemp = score
        for event in pygame.event.get(): # to quit game
            if event.type == pygame.QUIT:
                gameexit = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and paddle_x >= 0 and paddle_x <=800:
                    x_change = -20
                if event.key == pygame.K_RIGHT and paddle_x >= 0 and paddle_x <=800:
                    x_change = 20
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    x_change = 0
        if paddle_x <= 0:
            paddle_x = 1
        if paddle_x >= displaywidth:
            paddle_x = displaywidth-1
        if lives == 0: # lose game
            gameexit = True
        # if score == 36:
            #gameoutro()
            #gameexit = True
        lbound = paddle_x - 20
        rbound = paddle_x + (paddle_width/2) + 20
        if ball_going_up == False and ball_y >= 490 and ball_y <= 520 and ball_x <= rbound and ball_x >= lbound:# paddle hit
            ball_going_up = True
        elif ball_x <= 0 or ball_x >= 800: # hit side walls
            ball_going_right = flipflop(ball_going_right)
        elif ball_y >= 600: # hit floor
            lives -= 1
            paddle_x = 400-(paddle_width/2)
            paddle_y= 500
            ball_x = 400
            ball_y = 480
            brickxy = brick_generator()
            a = random.randint(0,1)
            if a == 1:
                ball_going_right = True
            else:
                ball_going_right = False
            ball_going_up = True
        elif ball_y <= 0: # hit ceiling
            ball_going_up = False
        paddle_x += x_change
        gamedisplay.fill(pygame.Color("gray"))
        counter("Score: ", score, 50,50)
        counter("Lives: ", lives, 150,50)
        score = detect(ball_x,ball_y,brickxy,score)
        if scoretemp != score:
            ball_going_up = flipflop(ball_going_up)
            print("ball up" + str(ball_going_up))
        if ball_going_up == True and ball_going_right == True:
            ball_x += ball_xchange
            ball_y -= ball_ychange
        elif ball_going_up == True and ball_going_right == False:
            ball_x -= ball_xchange
            ball_y -= ball_ychange
        elif ball_going_up == False and ball_going_right == True:
            ball_x += ball_xchange
            ball_y += ball_ychange
        elif ball_going_up == False and ball_going_right == False:
            ball_x -= ball_xchange
            ball_y += ball_ychange
        obj(paddle_x,paddle_y,paddle_width,paddle_height,red)
        obj(ball_x,ball_y,ball_width,ball_height,blue)
        pygame.display.update()#refreshs
        clock.tick(FPS) # sets the fps of the game
    lives = 3
    score = 0
    gameintro()
gameintro()

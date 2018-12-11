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
fontpath = pygame.font.match_font("comicsansms")
font = pygame.font.SysFont(fontpath, 25)
pheight = 20
pwidth = 150
bheight = 15
bwidth = 15
bup = True
a = random.randint(0,1)
if a == 1:
    bright = True
else:
    bright = False
dbx = 4
dby = 3
mx = 0
my = 0
px = 400-(pwidth/2)
py = 500
bx = 400
by = 480
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
def quit():
    pygame.quit()
    sys.exit()

def text(a,b,x,y):
    global font
    largetext = font
    textsurf, textrect = text_objects(a + str(b), largetext)
    textrect.center = ((x),(y))
    gamedisplay.blit(textsurf, textrect)
def text_objects(text, font):
    textSurface = font.render(text, True, black)
    return textSurface, textSurface.get_rect()
def messagetoscreen(msg, color):
    screentext = font.render(msg, True, color)
    gamedisplay.blit(screentext, [displaywidth/2, displayheight/2])
def flipflop(bright):
    if bright == True:
        bright = False
    elif bright == False:
        bright = True
    return bright
def obj(thingx, thingy, thingw, thingh, color):
    pygame.draw.rect(gamedisplay, color, [thingx, thingy, thingw, thingh])
def button(msg,x,y,w,h,ic,ac,action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    if x+w > mouse[0] > x and y+h > mouse[1] > y:
        pygame.draw.rect(gamedisplay, ac,(x,y,w,h))
        if click[0] == 1 and action != None:
            action()
    else:
        pygame.draw.rect(gamedisplay, ic,(x,y,w,h))
    smallText = pygame.font.SysFont("comicsansms",20)
    textSurf, textRect = text_objects(msg, smallText)
    textRect.center = ( (x+(w/2)), (y+(h/2)) )
    gamedisplay.blit(textSurf, textRect)
def brick():
    brickxy = []
    for i in range(0,4):
        for a in range(0,9):
            x = 0+(a*100)
            y = 250-(i*50)
            if i == 0:
                colour = red
            elif i == 1:
                colour = orange
            elif i == 2:
                colour = green
            elif i == 3:
                colour = blue
            brickxy.append([x,y,i])
            obj(x,y,100,50,colour)
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
        obj(x,y,100,50,colour)
def detect(bx,by,brickxy):
    global score
    for i in range(0,(len(brickxy)-1)):
        x = brickxy[i][0]
        y = brickxy[i][1]
        xlbound = x
        ylbound = y
        xrbound = x + 100
        yrbound = y + 50
        if bx <= xrbound and bx >= xlbound and by >= ylbound and by <= yrbound:
            brickxy[i][0] = displaywidth
            brickxy[i][1] = displayheight
            score += 1
    updatebrick(brickxy)
def gameintro():
    intro = True
    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        gamedisplay.fill(white)
        largetext = pygame.font.SysFont("comicsansms",50)
        textsurf, textrect = text_objects("Brickbreaker", largetext)
        textrect.center = ((displaywidth/2),(displayheight*0.25))
        gamedisplay.blit(textsurf, textrect)
        button("Start",150,450,100,50,green,bright_green,gameloop)
        button("Quit",550,450,100,50,red,bright_red,quit)
        pygame.display.update()
        clock.tick(15)
def gameloop():
    global mx, my, px, py, bx, by, bright, bup, FPS, lives, score, pheight, pwidth, dbx, dby
    gameexit = False
    dx = 0
    brickxy = brick()
    #pygame.mixer.Sound.play(theme)
    while not gameexit:
        mx,my = pygame.mouse.get_pos()
        brighttemp = bright
        buptemp = bup
        scoretemp = score
        for event in pygame.event.get(): # to quit game
            if event.type == pygame.QUIT:
                gameexit = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and px >= 0 and px <=800:
                    dx = -20
                if event.key == pygame.K_RIGHT and px >= 0 and px <=800:
                    dx = 20
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    dx = 0
        if px <= 0:
            px = 1
        if px >= 800:
            px = 799
        if lives == 0: # lose game
            gameexit = True
        lbound = px - 20
        rbound = px + (pwidth/2) + 20
        if bup == False and by >= 490 and by <= 520 and bx <= rbound and bx >= lbound:# paddle hit
            bup = True
        elif bx <= 0 or bx >= 800: # hit side walls
            bright = flipflop(bright)
        elif by >= 600: # hit floor
            lives -= 1
            px = 400-(pwidth/2)
            py = 500
            bx = 400
            by = 480
            brickxy = brick()
            a = random.randint(0,1)
            if a == 1:
                bright = True
            else:
                bright = False
            bup = True
        elif by <= 0: # hit ceiling
            bup = False
        px += dx
        gamedisplay.fill(pygame.Color("white"))
        text("Score: ", score, 50,50)
        text("Lives: ", lives, 150,50)
        detect(bx,by,brickxy)
        if scoretemp != score:
            bup = flipflop(bup)
        if bup == True and bright == True:
            bx += dbx
            by -= dby
        elif bup == True and bright == False:
            bx -= dbx
            by -= dby
        elif bup == False and bright == True:
            bx += dbx
            by += dby
        elif bup == False and bright == False:
            bx -= dbx
            by += dby
        obj(px,py,pwidth,pheight,red)
        obj(bx,by,bwidth,bheight,blue)
        #print(px, py, lbound, rbound, bx, by)
        pygame.display.update()#refreshs
        clock.tick(FPS) # sets the fps of the game
    lives = 3
    score = 0
    gameintro()
gameintro()

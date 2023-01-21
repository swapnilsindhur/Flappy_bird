
import random
import sys       # to use sys.exit to exit the program
import pygame
from pygame.locals import *   # basic pygame imports
# copys all names in pygame.locals into your current namespace.
# This is not neccessary, but saves you typing.
#  if it shows error:No module named '_curses'
# then do this: pip install windows-curses

#global variables
fps = 32
n=3
screenwidth = 289
screenheight = 511
screen = pygame.display.set_mode((screenwidth, screenheight)) 
groundy = screenheight*0.8
sprites = {}
sounds = {}
player = "gallery/sprites/bird.png"
pipe = 'gallery/sprites/pipe.png'
background = 'gallery/sprites/background.png'


def welcome():
    #shows the welcome screen
    playerx=int(screenwidth/6)
    playery=int((screenheight-sprites["player"].get_height())/2)
    messagey=int(screenwidth*0.29)
    messagex=int((screenwidth-sprites["message"].get_width())/1.5)
    basex=0
    while True:
        for event in pygame.event.get():
            if event.type==QUIT or (event.type==KEYDOWN and event.key==K_ESCAPE):
                pygame.quit()
                sys.exit()

            elif event.type==KEYDOWN and (event.key==K_SPACE or event.key== K_UP):
                return 
            else:
                screen.blit(sprites['background'],(0,0))
                screen.blit(sprites['message'],(messagex,messagey))
                screen.blit(sprites['player'],(playerx,playery))
                screen.blit(sprites['base'],(basex,groundy))
                pygame.display.update()
                fpsclock.tick(fps)
def maingame():
    score=0
    basex=0
    z=0
    
    playerx=int(screenwidth/5)
    playery=int(screenheight/2)
    #creating new pipes for bliting
    newpipe1=getpipes(n)
    newpipe2=getpipes(n)

    # my List of upper pipes
    upperpipes=[
        {'x':screenwidth+200,'y':newpipe1[0]['y']},
        {'x':screenwidth+200+z+(screenwidth/2),'y':newpipe2[0]['y']}
        ]
    # my List of lower pipes
    lowerpipes=[
        {'x':screenwidth+200,'y':newpipe1[1]['y']},
        {'x':screenwidth+200+z+(screenwidth/2),'y':newpipe2[1]['y']}
        ]
    pipeVelX = -4
    

    playerVelY = -9
    playerMaxVelY = 10
    playerMinVelY = -8
    playerAccY = 1

    playerFlapAccv = -8    # velocity while flapping
    playerFlapped = False  # It is true only when the bird is flapping
    
    while True:
        for event in pygame.event.get():
           if event.type==QUIT or (event.type==KEYDOWN and event.key==K_ESCAPE):
                pygame.quit()
                sys.exit()
           elif event.type==KEYDOWN and (event.key==K_SPACE or event.key== K_UP):  #
               if playery>0:
                   playerVelY=playerFlapAccv
                   sounds['wing'].play()
        crash=iscrash(playerx,playery,upperpipes,lowerpipes) #if its crashes then this function is executed
        if crash:   # if crash = true
            return
        playermidpos=playerx+sprites['player'].get_width()/2
        for pipe in upperpipes:
            pipemidpos=pipe['x']+sprites['pipe'][0].get_width()/2
            if pipemidpos<=playermidpos<pipemidpos+4:
                score+=1
                print(f"the score is {score}]")
                sounds['point'].play()
            
        if playerVelY<playerMaxVelY and not playerFlapped:
            playerVelY+=playerAccY
        if playerFlapped:
            playerFlapped=False
        playerheight=sprites['player'].get_height()
        playery =playery+min(playerVelY,groundy-playery-playerheight) 
        


        #to move the pipes towards left
        for upperpipe,lowerpipe in zip(upperpipes,lowerpipes):
            upperpipe['x'] += pipeVelX           
            lowerpipe['x'] += pipeVelX 
        # Add a new pipe when the first is about to cross the leftmost part of the screen
        if 0 < upperpipes[0]['x']< 5:
        #     if score<=10:
            newpipe=getpipes(n)
        #     if 10<score<20:    
        #         z+=2     
        #         pipeVelX+=-0.5         
        #         playerVelY+=-1         
        #         playerFlapAccv+=-1.5         
        #         playerAccY+=0.1         
        #         playerMaxVelY+=1         
        #         playerMinVelY+=-1         
        #         newpipe=getpipes(n+1.5)
        #     if 20<=score<30:
        #         pipeVelX+=-1
        #         playerVelY+=-2
        #         playerFlapAccv+=-2
        #         playerAccY+=0.2
        #         playerMaxVelY+=2
        #         playerMinVelY+=-2
            #     newpipe=getpipes(n+1.7)
                
            # if score>=30 :
            #     pipeVelX+=-1.5
            #     playerVelY+=-3
            #     playerFlapAccv+=-2.5
            #     playerAccY+=0.3
            #     playerMaxVelY+=3
            #     playerMinVelY+=-3
            #     newpipe=getpipes(n+2)
            # newpipe=getpipes(n)
            upperpipes.append(newpipe[0])
            lowerpipes.append(newpipe[1])
        

        # if the pipe is out of the screen, remove it      
        if upperpipes[0]['x'] < -sprites['pipe'][0].get_width():
            upperpipes.pop(0)
            lowerpipes.pop(0)
         



        #Lets blit our sprites now
        screen.blit((sprites['background']),(0,0))
        for upperpipe,lowerpipe in zip(upperpipes,lowerpipes):
            screen.blit(sprites['pipe'][0],(upperpipe['x'],upperpipe['y']))
            screen.blit(sprites['pipe'][1],(lowerpipe['x'],lowerpipe['y']))
        screen.blit(sprites['base'],(basex,groundy))
        screen.blit(sprites['player'],(playerx,playery))
        mydigits=[int(x) for x in list(str(score))]
        width=0
        for digit in mydigits:
            width+=sprites['nu'][digit].get_width()
        xoffset=(screenwidth-width)/2
        for digit in mydigits:
            screen.blit(sprites['nu'][digit],(xoffset,screenheight*0.12))
            xoffset+=sprites['nu'][digit].get_width()
        pygame.display.update()
        fpsclock.tick(fps)
        
        
    
        
        


def iscrash(playerx,playery,upperpipes,lowerpipes):
    if playery> groundy - 25  or playery<0:
        sounds['hit'].play()
        return True
    
    for pipe in upperpipes:
        pipeHeight = sprites['pipe'][0].get_height()
        if(playery < pipeHeight + pipe['y'] and abs(playerx - pipe['x']) < sprites['pipe'][0].get_width()-20):
            sounds['hit'].play()
            return True

    for pipe in lowerpipes:
        if (playery + sprites['player'].get_height() > pipe['y']) and abs(playerx - pipe['x']) < sprites['pipe'][0].get_width()-20:
            sounds['hit'].play()
            return True

    return False
    

                

def getpipes(n):
    """to genrate two pipes of some length"""
    pipeheight=sprites['pipe'][0].get_height()
    offset=screenheight/n #the empty space between the two pipes from where the bird will pass
    pipex=screenwidth+10
    y2=offset+random.randrange(0,int(screenheight-sprites['base'].get_height()-1.2*offset))
    y1=pipeheight-y2+offset
    pipe=[
        {'x':pipex,'y':-y1},  #upper pipe
        {'x':pipex,'y':y2}    #lower pipe
    ]
    return pipe


                



if __name__ == "__main__":
    # starting point of my game
    pygame.init()  # used to initialize all pygame modules
    fpsclock = pygame.time.Clock()
    pygame.display.set_caption("Flappy Bird game by Swapnil")
    sprites["nu"] = (
        pygame.image.load('gallery/sprites/0.png').convert_alpha(),
        pygame.image.load('gallery/sprites/1.png').convert_alpha(),
        pygame.image.load('gallery/sprites/2.png').convert_alpha(),
        pygame.image.load('gallery/sprites/3.png').convert_alpha(),
        pygame.image.load('gallery/sprites/4.png').convert_alpha(),
        pygame.image.load('gallery/sprites/5.png').convert_alpha(),
        pygame.image.load('gallery/sprites/6.png').convert_alpha(),
        pygame.image.load('gallery/sprites/7.png').convert_alpha(),
        pygame.image.load('gallery/sprites/8.png').convert_alpha(),
        pygame.image.load('gallery/sprites/9.png').convert_alpha()
    )
    sprites['pipe'] = (pygame.transform.rotate(pygame.image.load("gallery/sprites/pipe.png").convert_alpha(), 180),
                                               pygame.image.load("gallery/sprites/pipe.png").convert_alpha())
    sprites['message']=pygame.image.load("gallery/sprites/message.png").convert_alpha()
    sprites['base']=pygame.image.load("gallery/sprites/base.png").convert_alpha()
    #game audio's
    sounds['die']=pygame.mixer.Sound("gallery/audio/die.wav")
    sounds['hit']=pygame.mixer.Sound("gallery/audio/hit.wav")
    sounds['point']=pygame.mixer.Sound("gallery/audio/point.wav")
    sounds['smoosh']=pygame.mixer.Sound("gallery/audio/swoosh.wav")
    sounds['wing']=pygame.mixer.Sound("gallery/audio/wing.wav")
    sprites['player']=pygame.image.load(player).convert_alpha()
    sprites['background']=pygame.image.load(background).convert_alpha()
    while True:
        welcome()  #welcome screen is shown until a key is pressed
        maingame()  #actual game starts here
    

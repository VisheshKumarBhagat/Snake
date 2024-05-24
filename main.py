import pygame
from pygame.locals import *
import sys
import random
# initialize pygame
pygame.init()
SCRLEN = 1280
SCRWID = 720
SCREEN = pygame.display.set_mode((SCRLEN, SCRWID))
CLOCK = pygame.time.Clock()
FPS = 10
size = 25 #size of playground
square = 24 # size of each pixel
offset = 2 # gep between each pixel
# playgrd = size*[size*[0]]
back='#282a36'

def initialize():
    global playgrd, player, last, score
    playgrd=[]
    for _ in range(size):
        temp=[]
        for _ in range(size):
            temp.append(0)
        playgrd.append(temp)
    player = [[0,0]]
    playgrd[player[0][0]][player[0][1]] = 1
    last='right'
    score=0
def moveplayer(move, foodpos):
    global last, playgrd, player
    if move=='': 
        move=str(last)
    elif ((move=='up' and last=='down') or (move=='down' and last=='up') or (move=='left' and last=='right') or (move=='right' and last=='left')) and len(player)!=1:
        move=str(last)
    if move=='up':
        last = str(move)
        newpos = player[0].copy()
        if newpos[1]-1<0:
            newpos[1]=size-1
        else:
            newpos[1]-=1
    if move=='down':
        last = str(move)
        newpos = player[0].copy()
        if newpos[1]+1>=size:
            newpos[1]=0
        else:
            newpos[1]+=1
    if move=='left':
        last = str(move)
        newpos = player[0].copy()
        if newpos[0]-1<0:
            newpos[0]=size-1
        else:
            newpos[0]-=1
    if move=='right':
        last = str(move)
        newpos = player[0].copy()
        if newpos[0]+1>=size:
            newpos[0]=0
        else:
            newpos[0]+=1
    if newpos in player:
        return False, True
    if newpos[0] == foodpos[0] and newpos[1] == foodpos[1]:
        player.insert(0, newpos)
        for play in player:
            playgrd[play[0]][play[1]]=1
        return True, False
    player.insert(0, newpos)
    popped = player.pop()
    playgrd[popped[0]][popped[1]]=0
    for play in player:
        playgrd[play[0]][play[1]]=1
    return False, False
def maingame():
    global playgrd, player, last, score
    eaten = True
    foodpos = [random.randint(0,size-1), random.randint(0,size-1)]
    while True:
        while playgrd[foodpos[0]][foodpos[1]] == 1 and eaten == True:
            foodpos = [random.randint(0,size-1), random.randint(0,size-1)]
        playgrd[foodpos[0]][foodpos[1]] = 2
        eaten = False
        moves=''
        brake = False
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN and (event.key == K_k):
                brake=True
            if event.type == KEYDOWN and (event.key == K_w or event.key == K_UP):
                moves = 'up'
            if event.type == KEYDOWN and (event.key == K_s or event.key == K_DOWN):
                moves = 'down'
            if event.type == KEYDOWN and (event.key == K_a or event.key == K_LEFT):
                moves = 'left'
            if event.type == KEYDOWN and (event.key == K_d or event.key == K_RIGHT):
                moves = 'right'
        if brake:
            break
        eaten, collide = moveplayer(moves, foodpos)  
        score = len(player)  
        font = pygame.font.Font('freesansbold.ttf', 32)
        scoretxt = font.render('SCORE: '+str(score), True, 'green', back)
        SCREEN.fill(back)
        SCREEN.blit(scoretxt, (50,(SCRWID/2)))
        font = pygame.font.Font('freesansbold.ttf', 32)
        scoretxt = font.render('Press \'k\'', True, 'green', back)
        SCREEN.blit(scoretxt, ((SCRLEN/2+size*square/2) + 50,(SCRWID/2)))
        font = pygame.font.Font('freesansbold.ttf', 32)
        scoretxt = font.render('to restart', True, 'green', back)
        SCREEN.blit(scoretxt, ((SCRLEN/2+size*square/2) + 50,(SCRWID/2)+50))
        display()
        CLOCK.tick(FPS)
        if collide:
            break
        # print(playgrd)
    font = pygame.font.Font('freesansbold.ttf', 32)
    scoretxt = font.render('Press enter', True, 'green', back)
    SCREEN.blit(scoretxt, ((SCRLEN/2+size*square/2) + 50,(SCRWID/2)))
    font = pygame.font.Font('freesansbold.ttf', 32)
    scoretxt = font.render('to continue', True, 'green', back)
    SCREEN.blit(scoretxt, ((SCRLEN/2+size*square/2) + 50,(SCRWID/2)+50))
    display()
    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()  
            elif event.type == KEYDOWN and event.key == K_RETURN:
                initialize()
                return
def display():
    global score
    # SCREEN.fill('#000000')
    for i in range(size):
        for j in range(size):
            if playgrd[i][j]==0:
                rectangle = pygame.rect.Rect((SCRLEN/2-size*(square+offset)/2+(0+(i*(square+offset))),SCRWID/2-size*(square+offset)/2+(0+(j*(square+offset)))), (square, square))
                SCREEN.fill('red', rectangle)
            elif playgrd[i][j]==1:
                rectangle = pygame.rect.Rect((SCRLEN/2-size*(square+offset)/2+(0+(i*(square+offset))),SCRWID/2-size*(square+offset)/2+(0+(j*(square+offset)))), (square, square))
                SCREEN.fill('green', rectangle)
            elif playgrd[i][j]==2:
                rectangle = pygame.rect.Rect((SCRLEN/2-size*(square+offset)/2+(0+(i*(square+offset))),SCRWID/2-size*(square+offset)/2+(0+(j*(square+offset)))), (square, square))
                SCREEN.fill('blue', rectangle)
    pygame.display.flip()

if __name__ == '__main__':
    while True:
        initialize()
        SCREEN.fill(back)
        font = pygame.font.Font('freesansbold.ttf', 32)
        scoretxt = font.render('Press enter', True, 'green', back)
        SCREEN.blit(scoretxt, ((SCRLEN/2+size*square/2) + 50,(SCRWID/2)))
        font = pygame.font.Font('freesansbold.ttf', 32)
        scoretxt = font.render('to continue', True, 'green', back)
        SCREEN.blit(scoretxt, ((SCRLEN/2+size*square/2) + 50,(SCRWID/2)+50))
        display()
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            if event.type==KEYDOWN and event.key==K_RETURN:
                maingame()
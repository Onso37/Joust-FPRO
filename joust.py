import pygame
import random
import math

pygame.init()

screen = pygame.display.set_mode((1024,768))
empty_line = "0" * 32
full_line = "1" * 32
jogsize = (64,60)
enemsize = (64,52)
blocksize = (32,16)
screensize = (1024,768)

enemlist = []
egglist = []


platforms = [pygame.Rect(0,80,192,16), pygame.Rect(0,304,256,16), pygame.Rect(832,80,192,16), pygame.Rect(768,304,256,16), pygame.Rect(320,160,384,16), pygame.Rect(352,384,320,16), pygame.Rect(0,768-176,1024,176)]
nivel = pygame.image.load("nivel.png")
jogador_img = pygame.image.load("jogador.png")
inimigo_img = pygame.image.load("inimigo.png")
jogador_img.set_colorkey((0,0,0))
inimigo_img.set_colorkey((0,0,0))
tempo = 0

jogx = 100
jogy = 592-60


speed_dict = {-4: -1.2, -3: -0.8, -2: -0.4, -1: -0.2, 0: 0, 1: 0.2, 2: 0.4, 3: 0.8, 4: 1.2}
speed = 0
jogvy = 0
jogvx = 0

left = right = False
slide = False
sliding = False


clock = pygame.time.Clock()
running = True
while running:
    #1
    move = False
    jump = False
    for ev in pygame.event.get():
        if ev.type == pygame.QUIT:
            running = False
        elif ev.type == pygame.KEYDOWN:
            if ev.key == pygame.K_ESCAPE:
                running = False
            elif ev.key == pygame.K_LEFT:
                left = True
            elif ev.key == pygame.K_RIGHT:
                right = True
            elif ev.key == pygame.K_SPACE:
                jump = True
        elif ev.type == pygame.KEYUP:
            if ev.key == pygame.K_LEFT:
                left = False
            elif ev.key == pygame.K_RIGHT:
                right = False

    #2
    oldspeed = speed
    oldjogx = jogx
    joghitbox = pygame.Rect(jogx,jogy, jogsize[0], jogsize[1])
    enemhitbox = []
    if enemlist == []:
        for i in range(4):
            enemlist.append([random.randint(0,1)*(screensize[0]-enemsize[0]),random.randint(0,768-176-enemsize[0]),random.randint(0,1),random.randint(0,1)])

    for inimigo in enemlist:
        enemhitbox.append(pygame.Rect(inimigo[0],inimigo[1],enemsize[0],enemsize[1]))

           
    dt = clock.tick()
    tempo += dt
    if tempo >= 250:
        move = True


    
    if abs(speed) >= 3:
        slide = True
    else:
        slide = False

    if move and (jogvy == 0 or jump) and not sliding:
        if left and speed != -4:
            tempo = 0
            speed -= 1
        elif right and speed != 4:
            tempo = 0
            speed += 1

    if slide and (abs(oldspeed) - abs(speed)) == 1:
        sliding = True
        slide_dir = right


    if sliding:
        if slide_dir:
            jogvx += 0.001*dt
        else:
            jogvx -= 0.001*dt



    if jump and not sliding:
        jogvy -= 1
    else:
        jogvy += 0.003*dt


    for platform in platforms:
        if jogy <=0:
            jogvy = 0.3
            break
        elif joghitbox.colliderect(platform):
            if abs(joghitbox.bottom - platform.top) <= 1:
                jogvy = 0
                jogy = platform.top-jogsize[1]
            elif abs(joghitbox.top - platform.bottom) <=1:
                jogvy = 0.3
            elif abs(joghitbox.left - platform.right) <=1 or abs(joghitbox.right - platform.left) <=1:
                speed *= -1
        for i in range(len(enemlist)):
            if enemhitbox[i].top <= 0:
                enemlist[i][3] = int(not enemlist[i][3])
            if enemhitbox[i].colliderect(platform):
                if abs(enemhitbox[i].bottom - platform.top) <=1 or abs(enemhitbox[i].top - platform.bottom) <=1:
                    enemlist[i][3] = int(not enemlist[i][3])
                elif abs(enemhitbox[i].left - platform.right) <=1 or abs(enemhitbox[i].right - platform.left) <= 1:
                    enemlist[i][2] = int(not enemlist[i][2])
    jogx = (jogx + speed_dict[speed])%screensize[0] + jogvx
    jogy += jogvy
    if sliding and math.copysign(1, jogvx) != math.copysign(1, oldjogx - jogx):
        sliding = False
        jogvx = 0
        speed = 0
    
    #3
    screen.blit(nivel, (0, 0))
    screen.blit(jogador_img, (int(jogx), int(jogy)))
    for inimigo in enemlist:
        inimigo[0] += 0.6 * (inimigo[2]-0.5)
        inimigo[0] = inimigo[0]%screensize[0]
        inimigo[1] += 0.6 * (inimigo[3]-0.5)
        screen.blit(inimigo_img, (int(inimigo[0]), int(inimigo[1])))
    pygame.display.flip()














pygame.quit()

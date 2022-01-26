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
lives = 4

startgame = False
pygame.display.set_caption('Press SPACE to start')
while True:
    for ev in pygame.event.get():
        if ev.type == pygame.KEYDOWN:
            if ev.key == pygame.K_SPACE:
                startgame = True
    if startgame:
        break
pygame.display.set_caption("Joust")



enemlist = []
egglist = []


def spawnposition(ptero = False):
    x = random.randint(0,1)*(screensize[0]-enemsize[0])
    yzone = 2 if x == 0 else random.randint(2,3)
    if ptero:
        yzone = random.randint(2,3)
    if yzone == 2:
        y = random.randint(97, 303-enemsize[1])
    else:
        y = random.randint(321, 560-enemsize[1])
    return (x,y,0 if yzone == 3 else random.randint(0,1))
    
    
font = pygame.font.Font('freesansbold.ttf', 16)
text = font.render(f'{lives}', True, (255,255,255), (0,0,0))
textRect = text.get_rect()
textRect.center = (629, 698)

platforms = [pygame.Rect(0,80,192,16), pygame.Rect(0,304,256,16), pygame.Rect(832,80,192,16), pygame.Rect(768,304,256,16), pygame.Rect(320,160,384,16), pygame.Rect(352,384,320,16), pygame.Rect(0,768-176,1024,176)]
nivel = pygame.image.load("img/nivel.png")
jogador_img = pygame.image.load("img/jogador.png")
jogador_img2 = pygame.image.load("img/jogador2.png")
jogador_img3 = pygame.image.load("img/jogador3.png")
jogador_img4 = pygame.image.load("img/jogador4.png")
jogador_imgj1 = pygame.image.load("img/jogadorj1.png")
jogador_imgj2 = pygame.image.load("img/jogadorj2.png")
platS = pygame.image.load("img/platformS.png")
platL = pygame.image.load("img/platformL.png")
ovo_img = pygame.image.load("img/ovo.png")
ptero_img1 = pygame.image.load("img/ptero1.png")
ptero_img2 = pygame.image.load("img/ptero2.png")
start_img = pygame.image.load("img/start.png")

ptero_img1.set_colorkey((0,0,0))
ptero_img2.set_colorkey((0,0,0))
ovo_img.set_colorkey((0,0,0))
inimigo_img = pygame.image.load("img/inimigo.png")
inimigo_img2 = pygame.image.load("img/inimigo2.png")
jogador_img.set_colorkey((0,0,0))
jogador_img2.set_colorkey((0,0,0))
jogador_img3.set_colorkey((0,0,0))
jogador_img4.set_colorkey((0,0,0))
jogador_imgj1.set_colorkey((0,0,0))
jogador_imgj2.set_colorkey((0,0,0))
inimigo_img.set_colorkey((0,0,0))
inimigo_img2.set_colorkey((0,0,0))
tempo = 0
inimtempo = 0
inimigo_imgL = [inimigo_img, inimigo_img2, inimigo_img, inimigo_img2]
inimigo_flipL = [pygame.transform.flip(x, True, False) for x in inimigo_imgL]
jogador_imgL = [jogador_img, jogador_img2, jogador_img3, jogador_img4]
jogador_flipL = [pygame.transform.flip(x, True, False) for x in jogador_imgL]
jogador_imgjL = [jogador_imgj1, jogador_imgj2]
jogador_flipjL = [pygame.transform.flip(x, True, False) for x in jogador_imgjL]
ptero_imgL = [ptero_img1, ptero_img2, ptero_img1, ptero_img2]
walk = 0

jogx = 100
jogy = 592-jogsize[1]


speed_dict = {-4: -0.6, -3: -0.4, -2: -0.2, -1: -0.1, 0: 0, 1: 0.1, 2: 0.2, 3: 0.4, 4: 0.6}
speed = 0
jogvy = 0
jogvx = 0

left = right = False
slide = False
sliding = False
pterochance = 0
immortal = 0

jogsprite = pygame.sprite.Sprite()
jogsprite.image = jogador_img
jogsprite.rect = pygame.Rect(jogx, jogy, jogsize[0], jogsize[1])

joggroup = pygame.sprite.RenderUpdates()
joggroup.add(jogsprite)

inimigogroup = pygame.sprite.RenderUpdates()
pterogroup = pygame.sprite.RenderUpdates()

platformgroup = pygame.sprite.RenderUpdates()
platformlist = [(192-320,80),(256-320,304),(832,80),(768,304)]
for p in platformlist:
    tempplatform = pygame.sprite.Sprite()
    tempplatform.image = platS
    tempplatform.rect = pygame.Rect(p[0],p[1],320,16)
    platformgroup.add(tempplatform)

bigPlat = pygame.sprite.Sprite()
bigPlat.image = platL
bigPlat.rect = pygame.Rect(320,160,384,16)

smallPlat = pygame.sprite.Sprite()
smallPlat.image = platS
smallPlat.rect = pygame.Rect(352,384,320,16)

ground = pygame.sprite.Sprite()
ground.image = pygame.image.load("img/pixel.png")
ground.rect = pygame.Rect(0,592,1024,200)
sky = pygame.sprite.Sprite()
sky.image = pygame.image.load("img/pixel.png")
sky.rect = pygame.Rect(0,-100,1024,100)

platformgroup.add(bigPlat)
platformgroup.add(smallPlat)
platformgroup.add(ground)
platformgroup.add(sky)

touch = 0

lvltransition = True
pteroalive = False

clock = pygame.time.Clock()

starty = 450
startstatic = 0
while startstatic < 2000:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
    dt = clock.tick()
    screen.fill((0, 0, 0))
    screen.blit(start_img, (256,int(starty)))
    if starty > 250:
        starty -= 0.05*dt
    else:
        startstatic += 1*dt
    pygame.display.flip()

inimseek = False
level = -1
jumphold = False

running = True
while running:
    #1
    walk = (walk + 0.001) %4
    dead = []
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
                jumphold = True
        elif ev.type == pygame.KEYUP:
            if ev.key == pygame.K_LEFT:
                left = False
            elif ev.key == pygame.K_RIGHT:
                right = False
            elif ev.key == pygame.K_SPACE:
                jumphold = False

    #2
    oldspeed = speed
    oldjogx = jogx

    if enemlist == []:
        level += 1
        for i in range(4):
            spawn = spawnposition()
            enemlist.append([spawn[0],spawn[1],spawn[2],random.randint(0,1)])
            tempsprite = pygame.sprite.Sprite()
            tempsprite.image = inimigo_img
            tempsprite.rect = pygame.Rect(enemlist[-1][0], enemlist[-1][1], enemsize[0], enemsize[1])
            inimigogroup.add(tempsprite)
            if level == 1:
                platformgroup.remove(smallPlat)
                platformgroup.remove(bigPlat)
                lvltransition = True
        screen.blit(nivel, (0, 0))
        screen.blit(text, textRect)
        platformgroup.draw(screen)
        pygame.display.flip()
    lvltransition = False
    inimigoxdir = [x[2] for x in enemlist]

    if random.random() < pterochance and not pteroalive:
        pterosprite = pygame.sprite.Sprite()
        pterosprite.image = ptero_img1
        pterox = 0
        pteroy = spawnposition(True)[1]
        pterosprite.rect = pygame.Rect(pterox, pteroy, 128, 32)
        pterogroup.add(pterosprite)
        pteroalive = True
    
    dt = clock.tick()
    tempo += dt
    if level >= 2:
        inimtempo += dt
        if inimtempo >= 1000:
            inimtempo = 0
            inimseek = True
        else:
            inimseek = False
    
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

    if slide and (abs(oldspeed) - abs(speed)) == 1 and not sliding and touch > 0:
        sliding = True
        slidespeed = speed_dict[speed]
        slide_dir = right


    if sliding:
        if slide_dir:
            slidespeed += 0.0005*dt
        else:
            slidespeed -= 0.0005*dt



    if jump and not sliding:
        jogvy -= 0.05
    else:
        jogvy += 0.00018*dt
    touch -= 1

    ceiling = False
    if jogy <=0:
        ceiling = True
        jogvy = 0.012
        
    joghitbox = jogsprite.rect
    jogplat = pygame.sprite.spritecollide(jogsprite, platformgroup, False)
    if jogplat != [] and not ceiling:
        platform = jogplat[0].rect
        if abs(joghitbox.bottom - platform.top) <= 1:
            jogvy = 0
            jogy = platform.top-jogsize[1]
            touch = 300
        elif abs(joghitbox.top - platform.bottom) <=1:
            jogvy = 0.012
        elif abs(joghitbox.left - platform.right) <=1 or abs(joghitbox.right - platform.left) <=1:
            speed *= -1        

    inimplat = pygame.sprite.groupcollide(platformgroup, inimigogroup, False, False)
    for plat in inimplat.keys():
        plathitbox = plat.rect
        for inim in inimplat[plat]:
            i = inimigogroup.sprites().index(inim)
            enemhitbox = inim.rect
            if (abs(plathitbox.top - enemhitbox.bottom) < 2 and enemlist[i][3] == 1) or (abs(plathitbox.bottom - enemhitbox.top) < 2 and enemlist[i][3] == 0):
                enemlist[i][3] = int(not enemlist[i][3])
            elif (abs(plathitbox.right - enemhitbox.left) < 2 and enemlist[i][2] == 0) or (abs(plathitbox.left - enemhitbox.right) < 2 and enemlist[i][2] == 1):
                enemlist[i][2] = int(not enemlist[i][2])               
            if enemlist[i][1] < 0:
                enemlist[i][1] = 1
            if enemlist[i][1] > 592:
                enemlist[i][1] = 592-enemsize[1]

    joginim = pygame.sprite.spritecollide(jogsprite, inimigogroup, False)
    for i in joginim:
        index = inimigogroup.sprites().index(i)
        enemhitbox = i.rect
        if len(enemlist[index]) == 4:
            if enemhitbox.top > joghitbox.top:
                i.image = ovo_img
                i.rect = pygame.Rect(enemlist[index][0], enemlist[index][1], 40, 20)
                enemlist[index].append(0)
                jogvy -= 0.05
                speed = math.copysign(1,speed) if speed != 0 else 0
            elif enemhitbox.top < joghitbox.top and immortal == 0:
                jogx = 100
                jogy = 592-jogsize[1]
                speed = 0
                jogvx = 0
                jogvy = 0
                immortal = 500
                lives -= 1
                text = font.render(f'{lives}', True, (255,255,255), (0,0,0))
                textRect = text.get_rect()
                textRect.center = (629, 698)
                screen.blit(text, textRect)
                pygame.display.flip()
            else:      
                speed = -speed
                enemlist[index][2] = int(not enemlist[index][2])
        elif enemlist[index][4] >= 600:
            dead.append((index,i))



    if pteroalive:
        jogptero = pygame.sprite.spritecollide(jogsprite, pterogroup, False)
        for ptero in jogptero:
            pterohitbox = ptero.rect
            if abs(pterohitbox.right - joghitbox.left) <= 1:
                pterogroup.remove(ptero)
                pteroalive = False
                pterochance = 0
            elif immortal == 0:
                jogx = 100
                jogy = 592-jogsize[1]
                speed = 0
                jogvx = 0
                jogvy = 0
                immortal = 500
                lives -= 1
                text = font.render(f'{lives}', True, (255,255,255), (0,0,0))
                textRect = text.get_rect()
                textRect.center = (629, 698)
                screen.blit(text, textRect)
                pygame.display.flip()
        pterosprite.image = ptero_imgL[int(walk)]
        pterox += 0.20*dt
        pterosprite.rect = pygame.Rect(pterox, pteroy, 128, 32)
        if pterox > 1700:
            pterox = 0
            pteroy = spawnposition(True)[1]

    for d in sorted(dead, key=lambda t: t[0], reverse=True):
        del enemlist[d[0]]
        inimigogroup.remove(d[1])
    
    truespeed = speed_dict[speed] if not sliding else slidespeed
    jogx = (jogx + truespeed*dt)%screensize[0] 
    jogy += jogvy


    
    if sliding and abs(slidespeed) < 0.0005:
        sliding = False
        jogvx = 0
        speed = 0

    jogsprite.rect = pygame.Rect(jogx, jogy, jogsize[0], jogsize[1])
    counter = 0
    for inim in inimigogroup.sprites():
        if inimseek and level >= 2 and inim.image != ovo_img:
            enemhitbox = inim.rect
            if enemhitbox.top >= joghitbox.top:
                enemlist[counter][3] = 0
            else:
                enemlist[counter][3] = 1
        enemlist[counter][0] += 0.6 * (enemlist[counter][2]-0.5) * dt
        enemlist[counter][0] %= screensize[0]
        enemlist[counter][1] += 0.1 * (enemlist[counter][3]-0.5) * dt
        inim.rect= pygame.Rect(enemlist[counter][0], enemlist[counter][1], enemsize[0], enemsize[1])
        if len(enemlist[counter]) == 5:
            enemlist[counter][4] += dt
            inim.rect= pygame.Rect(enemlist[counter][0], enemlist[counter][1], 40, 20)
            if enemlist[counter][4] >= 15000:
                inim.image = inimigo_img
                enemlist[counter].pop()
        else:
            if enemlist[counter][2] == 0:
                inim.image = inimigo_flipL[int(walk)]
            else:
                inim.image = inimigo_imgL[int(walk)]
            inim.rect= pygame.Rect(enemlist[counter][0], enemlist[counter][1], enemsize[0], enemsize[1])    
        counter += 1
        
    if speed >= 0:
        if touch > 0:
            jogsprite.image = jogador_imgL[0 if speed == 0 else int(walk)]
        else:
            jogsprite.image = jogador_imgjL[0] if jumphold else jogador_imgjL[1]
    else:
        if touch > 0:
            jogsprite.image = jogador_flipL[0 if speed == 0 else int(walk)]
        else:
            jogsprite.image = jogador_flipjL[0] if jumphold else jogador_flipjL[1]


    pterochance += 0.00000000001
    #3
    inimigogroup.clear(screen, nivel)
    joggroup.clear(screen, nivel)
    platformgroup.clear(screen, nivel)
    pterogroup.clear(screen, nivel)
    pygame.display.update(inimigogroup.draw(screen))
    pygame.display.update(joggroup.draw(screen))
    pygame.display.update(platformgroup.draw(screen))
    pygame.display.update(pterogroup.draw(screen))
    if immortal == 500:
        pygame.time.delay(4000)
        clock.tick(1)
    if immortal > 0:
        immortal -= 1
    if lives <= 0:
        running = False
    if abs(jogvx) >= 0.2:
        jogvx = 0
        sliding = False














pygame.quit()

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
    return (x,y)
    
    
font = pygame.font.Font('freesansbold.ttf', 16)
text = font.render(f'{lives}', True, (255,255,255), (0,0,0))
textRect = text.get_rect()
textRect.center = (629, 698)

platforms = [pygame.Rect(0,80,192,16), pygame.Rect(0,304,256,16), pygame.Rect(832,80,192,16), pygame.Rect(768,304,256,16), pygame.Rect(320,160,384,16), pygame.Rect(352,384,320,16), pygame.Rect(0,768-176,1024,176)]
nivel = pygame.image.load("nivel.png")
jogador_img = pygame.image.load("jogador.png")
jogador_img2 = pygame.image.load("jogador2.png")
jogador_img3 = pygame.image.load("jogador3.png")
jogador_img4 = pygame.image.load("jogador4.png")
jogador_imgj1 = pygame.image.load("jogadorj1.png")
jogador_imgj2 = pygame.image.load("jogadorj2.png")
platS = pygame.image.load("platformS.png")
platL = pygame.image.load("platformL.png")
ovo_img = pygame.image.load("ovo.png")
ptero_img1 = pygame.image.load("ptero1.png")
ptero_img2 = pygame.image.load("ptero2.png")

ptero_img1.set_colorkey((0,0,0))
ptero_img2.set_colorkey((0,0,0))
ovo_img.set_colorkey((0,0,0))
inimigo_img = pygame.image.load("inimigo.png")
inimigo_img2 = pygame.image.load("inimigo2.png")
jogador_img.set_colorkey((0,0,0))
jogador_img2.set_colorkey((0,0,0))
jogador_img3.set_colorkey((0,0,0))
jogador_img4.set_colorkey((0,0,0))
jogador_imgj1.set_colorkey((0,0,0))
jogador_imgj2.set_colorkey((0,0,0))
inimigo_img.set_colorkey((0,0,0))
inimigo_img2.set_colorkey((0,0,0))
tempo = 0
inimigo_imgL = [inimigo_img, inimigo_img2, inimigo_img, inimigo_img2]
inimigo_flipL = [pygame.transform.flip(x, True, False) for x in inimigo_imgL]
jogador_imgL = [jogador_img, jogador_img2, jogador_img3, jogador_img4]
jogador_flipL = [pygame.transform.flip(x, True, False) for x in jogador_imgL]
jogador_imgjL = [jogador_imgj1, jogador_imgj2, jogador_imgj1, jogador_imgj2]
jogador_flipjL = [pygame.transform.flip(x, True, False) for x in jogador_imgjL]
ptero_imgL = [ptero_img1, ptero_img2, ptero_img1, ptero_img2]
walk = 0

jogx = 100
jogy = 592-jogsize[1]


speed_dict = {-4: -0.3, -3: -0.2, -2: -0.1, -1: -0.05, 0: 0, 1: 0.05, 2: 0.1, 3: 0.2, 4: 0.3}
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
ground.image = pygame.image.load("pixel.png")
ground.rect = pygame.Rect(0,592,1024,200)
sky = pygame.sprite.Sprite()
sky.image = pygame.image.load("pixel.png")
sky.rect = pygame.Rect(0,-100,1024,100)

platformgroup.add(bigPlat)
platformgroup.add(smallPlat)
platformgroup.add(ground)
platformgroup.add(sky)

touch = 0

lvltransition = True
pteroalive = False

clock = pygame.time.Clock()
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
        elif ev.type == pygame.KEYUP:
            if ev.key == pygame.K_LEFT:
                left = False
            elif ev.key == pygame.K_RIGHT:
                right = False

    #2
    oldspeed = speed
    oldjogx = jogx

    if enemlist == []:
        for i in range(4):
            spawn = spawnposition()
            enemlist.append([spawn[0],spawn[1],random.randint(0,1),random.randint(0,1)])
            tempsprite = pygame.sprite.Sprite()
            tempsprite.image = inimigo_img
            tempsprite.rect = pygame.Rect(enemlist[-1][0], enemlist[-1][1], enemsize[0], enemsize[1])
            inimigogroup.add(tempsprite)
            if not lvltransition:
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
            jogvx += 0.00025*dt
        else:
            jogvx -= 0.00025*dt



    if jump and not sliding:
        jogvy -= 0.3
    else:
        jogvy += 0.0012*dt
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
            touch = 200
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
            if abs(enemhitbox.bottom - plathitbox.top) <=1 or abs(enemhitbox.top - plathitbox.bottom) <=1 :
                enemlist[i][3] = int(not enemlist[i][3])
            elif abs(enemhitbox.left - plathitbox.right) <=1 or abs(enemhitbox.right - plathitbox.left) <= 1:
                enemlist[i][2] = int(not enemlist[i][2])
            if enemlist[i][1] < 0:
                enemlist[i][1] = 1
            if enemlist[i][1] > 592:
                enemlist[i][1] = 592-enemsize[1]
    
     
    
    joginim = pygame.sprite.spritecollide(jogsprite, inimigogroup, False)
    for i in joginim:
        index = inimigogroup.sprites().index(i)
        enemhitbox = i.rect
        if enemhitbox.top > joghitbox.top:
            if len(enemlist[index]) == 4:
                i.image = ovo_img
                i.rect = pygame.Rect(enemlist[index][0], enemlist[index][1], 40, 20)
                enemlist[index].append(0)
                jogvy -= 0.2
                speed = math.copysign(1,speed) if speed != 0 else 0
            elif enemlist[index][4] >= 750:
                dead.append((index,i))
        elif enemhitbox.top < joghitbox.top and len(enemlist[index]) == 4 and immortal == 0:
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
        pterox += 0.15
        pterosprite.rect = pygame.Rect(pterox, pteroy, 128, 32)
        if pterox > 1700:
            pterox = 0
            pteroy = spawnposition(True)[1]

    for d in dead:
        print(d[0])
        del enemlist[d[0]]
        inimigogroup.remove(d[1])
    
    jogx = (jogx + speed_dict[speed])%screensize[0] + jogvx
    jogy += jogvy


    
    if sliding and abs(jogx-oldjogx) < 0.00005:
        sliding = False
        jogvx = 0
        speed = 0

    jogsprite.rect = pygame.Rect(jogx, jogy, jogsize[0], jogsize[1])
    counter = 0
    for inim in inimigogroup.sprites():
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
            jogsprite.image = jogador_imgjL[int(walk)]
    else:
        if touch > 0:
            jogsprite.image = jogador_flipL[0 if speed == 0 else int(walk)]
        else:
            jogsprite.image = jogador_flipjL[int(walk)]


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
    if lives < 0:
        running = False














pygame.quit()

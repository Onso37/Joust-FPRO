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
jogador_img2 = pygame.image.load("jogador2.png")
jogador_img3 = pygame.image.load("jogador3.png")
jogador_img4 = pygame.image.load("jogador4.png")
jogador_imgj1 = pygame.image.load("jogadorj1.png")
jogador_imgj2 = pygame.image.load("jogadorj2.png")
platS = pygame.image.load("platformS.png")
platL = pygame.image.load("platformL.png")
ovo_img = pygame.image.load("ovo.png")

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
jogador_imgL = [jogador_img, jogador_img2, jogador_img3, jogador_img4]
jogador_imgjL = [jogador_imgj1, jogador_imgj2, jogador_imgj1, jogador_imgj2]
walk = 0

jogx = 100
jogy = 592-60


speed_dict = {-4: -1.2, -3: -0.8, -2: -0.4, -1: -0.2, 0: 0, 1: 0.2, 2: 0.4, 3: 0.8, 4: 1.2}
speed = 0
jogvy = 0
jogvx = 0

left = right = False
slide = False
sliding = False

jogsprite = pygame.sprite.Sprite()
jogsprite.image = jogador_img
jogsprite.rect = pygame.Rect(jogx, jogy, jogsize[0], jogsize[1])

joggroup = pygame.sprite.RenderUpdates()
joggroup.add(jogsprite)

inimigogroup = pygame.sprite.RenderUpdates()

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

touch = True

lvltransition = True

clock = pygame.time.Clock()
running = True
while running:
    #1
    walk = (walk + 0.01) %4
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
            enemlist.append([random.randint(0,1)*(screensize[0]-enemsize[0]),random.randint(0,768-176-enemsize[0]),random.randint(0,1),random.randint(0,1)])
            tempsprite = pygame.sprite.Sprite()
            tempsprite.image = inimigo_img
            tempsprite.rect = pygame.Rect(enemlist[-1][0], enemlist[-1][1], enemsize[0], enemsize[1])
            inimigogroup.add(tempsprite)
            if not lvltransition:
                platformgroup.remove(smallPlat)
                platformgroup.remove(bigPlat)
                lvltransition = True
        screen.blit(nivel, (0, 0))
        platformgroup.draw(screen)
        pygame.display.flip()
    lvltransition = False

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
    elif not touch:
        jogvy += 0.003*dt
    touch = False

    ceiling = False
    if jogy <=0:
        ceiling = True
        jogvy = 0.3
        
    joghitbox = jogsprite.rect
    jogplat = pygame.sprite.spritecollide(jogsprite, platformgroup, False)
    if jogplat != [] and not ceiling:
        platform = jogplat[0].rect
        if abs(joghitbox.bottom - platform.top) <= 1:
            jogvy = 0
            jogy = platform.top-jogsize[1]
            touch = True
        elif abs(joghitbox.top - platform.bottom) <=1:
            jogvy = 0.3
        elif abs(joghitbox.left - platform.right) <=1 or abs(joghitbox.right - platform.left) <=1:
            speed *= -1        

    inimplat = pygame.sprite.groupcollide(platformgroup, inimigogroup, False, False)
    for plat in inimplat.keys():
        plathitbox = plat.rect
        for inim in inimplat[plat]:
            i = inimigogroup.sprites().index(inim)
            enemhitbox = inim.rect
            if abs(enemhitbox.bottom - plathitbox.top) <=1 or abs(enemhitbox.top - plathitbox.bottom) <=1:
                enemlist[i][3] = int(not enemlist[i][3])
            elif abs(enemhitbox.left - plathitbox.right) <=1 or abs(enemhitbox.right - plathitbox.left) <= 1:
                enemlist[i][2] = int(not enemlist[i][2])
    
     
    

    joginim = pygame.sprite.spritecollide(jogsprite, inimigogroup, False)
    for i in joginim:
        index = inimigogroup.sprites().index(i)
        enemhitbox = i.rect
        if enemhitbox.top > joghitbox.top:
            if len(enemlist[index]) == 4:
                i.image = ovo_img
                i.rect = pygame.Rect(enemlist[index][0], enemlist[index][1], 40, 20)
                enemlist[index].append(0)
                jogvy -= 0.4
                speed = math.copysign(1,speed) if speed != 0 else 0
            elif enemlist[index][4] >= 2500:
                dead.append((index,i))
        elif enemhitbox.top < joghitbox.top and len(enemlist[index]) == 4:
            print("boo")
        else:
            speed = -speed
            enemlist[index][2] = int(not enemlist[index][2])        


    for d in dead:
        del enemlist[d[0]]
        inimigogroup.remove(d[1])
    
    jogx = (jogx + speed_dict[speed])%screensize[0] + jogvx
    jogy += jogvy


    
    if sliding and math.copysign(1, jogvx) != math.copysign(1, oldjogx - jogx):
        sliding = False
        jogvx = 0
        speed = 0

    jogsprite.rect = pygame.Rect(jogx, jogy, jogsize[0], jogsize[1])
    counter = 0
    for inim in inimigogroup.sprites():

        enemlist[counter][0] += 0.6 * (enemlist[counter][2]-0.5)
        enemlist[counter][0] %= screensize[0]
        enemlist[counter][1] += 0.6 * (enemlist[counter][3]-0.5)
        inim.rect= pygame.Rect(enemlist[counter][0], enemlist[counter][1], enemsize[0], enemsize[1])
        if len(enemlist[counter]) == 5:
            enemlist[counter][4] += dt
            inim.rect= pygame.Rect(enemlist[counter][0], enemlist[counter][1], 40, 20)
            if enemlist[counter][4] >= 15000:
                inim.image = inimigo_img
                enemlist[counter].pop()
        else:
            inim.rect= pygame.Rect(enemlist[counter][0], enemlist[counter][1], enemsize[0], enemsize[1])
        counter += 1
    
    #3
    inimigogroup.clear(screen, nivel)
    joggroup.clear(screen, nivel)
    platformgroup.clear(screen, nivel)
    pygame.display.update(inimigogroup.draw(screen))
    pygame.display.update(joggroup.draw(screen))
    pygame.display.update(platformgroup.draw(screen))
#    if touch:
#        jogsprite
#        screen.blit(jogador_imgL[0 if speed == 0 else int(walk)], (int(jogx), int(jogy)))
#    else:
#        screen.blit(jogador_imgjL[int(walk)], (int(jogx), int(jogy)))














pygame.quit()

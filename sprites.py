import pygame

pygame.init()


screen = pygame.display.set_mode((1024,768))

jogador_img = pygame.image.load("jogador.png")
jogador_img.set_colorkey((0,0,0))
jogsprite = pygame.sprite.Sprite()
jogsprite.image = jogador_img
jogsprite.rect = jogsprite.image.get_rect()

joggroup = pygame.sprite.RenderUpdates()
joggroup.add(jogsprite)


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
    pygame.display.flip()
    joggroup.draw(screen)

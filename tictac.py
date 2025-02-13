import pygame 
pygame.init()
WIDTH = 800
HEIGHT = 600 
screen = pygame.display.set_mode((WIDTH,HEIGHT))
background = pygame.image.load('C:/Users/USER/Downloads/Environment1.jpg')
background = pygame.transform.scale(background,(WIDTH,HEIGHT))
BLACK = (0,0,0)
finish = False 
picture = pygame.image.load('C:/Users/USER/Desktop/chbayah trans.PNG')
picture = pygame.transform.scale(picture,(100,100))
picture2 = pygame.image.load('C:/Users/USER/Desktop/chbayah bedhhar.png')
picture2 = pygame.transform.scale(picture2, (100, 100))
current_picture = picture
flipped = False
x , y = 0,0
previous_key = None
while not finish:
    screen.blit(background, (0,0))
    key = pygame.key.get_pressed()
    if key[pygame.K_d] or key[pygame.K_RIGHT] :
        x+=1
        if not flipped or previous_key ==pygame.K_w:
            current_picture = pygame.transform.flip(picture,True,False)
            flipped = True
        previous_key = pygame.K_d
    if key[pygame.K_a] or key[pygame.K_LEFT]:
        x-=1
        if flipped or previous_key ==pygame.K_w:
            current_picture = pygame.transform.flip(picture,True,False)
            flipped = False 
        previous_key = pygame.K_a
    if key[pygame.K_w] or key[pygame.K_UP]:
        y-=1
        if flipped:
            current_picture=pygame.transform.flip(picture2,True,False)
        else:
            current_picture=picture2
        previous_key = pygame.K_w
    if key[pygame.K_s] or key[pygame.K_DOWN]:
        y+=1
        if flipped:
            current_picture = pygame.transform.flip(picture,True,False)
        else:
            current_picture=picture
        previous_key = pygame.K_s
    screen.blit(current_picture, (x,y))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finish = True
    pygame.display.flip()
pygame.quit()
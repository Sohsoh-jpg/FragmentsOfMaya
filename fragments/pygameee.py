import pygame

pygame.init()

WIDTH = 800
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))

background = pygame.image.load('C:/Users/USER/Downloads/Environment1.jpg')
background = pygame.transform.scale(background, (WIDTH, HEIGHT))

picture1 = pygame.image.load('C:/Users/USER/Pictures/pic1.gif')
picture1 = pygame.transform.scale(picture1, (100, 100))

picture2 = pygame.image.load('C:/Users/USER/Pictures/pic2.gif')
picture2 = pygame.transform.scale(picture2, (100, 100))

picture3 = pygame.image.load('C:/Users/USER/Pictures/pic3.gif')
picture3 = pygame.transform.scale(picture3, (100, 100))

picture4 = pygame.image.load('C:/Users/USER/Pictures/pic4.gif')
picture4 = pygame.transform.scale(picture4, (100, 100))

x_pos = 250
y_pos = 250
original_y_pos = y_pos

clock = pygame.time.Clock()

last_switch_time = pygame.time.get_ticks()
current_image = picture1
image_flipped = False

is_jumping = False
jump_speed = 10
gravity = 0.5
y_velocity = 0

finish = False
while not finish:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finish = True

    keys = pygame.key.get_pressed()

    if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
        x_pos =x_pos+ 5
        if image_flipped:
            current_image = pygame.transform.flip(current_image, True, False)
            image_flipped = False

        current_time = pygame.time.get_ticks()
        if current_time - last_switch_time >= 500:
            if current_image == picture1:
                current_image = picture2
            elif current_image == picture2:
                current_image = picture3
            elif current_image == picture3:
                current_image = picture4
            else:
                current_image = picture1

            last_switch_time = current_time

    # Move left
    elif keys[pygame.K_a] or keys[pygame.K_LEFT]:
        x_pos -= 5
        if not image_flipped:
            current_image = pygame.transform.flip(current_image, True, False)
            image_flipped = True

        current_time = pygame.time.get_ticks()
        if current_time - last_switch_time >= 500:
            if current_image == picture1:
                current_image = picture2
            elif current_image == picture2:
                current_image = picture3
            elif current_image == picture3:
                current_image = picture4
            else:
                current_image = picture1

            last_switch_time = current_time

    if keys[pygame.K_SPACE] and not is_jumping:
        is_jumping = True
        y_velocity = -jump_speed

    
    if is_jumping:
        y_pos += y_velocity
        y_velocity = y_velocity+gravity

        if y_pos >= original_y_pos:
            y_pos = original_y_pos
            is_jumping = False
            y_velocity = 0

    if x_pos > WIDTH:
        x_pos = -current_image.get_width()
    elif x_pos < -current_image.get_width():
        x_pos = WIDTH

    screen.blit(background, (0, 0))
    screen.blit(current_image, (x_pos, y_pos))
    pygame.display.flip()

    clock.tick(60)

pygame.quit()

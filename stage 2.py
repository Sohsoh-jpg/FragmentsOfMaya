import pygame
import random
import math

# Initialize Pygame
pygame.init()

#Player assets
picture1 = pygame.image.load("C:/Users/chihe/OneDrive/Desktop/iss project/picture1.png")
picture1 = pygame.transform.scale(picture1, (100, 130))
picture1_flipped = pygame.transform.flip(picture1, True, False)

picture2 = pygame.image.load("C:/Users/chihe/OneDrive/Desktop/iss project/picture2.png")
picture2 = pygame.transform.scale(picture2, (100, 130))
picture2_flipped = pygame.transform.flip(picture2, True, False)

picture3 = pygame.image.load("C:/Users/chihe/OneDrive/Desktop/iss project/picture3.png")
picture3 = pygame.transform.scale(picture3, (100, 130))
picture3_flipped = pygame.transform.flip(picture3, True, False)

picture4 = pygame.image.load("C:/Users/chihe/OneDrive/Desktop/iss project/picture4.png")
picture4 = pygame.transform.scale(picture4, (100, 130))
picture4_flipped = pygame.transform.flip(picture4, True, False)

# Screen dimensions
SCREEN_WIDTH = 1500
SCREEN_HEIGHT = 900
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("2D Bullying Stage")

# Load the background image
background_image = pygame.image.load("C:/Users/chihe/OneDrive/Desktop/iss project/background.jpg")  # Replace with your image file path
background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))  # Scale to screen size

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
PURPLE = (255, 0, 255)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# Clock for controlling frame rate
clock = pygame.time.Clock()
FPS = 60

# Gravity
GRAVITY = 0.8

# Questions and answers
questions = [
    {
        "question": "What do we say to someone mean?",
        "choices": ["1. Stupid!", "2. That's Alright", "3. Be Mean", "4. Hit Them"],
        "correct_answer": 2
    },
    {
        "question": "Someone insults you in front of others. What’s the best response?",
        "choices": ["1. You're dumb", "2. Stay kind", "3. Whatever, loser", "4. Noted"],
        "correct_answer": 2
    },
    {
        "question": "A classmate mocks your clothes. What do you say?",
        "choices": ["1. So what?", "2. Take care", "3. Nice try", "4. Grow up"],
        "correct_answer": 2
    },
    {
        "question": "Someone rolls their eyes at you. How do you respond?",
        "choices": ["1. Chill out", "2. All good", "3. Keep hating", "4. You wish"],
        "correct_answer": 2
    },
    {
        "question": "A friend snaps at you for no reason. What’s the best thing to say?",
        "choices": ["1. I'm here", "2. Back off", "3. Calm down", "4. You mad?"],
        "correct_answer": 1
    }
]

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        # Load player images for animation
        self.picture1 = pygame.image.load("C:/Users/chihe/OneDrive/Desktop/iss project/picture1.png").convert_alpha()  # Replace with your image
        self.picture2 = pygame.image.load("C:/Users/chihe/OneDrive/Desktop/iss project/picture2.png").convert_alpha()  # Replace with your image
        self.picture3 = pygame.image.load("C:/Users/chihe/OneDrive/Desktop/iss project/picture3.png").convert_alpha()  # Replace with your image
        self.picture4 = pygame.image.load("C:/Users/chihe/OneDrive/Desktop/iss project/picture4.png").convert_alpha()  # Replace with your image

        # Create flipped versions of the images
        self.picture1_flipped = pygame.transform.flip(self.picture1, True, False)
        self.picture2_flipped = pygame.transform.flip(self.picture2, True, False)
        self.picture3_flipped = pygame.transform.flip(self.picture3, True, False)
        self.picture4_flipped = pygame.transform.flip(self.picture4, True, False)

        # Set initial image
        self.current_image = self.picture1
        self.image_flipped = False
        self.rect = self.current_image.get_rect()
        self.rect.topleft = (50, SCREEN_HEIGHT - 100)  # Start from the left

        # Movement variables
        self.speed = 5
        self.jump_speed = -15  # Negative because y-axis is inverted
        self.vel_y = 0  # Vertical velocity
        self.on_ground = False  # Track if the player is on the ground
        self.is_jumping = False  # Track if the player is jumping
        self.last_switch_time = 0  # Timer for animation switching

        # Health and collectibles
        self.collected_objects = 0
        self.health = 100  # Player starts with 100 health
        self.last_hit_time = 0  # Cooldown for taking damage

    def update(self, platforms):
        keys = pygame.key.get_pressed()

        # Horizontal movement
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.rect.x += self.speed
            if self.image_flipped:
                self.current_image = pygame.transform.flip(self.current_image, True, False)
                self.image_flipped = False
                self.current_image = self.picture1

            # Animation logic
            current_time = pygame.time.get_ticks()
            if current_time - self.last_switch_time >= 300:  # Switch every 300ms
                if self.current_image == self.picture1:
                    self.current_image = self.picture2
                elif self.current_image == self.picture2:
                    self.current_image = self.picture3
                elif self.current_image == self.picture3:
                    self.current_image = self.picture4
                else:
                    self.current_image = self.picture1

                self.last_switch_time = current_time

        elif keys[pygame.K_a] or keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
            if not self.image_flipped:
                self.current_image = pygame.transform.flip(self.current_image, True, False)
                self.image_flipped = True
                self.current_image = self.picture1_flipped

            # Animation logic
            current_time = pygame.time.get_ticks()
            if current_time - self.last_switch_time >= 300:  # Switch every 300ms
                if self.current_image == self.picture1_flipped:
                    self.current_image = self.picture2_flipped
                elif self.current_image == self.picture2_flipped:
                    self.current_image = self.picture3_flipped
                elif self.current_image == self.picture3_flipped:
                    self.current_image = self.picture4_flipped
                else:
                    self.current_image = self.picture1_flipped

                self.last_switch_time = current_time

        # Jumping
        if keys[pygame.K_SPACE] and self.on_ground:  # Only jump if on the ground
            self.is_jumping = True
            self.vel_y = self.jump_speed
            self.on_ground = False  # Player is no longer on the ground

        # Apply gravity
        if not self.on_ground:
            self.vel_y += GRAVITY
            self.rect.y += self.vel_y

        # Check for collisions with platforms
        self.on_ground = False
        for platform in platforms:
            if self.rect.colliderect(platform.rect):
                if self.vel_y > 0:  # Falling
                    self.rect.bottom = platform.rect.top
                    self.vel_y = 0
                    self.on_ground = True
                    self.is_jumping = False  # Reset jumping state when landing

        # Check if player is on the ground (bottom of the screen)
        if self.rect.bottom >= SCREEN_HEIGHT - 50:
            self.rect.bottom = SCREEN_HEIGHT - 50
            self.on_ground = True
            self.vel_y = 0
            self.is_jumping = False  # Reset jumping state when landing

        # Update the player's image
        self.image = self.current_image

    def take_damage(self, amount):
        """
        Reduces the player's health by the specified amount.
        """
        current_time = pygame.time.get_ticks()
        if current_time - self.last_hit_time > 1000:  # 1-second cooldown
            self.health -= amount
            self.last_hit_time = current_time
            print(f"Player health: {self.health}")
            if self.health <= 0:
                self.kill()
                print("Game Over! Player defeated.")

# Platform class
class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

# Bully class
class Bully(pygame.sprite.Sprite):
    def __init__(self, x, y, player):
        super().__init__()
        self.image = pygame.Surface((40, 40))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.speed = 2  # Speed at which the bully chases the player
        self.jump_speed = -15  # Jump strength (negative because y-axis is inverted)
        self.player = player  # Reference to the player
        self.vel_y = 0  # Vertical velocity for gravity
        self.on_ground = False  # Track if the bully is on the ground

    def update(self, platforms):
        # Calculate direction to the player
        dx = self.player.rect.x - self.rect.x
        dy = self.player.rect.y - self.rect.y
        distance = max(1, (dx ** 2 + dy ** 2) ** 0.5)  # Avoid division by zero

        # Normalize direction vector
        direction_x = dx / distance
        direction_y = dy / distance

        # Move towards the player
        self.rect.x += direction_x * self.speed

        # Apply gravity
        self.vel_y += GRAVITY
        self.rect.y += self.vel_y

        # Check for collisions with platforms
        self.on_ground = False
        for platform in platforms:
            if self.rect.colliderect(platform.rect):
                if self.vel_y > 0:  # Falling
                    self.rect.bottom = platform.rect.top
                    self.vel_y = 0
                    self.on_ground = True

        # Check if bully is on the ground (bottom of the screen)
        if self.rect.bottom >= SCREEN_HEIGHT - 50:
            self.rect.bottom = SCREEN_HEIGHT - 50
            self.on_ground = True
            self.vel_y = 0

        # Make the bully jump if the player is above and the bully is on the ground
        if self.on_ground and self.player.rect.y < self.rect.y:
            self.vel_y = self.jump_speed
            self.on_ground = False

# Collectible object class
class Collectible(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((30, 30))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

# Insult class
class Insult(pygame.sprite.Sprite):
    def __init__(self, x, y, target_x, target_y, text):
        super().__init__()
        self.font = pygame.font.Font(None, 24)  # Font for rendering the insult text
        self.image = self.font.render(text, True, RED)  # Render the insult text
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed = 5
        
        # Calculate direction vector
        dx = target_x - x
        dy = target_y - y
        distance = max(1, (dx ** 2 + dy ** 2) ** 0.5)  # Avoid division by zero
        self.direction_x = dx / distance
        self.direction_y = dy / distance

    def update(self):
        self.rect.x += self.speed * self.direction_x
        self.rect.y += self.speed * self.direction_y
        
        # Remove the insult if it goes off-screen
        if self.rect.right < 0 or self.rect.left > SCREEN_WIDTH or self.rect.bottom < 0 or self.rect.top > SCREEN_HEIGHT:
            self.kill()

# Boss class
class Boss(pygame.sprite.Sprite):
    def __init__(self, player):
        super().__init__()
        self.image = pygame.Surface((80, 80))
        self.image.fill(PURPLE)
        self.rect = self.image.get_rect()
        self.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT - 200)
        self.health = 10  # Boss starts with 10 health
        self.speed = 1  # Initial speed
        self.direction = 1  # Movement direction (1 for right, -1 for left)
        self.vel_y = 0  # Vertical velocity for gravity
        self.on_ground = False  # Track if the boss is on the ground
        self.player = player  # Reference to the player
        self.last_insult_time = 0  # Timer for shooting insults
        self.insult_cooldown = 2000  # Cooldown between insults (in milliseconds)
        self.insults = [
            "You're weak!", "Give up!", "No one likes you!", "You'll never win!", "Loser!"
        ]

    def update(self, platforms):
        # Horizontal movement
        self.rect.x += self.speed * self.direction

        # Apply gravity
        self.vel_y += GRAVITY
        self.rect.y += self.vel_y

        # Check for collisions with platforms
        self.on_ground = False
        for platform in platforms:
            if self.rect.colliderect(platform.rect):
                if self.vel_y > 0:  # Falling
                    self.rect.bottom = platform.rect.top
                    self.vel_y = 0
                    self.on_ground = True

        # Check if boss is on the ground (bottom of the screen)
        if self.rect.bottom >= SCREEN_HEIGHT - 50:
            self.rect.bottom = SCREEN_HEIGHT - 50
            self.on_ground = True
            self.vel_y = 0

        # Reverse direction if hitting screen edges
        if self.rect.left < 0:  # Left edge
            self.rect.left = 0
            self.direction *= -1  # Reverse direction
        elif self.rect.right > SCREEN_WIDTH:  # Right edge
            self.rect.right = SCREEN_WIDTH
            self.direction *= -1  # Reverse direction

        # Shoot insults at the player
        current_time = pygame.time.get_ticks()
        if current_time - self.last_insult_time > self.insult_cooldown:
            self.shoot_insult()
            self.last_insult_time = current_time

    def shoot_insult(self):
        """
        Shoots an insult towards the player.
        """
        insult_text = random.choice(self.insults)  # Randomly select an insult
        insult = Insult(self.rect.centerx, self.rect.centery, self.player.rect.centerx, self.player.rect.centery, insult_text)
        all_sprites.add(insult)
        insults.add(insult)  # Add the insult to the insults group

    def take_damage(self, amount):
        """
        Reduces the boss's health by the specified amount.
        If health drops to 0 or below, the boss is defeated.
        """
        self.health -= amount
        if self.health <= 0:
            self.kill()  # Remove the boss from the game
            print("Boss defeated!")

    def increase_speed(self):
        """
        Increases the boss's speed by 0.5 when the player answers incorrectly.
        """
        self.speed += 0.5
        print(f"Boss speed increased to {self.speed}")

# Bullet class (for shooting the correct answer)
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, target_x, target_y, answer_text):
        super().__init__()
        self.font = pygame.font.Font(None, 36)  # Font for rendering the answer text
        self.image = self.font.render(answer_text, True, WHITE)  # Render the answer text
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed = 10
        
        # Calculate direction vector
        dx = target_x - x
        dy = target_y - y
        distance = max(1, (dx ** 2 + dy ** 2) ** 0.5)  # Avoid division by zero
        self.direction_x = dx / distance
        self.direction_y = dy / distance

    def update(self, platforms):
        self.rect.x += self.speed * self.direction_x
        self.rect.y += self.speed * self.direction_y
        
        # Check for collisions with platforms
        if pygame.sprite.spritecollideany(self, platforms):
            self.kill()  # Destroy the bullet if it touches a platform
        
        # Remove the bullet if it goes off-screen
        if self.rect.right < 0 or self.rect.left > SCREEN_WIDTH or self.rect.bottom < 0 or self.rect.top > SCREEN_HEIGHT:
            self.kill()

# Crosshair class
class Crosshair(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((20, 20), pygame.SRCALPHA)  # Transparent surface
        pygame.draw.line(self.image, RED, (0, 10), (20, 10), 2)  # Horizontal line
        pygame.draw.line(self.image, RED, (10, 0), (10, 20), 2)  # Vertical line
        self.rect = self.image.get_rect()

    def update(self):
        self.rect.center = pygame.mouse.get_pos()  # Follow the mouse

# Flashback function
def show_flashback():
    screen.fill(BLACK)
    font = pygame.font.Font(None, 36)
    text = font.render("Flashback: Memories of bullying...", True, WHITE)
    screen.blit(text, (SCREEN_WIDTH // 4, SCREEN_HEIGHT // 2))
    pygame.display.flip()
    pygame.time.wait(3000)  # Show flashback for 3 seconds

# Transition to boss fight
def show_boss_transition():
    screen.fill(BLACK)
    font = pygame.font.Font(None, 48)
    text = font.render("Preparing for the Boss Fight...", True, WHITE)
    screen.blit(text, (SCREEN_WIDTH // 4, SCREEN_HEIGHT // 2))
    pygame.display.flip()
    pygame.time.wait(2000)  # Show transition for 2 seconds

# Game Over screen
def show_game_over():
    screen.fill(BLACK)
    font_large = pygame.font.Font(None, 72)
    font_small = pygame.font.Font(None, 36)
    
    # Game Over text
    game_over_text = font_large.render("GAME OVER", True, RED)
    screen.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, SCREEN_HEIGHT // 3))
    
    # Instruction text
    instruction_text = font_small.render("Press R to Restart or Q to Quit", True, WHITE)
    screen.blit(instruction_text, (SCREEN_WIDTH // 2 - instruction_text.get_width() // 2, SCREEN_HEIGHT // 2))
    
    pygame.display.flip()
    
    # Wait for player input
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return False  # Don't restart
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:  # Restart
                    waiting = False
                    return True  # Restart game
                elif event.key == pygame.K_q:  # Quit
                    pygame.quit()
                    return False  # Don't restart
        clock.tick(FPS)

# Display question and choices
def display_question(question_data):
    font = pygame.font.Font(None, 36)
    question = question_data["question"]
    choices = question_data["choices"]
    
    # Render the question and choices
    screen.blit(font.render(question, True, WHITE), (50, 100))
    for i, choice in enumerate(choices):
        screen.blit(font.render(choice, True, WHITE), (50, 150 + i * 50))

# Check answer
def check_answer(answer, boss, correct_answer, question_data):
    if answer == correct_answer:  # Correct answer
        # Get the correct answer text
        correct_answer_text = question_data["choices"][correct_answer - 1]
        
        # Create a bullet with the correct answer text and shoot it at the mouse position
        target_x, target_y = pygame.mouse.get_pos()
        bullet = Bullet(player.rect.centerx, player.rect.centery, target_x, target_y, correct_answer_text)
        all_sprites.add(bullet)
        bullets.add(bullet)  # Add the bullet to the bullets group
    else:  # Wrong answer
        boss.increase_speed()  # Increase boss speed
        print("Wrong! Boss speed increased!")

# Reset game function
def reset_game():
    # Clear all sprites
    all_sprites.empty()
    platforms.empty()
    bullies.empty()
    collectibles.empty()
    bullets.empty()
    insults.empty()

    # Recreate player
    global player
    player = Player()
    all_sprites.add(player)

    # Recreate platforms
    platform1 = Platform(200, SCREEN_HEIGHT - 100, 200, 20)
    platform2 = Platform(500, SCREEN_HEIGHT - 200, 200, 20)
    platforms.add(platform1, platform2)
    all_sprites.add(platform1, platform2)

    # Recreate bullies
    bully1 = Bully(300, SCREEN_HEIGHT - 140, player)  # Pass player reference
    bully2 = Bully(600, SCREEN_HEIGHT - 240, player)  # Pass player reference
    bullies.add(bully1, bully2)
    all_sprites.add(bully1, bully2)

    # Recreate collectibles
    for i in range(5):
        platform = random.choice([platform1, platform2])
        x = random.randint(platform.rect.left, platform.rect.right - 30)
        y = platform.rect.top - 40  # Spawn above the platform
        collectible = Collectible(x, y)
        collectibles.add(collectible)
        all_sprites.add(collectible)

    # Reset boss fight variables
    global boss_fight, current_question
    boss_fight = False
    current_question = random.choice(questions)

# Main game loop
running = True
while running:
    # Create sprites
    all_sprites = pygame.sprite.Group()
    platforms = pygame.sprite.Group()
    bullies = pygame.sprite.Group()
    collectibles = pygame.sprite.Group()
    bullets = pygame.sprite.Group()  # Group for bullets
    insults = pygame.sprite.Group()  # Group for insults

    # Create player
    player = Player()
    all_sprites.add(player)

    # Create platforms
    platform1 = Platform(200, SCREEN_HEIGHT - 100, 200, 20)
    platform2 = Platform(500, SCREEN_HEIGHT - 200, 200, 20)
    platforms.add(platform1, platform2)
    all_sprites.add(platform1, platform2)

    # Create bullies
    bully1 = Bully(300, SCREEN_HEIGHT - 140, player)  # Pass player reference
    bully2 = Bully(600, SCREEN_HEIGHT - 240, player)  # Pass player reference
    bullies.add(bully1, bully2)
    all_sprites.add(bully1, bully2)

    # Create collectibles
    for i in range(5):
        platform = random.choice([platform1, platform2])
        x = random.randint(platform.rect.left, platform.rect.right - 30)
        y = platform.rect.top - 40  # Spawn above the platform
        collectible = Collectible(x, y)
        collectibles.add(collectible)
        all_sprites.add(collectible)

    # Create boss
    boss = Boss(player)  # Pass player reference to the boss

    # Create crosshair
    crosshair = Crosshair()
    all_sprites.add(crosshair)

    # Game state variables
    boss_fight = False
    current_question = random.choice(questions)

    # Inner game loop
    game_active = True
    while game_active:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                game_active = False

            # Handle key presses for answering questions
            if event.type == pygame.KEYDOWN and boss_fight:
                if event.key == pygame.K_1:
                    check_answer(1, boss, current_question["correct_answer"], current_question)
                    current_question = random.choice(questions)  # Randomize the next question
                elif event.key == pygame.K_2:
                    check_answer(2, boss, current_question["correct_answer"], current_question)
                    current_question = random.choice(questions)  # Randomize the next question
                elif event.key == pygame.K_3:
                    check_answer(3, boss, current_question["correct_answer"], current_question)
                    current_question = random.choice(questions)  # Randomize the next question
                elif event.key == pygame.K_4:
                    check_answer(4, boss, current_question["correct_answer"], current_question)
                    current_question = random.choice(questions)  # Randomize the next question

            # Handle mouse click for shooting
            if event.type == pygame.MOUSEBUTTONDOWN and boss_fight:
                if event.button == 1:  # Left mouse button
                    # Get the mouse position
                    target_x, target_y = pygame.mouse.get_pos()
                    
                    # Create a bullet that moves towards the mouse position
                    bullet = Bullet(player.rect.centerx, player.rect.centery, target_x, target_y, current_question["choices"][current_question["correct_answer"] - 1])
                    all_sprites.add(bullet)
                    bullets.add(bullet)

        # Update
        player.update(platforms)  # Pass platforms to player.update()
        for bully in bullies:
            bully.update(platforms)  # Pass platforms to bully.update()
        if boss_fight:
            boss.update(platforms)  # Pass platforms to boss.update()
        bullets.update(platforms)  # Pass platforms to bullets.update()
        insults.update()  # Update insults
        crosshair.update()  # Update crosshair position

        # Check for collisions with collectibles
        collected = pygame.sprite.spritecollide(player, collectibles, True)
        if collected:
            player.collected_objects += len(collected)
            print(f"Collected {player.collected_objects}/5 objects")

        # Check if player collected all objects
        if player.collected_objects >= 5 and not boss_fight:
            boss_fight = True
            show_boss_transition()  # Show transition screen
            # Remove bullies and collectibles
            for bully in bullies:
                bully.kill()
            for collectible in collectibles:
                collectible.kill()
            # Add boss to the screen
            all_sprites.add(boss)

        # Boss fight logic
        if boss_fight:
            boss.update(platforms)

            # Display question continuously
            display_question(current_question)

            # Check if the boss is defeated
            if boss.health <= 0:
                show_flashback()
                game_active = False  # End the current game session

        # Check for collisions with bullies or boss
        if pygame.sprite.spritecollide(player, bullies, False) or pygame.sprite.collide_rect(player, boss):
            player.take_damage(10)  # Player loses 10 health on collision

        # Check for collisions between bullets and the boss
        if boss_fight:
            bullet_hits = pygame.sprite.spritecollide(boss, bullets, True)
            for bullet in bullet_hits:
                boss.take_damage(2)  # Boss takes damage when hit by a bullet

        # Check for collisions between insults and the player
        insult_hits = pygame.sprite.spritecollide(player, insults, True)
        for insult in insult_hits:
            player.take_damage(5)  # Player loses 5 health when hit by an insult

        # Check if player is defeated
        if player.health <= 0:
            print("Game Over! Player defeated.")
            game_active = False
            # Show game over screen and check if player wants to restart
            if not show_game_over():
                running = False
                break  # Exit the inner loop if player chooses to quit
            else:
                reset_game()  # Reset the game if player chooses to restart
                continue  # Skip the rest of the loop and start fresh

        # Draw
        screen.blit(background_image, (0, 0))  # Draw the background image
        all_sprites.draw(screen)  # Draw all sprites
        if boss_fight:
            display_question(current_question)  # Redraw the question on top

        # Display player health
        font = pygame.font.Font(None, 36)
        health_text = font.render(f"Health: {player.health}", True, WHITE)
        screen.blit(health_text, (10, 10))

        pygame.display.flip()  # Update the display
        clock.tick(FPS)

    # Reset the game for the next session
    if running:  # Only reset if we're still running
        reset_game()

pygame.quit()
import pygame
import os
pygame.font.init()
pygame.mixer.init()

# General parameters for game
WIDTH , HEIGHT = 900, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
BORDER = pygame.Rect(WIDTH//2 - 5, 0, 10, HEIGHT )
HELTH_FONT = pygame.font.SysFont('comicsans', 40)
WINNER_FONT = pygame.font.SysFont('comicsans', 100)
BULLET_HIT_SOUND = pygame.mixer.Sound('Assets/Grenade+1.mp3')
BULLET_FIRE_SOUND = pygame.mixer.Sound('Assets/Gun+Silencer.mp3')

# colors
RED = (255, 0, 0)
WHITE = (255, 250, 255)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)

SPACESHIP_WIDTH, SPACESHIP_HEIGHT = 55, 40
YELLOW_HIT = pygame.USEREVENT + 1
RED_HIT = pygame.USEREVENT + 2
VEL = 5
BULLET_VEL = 7
MAX_BULLET = 3
FPS = 60

# yellow spaceship
YELLOW_SPACESHIP_IMG = pygame.image.load(os.path.join('Assets', 'spaceship_yellow.png'))
YELLOW_SPACESHIP_IMG = pygame.transform.scale(YELLOW_SPACESHIP_IMG,(SPACESHIP_WIDTH, SPACESHIP_HEIGHT))
YELLOW_SPACESHIP_IMG = pygame.transform.rotate(YELLOW_SPACESHIP_IMG, 90)

# red spaceship
RED_SPACESHIP_IMG = pygame.image.load(os.path.join('Assets', 'spaceship_red.png'))
RED_SPACESHIP_IMG = pygame.transform.scale(RED_SPACESHIP_IMG,(SPACESHIP_WIDTH, SPACESHIP_HEIGHT))
RED_SPACESHIP_IMG = pygame.transform.rotate(RED_SPACESHIP_IMG, 270 )

SPACE = pygame.image.load(os.path.join('Assets', 'space.png'))
SPACE = pygame.transform.scale(SPACE,(WIDTH, HEIGHT))
    
# window things
def draw_window(red, yellow, red_bullets, yellow_bullets, red_health, yellow_health):
    WIN.blit(SPACE,(0, 0))
    pygame.draw.rect(WIN, BLACK, BORDER)    

    red_helth_text = HELTH_FONT.render('Health: ' + str(red_health), 1, WHITE)
    yellow_helth_text = HELTH_FONT.render('Health ' + str(yellow_health), 1, WHITE)
    
    WIN.blit(red_helth_text, (WIDTH - red_helth_text.get_width() -10, 10))
    WIN.blit(yellow_helth_text, (10, 10))
    
    WIN.blit(YELLOW_SPACESHIP_IMG,(yellow.x,yellow.y))
    WIN.blit(RED_SPACESHIP_IMG,(red.x, red.y))
    
    for bullet in red_bullets:
        pygame.draw.rect(WIN, RED, bullet)

    for bullet in yellow_bullets:
        pygame.draw.rect(WIN, YELLOW, bullet)

    pygame.display.update()

#  move spaceship
def move_yellow(key_pressed, yellow):
    # move yellow
    if key_pressed[pygame.K_a] and yellow.x - VEL > 0: #left
        yellow.x -= VEL
    if key_pressed[pygame.K_s]and yellow.y + VEL + yellow.height  < HEIGHT - 10: #donw
        yellow.y += VEL
    if key_pressed[pygame.K_d] and yellow.x + VEL +yellow.width < BORDER.x + BORDER.width : #right
        yellow.x += VEL
    if key_pressed[pygame.K_w] and yellow.y - VEL > 0: #up
        yellow.y -= VEL
    
def move_red(key_pressed, red):
    if key_pressed[pygame.K_LEFT] and red.x - VEL > BORDER.x + BORDER.width : #left
        red.x -= VEL
    if key_pressed[pygame.K_DOWN]and red.y + VEL + red.height  < HEIGHT - 10: #donw
        red.y += VEL
    if key_pressed[pygame.K_RIGHT]and red.x + VEL + red.width < WIDTH + 15: #right
        red.x += VEL
    if key_pressed[pygame.K_UP] and red.y - VEL > 0: #up
        red.y -= VEL

# bullets
def handle_bullets(yellow_bullets, red_bullets, red, yellow, RED_HIT, YELLOW_HIT):
    for bullet in yellow_bullets:
        bullet.x += BULLET_VEL
        if red.colliderect(bullet):
            pygame.event.post(pygame.event.Event(RED_HIT))
            yellow_bullets.remove(bullet)
        elif bullet.x > WIDTH:
            yellow_bullets.remove(bullet)

    for bullet in red_bullets:
        bullet.x -= BULLET_VEL
        if yellow.colliderect(bullet):
            pygame.event.post(pygame.event.Event(YELLOW_HIT))
            red_bullets.remove(bullet)
        elif bullet.x < 0:
            red_bullets.remove(bullet)


def draw_winner(text): 
    draw_text = WINNER_FONT.render(text,1, WHITE)
    WIN.blit(draw_text,(WIDTH//2 - draw_text.get_width()/2, HEIGHT//2 - draw_text.get_height()/2 ))
    pygame.display.update()
    pygame.time.delay(5000)

# main
def main():
    red = pygame.Rect(700, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
    yellow = pygame.Rect(115, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
    clock = pygame.time.Clock()
    red_bullets = []
    yellow_bullets = []
    red_health = 10
    yellow_health =  10
    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
    
                
        # bullets
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LCTRL and len(yellow_bullets) < MAX_BULLET:
                    bullet = pygame.Rect(yellow.x + yellow.width, yellow.y + yellow.height//2 -2, 10, 5)
                    yellow_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()

                if event.key == pygame.K_RCTRL and len(red_bullets) < MAX_BULLET:
                    bullet = pygame.Rect(red.x , red.y + red.height//2 -2, 10, 5)
                    red_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()
           
            if event.type == RED_HIT:
                red_health -= 1
                BULLET_HIT_SOUND.play()

            if event.type == YELLOW_HIT:
                yellow_health -= 1
                BULLET_HIT_SOUND.play()
            
        winner_text = ''
            
        if red_health <= 0:
            winner_text = 'Yellow wins!'

        if yellow_health <= 0:
            winner_text = 'Red wins!'
           
        if winner_text != '':
            draw_winner(winner_text)
            break

        handle_bullets(yellow_bullets, red_bullets, red, yellow, RED_HIT, YELLOW_HIT)
        key_pressed = pygame.key.get_pressed()
        move_yellow(key_pressed, yellow)
        move_red(key_pressed, red)
        draw_window(red, yellow, red_bullets, yellow_bullets, red_health, yellow_health)
    
    
    main()



if __name__ == '__main__':
    main()
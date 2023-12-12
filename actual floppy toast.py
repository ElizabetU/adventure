import pygame, sys, random

def draw_floor():
    screen.blit(floor_surface, (floor_x_pos, 900))
    screen.blit(floor_surface, (floor_x_pos + 576,900))

def create_knife():
    random_knife_pos = random.choice(knife_height)
    bottom_knife = knife_surface.get_rect(midtop = (700, random_knife_pos))
    top_knife = knife_surface.get_rect(midbottom = (700, random_knife_pos - 300))
    return bottom_knife, top_knife

def move_knives(knives):
    for knife in knives:
        knife.centerx -= 5
    return knives

def draw_knives(knives):
    for knife in knives:
        if knife.bottom >= 1024:
            screen.blit(knife_surface, knife)
        else:
            flip_knife = pygame.transform.flip(knife_surface, False, True)
            screen.blit(flip_knife, knife)
def remove_knives(knives):
    for knife in knives:
        if knife.centerx == -600:
            knives.remove(knife)
    return knives

def check_collision(knives):
    for knife in knives:
        if toast_rect.colliderect(knife):
            return False

    if toast_rect.top <= -100 or toast_rect.bottom >= 900:
        return False

    return True

def rotate_toast(toast):
    new_toast = pygame.transform.rotozoom(toast, -toast_movement * 3, 1)
    return new_toast

def score_display(game_state):
    if game_state == 'main_game':
        score_surface = game_font.render(str(int(score)), True, (255, 255, 255))
        score_rect = score_surface.get_rect(center = (288, 100))
        screen.blit(score_surface, score_rect)
    if game_state == 'game_over':
        score_surface = game_font.render(f'Score:{int(score)}', True, (255, 255, 255))
        score_rect = score_surface.get_rect(center = (288, 100))
        screen.blit(score_surface, score_rect)

        high_score_surface = game_font.render(f'High Score:{int(score)}', True, (255, 255, 255))
        high_score_rect = score_surface.get_rect(center = (288, 850))
        screen.blit(high_score_surface, high_score_rect)
       
def update_score(score, high_score):
    if score > high_score:
        high_score = score
    return high_score

pygame.mixer.pre_init(frequency = 44100, size = 16, channels = 1, buffer = 512)
pygame.init()
screen = pygame.display.set_mode((576, 1024))
clock = pygame.time.Clock()
game_font = pygame.font.Font('04B_19.ttf',40)

#Game Variables

gravity = 0.25
toast_movement = 0
game_active = True
score = 0
high_score = 0

bg_surface = pygame.image.load('images/blue.jpeg').convert()
bg_surface = pygame.transform.scale2x(bg_surface)

floor_surface = pygame.image.load('images/blue.jpeg').convert()
floor_surface = pygame.transform.scale2x(floor_surface)
floor_x_pos = 0

toast_index = 0
TOAST = pygame.USEREVENT + 1
pygame.time.set_timer(TOAST,200)

toast_surface = pygame.image.load('images/toast.jpeg').convert_alpha()
toast_surface = pygame.transform.scale2x(toast_surface)
toast_rect = toast_surface.get_rect(center = (100,512))

knife_surface = pygame.image.load('images/knife.jpeg')
knife_surface = pygame.transform.scale2x(knife_surface)
knife_list = []
SPAWNKNIFE = pygame.USEREVENT
pygame.time.set_timer(SPAWNKNIFE, 1200)
knife_height = [400, 600, 800]

               
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and game_active:
                toast_movement = 0
                toast_movement -= 12
            if event.key == pygame.K_SPACE and game_active == False:
                game_active = True
                knife_list.clear()
                toast_rect.center = (100, 512)
                toast_movement = 0
                score = 0
                   
        if event.type == SPAWNKNIFE:
                knife_list.extend(create_knife())

                if event.type == SPAWNKNIFE:
                    if toast_index < 2:
                        toast_index += 1
                    else:
                        toast_index = 0
           
    screen.blit(bg_surface,(0,0))

    if game_active:
        # Toast
        toast_movement += gravity
        rotated_toast = rotate_toast(toast_surface)
        toast_rect.centery += toast_movement
        screen.blit(rotated_toast, toast_rect)
        game_active = check_collision(knife_list)

        #Knives
        knife_list = move_knives(knife_list)
        knife_list = remove_knives(knife_list)
        draw_knives(knife_list)

        score += 0.01
        score_display('main_game')
        high_score = update_score(score,high_score)
        score_display('game_over')
   
    #Floor
    floor_x_pos = -1
    draw_floor()
    if floor_x_pos <= -576:
            floor_x_pos = 0

   
           
           
    pygame.display.update()
    clock.tick(120)

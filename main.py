import pygame
import sys
from pygame.locals import *
import glob
from spritesheet_functions import SpriteSheet
import time
from coin_show import CoinSprite
pygame.init()

clock = pygame.time.Clock()

pygame.display.set_caption('OvO Runner Game')

bg = pygame.image.load("BG.png")
WINDOW_SIZE = (900, 600)
# This will be the Surface where we will blit everything
display = pygame.Surface((1000, 800))
# Then we will scale (every frame) the display onto the screen
screen = pygame.display.set_mode(WINDOW_SIZE, 0, 32)
startTime = time.time()

coin_locations = [[20,15], [350,15], [15, 330], [10, 430], [25, 430], [160, 530], [200, 530], [310, 480], [370, 480], [340, 380], [320, 180],[530, 530], [830, 530], [560, 380], [860, 120]]
coin_sprite_group_lists = []
coin_sprite_show_lists = []

for coin_location in coin_locations:
    coin_sprite_show = CoinSprite(coin_location)
    coin_sprite_show_lists.append(coin_sprite_show)
    coin_sprite_group_lists.append(pygame.sprite.Group(coin_sprite_show))


def show_coin():
    for coin_sprite_group_list in coin_sprite_group_lists:
        coin_sprite_group_list.update()
        coin_sprite_group_list.draw(display)


def collect_coin(rect, score):
    for coin_sprite_show_list in coin_sprite_show_lists:
        if rect.colliderect(coin_sprite_show_list):
            index_coin = coin_sprite_show_lists.index(coin_sprite_show_list)
            del coin_sprite_show_lists[index_coin]
            del coin_sprite_group_lists[index_coin]
            score = score + 10
    return score


def display_snowman():
    shon_man_loc = (500,200)
    show_img = pygame.image.load("SnowMan.png")
    show_img = pygame.transform.smoothscale(show_img,(60,60))
    display.blit(show_img, shon_man_loc)


font = pygame.font.SysFont(None, 30)
def show_score(text):
    screen_text = font.render(text, True, (255,165,0))
    display.blit(screen_text, (800, 5))
    game_time = "Time "+ str(int(time.time() - startTime))
    game_time_text = font.render(game_time, True, (255,165,0))
    display.blit(game_time_text, (800,25))


def game_over_msg(msg):
    font = pygame.font.SysFont(None, 50)
    screen_text = font.render(msg, True, (255, 165, 0))
    screen.fill((255,255,255))
    screen.blit(screen_text, (200, 200))

game_map1 = """
ooe--------------jo
------foooooe------
oe--j----y-----foe-
------j--y---------
---j----oyoo-----jo
------------------j
oooe-----------fooo
-----qr----j-------
oe---------------jo
------qr------j--
---qr-----j-----foo
""".splitlines()

game_map = [list(lst) for lst in game_map1]

tl = {}
dirt_img_orig = pygame.image.load('Tiles\\2.png')
grass_img_orig = pygame.image.load('Tiles\\7.png')
grassr_orig_1 = pygame.image.load('Tiles\\1.png')
grassr_orig_2 = pygame.image.load('Tiles\\3.png')
dirt_img_3 = pygame.image.load('Tiles\\10.png')
lowwidth_tile_orig = pygame.image.load('Tiles\\15.png')
lowwidth_tile_1_orig = pygame.image.load('Tiles\\14.png')
lowwidth_tile_2_orig = pygame.image.load('Tiles\\16.png')
dirt_end_soomth_orig = pygame.image.load('Tiles\\3.png')
dirt_start_soomth_orig = pygame.image.load('Tiles\\1.png')


fire = pygame.image.load('fire.png')
fire = pygame.transform.smoothscale(fire, (40,40))

tl["o"] = dirt_img = pygame.transform.smoothscale(dirt_img_orig, (50,50))
tl["x"] = grass_img = pygame.transform.smoothscale(grass_img_orig, (50,50))
tl["<"] = grassr = pygame.transform.smoothscale(grassr_orig_1, (50,50))
tl[">"] = grassr = pygame.transform.smoothscale(grassr_orig_2, (50,50))
tl["y"] = dirt_img_3 = pygame.transform.smoothscale(dirt_img_3, (50,50))
tl["j"] = lowwidth_tile = pygame.transform.smoothscale(lowwidth_tile_orig, (50,50))
tl["q"] = lowwidth_tile_1 = pygame.transform.smoothscale(lowwidth_tile_1_orig, (50,50))
tl["r"] = lowwidth_tile_2 = pygame.transform.smoothscale(lowwidth_tile_2_orig, (50,50))
tl["e"] = dirt_end_soomth = pygame.transform.smoothscale(dirt_end_soomth_orig, (50,50))
tl["f"] = dirt_start_soomth_orig = pygame.transform.smoothscale(dirt_start_soomth_orig, (50,50))


exit = pygame.image.load("exit.png")
exit = pygame.transform.smoothscale(exit, (50,50))



def collision_test(rect, tiles):
    "Returns the Rect of the tile with which the player collides"
    hit_list = []
    for tile in tiles:
        if rect.colliderect(tile):
            hit_list.append(tile)
    return hit_list


def move(rect, movement, tiles):
    collision_types = {
        'top': False, 'bottom': False, 'right': False, 'left': False}
    rect.x += movement[0]
    hit_list = collision_test(rect, tiles)
    for tile in hit_list:
        if movement[0] > 0:
            rect.right = tile.left
            collision_types['right'] = True
        elif movement[0] < 0:
            rect.left = tile.right
            collision_types['left'] = True
    rect.y += movement[1]
    hit_list = collision_test(rect, tiles)
    for tile in hit_list:
        if movement[1] > 0:
            rect.bottom = tile.top
            collision_types['bottom'] = True
        elif movement[1] < 0:
            rect.top = tile.bottom
            collision_types['top'] = True
    return rect, collision_types

def main():
    player_img = pygame.image.load('player.png').convert()
    player_img.set_colorkey((0, 0, 0))
    player_rect = pygame.Rect(100, 350, 30, 30)
    moving_right = False
    moving_left = False
    # For the pygame.transform.flip(player_img, 1, 0)
    stay_right = True
    momentum = 0
    air_timer = 0
    score = 0
    game_over = False
    loop = 1
    won = 0
    startTime = time.time()
    while loop:
        # CLEAR THE SCREEN
        # display.fill((146, 244, 255))
        if game_over:
            if won == 1:
                msg = "You won the game press w to continue"
                game_over_msg(msg)
            else:
                msg = "You Lost the press w to continue"
                game_over_msg(msg)
            for event in pygame.event.get():
                if event.type == QUIT:
                    loop = 0
                if event.type == KEYDOWN:
                    if event.key == K_w:
                        main()
        else:
            display.blit(bg, (0,0))
            display.blit(fire, (20,20))
            # Tiles are blitted  ==========================
            tile_rects = []
            y = 0
            for line_of_symbols in game_map:
                x = 0
                for symbol in line_of_symbols:
                    if symbol in tl:
                        # draw the symbol for image
                        display.blit(
                            tl[symbol], (x * 50, y * 50))
                    # draw a rectangle for every symbol except for the empty one
                    if symbol != "-":
                        tile_rects.append(pygame.Rect(x * 50, y * 50, 30, 40))
                    x += 1
                y += 1
            # ================================================

            # MOVEMENT OF THE PLAYER
            player_movement = [0, 0]
            if moving_right:
                player_movement[0] += 2.5
            if moving_left:
                player_movement[0] -= 2.5
            player_movement[1] += momentum
            momentum += 1.7
            if momentum > 6:
                momentum = 6

            player_rect, collisions = move(player_rect, player_movement, tile_rects)

            if collisions['bottom']:
                air_timer = 0
                momentum = 0
            else:
                air_timer += 1

            # Flip the player image when goes to the left
            if stay_right:
                display.blit(
                    player_img, (player_rect.x, player_rect.y))
            else:
                display.blit(
                    pygame.transform.flip(player_img, 1, 0),
                    (player_rect.x, player_rect.y))

            for event in pygame.event.get():
                if event.type == QUIT:
                    loop = 0
                if event.type == KEYDOWN:
                    if event.key == K_RIGHT:
                        moving_right = True
                        stay_right = True
                    if event.key == K_LEFT:
                        moving_left = True
                        stay_right = False
                    if event.key == K_SPACE:
                        if air_timer < 10:
                            momentum = -20
                if event.type == KEYUP:
                    if event.key == K_RIGHT:
                        moving_right = False
                    if event.key == K_LEFT:
                        moving_left = False

            if player_rect.y + 300 > WINDOW_SIZE[0]:
                game_over = True
            show_coin()
            score = collect_coin(player_rect, score)
            display_snowman()
            if player_rect.x > 850 and player_rect.y > 500:
                game_over = True
                won = 1
            show_score("Score: "+str(score))
            screen.blit(display, (0, 0))
        pygame.display.update()
        clock.tick(100)
main()
pygame.quit()
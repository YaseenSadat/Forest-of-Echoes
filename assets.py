"""
This module contains the assignment of every image and mp3 file into their selected variables
"""
import pygame

pygame.init()
display_info = pygame.display.Info()
window_size = (display_info.current_w, display_info.current_h)
clock = pygame.time.Clock().tick(60)
screen = pygame.display.set_mode(window_size, pygame.FULLSCREEN)
pygame.mixer.init()
pygame.display.set_caption("Forest of Echoes")

# Colours
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
D_BLUE = (7, 18, 34, 255)
GRAY = (128, 128, 128)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
L_GREEN = (63, 112, 77)
ORANGE = (254, 68, 3, 255)
YELLOW = (255, 252, 15, 255)

# Sound effects and Music
start_music = 'graphics/start_music.mp3'
game_music = 'graphics/game_music.mp3'
win_music = 'graphics/win_music.mp3'
lose_music = 'graphics/lose_music.mp3'
inventory_use_music = 'graphics/inventory_use_music.mp3'
chest_sound = 'graphics/chest_sound.mp3'
flaregun_sound = 'graphics/flaregun_sound.mp3'
place_sound = 'graphics/place_sound.mp3'
eat_sound = 'graphics/eat_sound.mp3'
pickup_sound = 'graphics/pickup_sound.mp3'
campfire_sound = 'graphics/campfire_sound.mp3'
footsteps_sound = 'graphics/footsteps_sound.mp3'
craft_sound = 'graphics/craft_sound.mp3'
sign_sound = 'graphics/sign_sound.mp3'
error_sound = 'graphics/error_sound.mp3'
dying_sound = 'graphics/dying_sound.mp3'
select_sound = 'graphics/select_sound.mp3'
breathe_sound = 'graphics/breathe_sound.mp3'


# Background Image
background_start_image = pygame.transform.scale(pygame.image.load('graphics/background_start_screen.png'), window_size)

# Buttons frames
button_image = pygame.transform.scale(pygame.image.load('graphics/button_back.png'), (230, 80))
small_button_image = pygame.transform.scale(pygame.image.load('graphics/button_back.png'), (150, 50))
game_button = pygame.transform.scale(pygame.image.load('graphics/interact_button.png'), (130, 50))
game_button1 = pygame.transform.scale(pygame.image.load('graphics/interact_button.png'), (90, 45))
item_frame = pygame.transform.scale(pygame.image.load('graphics/item_frame.png'), (170, 170))
item_frame1 = pygame.transform.scale(pygame.image.load('graphics/item_frame.png'), (120, 120))

# Game Signs Images
wooden_sign1 = pygame.transform.scale(pygame.image.load('graphics/wooden_sign1.png'), (900, 800))
wooden_sign2 = pygame.transform.scale(pygame.image.load('graphics/wooden_sign2.png'), (900, 800))
wooden_sign3 = pygame.transform.scale(pygame.image.load('graphics/wooden_sign3.png'), (900, 800))

# Player Hearts Images
full_heart = pygame.transform.scale(pygame.image.load('graphics/full_heart.png'), (40, 40))
half_heart = pygame.transform.scale(pygame.image.load('graphics/half_heart.png'), (40, 40))
empty_heart = pygame.transform.scale(pygame.image.load('graphics/empty_heart.png'), (40, 40))

# Start screen rect
start_button_image = button_image
menu_button_image = button_image
exit_button_image = button_image
start_button_rect = start_button_image.get_rect()
menu_button_rect = menu_button_image.get_rect()
exit_button_rect = exit_button_image.get_rect()
small_button_rect = small_button_image.get_rect()
start_button_rect.x, start_button_rect.y = window_size[0] / 2.5, 650
menu_button_rect.x, menu_button_rect.y = window_size[0] / 2.5, 750
exit_button_rect.x, exit_button_rect.y = window_size[0] / 2.5, 850

# Game Screen rect
game_button_size = game_button.get_size()
small_button_size = small_button_image.get_size()
interact_button_rect = pygame.Rect(1350, 500, *game_button_size)
pick_up_button_rect = pygame.Rect(1350, 600, *game_button_size)
use_item_button_rect = pygame.Rect(1350, 700, *game_button_size)
inventory_button_rect = pygame.Rect(1350, 800, *game_button_size)
help_button_rect = pygame.Rect(1350, 200, *game_button_size)
yes_button_rect = pygame.Rect(5, 200, *small_button_size)
no_button_rect = pygame.Rect(5, 280, *small_button_size)

# Selection Screen Rect
proceed_rect = pygame.Rect(1300, 880, *game_button_size)
map1_rect = pygame.Rect(1110, 480, *game_button_size)
map2_rect = pygame.Rect(1110, 630, *game_button_size)
map3_rect = pygame.Rect(1110, 780, *game_button_size)
dark_mode_rect = pygame.Rect(210, 430, 80, 100)
male_rect = pygame.Rect(653, 400, 200, 250)
girl_rect = pygame.Rect(653, 680, 200, 250)
easy_rect = pygame.Rect(55, 730, 130, 60)
medium_rect = pygame.Rect(190, 730, 120, 60)
hard_rect = pygame.Rect(310, 730, 130, 60)

# Use Screen Rect
pear_rect = pygame.Rect(460, 541, 55, 55)
apple_rect = pygame.Rect(590, 541, 55, 55)
orange_rect = pygame.Rect(725, 541, 55, 55)
campfire_rect = pygame.Rect(852, 538, 70, 70)
flaregun_rect = pygame.Rect(990, 538, 70, 70)
game_button_rect = pygame.Rect(1350, 440, 90, 45)

# Inventory Screen Rect
craft_button_rect = pygame.Rect(window_size[0] - 290, 690, *game_button_size)
campfire_materials = ['Matchbox', 'Logs', 'Rock']

# Menu Screen Rect
reveal_rect = pygame.Rect(1200, 750, *game_button_size)

# Fonts
dash_180 = pygame.font.Font('graphics/dashhorizon.otf', 180)
pixel_150 = pygame.font.Font('graphics/pixelboy.ttf', 150)
pixel_100 = pygame.font.Font('graphics/pixelboy.ttf', 100)
pixel_70 = pygame.font.Font('graphics/pixelboy.ttf', 70)
pixel_50 = pygame.font.Font('graphics/pixelboy.ttf', 50)
pixel_40 = pygame.font.Font('graphics/pixelboy.ttf', 40)
pixel_35 = pygame.font.Font('graphics/pixelboy.ttf', 35)
pixel_30 = pygame.font.Font('graphics/pixelboy.ttf', 30)
pixel_24 = pygame.font.Font('graphics/pixelboy.ttf', 24)
steph_24 = pygame.font.Font('graphics/Stepalange.otf', 24)
steph_20 = pygame.font.Font('graphics/Stepalange.otf', 20)
steph_15 = pygame.font.Font('graphics/Stepalange.otf', 15)

# Pathway Images and Rotations
pathway_hori_image = pygame.image.load('graphics/pathway_hori.png')
pathway_vert_image = pygame.image.load('graphics/pathway_vert.png')
orig_l_curve_image = pygame.image.load('graphics/L_curve.png')
t_path_image = pygame.image.load('graphics/T_path.png')
all_path_image = pygame.image.load('graphics/all_path.png')

orig_l_curve_image = pygame.transform.scale(orig_l_curve_image, (50, 50))
pathway_hori_image = pygame.transform.scale(pathway_hori_image, (55, 45))
pathway_vert_image = pygame.transform.scale(pathway_vert_image, (45, 55))
t_path_image = pygame.transform.scale(t_path_image, (50, 45))
all_path_image = pygame.transform.scale(all_path_image, (50, 50))

inverse_l_image = pygame.transform.rotate(orig_l_curve_image, 90)
up_left_l_image = pygame.transform.rotate(orig_l_curve_image, 270)
up_right_l_image = pygame.transform.rotate(orig_l_curve_image, 180)
upside_down_t_image = pygame.transform.rotate(t_path_image, 180)
right_t_image = pygame.transform.rotate(t_path_image, 90)

l_curve_image = pygame.transform.scale(orig_l_curve_image, (50, 45))
inverse_l_image = pygame.transform.scale(inverse_l_image, (50, 45))
up_right_l_image = pygame.transform.scale(up_right_l_image, (45, 50))

# Campfire Images
campfire_image = pygame.transform.scale(pygame.image.load('graphics/campfire_img.png'), (40, 40))
campfire_base = pygame.transform.scale(pygame.image.load('graphics/campfire_base.png'), (40, 40))

campfire_images = [
    pygame.transform.scale(pygame.image.load('graphics/campfire_img.png'), (40, 40)),
    pygame.transform.scale(pygame.image.load('graphics/campfire_1.png'), (40, 40)),
    pygame.transform.scale(pygame.image.load('graphics/campfire_2.png'), (40, 40)),
    pygame.transform.scale(pygame.image.load('graphics/campfire_3.png'), (40, 40))
]

# Selection Screen Images
off_switch = pygame.transform.scale(pygame.image.load('graphics/off_switch.png'), (80, 100))
on_switch = pygame.transform.scale(pygame.image.load('graphics/on_switch.png'), (80, 100))

check_mark = pygame.transform.scale(pygame.image.load('graphics/check_mark.png'), (100, 60))
difficulty_scale = pygame.transform.scale(pygame.image.load('graphics/difficulty_scale.png'), (400, 80))
difficulty_check = pygame.transform.scale(pygame.image.load('graphics/diff_check.png'), (50, 50))

example_man = pygame.transform.scale(pygame.image.load('graphics/man_down_1.png'), (200, 250))
example_girl = pygame.transform.scale(pygame.image.load('graphics/girl_down_1.png'), (200, 250))

man_dead = pygame.transform.scale(pygame.image.load('graphics/male_dead.png'), (40, 30))
girl_dead = pygame.transform.scale(pygame.image.load('graphics/girl_dead.png'), (40, 30))

# Male and Female Images
man_up_0 = pygame.transform.scale(pygame.image.load('graphics/man_up_0.png'), (30, 40))
man_up_1 = pygame.transform.scale(pygame.image.load('graphics/man_up_1.png'), (30, 40))
man_up_2 = pygame.transform.scale(pygame.image.load('graphics/man_up_2.png'), (30, 40))
girl_up_0 = pygame.transform.scale(pygame.image.load('graphics/girl_up_0.png'), (30, 40))
girl_up_1 = pygame.transform.scale(pygame.image.load('graphics/girl_up_1.png'), (30, 40))
girl_up_2 = pygame.transform.scale(pygame.image.load('graphics/girl_up_2.png'), (30, 40))

man_down_0 = pygame.transform.scale(pygame.image.load('graphics/man_down_0.png'), (30, 40))
man_down_1 = pygame.transform.scale(pygame.image.load('graphics/man_down_1.png'), (30, 40))
man_down_2 = pygame.transform.scale(pygame.image.load('graphics/man_down_2.png'), (30, 40))
girl_down_0 = pygame.transform.scale(pygame.image.load('graphics/girl_down_0.png'), (30, 40))
girl_down_1 = pygame.transform.scale(pygame.image.load('graphics/girl_down_1.png'), (30, 40))
girl_down_2 = pygame.transform.scale(pygame.image.load('graphics/girl_down_2.png'), (30, 40))

man_right_0 = pygame.transform.scale(pygame.image.load('graphics/man_right_0.png'), (30, 40))
man_right_1 = pygame.transform.scale(pygame.image.load('graphics/man_right_1.png'), (30, 40))
man_right_2 = pygame.transform.scale(pygame.image.load('graphics/man_right_2.png'), (30, 40))
girl_right_0 = pygame.transform.scale(pygame.image.load('graphics/girl_right_0.png'), (30, 40))
girl_right_1 = pygame.transform.scale(pygame.image.load('graphics/girl_right_1.png'), (30, 40))
girl_right_2 = pygame.transform.scale(pygame.image.load('graphics/girl_right_2.png'), (30, 40))

man_left_0 = pygame.transform.scale(pygame.image.load('graphics/man_left_0.png'), (30, 40))
man_left_1 = pygame.transform.scale(pygame.image.load('graphics/man_left_1.png'), (30, 40))
man_left_2 = pygame.transform.scale(pygame.image.load('graphics/man_left_2.png'), (30, 40))
girl_left_0 = pygame.transform.scale(pygame.image.load('graphics/girl_left_0.png'), (30, 40))
girl_left_1 = pygame.transform.scale(pygame.image.load('graphics/girl_left_1.png'), (30, 40))
girl_left_2 = pygame.transform.scale(pygame.image.load('graphics/girl_left_2.png'), (30, 40))

man_down = [man_down_1, man_down_0, man_down_2]
man_up = [man_up_1, man_up_0, man_up_2]
man_left = [man_left_1, man_left_0, man_left_2]
man_right = [man_right_1, man_right_0, man_right_2]
man_dead1 = [man_dead]

girl_down = [girl_down_1, girl_down_0, girl_down_2]
girl_up = [girl_up_1, girl_up_0, girl_up_2]
girl_left = [girl_left_1, girl_left_0, girl_left_2]
girl_right = [girl_right_1, girl_right_0, girl_right_2]
girl_dead1 = [girl_dead]


# GAME TILES

chest_image = pygame.transform.scale(pygame.image.load('graphics/chest.png'), (40, 40))
sign_tile_image = pygame.transform.scale(pygame.image.load('graphics/sign_tile.png'), (40, 40))

grass_tile_image = pygame.transform.scale(pygame.image.load('graphics/green_grass_tile.png'), (50, 50))
flower_grass_tile_image = pygame.transform.scale(pygame.image.load('graphics/flower_grass_tile.png'), (50, 50))
pathway_tile_image = pygame.transform.scale(pygame.image.load('graphics/pathways_tile.png'), (50, 50))
individual_tree_image = pygame.transform.scale(pygame.image.load('graphics/individual_tree.png'), (44, 44))
water_tile_image = pygame.transform.scale(pygame.image.load('graphics/water_tile.png'), (50, 50))
bridge_tile_image = pygame.transform.scale(pygame.image.load('graphics/bridge_tile.png'), (50, 50))
hill_tile_image = pygame.transform.scale(pygame.image.load('graphics/hill_tile.png'), (200, 190))
red_bushes_image = pygame.transform.scale(pygame.image.load('graphics/red_bushes.png'), (40, 40))
white_bushes_image = pygame.transform.scale(pygame.image.load('graphics/white_bushes.png'), (40, 40))
purple_bushes_image = pygame.transform.scale(pygame.image.load('graphics/purple_bushes.png'), (40, 40))
blue_bushes_image = pygame.transform.scale(pygame.image.load('graphics/blue_bushes.png'), (40, 40))
tulips_image = pygame.transform.scale(pygame.image.load('graphics/tulips.png'), (40, 40))
ground_vern_image = pygame.transform.scale(pygame.image.load('graphics/ground_vern.png'), (40, 40))


# Item Images
rock_image = pygame.transform.scale(pygame.image.load('graphics/rock.png'), (30, 30))
w_rock_image = pygame.transform.scale(pygame.image.load('graphics/w_rock_image.png'), (30, 30))
blue_key_image = pygame.transform.scale(pygame.image.load('graphics/blue_key.png'), (15, 25))
gold_key_image = pygame.transform.scale(pygame.image.load('graphics/gold_key.png'), (15, 25))
copper_key_image = pygame.transform.scale(pygame.image.load('graphics/copper_key.png'), (15, 25))
wood_key_image = pygame.transform.scale(pygame.image.load('graphics/wood_key.png'), (15, 25))
matchbox_image = pygame.transform.scale(pygame.image.load('graphics/matchbox.png'), (30, 30))
w_matchbox_image = pygame.transform.scale(pygame.image.load('graphics/w_matchbox_img.png'), (30, 30))
logs_image = pygame.transform.scale(pygame.image.load('graphics/logs_image.png'), (40, 25))
w_logs_image = pygame.transform.scale(pygame.image.load('graphics/w_logs_image.png'), (40, 25))
orange_fruit_image = pygame.transform.scale(pygame.image.load('graphics/orange_fruit.png'), (25, 25))
pear_fruit_image = pygame.transform.scale(pygame.image.load('graphics/pear_fruit.png'), (25, 25))
apple_fruit_image = pygame.transform.scale(pygame.image.load('graphics/apple_fruit.png'), (25, 25))
w_campfire_image = pygame.transform.scale(pygame.image.load('graphics/w_campfire_img.png'), (90, 90))
flaregun_image = pygame.transform.scale(pygame.image.load('graphics/flare_gun.png'), (55, 55))
jewel_bag = pygame.transform.scale(pygame.image.load('graphics/jewel_bag.png'), (55, 55))

"""
This module contains functions to support the main game logic and rendering for a Pygame-based game.

Functions:
- render_text: Renders multiple lines of text on the screen.
- display_text: Displays win or lose text on the screen.
- pause_campfire: Stops the campfire sound if it is playing.
- open_chest: Handles the actions when a player opens a chest.
- get_health_decrement: Returns the health decrement interval based on the game difficulty.
- initialize_player: Initializes the player object with the appropriate images.
- display_inventory: Displays the player's inventory on the screen.
- display_menu: Displays the game menu with controls, credits, and help sections.
- display_selection: Displays the selection screen where users choose preferences.
- display_win: Displays the win screen with statistics.
- display_gameover: Displays the game over screen with statistics.
- display_start: Displays the start screen with game title and options.
- display_use_text: Displays the use item screen with options.
- display_mask: Displays a mask effect for dark mode around the player.
- display_messages: Displays various game messages based on player actions.
- display_buttons: Displays in-game buttons for interaction.
- display_time: Displays the elapsed time on the screen.
- display_hearts: Displays the player's health as heart icons.
- interact_checker: Checks the player's current grid code for interactions.
- display_fruit_message: Displays a message when the player eats a fruit.
- display_error_message: Displays an error message for invalid actions.
- display_campfire_message: Displays a message when the player places a campfire.
- display_items: Displays items from the player's inventory on the screen.
- get_item_image: Returns the image associated with an item name.
- campfire_valid_loc: Checks if a location is valid for placing a campfire.
- display_map: Displays the game map and items on the screen.
"""

from assets import *
from data import *


def render_text(screen, text_lines, font, color, start_pos, line_spacing):
    """
    Renders multiple lines of text on the screen for the menu.
    """
    x, y = start_pos
    for line in text_lines:
        text_surface = font.render(line, True, color)
        screen.blit(text_surface, (x, y))
        y += text_surface.get_height() + line_spacing


def get_map_difficulty(value) -> str:
    """
    By getting the map name it retuns the map difficulty
    """
    if value == 'map1':
        return 'Easy'
    elif value == 'map2':
        return 'Medium'
    elif value == 'map3':
        return 'Hard'


def display_intro(screen, start_time):
    """
    Display the introduction scene with text appearing every 5 seconds.
    """
    screen.fill(D_BLUE)

    screen.blit(small_button_image, (5, 5))
    return_text = pixel_40.render('RETURN', True, WHITE)
    return_text_rect = return_text.get_rect(topleft=(24, 20))
    screen.blit(return_text, return_text_rect)

    text1 = pixel_40.render('Story Intro', True, WHITE)
    screen.blit(text1, (680, 100))

    text_lines = [
        "     Deep within the enigmatic expanse of the Whispering Woods, a legend persists, veiled in the",
        "shroud of twilight and tangled roots. This forest, ancient and whispering secrets of old, guards the",
        "path to a mysterious treasure, a chest filled with jewels worth millions and the elusive promise of",
        "escape.",
        "",
        "     You are an intrepid traveler who, by fate or fortune, finds yourself lost amidst the foreboding trees",
        "as dusk descends. With the canopy closing in and the night creatures stirring, hope seems as",
        "distant as the setting sun. Yet, scattered through the forest, hidden enigmas crafted by nature",
        "itself beckon to those daring enough to solve them.",
        "",
        "     Your journey is fraught with peril, for many have sought the chest's riches and means of escape,",
        "only to become mere whispers among the leaves. Arm yourself with courage and cunning; the",
        "forest neither aids nor obstructs, but silently observes as you carve your path through its heart.",
        "",
        "     Will you uncover the secrets of the Whispering Woods and claim what countless others have",
        "sought, or will you, too, fade into the forest's eternal tales?",
        "",
        '                                                         ~ Good Luck Traveler! ~'

    ]

    current_time = pygame.time.get_ticks()
    elapsed_time = (current_time - start_time) // 1000

    paragraphs_to_display = elapsed_time // 6

    paragraphs = [
        text_lines[0:3],
        text_lines[4:8],
        text_lines[9:13],
        text_lines[14:16],
        text_lines[17:19]
    ]

    for i in range(paragraphs_to_display + 1):
        if i < len(paragraphs):
            render_text(screen, paragraphs[i], steph_24, WHITE, (350, 170 + i * 160), 8)


def display_text(screen, value):
    """
    Displays win or lose text on the screen.
    """
    if value == 'win':
        end_text = pixel_30.render("Congrats on Escaping the Forest", True, WHITE)
        screen.blit(end_text, (window_size[0] / 2 - end_text.get_width() / 2 + 50, 840))
        end_text1 = steph_15.render("You will be shortly transported to the end page!", True, WHITE)
        screen.blit(end_text1, (window_size[0] / 2 - end_text1.get_width() / 2 + 50, 860))
    elif value == 'lose':
        end_text = pixel_30.render("Unfortunate ending!!", True, WHITE)
        screen.blit(end_text, (window_size[0] / 2 - end_text.get_width() / 2 + 50, 840))
        end_text1 = steph_15.render("You will be shortly transported to the end page!", True, WHITE)
        screen.blit(end_text1, (window_size[0] / 2 - end_text1.get_width() / 2 + 50, 860))


def pause_campfire(campfire_sound_playing, campfire_sound1) -> bool:
    """
    Stops the campfire sound if it is playing.
    """
    if campfire_sound_playing:
        campfire_sound1.stop()
        return False
    return campfire_sound_playing


def open_chest(player):
    """
    Handles the actions when a player opens a chest.
    """
    play_sound_effect(chest_sound, 0.4)
    player.remove_item_from_inventory('Wood Key')
    player.remove_item_from_inventory('Gold Key')
    player.remove_item_from_inventory('Blue Key')
    player.remove_item_from_inventory('Copper Key')
    player.inventory['FlareGun'] = 'Your only escape! Find the perfect place to fire!'
    player.inventory['JewelBag'] = 'The Hidden Treasure Worth Millions!!'


def get_health_decrement(game_state) -> int:
    """
    Returns the health decrement interval based on the game difficulty.
    """
    if game_state.current_difficulty() == 'easy':
        health_decrement_interval = 25000
    elif game_state.current_difficulty() == 'medium':
        health_decrement_interval = 16000
    elif game_state.current_difficulty() == 'hard':
        health_decrement_interval = 1000
    else:
        raise ValueError
    return health_decrement_interval


def initialize_player(game_state) -> Player:
    """
    Initializes the player object with the appropriate images.
    """
    player_images = {
        'down': man_down,
        'up': man_up,
        'left': man_left,
        'right': man_right,
        'dead': man_dead1
    }
    if game_state.current_gender() == 'male':
        player_images = {
            'down': man_down,
            'up': man_up,
            'left': man_left,
            'right': man_right,
            'dead': man_dead1
        }
    elif game_state.current_gender() == 'girl':
        player_images = {
            'down': girl_down,
            'up': girl_up,
            'left': girl_left,
            'right': girl_right,
            'dead': girl_dead1
        }

    return Player(260, 150, [1, 1], player_images)


def display_inventory(screen, display_message, player):
    """
    Displays the player's inventory on the screen.
    """
    screen.fill(D_BLUE)

    if display_message:
        blah = steph_15.render('You have crafted a Campfire!', True, WHITE)
        screen.blit(blah, (window_size[0] - 290, 750))
        blah1 = steph_15.render('Items have been removed from your inventory', True, WHITE)
        screen.blit(blah1, (window_size[0] - 340, 770))

    pygame.draw.rect(screen, BLACK, pygame.Rect(400, 200, 706, 564))
    start_x, start_y = 400, 200
    for row in range(4):
        for col in range(5):
            x = start_x + col * 135
            y = start_y + row * 132
            screen.blit(item_frame, (x, y))

    inventory_text = pixel_150.render('INVENTORY', True, GRAY)
    inventory_text1 = pixel_150.render('INVENTORY', True, WHITE)
    screen.blit(inventory_text, (438, 80))
    screen.blit(inventory_text1, (443, 85))

    screen.blit(small_button_image, (5, 5))
    return_text = pixel_40.render('RETURN', True, WHITE)
    return_text_rect = return_text.get_rect(topleft=(24, 20))
    screen.blit(return_text, return_text_rect)

    new_matchbox = pygame.transform.scale(matchbox_image, (50, 50))
    w_matchbox = pygame.transform.scale(w_matchbox_image, (50, 50))
    new_log = pygame.transform.scale(logs_image, (45, 40))
    w_log = pygame.transform.scale(w_logs_image, (45, 40))
    new_rock = pygame.transform.scale(rock_image, (45, 45))
    w_rock = pygame.transform.scale(w_rock_image, (45, 45))
    campfire_resized = pygame.transform.scale(campfire_image, (90, 90))

    screen.blit(item_frame1, (window_size[0] - 370, 470))
    screen.blit(item_frame1, (window_size[0] - 270, 470))
    screen.blit(item_frame1, (window_size[0] - 170, 470))

    if all(key in player.inventory for key in campfire_materials):
        craft_text = pixel_40.render('CRAFT', True, GREEN)
        screen.blit(new_matchbox, (window_size[0] - 335, 500))
        screen.blit(new_log, (window_size[0] - 233, 505))
        screen.blit(new_rock, (window_size[0] - 135, 503))
        screen.blit(campfire_resized, (window_size[0] - 260, 580))
    else:
        craft_text = pixel_40.render('CRAFT', True, RED)
        screen.blit(w_matchbox, (window_size[0] - 335, 500))
        screen.blit(w_log, (window_size[0] - 233, 505))
        screen.blit(w_rock, (window_size[0] - 135, 503))
        if 'Matchbox' in player.inventory:
            screen.blit(new_matchbox, (window_size[0] - 335, 500))
        if 'Logs' in player.inventory:
            screen.blit(new_log, (window_size[0] - 233, 505))
        if 'Rock' in player.inventory:
            screen.blit(new_rock, (window_size[0] - 135, 503))
        screen.blit(w_campfire_image, (window_size[0] - 260, 580))

    screen.blit(small_button_image, craft_button_rect.topleft)
    screen.blit(small_button_image, (window_size[0] - 290, 690))
    craft_text_rect = craft_text.get_rect(topleft=(window_size[0] - 260, 705))
    screen.blit(craft_text, craft_text_rect)

    start_y1 = 200
    count = 0

    for item in player.inventory:
        item_image = get_item_image(item)
        item_descr = player.inventory[item]

        if item_image:
            scaled_item_image = pygame.transform.scale(item_image, (55, 55))
            scaled_item_image1 = pygame.transform.scale(item_image, (45, 45))

            col, row = count % 5, count // 5

            screen_x = 445 + col * 135 + (75 - scaled_item_image.get_width()) // 2
            screen_y = 240 + row * 135 + (75 - scaled_item_image.get_height()) // 2

            screen.blit(scaled_item_image, (screen_x, screen_y))
            screen.blit(scaled_item_image1, (10, start_y1))
            decription = steph_15.render(item_descr, True, WHITE)
            screen.blit(decription, (70, start_y1 + 17))

            start_y1 += 60
            count = count + 1


def display_menu(screen, is_reveal):
    """
    Displays the menu on the screen.
    """
    screen.fill(D_BLUE)
    screen.blit(small_button_image, (5, 5))
    return_text = pixel_40.render('RETURN', True, WHITE)
    return_text_rect = return_text.get_rect(topleft=(24, 20))
    screen.blit(return_text, return_text_rect)

    text1 = pixel_40.render('Controls', True, WHITE)
    screen.blit(text1, (50, 700))

    text2 = steph_15.render('W or Up Arrow = Upward Movement', True, WHITE)
    screen.blit(text2, (50, 740))
    text3 = steph_15.render('A or Left Arrow = Leftward Movement', True, WHITE)
    screen.blit(text3, (50, 760))
    text4 = steph_15.render('D or Right Arrow = Rightward Movement', True, WHITE)
    screen.blit(text4, (50, 780))
    text5 = steph_15.render('S or Down Arrow = Downward Movement', True, WHITE)
    screen.blit(text5, (50, 800))
    text6 = steph_15.render('Rest of the game mechanics are buttons which you can click', True, WHITE)
    screen.blit(text6, (50, 830))

    text1 = pixel_40.render('Credits', True, WHITE)
    screen.blit(text1, (650, 700))

    text2 = steph_15.render('Game Development: 100% Me', True, WHITE)
    screen.blit(text2, (650, 740))
    text3 = steph_15.render('Digital Images: Varied between AI generation and Google Images', True, WHITE)
    screen.blit(text3, (650, 760))
    text4 = steph_15.render('Music and Sound Effects: Found online through youtube', True, WHITE)
    screen.blit(text4, (650, 780))

    text1 = pixel_40.render('Help ~ Spoilers', True, WHITE)
    screen.blit(text1, (1150, 700))

    screen.blit(small_button_image, (1200, 750))
    proceed_text = pixel_35.render('Reveal', True, WHITE)
    screen.blit(proceed_text, (1230, 765))

    if is_reveal:
        text2 = steph_15.render('There are 4 keys scattered throughout the map', True, WHITE)
        screen.blit(text2, (1150, 830))
        text3 = steph_15.render('After collecting the four, you can open the chest', True, WHITE)
        screen.blit(text3, (1150, 850))
        text4 = steph_15.render('You must fire the flare gun at the top of the hill', True, WHITE)
        screen.blit(text4, (1150, 870))
        text5 = steph_15.render('The hill is always in the top right of the map', True, WHITE)
        screen.blit(text5, (1150, 890))

    text1 = pixel_40.render('Story Intro', True, WHITE)
    screen.blit(text1, (680, 100))
    text_lines = [
        "     Deep within the enigmatic expanse of the Whispering Woods, a legend persists, veiled in the",
        "shroud of twilight and tangled roots. This forest, ancient and whispering secrets of old, guards the",
        "path to a mysterious treasure, a chest filled with jewels worth millions and the elusive promise of",
        "escape.",
        "",
        "     You are an intrepid traveler who, by fate or fortune, finds yourself lost amidst the foreboding trees",
        "as dusk descends. With the canopy closing in and the night creatures stirring, hope seems as",
        "distant as the setting sun. Yet, scattered through the forest, hidden enigmas crafted by nature",
        "itself beckon to those daring enough to solve them.",
        "",
        "     Your journey is fraught with peril, for many have sought the chest's riches and means of escape,",
        "only to become mere whispers among the leaves. Arm yourself with courage and cunning; the",
        "forest neither aids nor obstructs, but silently observes as you carve your path through its heart.",
        "",
        "     Will you uncover the secrets of the Whispering Woods and claim what countless others have",
        "sought, or will you, too, fade into the forest's eternal tales?"
    ]
    render_text(screen, text_lines, steph_24, WHITE, (350, 170), 5)


def display_selection(screen, game_state, which_msg, current_time, msg_start):
    """
    Displays the selection screen where users choose preferences.
    """
    screen.fill(D_BLUE)

    if which_msg == 'error' and current_time - msg_start <= 3000:
        blah = steph_15.render('Must Select a character and Map!', True, WHITE)
        screen.blit(blah, (1270, 860))
    elif which_msg == 'error':
        pygame.draw.rect(screen, D_BLUE, pygame.Rect(1170, 700, 250, 100))

    if game_state.current_map() == 'map1':
        pygame.draw.rect(screen, D_BLUE, pygame.Rect(1110, 480, 210, 100))
        screen.blit(check_mark, (1300, 480))
    elif game_state.current_map() == 'map2':
        pygame.draw.rect(screen, D_BLUE, pygame.Rect(1110, 480, 210, 100))
        screen.blit(check_mark, (1300, 630))
    elif game_state.current_map() == 'map3':
        pygame.draw.rect(screen, D_BLUE, pygame.Rect(1110, 480, 210, 100))
        screen.blit(check_mark, (1300, 780))

    if game_state.current_gender() == 'male':
        pygame.draw.rect(screen, D_BLUE, pygame.Rect(850, 750, 210, 100))
        screen.blit(check_mark, (900, 500))
    elif game_state.current_gender() == 'girl':
        pygame.draw.rect(screen, D_BLUE, pygame.Rect(850, 490, 210, 100))
        screen.blit(check_mark, (900, 780))

    if game_state.current_difficulty() == 'easy':
        pygame.draw.rect(screen, D_BLUE, pygame.Rect(100, 790, 60, 60))
        pygame.draw.rect(screen, D_BLUE, pygame.Rect(230, 790, 60, 60))
        pygame.draw.rect(screen, D_BLUE, pygame.Rect(330, 790, 60, 60))
        screen.blit(difficulty_check, (100, 800))
    elif game_state.current_difficulty() == 'medium':
        pygame.draw.rect(screen, D_BLUE, pygame.Rect(100, 790, 60, 60))
        pygame.draw.rect(screen, D_BLUE, pygame.Rect(230, 790, 60, 60))
        pygame.draw.rect(screen, D_BLUE, pygame.Rect(330, 790, 60, 60))
        screen.blit(difficulty_check, (230, 800))
    elif game_state.current_difficulty() == 'hard':
        pygame.draw.rect(screen, D_BLUE, pygame.Rect(100, 790, 60, 60))
        pygame.draw.rect(screen, D_BLUE, pygame.Rect(230, 790, 60, 60))
        pygame.draw.rect(screen, D_BLUE, pygame.Rect(330, 790, 60, 60))
        screen.blit(difficulty_check, (330, 800))

    screen.blit(small_button_image, (5, 5))
    return_text = pixel_40.render('RETURN', True, WHITE)
    return_text_rect = return_text.get_rect(topleft=(24, 20))
    screen.blit(return_text, return_text_rect)

    screen.blit(small_button_image, (1300, 880))
    proceed_text = pixel_35.render('PROCEED', True, WHITE)
    screen.blit(proceed_text, (1320, 895))

    select_text = pixel_100.render('Choose your preferences', True, GRAY)
    screen.blit(select_text, (300, 80))
    screen.blit(pixel_100.render('Choose your preferences', True, WHITE), (305, 85))

    screen.blit(pixel_50.render('Dark Mode?', True, GRAY), (150, 350))
    screen.blit(pixel_50.render('Dark Mode?', True, WHITE), (153, 353))
    rec_text = steph_15.render('Dark Mode is heavily reccomended!', True, WHITE)
    screen.blit(rec_text, (160, 560))
    screen.blit(on_switch if game_state.is_dark_mode() else off_switch, (210, 430))

    screen.blit(pixel_50.render('Difficulty?', True, GRAY), (130, 650))
    screen.blit(pixel_50.render('Difficulty?', True, WHITE), (133, 653))

    screen.blit(difficulty_scale, (40, 720))

    screen.blit(pixel_50.render('Character?', True, GRAY), (640, 350))
    screen.blit(pixel_50.render('Character?', True, WHITE), (643, 353))
    screen.blit(example_man, (653, 400))
    screen.blit(example_girl, (653, 680))

    screen.blit(pixel_50.render('Map?', True, GRAY), (1140, 350))
    screen.blit(pixel_50.render('Map?', True, WHITE), (1143, 353))

    screen.blit(small_button_image, (1110, 480))
    diff_text1 = pixel_35.render(' EASY', True, GREEN)
    screen.blit(diff_text1, (1150, 495))

    screen.blit(small_button_image, (1110, 630))
    diff_text2 = pixel_35.render('MEDIUM', True, YELLOW)
    screen.blit(diff_text2, (1140, 645))

    screen.blit(small_button_image, (1110, 780))
    diff_text3 = pixel_35.render(' HARD', True, RED)
    screen.blit(diff_text3, (1145, 795))


def display_win(screen, game_state, timer):
    """
    Displays the win screen with statistics.
    """
    screen.fill(L_GREEN)
    screen.blit(small_button_image, (5, 5))
    return_text = pixel_40.render('RETURN', True, WHITE)
    return_text_rect = return_text.get_rect(topleft=(24, 20))
    screen.blit(return_text, return_text_rect)

    you_text = dash_180.render('You', True, GRAY)
    escaped_text = dash_180.render('Escaped!', True, GRAY)

    you_text2 = dash_180.render('You', True, WHITE)
    escaped_text2 = dash_180.render('Escaped!', True, WHITE)

    screen.blit(you_text, (window_size[0] / 2 - you_text.get_width() / 2, 150))
    screen.blit(escaped_text, (window_size[0] / 2 - escaped_text.get_width() / 2, 300))

    screen.blit(you_text2, ((window_size[0] / 2 - you_text.get_width() / 2) - 5, 145))
    screen.blit(escaped_text2, ((window_size[0] / 2 - escaped_text.get_width() / 2) - 5, 295))

    end_text = pixel_100.render('You beat the game!', True, GRAY)
    end_text1 = pixel_100.render('You beat the game!', True, WHITE)
    screen.blit(end_text, (window_size[0] / 2 - end_text.get_width() / 2, 500))
    screen.blit(end_text1, (window_size[0] / 2 - end_text.get_width() / 2 - 5, 495))

    stat_text = pixel_70.render('Statistics', True, GRAY)
    stat_text1 = pixel_70.render('Statistics', True, WHITE)
    screen.blit(stat_text, (window_size[0] / 2 - stat_text.get_width() / 2, 610))
    screen.blit(stat_text1, (window_size[0] / 2 - stat_text.get_width() / 2, 605))
    pygame.draw.rect(screen, BLACK, pygame.Rect(560, 660, 392, 13))
    pygame.draw.rect(screen, GRAY, pygame.Rect(560, 660, 390, 10))

    time_text = pixel_40.render("Time Played:", True, WHITE)
    screen.blit(time_text, (500, 700))
    result1_text = pixel_40.render(f"{round(timer.get_time(), 2)} seconds", True, WHITE)
    screen.blit(result1_text, (900, 700))

    health_text = pixel_40.render("Health Gained:", True, WHITE)
    screen.blit(health_text, (500, 750))
    result2_text = pixel_40.render(f"{round(game_state.statistics['Health Gained'], 2)} hearts", True, WHITE)
    screen.blit(result2_text, (900, 750))

    health_text1 = pixel_40.render("Health Lost:", True, WHITE)
    screen.blit(health_text1, (500, 800))
    result3_text = pixel_40.render(f"{round(game_state.statistics['Health Lost'], 2)} hearts", True, WHITE)
    screen.blit(result3_text, (900, 800))

    diff_text = pixel_40.render("Difficulty Level:", True, WHITE)
    screen.blit(diff_text, (500, 850))
    result4_text = pixel_40.render(f"{game_state.current_difficulty()}", True, WHITE)
    screen.blit(result4_text, (900, 850))

    map_text = pixel_40.render("Map Difficulty:", True, WHITE)
    screen.blit(map_text, (500, 900))
    result4_text = pixel_40.render(f"{get_map_difficulty(game_state.current_map())}", True, WHITE)
    screen.blit(result4_text, (900, 900))

    help_text = pixel_40.render("Help Tracker:", True, WHITE)
    screen.blit(help_text, (500, 950))
    result4_text = pixel_40.render(f"{game_state.help_tracker}", True, WHITE)
    screen.blit(result4_text, (900, 950))


def display_gameover(screen, game_state, timer):
    """
    Displays the gameover screen with statistics.
    """
    screen.fill((128, 0, 0))
    screen.blit(small_button_image, (5, 5))
    return_text = pixel_40.render('RETURN', True, WHITE)
    return_text_rect = return_text.get_rect(topleft=(24, 20))
    screen.blit(return_text, return_text_rect)

    game_text = dash_180.render('Game', True, GRAY)
    over_text = dash_180.render('Over!', True, GRAY)

    game_text2 = dash_180.render('Game', True, WHITE)
    over_text2 = dash_180.render('Over!', True, WHITE)

    screen.blit(game_text, (window_size[0] / 2 - game_text.get_width() / 2, 150))
    screen.blit(over_text, (window_size[0] / 2 - over_text.get_width() / 2, 300))

    screen.blit(game_text2, ((window_size[0] / 2 - game_text2.get_width() / 2) - 5, 145))
    screen.blit(over_text2, ((window_size[0] / 2 - over_text2.get_width() / 2) - 5, 295))

    end_text = pixel_100.render('You ran out of hearts!', True, GRAY)
    end_text1 = pixel_100.render('You ran out of hearts!', True, WHITE)
    screen.blit(end_text, (window_size[0] / 2 - end_text.get_width() / 2, 500))
    screen.blit(end_text1, (window_size[0] / 2 - end_text.get_width() / 2 - 5, 495))

    stat_text = pixel_70.render('Statistics', True, GRAY)
    stat_text1 = pixel_70.render('Statistics', True, WHITE)
    screen.blit(stat_text, (window_size[0] / 2 - stat_text.get_width() / 2, 610))
    screen.blit(stat_text1, (window_size[0] / 2 - stat_text.get_width() / 2, 605))
    pygame.draw.rect(screen, BLACK, pygame.Rect(560, 660, 392, 13))
    pygame.draw.rect(screen, GRAY, pygame.Rect(560, 660, 390, 10))

    time_text = pixel_40.render("Time Played:", True, WHITE)
    screen.blit(time_text, (500, 700))
    result1_text = pixel_40.render(f"{round(timer.get_time(), 2)} seconds", True, WHITE)
    screen.blit(result1_text, (900, 700))

    health_text = pixel_40.render("Health Gained:", True, WHITE)
    screen.blit(health_text, (500, 750))
    result2_text = pixel_40.render(f"{round(game_state.statistics['Health Gained'], 2)} hearts", True, WHITE)
    screen.blit(result2_text, (900, 750))

    health_text1 = pixel_40.render("Health Lost:", True, WHITE)
    screen.blit(health_text1, (500, 800))
    result3_text = pixel_40.render(f"{round(game_state.statistics['Health Lost'], 2)} hearts", True, WHITE)
    screen.blit(result3_text, (900, 800))

    diff_text = pixel_40.render("Difficulty Level:", True, WHITE)
    screen.blit(diff_text, (500, 850))
    result4_text = pixel_40.render(f"{game_state.current_difficulty()}", True, WHITE)
    screen.blit(result4_text, (900, 850))

    map_text = pixel_40.render("Map Difficulty:", True, WHITE)
    screen.blit(map_text, (500, 900))
    result4_text = pixel_40.render(f"{get_map_difficulty(game_state.current_map())}", True, WHITE)
    screen.blit(result4_text, (900, 900))

    help_text = pixel_40.render("Help Tracker:", True, WHITE)
    screen.blit(help_text, (500, 950))
    result4_text = pixel_40.render(f"{game_state.help_tracker}", True, WHITE)
    screen.blit(result4_text, (900, 950))


def display_start(screen):
    """
    Displays the start screen with game title and options.
    """
    screen.blit(background_start_image, (0, 0))

    forest_text = dash_180.render('Forest', True, ORANGE)
    of_text = dash_180.render('of', True, ORANGE)
    echoes_text = dash_180.render('Echoes', True, ORANGE)

    forest_text2 = dash_180.render('Forest', True, YELLOW)
    of_text2 = dash_180.render('of', True, YELLOW)
    echoes_text2 = dash_180.render('Echoes', True, YELLOW)

    screen.blit(forest_text, (window_size[0] / 2 - forest_text.get_width() / 2, 130))
    screen.blit(of_text, (window_size[0] / 2 - of_text.get_width() / 2, 295))
    screen.blit(echoes_text, (window_size[0] / 2 - echoes_text.get_width() / 2, 455))

    screen.blit(forest_text2, ((window_size[0] / 2 - forest_text.get_width() / 2) - 5, 125))
    screen.blit(of_text2, ((window_size[0] / 2 - of_text.get_width() / 2) - 5, 290))
    screen.blit(echoes_text2, ((window_size[0] / 2 - echoes_text.get_width() / 2) - 5, 450))

    screen.blit(start_button_image, (start_button_rect.x, start_button_rect.y))
    screen.blit(menu_button_image, (menu_button_rect.x, menu_button_rect.y))
    screen.blit(exit_button_image, (exit_button_rect.x, exit_button_rect.y))

    start_text = pixel_70.render('START', True, WHITE)
    menu_text = pixel_70.render('MENU', True, WHITE)
    exit_text = pixel_70.render('EXIT', True, WHITE)

    start_text_x = start_button_rect.x + start_button_image.get_width() / 2 - start_text.get_width() / 2
    start_text_y = start_button_rect.y + start_button_image.get_height() / 2 - start_text.get_height() / 2
    menu_text_x = menu_button_rect.x + menu_button_image.get_width() / 2 - menu_text.get_width() / 2
    menu_text_y = menu_button_rect.y + menu_button_image.get_height() / 2 - menu_text.get_height() / 2
    exit_text_x = exit_button_rect.x + exit_button_image.get_width() / 2 - exit_text.get_width() / 2
    exit_text_y = exit_button_rect.y + exit_button_image.get_height() / 2 - exit_text.get_height() / 2

    screen.blit(start_text, (start_text_x, start_text_y))
    screen.blit(menu_text, (menu_text_x, menu_text_y))
    screen.blit(exit_text, (exit_text_x, exit_text_y))


def display_use_text(certain_button, current_time, msg_start, game_button_rect, indicator, screen, which_msg):
    """
    Displays the use item screen with options.
    """
    screen.fill(D_BLUE)
    if certain_button and current_time - msg_start <= 4000:
        game_button_rect.x = [445, 575, 705, 840, 975][indicator - 1]
        ex_x = game_button_rect.x
        screen.blit(game_button1, game_button_rect.topleft)
        yes_text = pixel_24.render('Yes', True, BLACK)
        screen.blit(yes_text, (ex_x + 25, 455))
        blah1 = steph_15.render('Are you sure you want to use this item?', True, WHITE)
        screen.blit(blah1, (ex_x - 50, 400))

    if which_msg == 'fruit' and current_time - msg_start <= 5000:
        display_fruit_message(screen, window_size)
    elif which_msg == 'campfire' and current_time - msg_start <= 5000:
        display_campfire_message(screen, window_size)
    elif which_msg == 'error' and current_time - msg_start <= 5000:
        display_error_message(screen, window_size)
    elif which_msg == 'error1' and current_time - msg_start <= 5000:
        display_error_message(screen, window_size)

    select_text = pixel_100.render('Select Which Item', True, GRAY)
    select_text1 = pixel_100.render('Select Which Item', True, WHITE)
    screen.blit(select_text, (400, 80))
    screen.blit(select_text1, (405, 85))

    use_text = pixel_100.render('You want to Use', True, GRAY)
    use_text1 = pixel_100.render('You want to Use', True, WHITE)
    screen.blit(use_text, (438, 150))
    screen.blit(use_text1, (443, 155))

    screen.blit(small_button_image, (5, 5))
    return_text = pixel_40.render('RETURN', True, WHITE)
    return_text_rect = return_text.get_rect(topleft=(24, 20))
    screen.blit(return_text, return_text_rect)


def display_mask(player, game_state, campfire_light, screen):
    """
    Displays a mask effect for dark mode around the player.
    """
    mask = pygame.Surface((1130, 715))
    player_position = player.get_player_grid_location()
    circle_center = ((player_position[0] * 50) + 40, (player_position[1] * 50) + 35)
    mask.fill((0, 0, 0))
    if game_state.current_difficulty() == 'easy':
        pygame.draw.circle(mask, (255, 255, 255, 0), circle_center, 80)
    elif game_state.current_difficulty() == 'medium':
        pygame.draw.circle(mask, (255, 255, 255, 0), circle_center, 60)
    elif game_state.current_difficulty() == 'hard':
        pygame.draw.circle(mask, (255, 255, 255, 0), circle_center, 40)

    if campfire_light:
        x = game_state.campfire_location()[0]
        y = game_state.campfire_location()[1]
        x1 = (x * 50) + 40
        y1 = (y * 50) + 30
        pygame.draw.circle(mask, (255, 255, 255, 0), (x1, y1), 100)

    mask.set_colorkey((255, 255, 255))
    screen.blit(mask, (185, 85))


def display_messages(screen, msg_display, current_time, msg_start):
    """
    Displays various game messages based on player actions.
    """
    if msg_display == 'pick up' and current_time - msg_start <= 2500:
        blah = steph_15.render('Item has been added to inventory!', True, WHITE)
        screen.blit(blah, (700, 830))
    if msg_display == 'pick up error' and current_time - msg_start <= 2500:
        blah = steph_15.render('There are no items to pick up here!', True, WHITE)
        screen.blit(blah, (700, 830))
    if msg_display == 'interact error' and current_time - msg_start <= 2500:
        blah = steph_15.render('There is nothing to interact with!', True, WHITE)
        screen.blit(blah, (700, 830))
    if msg_display == 'key error' and current_time - msg_start <= 2500:
        blah = steph_15.render('The chest is locked', True, WHITE)
        screen.blit(blah, (700, 830))
    if msg_display == 'sign1' and current_time - msg_start <= 5000:
        screen.blit(wooden_sign1, (300, 50))
    if msg_display == 'sign2' and current_time - msg_start <= 5000:
        screen.blit(wooden_sign2, (300, 50))
    if msg_display == 'sign3' and current_time - msg_start <= 5000:
        screen.blit(wooden_sign3, (300, 50))
    if msg_display == 'chest opened' and current_time - msg_start <= 10000:
        blah = steph_15.render('Chest is Opened!!', True, WHITE)
        screen.blit(blah, (720, 830))
        blah1 = steph_15.render('You have found the Hidden Treasure!!', True, WHITE)
        screen.blit(blah1, (665, 850))
        blah2 = steph_15.render('With the treasure is a Flare Gun', True, WHITE)
        screen.blit(blah2, (685, 870))
        blah3 = steph_15.render('Quickly Fire it at the Correct Location!', True, WHITE)
        screen.blit(blah3, (675, 890))
    if msg_display == 'return':
        blah = steph_15.render('Are you sure', True, WHITE)
        screen.blit(blah, (40, 150))
        blah1 = steph_15.render('you want to leave?', True, WHITE)
        screen.blit(blah1, (25, 165))
        screen.blit(small_button_image, (5, 200))
        yes_text = pixel_40.render('YES', True, WHITE)
        screen.blit(yes_text, (50, 215))
        screen.blit(small_button_image, (5, 280))
        no_text = pixel_40.render('NO', True, WHITE)
        screen.blit(no_text, (60, 295))


def display_buttons(screen, game_state):
    """
    Displays in-game buttons for interaction.
    """
    screen.blit(small_button_image, (5, 5))
    return_text = pixel_40.render('RETURN', True, WHITE)
    screen.blit(return_text, (24, 20))

    screen.blit(game_button, (1350, 500))
    interact_text = pixel_24.render('INTERACT', True, BLACK)
    screen.blit(interact_text, (1370, 518))

    screen.blit(game_button, (1350, 600))
    pick_up_text = pixel_24.render('PICK UP', True, BLACK)
    screen.blit(pick_up_text, (1380, 618))

    screen.blit(game_button, (1350, 700))
    use_item_text = pixel_24.render('USE ITEM', True, BLACK)
    screen.blit(use_item_text, (1372, 718))

    screen.blit(game_button, (1350, 800))
    inventory_text = pixel_24.render('INVENTORY', True, BLACK)
    screen.blit(inventory_text, (1365, 818))

    if game_state.is_dark_mode():
        screen.blit(game_button, (1350, 200))
        inventory_text = pixel_24.render('HELP', True, BLACK)
        screen.blit(inventory_text, (1390, 218))
        text1 = steph_15.render('This temporarily pauses', True, WHITE)
        screen.blit(text1, (1350, 260))
        text2 = steph_15.render('dark mode', True, WHITE)
        screen.blit(text2, (1380, 280))


def display_time(timer, screen):
    """
    Displays the elapsed time on the screen.
    """
    elapsed_seconds = timer.get_time()
    timer_text = pixel_30.render(f"Elapsed Time: {elapsed_seconds:.2f} seconds", True, WHITE)
    screen.blit(timer_text, (200, 890))


def display_hearts(player, screen):
    """
    Displays the player's health as heart icons.
    """
    if player.health <= 2.0:
        blah = steph_15.render('Your almost out of health!', True, RED)
        screen.blit(blah, (200, 920))
    for i in range(7):
        x = 200 + i * 50
        screen.blit(empty_heart, (x, 830))
    if player.health >= 7:
        for i in range(7):
            x = 200 + i * 50
            screen.blit(full_heart, (x, 830))
    elif player.health >= 6.5:
        for i in range(6):
            x = 200 + i * 50
            screen.blit(full_heart, (x, 830))
        screen.blit(half_heart, (200 + 6 * 50, 830))
    elif player.health >= 6:
        for i in range(6):
            x = 200 + i * 50
            screen.blit(full_heart, (x, 830))
    elif player.health >= 5.5:
        for i in range(5):
            x = 200 + i * 50
            screen.blit(full_heart, (x, 830))
        screen.blit(half_heart, (200 + 5 * 50, 830))
    elif player.health >= 5:
        for i in range(5):
            x = 200 + i * 50
            screen.blit(full_heart, (x, 830))
    elif player.health >= 4.5:
        for i in range(4):
            x = 200 + i * 50
            screen.blit(full_heart, (x, 830))
        screen.blit(half_heart, (200 + 4 * 50, 830))
    elif player.health >= 4:
        for i in range(4):
            x = 200 + i * 50
            screen.blit(full_heart, (x, 830))
    elif player.health >= 3.5:
        for i in range(3):
            x = 200 + i * 50
            screen.blit(full_heart, (x, 830))
        screen.blit(half_heart, (200 + 3 * 50, 830))
    elif player.health >= 3:
        for i in range(3):
            x = 200 + i * 50
            screen.blit(full_heart, (x, 830))
    elif player.health >= 2.5:
        for i in range(2):
            x = 200 + i * 50
            screen.blit(full_heart, (x, 830))
        screen.blit(half_heart, (200 + 2 * 50, 830))
    elif player.health >= 2:
        for i in range(2):
            x = 200 + i * 50
            screen.blit(full_heart, (x, 830))
    elif player.health >= 1.5:
        x = 200
        screen.blit(full_heart, (x, 830))
        screen.blit(half_heart, (x + 50, 830))
    elif player.health >= 1:
        x = 200
        screen.blit(full_heart, (x, 830))
    elif player.health >= 0.5:
        x = 200
        screen.blit(half_heart, (x, 830))


def interact_checker(player, game_state) -> str:
    """
    Checks the player's current grid code for interactions.
    """
    if player.get_player_grid_code(game_state) not in {4, 6, 7, 8}:
        return 'Error'
    elif player.get_player_grid_code(game_state) == 4:
        return 'Chest'
    elif player.get_player_grid_code(game_state) == 6:
        return 'sign1'
    elif player.get_player_grid_code(game_state) == 7:
        return 'sign2'
    elif player.get_player_grid_code(game_state) == 8:
        return 'sign3'


def display_fruit_message(screen, window_size):
    """
    Displays a message when the player eats a fruit.
    """
    blah = steph_24.render('You ate the fruit!!', True, WHITE)
    screen.blit(blah, (window_size[0] // 2 - 100, 290))
    blah0 = steph_24.render('You have gained two additional hearts!!', True, WHITE)
    screen.blit(blah0, (window_size[0] // 2 - 200, 320))
    blah1 = steph_24.render('The item has been removed from your inventory', True, WHITE)
    screen.blit(blah1, (window_size[0] // 2 - 220, 350))


def display_error_message(screen, window_size):
    """
    Displays an error message for invalid actions.
    """
    blah = steph_24.render('You are not in a valid location', True, WHITE)
    screen.blit(blah, (window_size[0] // 2 - 100, 290))


def display_campfire_message(screen, window_size):
    """
    Displays a message when the player places a campfire.
    """
    blah = steph_24.render('You have placed a campfire down!', True, WHITE)
    screen.blit(blah, (window_size[0] // 2 - 150, 290))
    blah0 = steph_24.render('Heal yourself by staying on the campfire', True, WHITE)
    screen.blit(blah0, (window_size[0] // 2 - 195, 320))
    blah1 = steph_24.render('The item has been removed from your inventory', True, WHITE)
    screen.blit(blah1, (window_size[0] // 2 - 220, 350))


def display_items(screen, start_x, window_size, inventory):
    """
    Displays items from the player's inventory on the screen.
    """
    resize_pear = pygame.transform.scale(pear_fruit_image, (55, 55))
    resize_apple = pygame.transform.scale(apple_fruit_image, (55, 55))
    resize_orange = pygame.transform.scale(orange_fruit_image, (55, 55))
    resize_campfire = pygame.transform.scale(campfire_image, (70, 70))
    resize_flaregun = pygame.transform.scale(flaregun_image, (70, 70))
    y = window_size[1] // 2
    for col in range(5):
        x = start_x + col * 135
        screen.blit(item_frame, (x, y))
        if 'Pear' in inventory:
            screen.blit(resize_pear, (460, window_size[1] // 2 + 50))
        if 'Apple' in inventory:
            screen.blit(resize_apple, (590, window_size[1] // 2 + 50))
        if 'Orange' in inventory:
            screen.blit(resize_orange, (725, window_size[1] // 2 + 50))
        if 'Campfire' in inventory:
            screen.blit(resize_campfire, (852, window_size[1] // 2 + 47))
        if 'FlareGun' in inventory:
            screen.blit(resize_flaregun, (990, window_size[1] // 2 + 47))


def get_item_image(item_name) -> pygame.Surface:
    """
    Returns the image associated with an item name.
    """
    item_name = item_name.strip().lower()
    if item_name == "apple":
        return apple_fruit_image
    elif item_name == "orange":
        return orange_fruit_image
    elif item_name == "pear":
        return pear_fruit_image
    elif item_name == "matchbox":
        return matchbox_image
    elif item_name == "logs":
        return logs_image
    elif item_name == "rock":
        return rock_image
    elif item_name == "blue key":
        return blue_key_image
    elif item_name == "gold key":
        return gold_key_image
    elif item_name == "copper key":
        return copper_key_image
    elif item_name == "wood key":
        return wood_key_image
    elif item_name == "campfire":
        return campfire_image
    elif item_name == "flaregun":
        return flaregun_image
    elif item_name == "jewelbag":
        return jewel_bag


def campfire_valid_loc(value) -> bool:
    """
    Checks if a location is valid for placing a campfire.
    """
    if value not in {2, 3, 4, 5, 6, 7, 8, 11, 10, 11, 12, 13, 14, 15, 16}:
        return True
    else:
        return False


def display_map(player, screen, game_state):
    """
    Displays the game map and items on the screen.
    """

    pygame.draw.rect(screen, BLACK, (185, 85, 1130, 730), 15)
    grid_x, grid_y = 20, 12
    tile_width, tile_height = 50, 50

    grid_start_x = 250
    grid_start_y = 150

    for row in range(-1, grid_y + 1):
        for col in range(-1, grid_x + 1):
            tile_x = grid_start_x + col * tile_width
            tile_y = grid_start_y + row * tile_height
            screen.blit(grass_tile_image, (tile_x, tile_y))

    map_name = game_state.current_map()
    map_file_path = f'{map_name}'
    with open(map_file_path, 'r') as map_file:
        game_map = load_map(map_file)

        for y, row in enumerate(game_map):
            for x, tile in enumerate(row):
                if tile == 0:
                    screen.blit(individual_tree_image, ((x * tile_width) + 202, (y * tile_height) + 102))
                elif tile == 2:
                    screen.blit(water_tile_image, ((x * tile_width) + 200, (y * tile_height) + 100))
                elif tile == 4:
                    screen.blit(chest_image, ((x * tile_width) + 205, (y * tile_height) + 105))
                elif tile == 5:
                    screen.blit(bridge_tile_image, ((x * tile_width) + 200, (y * tile_height) + 100))
                elif tile in {6, 7, 8}:
                    screen.blit(sign_tile_image, ((x * tile_width) + 200, (y * tile_height) + 100))
                elif tile == 10:
                    screen.blit(flower_grass_tile_image, ((x * tile_width) + 200, (y * tile_height) + 100))
                elif tile == 11:
                    screen.blit(red_bushes_image, ((x * tile_width) + 205, (y * tile_height) + 103))
                elif tile == 12:
                    screen.blit(white_bushes_image, ((x * tile_width) + 205, (y * tile_height) + 103))
                elif tile == 13:
                    screen.blit(purple_bushes_image, ((x * tile_width) + 205, (y * tile_height) + 103))
                elif tile == 14:
                    screen.blit(blue_bushes_image, ((x * tile_width) + 205, (y * tile_height) + 103))
                elif tile == 15:
                    screen.blit(tulips_image, ((x * tile_width) + 205, (y * tile_height) + 103))
                elif tile == 16:
                    screen.blit(ground_vern_image, ((x * tile_width) + 205, (y * tile_height) + 103))
                elif tile == 20:
                    screen.blit(pathway_hori_image, ((x * tile_width) + 195, (y * tile_height) + 100))
                elif tile == 21:
                    screen.blit(pathway_vert_image, ((x * tile_width) + 200, (y * tile_height) + 95))
                elif tile == 22:
                    screen.blit(l_curve_image, ((x * tile_width) + 202, (y * tile_height) + 100))
                elif tile == 23:
                    screen.blit(inverse_l_image, ((x * tile_width) + 200, (y * tile_height) + 100))
                elif tile == 24:
                    screen.blit(up_left_l_image, ((x * tile_width) + 200, (y * tile_height) + 100))
                elif tile == 25:
                    screen.blit(up_right_l_image, ((x * tile_width) + 200, (y * tile_height) + 100))
                elif tile == 26:
                    screen.blit(t_path_image, ((x * tile_width) + 200, (y * tile_height) + 100))
                elif tile == 27:
                    screen.blit(all_path_image, ((x * tile_width) + 200, (y * tile_height) + 100))
                elif tile == 28:
                    screen.blit(upside_down_t_image, ((x * tile_width) + 200, (y * tile_height) + 100))
                elif tile == 29:
                    screen.blit(right_t_image, ((x * tile_width) + 200, (y * tile_height) + 100))

        screen.blit(hill_tile_image, (1100, 110))
        for location, item in game_state.items.items():
            item_image = get_item_image(item.name)
            x, y = location
            screen_x = 210 + (x * 50)
            screen_y = 110 + (y * 50)
            screen.blit(item_image, (screen_x, screen_y))

        screen.blit(player.current_image, (player.player_x, player.player_y))

"""
This module contains the main game loop and supporting functions for a Pygame-based game.

The module performs the following tasks:
- Initializes Pygame and sets up the game display, mixer, and timer.
- Defines the main game screen function that handles the core game logic, including player inputs,
  game state updates, rendering, and audio management.
- Provides additional screens for inventory management, item usage, game win, and gameover states.
- Implements the main menu and selection screens where players can configure game settings and start the game.
- Includes helper functions for stopping the campfire sound and managing game state transitions.

Functions:
- game_screen: The main game screen where the game logic and player interactions are handled.
- inventory_screen: The inventory screen where players can view and craft items.
- use_screen: The screen where players can use specific items from their inventory.
- win_screen: The screen displayed when the player wins the game.
- gameover_screen: The screen displayed when the player loses the game.
- menu_screen: The main menu screen of the game.
- selection_screen: The screen where users choose game preferences.
- start_screen: The starting screen of the game.
- main: The main function that initializes the game state and starts the game.
"""

import sys
from set import *

timer = Timer()


def game_screen(game_state, player, current_game_map):
    """
    This screen is where the game itself is being played.

    The function performs the following tasks:
    - Initializes game states and variables.
    - Handles player inputs (mouse and keyboard events).
    - Updates player movement and interactions.
    - Manages audio effects and background music.
    - Renders game elements like the map, player, and UI components.
    - Checks for game state changes like health updates, item pickups, and game end conditions.
    """

    if not timer.running:
        timer.start()

    last_update_time = pygame.time.get_ticks()

    campfire_active = False
    campfire_start = None
    campfire_i = 0
    is_campfire_sound = False

    end_buffer = None

    confirm_flag = False

    msg_display = None
    msg_start = 0
    last_health_update_time = 0

    dying_sound_played = False
    footstep_sound = pygame.mixer.Sound(footsteps_sound)
    footstep_sound.set_volume(0.25)
    pressed_keys = set()

    campfire_sound1 = pygame.mixer.Sound(campfire_sound)
    campfire_sound1.set_volume(0.1)

    health_decrement_interval = get_health_decrement(game_state)

    dark_mode_temp_off = False
    dark_mode_off_start = None

    play_music(game_music, 0.4)
    running_game = True
    last_breath_time = pygame.time.get_ticks()
    while running_game:
        current_time = pygame.time.get_ticks()
        if (current_time - last_breath_time) >= 1000 and not confirm_flag and running_game:
            play_sound_effect(breathe_sound, 1)
            last_breath_time = current_time
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                timer.stop()
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if small_button_rect.collidepoint(event.pos):
                    play_sound_effect(select_sound, 0.2)
                    msg_display = 'return'
                    confirm_flag = True
                if confirm_flag:
                    timer.stop()
                    pygame.mixer.music.pause()
                    if yes_button_rect.collidepoint(event.pos):
                        play_sound_effect(select_sound, 0.2)
                        timer.reset()
                        timer.stop()
                        is_campfire_sound = pause_campfire(is_campfire_sound, campfire_sound1)
                        running_game = False
                        game_state.reset()
                        start_screen(game_state)
                    elif no_button_rect.collidepoint(event.pos):
                        play_sound_effect(select_sound, 0.2)
                        timer.start()
                        pygame.mixer.music.unpause()
                        msg_display = 'none'
                        confirm_flag = False

                elif use_item_button_rect.collidepoint(event.pos):
                    timer.stop()
                    play_sound_effect(select_sound, 0.2)
                    pygame.mixer.music.pause()
                    is_campfire_sound = pause_campfire(is_campfire_sound, campfire_sound1)
                    if footstep_sound.get_num_channels():
                        footstep_sound.stop()
                    use_screen(game_state, player, current_game_map)
                    running_game = False
                elif inventory_button_rect.collidepoint(event.pos):
                    timer.stop()
                    play_sound_effect(select_sound, 0.2)
                    pygame.mixer.music.pause()
                    is_campfire_sound = pause_campfire(is_campfire_sound, campfire_sound1)
                    if footstep_sound.get_num_channels():
                        footstep_sound.stop()
                    inventory_screen(game_state, player, current_game_map)
                    running_game = False

                elif interact_button_rect.collidepoint(event.pos):
                    if interact_checker(player, game_state) == 'Error':
                        play_sound_effect(error_sound, 0.3)
                        msg_display = 'interact error'
                        msg_start = current_time
                    elif interact_checker(player, game_state) in {'sign1', 'sign2', 'sign3'}:
                        play_sound_effect(sign_sound, 0.3)
                        msg_display = interact_checker(player, game_state)
                        msg_start = current_time
                    elif interact_checker(player, game_state) == 'Chest':
                        if all(key in player.inventory for key in {'Wood Key', 'Gold Key', 'Blue Key', 'Copper Key'}):
                            open_chest(player)
                            msg_display = 'chest opened'
                            msg_start = current_time
                        else:
                            play_sound_effect(error_sound, 0.3)
                            msg_display = 'key error'
                            msg_start = current_time

                elif pick_up_button_rect.collidepoint(event.pos):
                    player_grid_pos = player.get_player_grid_location()
                    player_grid_tuple = (player_grid_pos[0], player_grid_pos[1])
                    items_on_ground = game_state.items
                    if player_grid_tuple in items_on_ground:
                        play_sound_effect(pickup_sound, 3)
                        item = items_on_ground.pop(player_grid_tuple)
                        game_state.remove_item(player_grid_tuple)
                        player.item_to_inventory(item)
                        msg_display = 'pick up'
                        msg_start = current_time
                    else:
                        play_sound_effect(error_sound, 0.3)
                        msg_display = 'pick up error'
                        msg_start = current_time

                elif help_button_rect.collidepoint(event.pos) and game_state.is_dark_mode():
                    play_sound_effect(select_sound, 0.2)
                    dark_mode_temp_off = True
                    dark_mode_off_start = pygame.time.get_ticks()
                    game_state.toggle_dark_mode()
                    game_state.help_tracker += 1

            elif event.type == pygame.KEYDOWN:
                if event.key in [pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN,
                                 pygame.K_a, pygame.K_w, pygame.K_s, pygame.K_d]:
                    pressed_keys.add(event.key)
                    if (not confirm_flag and not footstep_sound.get_num_channels() and not game_state.check_end()
                            and not player.health < 0.5):
                        footstep_sound.play(-1)

            elif event.type == pygame.KEYUP:
                if event.key in [pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN,
                                 pygame.K_a, pygame.K_w, pygame.K_s, pygame.K_d]:
                    pressed_keys.discard(event.key)
                    if not pressed_keys:
                        footstep_sound.stop()

        screen.fill(D_BLUE)
        if not confirm_flag and not game_state.check_end() and not player.health < 0.5:
            player.handle_movement(current_game_map)

        display_time(timer, screen)
        display_hearts(player, screen)
        display_buttons(screen, game_state)
        display_map(player, screen, game_state)

        if game_state.is_dark_mode() and not dark_mode_temp_off:
            display_mask(player, game_state, campfire_active, screen)
        display_messages(screen, msg_display, current_time, msg_start)

        if dark_mode_temp_off:
            current_time = pygame.time.get_ticks()
            if (current_time - dark_mode_off_start) >= 1000:
                dark_mode_temp_off = False
                game_state.toggle_dark_mode()

        if game_state.is_campfire() and campfire_active is False:
            campfire_active = True
            campfire_start = current_time

        if campfire_active and not is_campfire_sound:
            campfire_sound1.play(-1)
            is_campfire_sound = True

        if not campfire_active and is_campfire_sound:
            campfire_sound1.stop()
            is_campfire_sound = False

        if campfire_active == 1:
            x = game_state.campfire_location()[0]
            y = game_state.campfire_location()[1]
            x1 = (x * 50) + 205
            y1 = (y * 50) + 100
            if current_time - campfire_start < 15000:
                if (current_time - last_update_time) > 200:
                    campfire_i = (campfire_i + 1) % len(campfire_images)
                    last_update_time = current_time
                screen.blit(campfire_images[campfire_i], (x1, y1))
                if player.get_player_grid_location() == [x, y]:
                    if player.health <= 7:
                        player.health += 0.01
                        game_state.health_gained_adder(0.01)
                campfire_active = True
            else:
                screen.blit(campfire_base, (x1, y1))
                game_state.toggle_campfire()
                campfire_active = False

        if game_state.check_end():
            timer.stop()
            is_campfire_sound = pause_campfire(is_campfire_sound, campfire_sound1)
            if not end_buffer:
                end_buffer = current_time

            if current_time - end_buffer <= 5000:
                display_text(screen, 'win')
            else:
                running_game = False
                win_screen(game_state)

        if player.health < 0.5 and not dying_sound_played:
            play_sound_effect(dying_sound, 0.6)
            dying_sound_played = True
        if (current_time - last_health_update_time) > health_decrement_interval and not game_state.check_end():
            if not confirm_flag:
                player.health -= 0.5
                game_state.health_lost_adder()
                last_health_update_time = current_time
        if player.health < 0.5:
            player.kill_player()
            timer.stop()
            is_campfire_sound = pause_campfire(is_campfire_sound, campfire_sound1)
            if not end_buffer:
                end_buffer = current_time
            if current_time - end_buffer <= 4000:
                display_text(screen, 'lose')
            else:
                running_game = False
                gameover_screen(game_state, timer)

        pygame.display.flip()


def inventory_screen(game_state, player, current_game_map):
    """
    The inventory screen where players can view and craft items .

    The function performs the following tasks:
    - Handles mouse click events for crafting and using items.
    - Calls the inventory display.
    - Handles crafting
    """
    running_inventory = True
    display_message = False

    play_music(inventory_use_music, 0.3)
    while running_inventory:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if small_button_rect.collidepoint(event.pos):
                    play_sound_effect(select_sound, 0.2)
                    pygame.mixer.music.stop()
                    running_inventory = False
                    game_screen(game_state, player, current_game_map)
                if craft_button_rect.collidepoint(event.pos):
                    if all(key in player.inventory for key in campfire_materials):
                        play_sound_effect(select_sound, 0.2)
                        player.remove_item_from_inventory('Matchbox')
                        player.remove_item_from_inventory('Logs')
                        player.remove_item_from_inventory('Rock')
                        play_sound_effect(craft_sound, 0.4)
                        player.inventory['Campfire'] = 'Heating Mechanism: Allows you to regain health'
                        display_message = True
                    else:
                        play_sound_effect(error_sound, 0.3)

        display_inventory(screen, display_message, player)

        pygame.display.flip()


def use_screen(game_state, player, current_game_map):
    """
    The use screen where players can use specific items from their inventory.
    This function handles the display and interaction for using items like fruits,
    campfires, and flare guns. It allows players to use items and returns to the main
    game screen after using an item.

    The function performs the following tasks:
    - Handles mouse click events for selecting and using items.
    - Updates player health and inventory based on used items.
    - calls the use screen display
    """

    running_use = True
    certain_button = False
    indicator = 0
    which_msg = None
    msg_start = 0

    play_music(inventory_use_music, 0.5)
    while running_use:
        current_time = pygame.time.get_ticks()
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if small_button_rect.collidepoint(event.pos):
                    play_sound_effect(select_sound, 0.2)
                    pygame.mixer.music.stop()
                    game_screen(game_state, player, current_game_map)
                    running_use = False
                if pear_rect.collidepoint(event.pos) and 'Pear' in player.inventory:
                    play_sound_effect(select_sound, 0.2)
                    indicator = 1
                    msg_start = current_time
                    certain_button = True
                if apple_rect.collidepoint(event.pos) and 'Apple' in player.inventory:
                    play_sound_effect(select_sound, 0.2)
                    indicator = 2
                    msg_start = current_time
                    certain_button = True
                if orange_rect.collidepoint(event.pos) and 'Orange' in player.inventory:
                    play_sound_effect(select_sound, 0.2)
                    indicator = 3
                    msg_start = current_time
                    certain_button = True
                if campfire_rect.collidepoint(event.pos) and 'Campfire' in player.inventory:
                    play_sound_effect(select_sound, 0.2)
                    indicator = 4
                    msg_start = current_time
                    certain_button = True
                if flaregun_rect.collidepoint(event.pos) and 'FlareGun' in player.inventory:
                    play_sound_effect(select_sound, 0.2)
                    indicator = 5
                    msg_start = current_time
                    certain_button = True
                if certain_button and game_button_rect.collidepoint(event.pos):
                    certain_button = False
                    if indicator in {1, 2, 3}:
                        play_sound_effect(select_sound, 0.2)
                        play_sound_effect(eat_sound, 0.5)
                        player.remove_item_from_inventory(
                            'Pear' if indicator == 1 else 'Apple' if indicator == 2 else 'Orange')
                        if player.health >= 5:
                            game_state.health_gained_adder(7 - player.health)
                            player.health = 7
                        else:
                            game_state.health_gained_adder(2)
                            player.health += 2
                        which_msg = 'fruit'
                        msg_start = current_time
                    elif indicator == 4:
                        if campfire_valid_loc(player.get_player_grid_code(game_state)):
                            play_sound_effect(select_sound, 0.2)
                            play_sound_effect(place_sound, 0.5)
                            player.remove_item_from_inventory('Campfire')
                            which_msg = 'campfire'
                            msg_start = current_time
                            game_state.set_campfire_location(player)
                            game_state.toggle_campfire()
                        else:
                            play_sound_effect(error_sound, 0.3)
                            which_msg = 'error'
                            msg_start = current_time
                    elif indicator == 5:
                        if player.get_player_grid_code(game_state) == 77:
                            play_sound_effect(select_sound, 0.2)
                            play_sound_effect(flaregun_sound, 0.3)
                            player.remove_item_from_inventory('FlareGun')
                            game_state.end_game()
                            if game_state.is_dark_mode():
                                game_state.toggle_dark_mode()
                            game_screen(game_state, player, current_game_map)
                        else:
                            play_sound_effect(error_sound, 0.3)
                            which_msg = 'error1'
                            msg_start = current_time

        display_use_text(certain_button, current_time, msg_start, game_button_rect, indicator, screen,
                         which_msg)
        display_items(screen, 400, window_size, player.inventory)

        pygame.display.flip()


def win_screen(game_state):
    """
    This function handles the win screen where players are congratulated for winning.
    It allows players to return to the main menu and reset the game state.

    The function performs the following tasks:
    - Renders the win screen with congratulatory messages.
    """
    running_win = True
    play_music(win_music, 0.1)
    while running_win:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if small_button_rect.collidepoint(event.pos):
                    play_sound_effect(select_sound, 0.2)
                    running_win = False
                    timer.reset()
                    game_state.reset()
                    start_screen(game_state)

        display_win(screen, game_state, timer)

        pygame.display.flip()


def gameover_screen(game_state, timer):
    """
    The screen displayed when the player loses the game.

    This function handles the game over screen where players are informed that they have lost.
    It allows players to return to the main menu and reset the game state.

    The function performs the following tasks:
    - Renders the game over screen with failure messages.
    """
    running_end = True
    play_music(lose_music, 0.2)
    while running_end:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if small_button_rect.collidepoint(event.pos):
                    play_sound_effect(select_sound, 0.2)
                    running_end = False
                    game_state.reset()
                    timer.reset()
                    start_screen(game_state)

        display_gameover(screen, game_state, timer)

        pygame.display.flip()


def menu_screen():
    """
    The main menu screen of the game.

    This function handles the main menu where players can see the introduction story, key binds and spoilers

    The function performs the following tasks:
    - Renders the main menu screen with options.
    """
    running_menu = True
    reveal = False
    while running_menu:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if small_button_rect.collidepoint(event.pos):
                    play_sound_effect(select_sound, 0.2)
                    running_menu = False
                if reveal_rect.collidepoint(event.pos):
                    play_sound_effect(select_sound, 0.2)
                    reveal = True

        display_menu(screen, reveal)

        pygame.display.flip()


def intro_screen(game_state, player, current_game_map):
    """
    The introduction screen which explains the game story to the character.
    """
    running_intro = True
    start_time = pygame.time.get_ticks()
    play_music(inventory_use_music, 0.2)
    while running_intro:
        current_time = pygame.time.get_ticks()
        display_intro(screen, start_time)
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if small_button_rect.collidepoint(event.pos):
                    play_sound_effect(select_sound, 0.2)
                    running_intro = False
                    game_state.reset()
                    start_screen(game_state)
        if (current_time - start_time) > 100:
            running_intro = False

        pygame.display.update()
    pygame.mixer.music.stop()
    game_screen(game_state, player, current_game_map)


def selection_screen(game_state):
    """
    The selection screen where users choose game preferences.

    This function handles the selection screen for setting up game preferences,
    including selecting gender, difficulty, dark mode, and map.

    The function performs the following tasks:
    - Renders the selection screen with options and messages.
    """
    running_selection = True

    which_msg = None
    msg_start = 0
    while running_selection:
        current_time = pygame.time.get_ticks()
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if small_button_rect.collidepoint(event.pos):
                    play_sound_effect(select_sound, 0.2)
                    running_selection = False
                    start_screen(game_state)
                elif proceed_rect.collidepoint(event.pos):
                    if game_state.current_gender() != 'None' and game_state.map != 'None':
                        play_sound_effect(select_sound, 0.2)
                        pygame.mixer.music.stop()
                        current_game_map = load_game_map(game_state)
                        player = initialize_player(game_state)
                        running_selection = False
                        intro_screen(game_state, player, current_game_map)
                    else:
                        play_sound_effect(error_sound, 0.3)
                        which_msg = 'error'
                        msg_start = current_time
                elif dark_mode_rect.collidepoint(event.pos):
                    play_sound_effect(select_sound, 0.2)
                    game_state.toggle_dark_mode()
                elif male_rect.collidepoint(event.pos):
                    play_sound_effect(select_sound, 0.2)
                    game_state.set_gender('male')
                elif girl_rect.collidepoint(event.pos):
                    play_sound_effect(select_sound, 0.2)
                    game_state.set_gender('girl')
                elif easy_rect.collidepoint(event.pos):
                    play_sound_effect(select_sound, 0.2)
                    game_state.set_difficulty('easy')
                elif medium_rect.collidepoint(event.pos):
                    play_sound_effect(select_sound, 0.2)
                    game_state.set_difficulty('medium')
                elif hard_rect.collidepoint(event.pos):
                    play_sound_effect(select_sound, 0.2)
                    game_state.set_difficulty('hard')
                elif map1_rect.collidepoint(event.pos):
                    play_sound_effect(select_sound, 0.2)
                    game_state.map_selector('map1')
                elif map2_rect.collidepoint(event.pos):
                    play_sound_effect(select_sound, 0.2)
                    game_state.map_selector('map2')
                elif map3_rect.collidepoint(event.pos):
                    play_sound_effect(select_sound, 0.2)
                    game_state.map_selector('map3')
        display_selection(screen, game_state, which_msg, current_time, msg_start)

        pygame.display.flip()


def start_screen(game_state):
    """
    The starting screen of the game.

    This function handles the initial screen where players can start the game, go to the menu,
    or exit the game.

    - Renders the starting screen with options.
    """
    running_start = True
    play_music(start_music, 0.1)
    while running_start:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = pygame.mouse.get_pos()
                if start_button_rect.collidepoint(mouse_pos):
                    play_sound_effect(select_sound, 0.2)
                    selection_screen(game_state)
                elif menu_button_rect.collidepoint(mouse_pos):
                    play_sound_effect(select_sound, 0.2)
                    menu_screen()
                elif exit_button_rect.collidepoint(mouse_pos):
                    pygame.quit()
                    sys.exit()

        display_start(screen)
        pygame.display.flip()


def main():
    """
    The main function that initializes the game state and starts the game.

    This function sets up the initial game state and calls the start screen to begin the game.

    The function performs the following tasks:
    - Initializes the game state.
    - Calls the start screen to display the initial game menu.
    """

    game_state = GameState()
    start_screen(game_state)


main()
pygame.quit()
sys.exit()

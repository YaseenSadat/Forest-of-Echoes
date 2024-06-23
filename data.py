"""
This module contains classes and functions to support the main game logic, including player actions,
game state management, and item interactions in a Pygame-based game.

Functions:
- play_music: Plays background music.
- play_sound_effect: Plays a sound effect.
- load_map: Loads a map from a text file-like object.
- load_game_map: Loads the game map from a local file.

Classes:
- Item: Represents an item within the game.
- World: Represents the game world, including the map layout and item placements.
- Player: Represents the player in the game, including their position, inventory, and movement.
- Timer: A timer class for managing time-related operations in the game.
- GameState: Manages the overall game state, including game settings and player stats."""
from typing import TextIO

import pygame
import random


def play_music(track, volume):
    """
    Plays background music.
    """
    pygame.mixer.music.load(track)
    pygame.mixer.music.set_volume(volume)
    pygame.mixer.music.play(-1)


def play_sound_effect(sound_file, volume):
    """
    Plays a sound effect.
    """
    sound = pygame.mixer.Sound(sound_file)
    sound.set_volume(volume)
    sound.play()


class Item:
    """
    Represents an item within a game, characterized by its name and description.
    """
    name: str
    descr_one: str

    def __init__(self, name: str, descr_one: str) -> None:
        """
        Initialize a new item with a name and a description.

        Instance Attributes:
        - name: The name of the item
        - descr_one: The description of the item
        """

        self.name = name
        self.descr_one = descr_one


class World:
    """
    Represents the game world, including the map layout and item placements.
    Instance Attributes:
    - map: nested lists containing map data information.
    - items: dictionary of all the items
    - map_data: file conting map grid
    """
    map: list[list[int]]
    items: dict[str, Item]
    map_data: TextIO

    def __init__(self, map_data: TextIO) -> None:
        """
        Initialize the world by loading the map from provided data.
        """
        self.map = load_map(map_data)
        self.locations = {}


class Player:
    """
    Represents the player in the game, including their position, inventory, and movement.
    """
    player_x: int
    player_y: int
    player_code: list[int]
    player_images: dict[str, list[pygame.Surface]]
    inventory: dict[str, str]

    def __init__(self, player_x: int, player_y: int, player_code: list[int], player_images):
        """
        Initialize the player with a starting position, code, and image set.
        """
        self.player_y = player_y
        self.player_x = player_x
        self.player_code = player_code
        self.inventory = {
            # 'Apple': 'Food Item: Gives +2 health',
            # 'Orange': 'Food Item: Gives +2 health',
            # 'Pear': 'Food Item: Gives +2 health',
            # 'Matchbox': 'Crafting Item: Used to craft a campfire',
            # 'Logs': 'Crafting Item: Used to craft a campfire',
            # 'Rock': 'Crafting Item: Used to craft a campfire',
            # 'Blue Key': 'Crucial Key: Necessary to open chest',
            # 'Gold Key': 'Crucial Key: Necessary to open chest',
            # 'Copper Key': 'Crucial Key: Necessary to open chest',
            # 'Wood Key': 'Crucial Key: Necessary to open chest',
            # 'Campfire': 'Heating Mechanism: Allows you to regain health',
            # 'FlareGun': 'gun',
            # 'JewelBag': 'the bag'

        }

        self.player_images = player_images
        self.current_image = self.player_images['down'][0]
        self.direction = 'down'
        self.frame_index = 0
        self.animation_speed = 0.2
        self.last_update = pygame.time.get_ticks()
        self.health = 7

    def kill_player(self):
        """
        Change the player image to their dead one
        """
        self.current_image = self.player_images['dead'][0]

    def get_player_grid_location(self) -> list[int]:
        """
        Calculate and returns the player's grid location based on the player's current x,y position.
        """
        new_x, new_y = self.player_x, self.player_y
        return [((new_x - 185) // 50), ((new_y - 68) // 50)]

    def get_player_grid_code(self, game_state):
        """
        Calculate and returns the player's grid code based on the player's current grid position.
        """
        map_name = game_state.current_map()
        map_file_path = f'{map_name}'
        with open(map_file_path, 'r') as file:
            lines = file.readlines()
            map_grid = [line.strip().split() for line in lines]

        x, y = self.get_player_grid_location()[0], self.get_player_grid_location()[1]

        return int(map_grid[y][x])

    def item_to_inventory(self, item: Item) -> None:
        """
        Add an item to the player's inventory.
        """
        self.inventory[item.name] = item.descr_one

    def remove_item_from_inventory(self, title: str):
        """
        Remove an item from the player's inventory by its title.
        """
        del self.inventory[title]

    def handle_movement(self, game_map):
        """
        Handle player movement based on keyboard inputs and update position and animation.
        """
        keys = pygame.key.get_pressed()
        step = 1
        new_x, new_y = self.player_x, self.player_y
        moving = False

        if keys[pygame.K_w] or keys[pygame.K_UP]:
            new_y -= step
            self.direction = 'up'
            moving = True
        elif keys[pygame.K_s] or keys[pygame.K_DOWN]:
            new_y += step
            self.direction = 'down'
            moving = True
        elif keys[pygame.K_a] or keys[pygame.K_LEFT]:
            new_x -= step
            self.direction = 'left'
            moving = True
        elif keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            new_x += step
            self.direction = 'right'
            moving = True

        now = pygame.time.get_ticks()
        if moving:
            if now - self.last_update > 100:
                self.last_update = now
                self.frame_index = (self.frame_index + 1) % len(self.player_images[self.direction])
                self.current_image = self.player_images[self.direction][self.frame_index]
        else:
            self.frame_index = 0
            self.current_image = self.player_images[self.direction][self.frame_index]

        grid_x_right = (new_x - 180) // 50
        grid_y_bottom = (new_y - 60) // 50
        grid_x_left = (new_x - 195) // 50
        grid_y_top = (new_y - 75) // 50

        if game_map[grid_y_bottom][grid_x_right] not in [0, 2, 98] and game_map[grid_y_top][grid_x_left] not in [0, 2,
                                                                                                                 98]:
            self.player_x, self.player_y = new_x, new_y


def load_map(map_data: TextIO) -> list[list[int]]:
    """
    Loads a map from a text file-like object and converts it into a list of integer lists representing the game map.
    """

    map_list = []
    for line in map_data:
        row = [int(num) for num in line.split()]
        map_list.append(row)
    return map_list


def load_game_map(game_state):
    """
    Loads the game map from a local file.
    """
    game_map_data = []
    map_name = game_state.current_map()
    map_file_path = f'{map_name}'
    with open(map_file_path, 'r') as map_data:
        for line in map_data:
            row = [int(num) for num in line.split()]
            game_map_data.append(row)
    return game_map_data


class Timer:
    """
    A timer class for managing time-related operations in the game.
    """

    def __init__(self):
        self.start_ticks = 0
        self.elapsed_time = 0
        self.running = False

    def start(self):
        """
        Start the timer.
        """
        if not self.running:
            self.start_ticks = pygame.time.get_ticks()
            self.running = True

    def stop(self):
        """
        Stop the timer and calculate the elapsed time.
        """
        if self.running:
            self.elapsed_time += (pygame.time.get_ticks() - self.start_ticks)
            self.running = False

    def get_time(self) -> float:
        """
        Get and return the current elapsed time in seconds.
        """
        if self.running:
            return (pygame.time.get_ticks() - self.start_ticks + self.elapsed_time) / 1000
        return self.elapsed_time / 1000

    def reset(self):
        """
        Reset the timer to zero.
        """
        self.start_ticks = pygame.time.get_ticks()
        self.elapsed_time = 0
        self.running = False


def set_items(map_value):
    """
    Chooses and sets the items on the map
    """
    # Predefined coordinates for each map
    coordinates_map1 = [(2, 10), (5, 12), (12, 1), (10, 3), (12, 5), (19, 5), (20, 8), (12, 12), (20, 12), (1, 9)]
    coordinates_map2 = [(20, 12), (8, 1), (1, 6), (7, 9), (7, 4), (14, 1), (6, 12), (8, 6), (20, 7), (1, 12)]
    coordinates_map3 = [(5, 3), (14, 6), (20, 12), (10, 1), (13, 8), (8, 9), (1, 4), (17, 7), (16, 3), (6, 12)]

    # Items available
    items = [
        Item("Apple", 'Food Item: Gives +2 health'),
        Item("Orange", 'Food Item: Gives +2 health'),
        Item("Pear", 'Food Item: Gives +2 health'),
        Item("Matchbox", 'Crafting Item: Used to craft a campfire'),
        Item("Logs", 'Crafting Item: Used to craft a campfire'),
        Item("Rock", 'Crafting Item: Used to craft a campfire'),
        Item("Blue Key", 'Crucial Key: Necessary to open chest'),
        Item("Gold Key", 'Crucial Key: Necessary to open chest'),
        Item("Copper Key", 'Crucial Key: Necessary to open chest'),
        Item("Wood Key", 'Crucial Key: Necessary to open chest')
    ]

    # Shuffle the items
    random.shuffle(items)

    # Select the coordinate list based on the map
    coordinates = {
        'map1': coordinates_map1,
        'map2': coordinates_map2,
        'map3': coordinates_map3
    }.get(map_value, [])

    # Assign shuffled items to the coordinates
    return {coord: item for coord, item in zip(coordinates, items)}


class GameState:
    """
    Manages the overall game state, including game settings and player stats.
    """

    def __init__(self):
        self.dark_mode = True
        self.campfire = False
        self.gender = 'None'
        self.difficulty = 'medium'
        self.end = False
        self.campfire_locations = []
        self.statistics = {'Health Lost': 0, 'Health Gained': 0}
        self.map = 'None'
        self.items = set_items(self.map)
        self.help_tracker = 0

    def remove_item(self, location):
        """
        Remove an item from the items dictionary based on its location.
        """
        if location in self.items:
            self.items.pop(location)

    def current_map(self) -> str:
        """
        Get the current map.
        """
        return self.map

    def map_selector(self, value):
        """
        f
        """
        if value == 'map1':
            self.map = 'map1'
            self.items = set_items('map1')
        elif value == 'map2':
            self.map = 'map2'
            self.items = set_items('map2')
        elif value == 'map3':
            self.map = 'map3'
            self.items = set_items('map3')

    def health_lost_adder(self):
        """
        Increment the 'Health Lost' statistic.
        """
        self.statistics['Health Lost'] += 0.5

    def health_gained_adder(self, value):
        """
        Increment the 'Health Gained' statistic.
        """
        self.statistics['Health Gained'] += value

    def set_campfire_location(self, player):
        """
        Record the player's current grid location as a campfire location.
        """
        self.campfire_locations.append(player.get_player_grid_location())

    def campfire_location(self):
        """
        Get the initial campfire location.
        """
        return self.campfire_locations[0]

    def reset(self):
        """
        Resets the game state to default values.
        """
        self.dark_mode = True
        self.campfire = False
        self.gender = 'None'
        self.difficulty = 'medium'
        self.end = False
        self.map = 'None'
        self.help_tracker = 0

    def end_game(self):
        """
        Set the game to end.
        """
        self.end = True

    def check_end(self) -> bool:
        """
        Check if the game has ended.
        """
        return self.end is True

    def toggle_dark_mode(self):
        """
        Toggle the dark mode setting on and off.
        """
        self.dark_mode = not self.dark_mode

    def is_dark_mode(self) -> bool:
        """
        Return if it is dark_mode
        """
        return self.dark_mode

    def toggle_campfire(self):
        """
        Toggle the campfire setting on and off
        """
        self.campfire = not self.campfire

    def is_campfire(self) -> bool:
        """
        Return wheter the campfire is on or not
        """
        return self.campfire

    def set_gender(self, value):
        """
        set the gender
        """
        if value == 'male':
            self.gender = 'male'
        elif value == 'girl':
            self.gender = 'girl'

    def current_gender(self) -> str:
        """
        Get the current gender of the player.
        """
        return self.gender

    def set_difficulty(self, value):
        """
        set the difficulty of the gain
        """
        if value == 'easy':
            self.difficulty = 'easy'
        elif value == 'medium':
            self.difficulty = 'medium'
        elif value == 'hard':
            self.difficulty = 'hard'

    def current_difficulty(self) -> str:
        """
        Get the current game difficulty.
        """
        return self.difficulty

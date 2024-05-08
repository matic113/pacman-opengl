import random

from collision import *
from shapes import *
from textures import *

####################################
########### CONSTANTS ###############

WINDOW_WIDTH, WINDOW_HEIGHT = 600, 650
RIBBON_HEIGHT = 40


class Player:
    FRAME_UPDATE_INTERVAL = 20
    EMPOWERED_DURATION = 500  # 500 frames * 20ms = 10 seconds

    def __init__(self, x: int, y: int, size: int, speed: int):
        """Initialize a new player."""
        self.x_pos = x
        self.y_pos = y
        self.prev_x = x
        self.prev_y = y
        self.length = size
        self.speed = speed
        self.rect = Rectangle(x, y, size, size)
        self.direction = "Moving Right"
        self.requested_direction = self.direction
        self.texture_ids = [1, 2]
        self.frame_counter = 0
        self.can_move = False
        self.empowered = False
        self.empowered_timer = 0

    def get_texture_ids(self) -> list:
        """Return the texture IDs for the player."""

        if self.direction == "Moving Right":
            return [1, 2]
        if self.direction == "Moving Left":
            return [3, 4]
        if self.direction == "Moving Up":
            return [5, 6]
        if self.direction == "Moving Down":
            return [7, 8]

    def clone(self) -> "Player":
        """Create a copy of the player."""
        return Player(self.x_pos, self.y_pos, self.length, self.speed)

    def teleport(self, x: int, y: int):
        """Move the player to a new position instantly."""
        self.x_pos = x
        self.y_pos = y
        self.rect = Rectangle(x, y, self.length, self.length)

    def end_frame(self):
        """Update the player's state at the end of a frame."""
        self.frame_counter += 1
        if self.frame_counter >= self.FRAME_UPDATE_INTERVAL:
            self.prev_x = self.x_pos
            self.prev_y = self.y_pos
            self.frame_counter = 0

        if self.empowered:
            self.empowered_timer += 1
            if self.empowered_timer >= self.EMPOWERED_DURATION:
                self.empowered = False
                self.empowered_timer = 0

    @property
    def is_moving(self) -> bool:
        """Check if the player is moving."""
        return self.x_pos != self.prev_x or self.y_pos != self.prev_y


class Ghost:
    ghost_textures = {"yellow": [0, 1], "red": [2, 3], "blue": [4, 5], "pink": [6, 7]}
    MOVE_TO_TARGET = 1
    MOVE_TO_START = -1
    direction_stack = []

    def __init__(
        self,
        x: int,
        y: int,
        size: int,
        speed: int,
        ghost_color: str,
        nearby_blocks: list,
    ):
        self.x_pos = x
        self.y_pos = y
        self.length = size
        self.speed = speed
        self.nearby_blocks = nearby_blocks
        self.rect = Rectangle(x, y, size, size)
        self.state = self.MOVE_TO_TARGET
        self.direction = random.choice(self.nearby_blocks)
        self.texture_ids = self.ghost_textures[ghost_color]

    def clone(self) -> "Ghost":
        """Create a copy of the ghost."""
        return Ghost(
            self.x_pos,
            self.y_pos,
            self.length,
            self.speed,
            self.start,
            self.target,
            self.ghost_color,
        )

    def change_direction(self):
        direction = random.choice(self.nearby_blocks)

        while len(self.direction_stack) > 2 and direction == self.direction_stack[-2]:
            direction = random.choice(self.nearby_blocks)

        self.direction_stack.append(direction)

        self.direction = direction

    def move_to_block(self, block, walls):
        """Move the ghost to a specific block."""
        new_x = self.x_pos
        new_y = self.y_pos

        if self.x_pos < block[0]:
            new_x += self.speed
        elif self.x_pos > block[0]:
            new_x -= self.speed

        if self.y_pos < block[1]:
            new_y += self.speed
        elif self.y_pos > block[1]:
            new_y -= self.speed

        if is_colliding_walls(self, walls):
            self.change_direction()
            return

        else:
            self.teleport(new_x, new_y)

            if block == (new_x, new_y):
                self.change_direction()

    def move_randomly(self, walls):
        position = (self.x_pos, self.y_pos)

        if not (self.x_pos == self.direction[0] or self.y_pos == self.direction[1]):
            self.change_direction()
            return

        self.move_to_block(self.direction, walls)

    def teleport(self, x: int, y: int):
        """Move the ghost to a new position instantly."""
        self.x_pos = x
        self.y_pos = y
        self.rect = Rectangle(x, y, self.length, self.length)


class Fruit:
    def __init__(self, x, y, size, type):
        self.x_pos = x
        self.y_pos = y
        self.size = size
        self.type = type
        self.rect = Rectangle(x, y, size, size)


class Wall:
    def __init__(self, x, y, length, width):
        self.rect = Rectangle(x, y, length, width)
        self.color = (1, 1, 1)

    def draw(self):
        glColor(self.color)
        self.rect.draw()
        glColor(1, 1, 1)

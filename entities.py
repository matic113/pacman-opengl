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
        self.can_move = True
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

    def __init__(
        self,
        x: int,
        y: int,
        size: int,
        speed: int,
        starting_block: tuple,
        target_block: tuple,
        ghost_color: str,
    ):
        self.x_pos = x
        self.y_pos = y
        self.length = size
        self.speed = speed
        self.rect = Rectangle(x, y, size, size)
        self.direction = self.MOVE_TO_TARGET
        self.start = starting_block
        self.target = target_block
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

    def move(self):
        """Move the ghost from Start to Target and vice versa. Note that StartBlock < TargetBlock."""
        new_x = self.x_pos
        new_y = self.y_pos

        if self.start[0] == self.target[0]:
            if self.direction == self.MOVE_TO_TARGET:  # Move to target
                if self.y_pos < self.target[1]:
                    new_y += self.speed
                else:  # Reached Target
                    self.direction = self.MOVE_TO_START
            else:  # Move to Start
                if self.y_pos > self.start[1]:
                    new_y -= self.speed
                else:
                    self.direction = self.MOVE_TO_TARGET

        if self.start[1] == self.target[1]:  # Ghost is moving horizontally
            if self.direction == self.MOVE_TO_TARGET:  # Move to target
                if self.x_pos < self.target[0]:
                    new_x += self.speed
                else:  # Reached Target
                    self.direction = self.MOVE_TO_START
            else:  # Move to Start
                if self.x_pos > self.start[0]:
                    new_x -= self.speed
                else:
                    self.direction = self.MOVE_TO_TARGET

        if new_x - self.length / 2 > 0 and new_x + self.length / 2 < WINDOW_WIDTH:
            self.x_pos = new_x

        if (
            new_y - self.length / 2 > 0
            and new_y + self.length / 2 < WINDOW_HEIGHT - RIBBON_HEIGHT
        ):
            self.y_pos = new_y

        self.rect = Rectangle(self.x_pos, self.y_pos, self.length, self.length)

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

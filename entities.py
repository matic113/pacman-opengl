from collision import *
from shapes import *
from textures import *

####################################
########### CONSTANTS ###############

WINDOW_WIDTH, WINDOW_HEIGHT = 600, 650
RIBBON_HEIGHT = 40

ghost_textures = { "yellow" : [0, 1], "red" : [2, 3], "blue" : [4, 5],"pink" : [6, 7]}

class Player:
    def __init__(self, x, y, size, speed):
        self.x_pos = x
        self.y_pos = y
        self.prev_x = x
        self.prev_y = y
        self.length = size
        self.speed = speed
        self.rect = Rectangle(x, y, size, size)
        self.direction = "Moving Right"
        self.texture_ids = [1, 2]
        self.frame_counter = 0
        self.can_move = True
        self.empowered = False
        self.empowered_timer = 0

    def clone(self):
        return Player(self.x_pos, self.y_pos, self.length, self.speed)

    def teleport(self, x, y):
        self.x_pos = x
        self.y_pos = y
        self.rect = Rectangle(x, y, self.length, self.length)

    def end_frame(self):
        self.frame_counter += 1
        if self.frame_counter >= 20:  # Update previous position every 20 frames
            self.prev_x = self.x_pos
            self.prev_y = self.y_pos
            self.frame_counter = 0

        if self.empowered:
            self.empowered_timer += 1
            if self.empowered_timer >= 1000:
                self.empowered = False
                self.empowered_timer = 0

    @property
    def is_moving(self):
        return self.x_pos != self.prev_x or self.y_pos != self.prev_y


class Ghost:
    def __init__(self, x, y, size, speed, starting_block, target_block, ghost_color):
        self.x_pos = x
        self.y_pos = y
        self.length = size
        self.speed = speed
        self.rect = Rectangle(x, y, size, size)
        self.direction = 1
        self.start = starting_block
        self.target = target_block
        self.texture_ids = ghost_textures[ghost_color]


    def clone(self):
        return Ghost(self.x_pos, self.y_pos, self.length, self.speed)

    def draw(self):
        glColor(1, 0, 0)  # Red color
        self.rect.draw()

    def move(self):
        dx, dy = 0, 0

        new_x = self.x_pos
        new_y = self.y_pos

        if self.start[0] == self.target[0]:
            if self.direction == 1:  # Move to target
                if self.y_pos < self.target[1]:
                    new_y += self.speed
                else:  # Reached Target
                    self.direction = -1
            else:  # Move to Start
                if self.y_pos > self.start[1]:
                    new_y -= self.speed
                else:
                    self.direction = 1

        if self.start[1] == self.target[1]:  # Ghost is moving horizontally
            if self.direction == 1:  # Move to target
                if self.x_pos < self.target[0]:
                    new_x += self.speed
                else:  # Reached Target
                    self.direction = -1
            else:  # Move to Start
                if self.x_pos > self.start[0]:
                    new_x -= self.speed
                else:
                    self.direction = 1

        if new_x - self.length / 2 > 0 and new_x + self.length / 2 < WINDOW_WIDTH:
            self.x_pos = new_x

        if (
            new_y - self.length / 2 > 0
            and new_y + self.length / 2 < WINDOW_HEIGHT - RIBBON_HEIGHT
        ):
            self.y_pos = new_y

        self.rect = Rectangle(self.x_pos, self.y_pos, self.length, self.length)

    def teleport(self, x, y):
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

    def draw(self):
        self.rect.draw()

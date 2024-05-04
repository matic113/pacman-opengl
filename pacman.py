import json
import time
from math import cos, sin
from random import randint

import pygame
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

from collision import *
from entities import *
from shapes import *
from textures import *

####################################
########### constants ##############
####################################

FONT_DOWNSCALE = 0.13

WINDOW_WIDTH = 456
WINDOW_HEIGHT = 536

RIBBON_HEIGHT = 40

FRAME_INTERVAL = 10  # try  1000 msec

PLAYER_SIZE = 30
SPEED = 1.5

# GAME GRID
GRID_SIZE = 8

# Atlas SIZE

PLAYER_ATLAS_SIZE = 9
GHOST_ATLAS_SIZE = 11
PLAYER_DEATH_ATLAS_SIZE = 11

##################Load Sounds###########


def init_sound():
    pygame.mixer.init()

    global eat_sound, game_over_sound, death_sound
    eat_sound = pygame.mixer.Sound("res/audio/sound_effects/pacman_chomp.wav")
    death_sound = pygame.mixer.Sound("res/audio/sound_effects/pacman_death.wav")


def playDeathAnimation(player):
    global lives

    player.can_move = False
    lives -= 1
    death_sound.play()
    time.sleep(1.2)
    player.teleport(START_X, START_Y)
    player.can_move = True

    if lives == 0:
        sys.exit(0)


####################################
########### game state #############
####################################

SCORE = 0
BEST_SCORE = 100
lives = 3

START_X = 224
START_Y = 216

fruits = []

walls = []

ghosts = []


####################################
######## graphics helpers ##########
####################################
# Initialization
def init_window():
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGBA)
    glutInitWindowSize(WINDOW_WIDTH, WINDOW_HEIGHT)
    glutInitWindowPosition(0, 0)
    glutCreateWindow(b"PacMan OpenGL")
    glClearColor(0.0, 0.0, 0.0, 0.0)
    glDisable(GL_DEPTH_TEST)
    glEnable(GL_TEXTURE_2D)
    glEnable(GL_BLEND)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0, WINDOW_WIDTH, 0, WINDOW_HEIGHT, 0, 1)

    glMatrixMode(GL_MODELVIEW)
    loadTextures()


def init_entities():
    global player, walls, ghosts, fruits

    player = Player(x=START_X, y=START_Y, size=PLAYER_SIZE, speed=SPEED)

    ghost1 = Ghost(
        x=30,
        y=358,
        size=30,
        speed=1,
        starting_block=(20, 358),
        target_block=(20, 470),
        ghost_color="red",
    )
    ghost2 = Ghost(
        x=30,
        y=24,
        size=30,
        speed=1,
        starting_block=(30, 28),
        target_block=(420, 28),
        ghost_color="blue",
    )

    ghosts.append(ghost1)
    ghosts.append(ghost2)

    # Load walls from a JSON file
    with open("walls.json", "r") as f:
        walls_data = json.load(f)

    for wall in walls_data:
        wallStartBlock, wallEndBlock = wall["Wall_cords"]
        wall_size = wall["Wall_size"]
        walls.append(create_wall(wallStartBlock, wallEndBlock, wall_size))

    with open("fruits.json", "r") as z:
        fruits_data = json.load(z)

    for fruit in fruits_data:
        x, y = fruit["position"]
        if fruit["type"] == "normal":
            fruit_size = 8
            fruit_type = "normal"
        elif fruit["type"] == "super":
            fruit_size = 16
            fruit_type = "super"

        fruit = Fruit(x, y, fruit_size, fruit_type)
        fruits.append(fruit)


def debug_player(player):
    x_pos = "x : " + str(player.x_pos)
    y_pos = "y : " + str(player.y_pos)
    isMoving = "isMoving : " + str(player.is_moving)
    direction = player.direction
    texture = "Texture_id : " + str(player.texture_ids)

    glColor(1, 1, 1)  # White color
    draw_text(x_pos, 10, 575)
    draw_text(y_pos, 10, 550)
    draw_text(isMoving, 100, 575)
    draw_text(direction, 10, 525)
    draw_text(texture, 10, 500)


def move_player():
    global player

    if player.direction == "Moving Right":
        new_x = player.x_pos + player.speed
        new_y = player.y_pos
    if player.direction == "Moving Left":
        new_x = player.x_pos - player.speed
        new_y = player.y_pos
    if player.direction == "Moving Up":
        new_x = player.x_pos
        new_y = player.y_pos + player.speed
    if player.direction == "Moving Down":
        new_x = player.x_pos
        new_y = player.y_pos - player.speed

    new_player = player.clone()
    new_player.teleport(new_x, new_y)

    # Check if the new position is within the game window
    if not is_colliding_walls(new_player, walls) and player.can_move:
        if new_x - PLAYER_SIZE / 2 > 0 and new_x + PLAYER_SIZE / 2 < WINDOW_WIDTH:
            player.teleport(new_x, player.y_pos)

        if (
            new_y - PLAYER_SIZE / 2 > 0
            and new_y + PLAYER_SIZE / 2 < WINDOW_HEIGHT - RIBBON_HEIGHT
        ):
            player.teleport(player.x_pos, new_y)


def create_wall(start_block, end_block, wall_size):
    x, y = 0, 0
    length, height = 0, 0

    if start_block[0] == end_block[0]:  # Vertical Wall
        x = start_block[0]
        y = (start_block[1] + end_block[1]) / 2
        length = wall_size
        height = abs(start_block[1] - end_block[1]) + wall_size / 2

    if start_block[1] == end_block[1]:  # Horizontal Wall
        x = (start_block[0] + end_block[0]) / 2
        y = start_block[1]
        length = abs(start_block[0] - end_block[0]) + wall_size / 2
        height = wall_size

    return Wall(x, y, length, height)


def draw_score():
    global SCORE, lives, BEST_SCORE

    string = "SCORE : " + str(SCORE)
    draw_text(string, x=10, y=WINDOW_HEIGHT - 25)
    string = "LIVES : " + str(lives)
    draw_text(string, WINDOW_WIDTH - 110, y=WINDOW_HEIGHT - 25)
    string = "BEST SCORE"
    draw_text(string, WINDOW_WIDTH - 280, WINDOW_HEIGHT - 20)
    string = str(BEST_SCORE)
    draw_text(string, WINDOW_WIDTH - 240, WINDOW_HEIGHT - 37)


def draw_level():
    level = Rectangle(
        WINDOW_WIDTH / 2,
        (WINDOW_HEIGHT - RIBBON_HEIGHT) / 2,
        WINDOW_WIDTH,
        WINDOW_HEIGHT - RIBBON_HEIGHT,
    )

    draw_entity(level, sprite_id["level"])


def draw_text(string, x, y):
    glLineWidth(2)
    glColor(1, 1, 1)  # Yellow Color
    glPushMatrix()  # remove the previous transformations
    # glScale(0.13,0.13,1)  # TODO: Try this line
    glTranslate(x, y, 0)
    glScale(
        FONT_DOWNSCALE, FONT_DOWNSCALE, 1
    )  # when writing text and see nothing downscale it to a very small value .001 and draw at center
    string = string.encode()  # conversion from Unicode string to byte string
    for c in string:
        glutStrokeCharacter(GLUT_STROKE_ROMAN, c)  # type: ignore
    glPopMatrix()


def draw_ghosts():
    global ghosts, player
    
    for ghost in ghosts:
        if player.empowered:
            ghost_tex = [8, 9]
        else:
            ghost_tex = ghost.texture_ids

        draw_from_atlas(ghost,sprite_id["ghosts"],GHOST_ATLAS_SIZE, ghost_tex)


def check_collision():
    global ghosts, player, fruits, lives, SCORE

    for ghost in ghosts:
        ghost.move()

        if is_colliding_rect(player, ghost):
            if player.empowered:
                ghosts.remove(ghost)
                SCORE += 200
            else:
                playDeathAnimation(player)

    for fruit in fruits:
        if is_colliding_rect(player.rect, fruit.rect):
            fruits.remove(fruit)
            if fruit.type == "normal":
                SCORE += 10
            elif fruit.type == "super":
                player.empowered = True
                SCORE += 50
            eat_sound.play()


####################################
############# callbacks  ###########
####################################


# noinspection PyUnusedLocal,PyShadowingNames
def keyboard_callback(key, x, y):
    if key == b"q":
        sys.exit(0)


def special_keys_callback(key, x, y):
    global player

    if key == GLUT_KEY_RIGHT:
        player.direction = "Moving Right"
        player.texture_ids = [1, 2]
    if key == GLUT_KEY_LEFT:
        player.direction = "Moving Left"
        player.texture_ids = [3, 4]
    if key == GLUT_KEY_UP:
        player.direction = "Moving Up"
        player.texture_ids = [5, 6]
    if key == GLUT_KEY_DOWN:
        player.direction = "Moving Down"
        player.texture_ids = [7, 8]


# def mouse_callback(x, y):
#     global current_mouse_x
#     current_mouse_x = x  # we only track the x coordinate


####################################
############# timers  ##############
####################################


def game_loop(frame):
    draw_game()
    print(frame)
    glutTimerFunc(FRAME_INTERVAL, game_loop, frame + 1)  # TODO: replace 1 by v+1


########################################################


# noinspection PyShadowingNames
def generate_fruits(n):
    global fruits
    fruit_radius = 10
    while len(fruits) < n:
        x = randint(1, 56) * 8
        y = randint(1, 61) * 8

        fruit = Fruit(x, y, fruit_radius)
        if is_colliding_walls(fruit, walls):
            continue
        fruits.append(fruit)

    return fruits


def draw_fruits():
    for fruit in fruits:
        if fruit.type == "normal":
            draw_entity(fruit, 13)
        elif fruit.type == "super":
            draw_entity(fruit, 10)


def draw_walls():
    glColor(1, 1, 1)  # Pink color
    for wall in walls:
        wall.draw()


def draw_game():
    global SCORE, lives, player

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    draw_score()
    draw_level()

    draw_fruits()

    draw_walls()  # TODO : WALLS VISIBILITY

    draw_ghosts()

    # draw(player,player.texture_ids)
    draw_from_atlas(player, sprite_id["pacman"], PLAYER_ATLAS_SIZE, player.texture_ids)
    move_player()
    check_collision()
    player.end_frame()

    glutSwapBuffers()


def main():
    init_entities()
    init_sound()

    # openGL Intialization
    init_window()
    glutDisplayFunc(draw_game)
    glutTimerFunc(FRAME_INTERVAL, game_loop, 1)
    glutKeyboardFunc(keyboard_callback)
    glutSpecialFunc(special_keys_callback)
    glutMainLoop()


if __name__ == "__main__":
    main()

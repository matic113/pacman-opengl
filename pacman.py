import random
from math import cos, sin

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

WINDOW_WIDTH = 600
WINDOW_HEIGHT = 650

RIBBON_HEIGHT = 40

INTERVAL = 10  # try  1000 msec

PLAYER_RADIUS = 30
SPEED = 2

# GAME GRID

####################################
########### game state #############
####################################

SCORE = 0
BEST_SCORE = 9999
lives = 3
player_x = 300
player_y = 300

plStates = {0: "Moving Up", 1: "Moving Down", 2: "Moving Left", 3: "Moving Right"}
plCurrent_state = 3

fruits = []
walls_cords = [
    ((400, 400), (400, 100)),
    ((200, 400), (200, 100)),
    ((200, 460), (400, 460)),
]
walls = []

ghosts = []


####################################
######## graphics helpers ##########
####################################
# Initialization
def init():
    glClearColor(0.0, 0.0, 0.0, 0.0)
    glEnable(GL_TEXTURE_2D)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0, WINDOW_WIDTH, 0, WINDOW_HEIGHT, 0, 1)

    glMatrixMode(GL_MODELVIEW)
    loadTextures()

    global player
    global walls
    global ghosts
    player = Player(x=300, y=300, size=PLAYER_RADIUS, speed=SPEED)

    ghost1 = Ghost(
        x=100,
        y=50,
        size=30,
        speed=1,
        starting_block=(100, 100),
        target_block=(500, 100),
    )
    ghost2 = Ghost(
        x=100,
        y=50,
        size=30,
        speed=1,
        starting_block=(100, 100),
        target_block=(100, 500),
    )
    ghosts.append(ghost1)
    ghosts.append(ghost2)
    generate_fruits(10)

    for cord in walls_cords:
        walls.append(create_wall(cord[0], cord[1]))


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


def create_wall(block_1, block_2):
    length, width = 0, 0
    x, y = 0, 0

    if block_1[0] == block_2[0]:  # Vertical Wall
        x = block_1[0]
        y = (block_1[1] + block_2[1]) / 2
        length = 10
        height = abs(block_1[1] - block_2[1]) + 10

    if block_1[1] == block_2[1]:  # Horizontal Wall
        x = (block_1[0] + block_2[0]) / 2
        y = block_1[1]
        length = abs(block_1[0] - block_2[0]) + 10
        height = 10

    return Wall(x, y, length, height)


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


def draw_mouth(player):
    global plCurrent_state

    glLoadIdentity()
    glColor(0, 0, 0)  # Black color

    state = plStates[plCurrent_state]
    if state == "Moving Right":
        draw_cutout(player, -45, 45)
    if state == "Moving Up":
        draw_cutout(player, 45, 135)
    if state == "Moving Left":
        draw_cutout(player, 135, 225)
    if state == "Moving Down":
        draw_cutout(player, 225, 315)


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
        player.texture_ids = [0, 1]
    if key == GLUT_KEY_LEFT:
        player.direction = "Moving Left"
        player.texture_ids = [2, 3]
    if key == GLUT_KEY_UP:
        player.direction = "Moving Up"
        player.texture_ids = [4, 5]
    if key == GLUT_KEY_DOWN:
        player.direction = "Moving Down"
        player.texture_ids = [6, 7]


# def mouse_callback(x, y):
#     global current_mouse_x
#     current_mouse_x = x  # we only track the x coordinate


####################################
############# timers  ##############
####################################


def game_timer(frame):
    draw_game()
    print(frame)
    glutTimerFunc(INTERVAL, game_timer, frame + 1)  # TODO: replace 1 by v+1


########################################################


# noinspection PyShadowingNames
def generate_fruits(n):
    global fruits
    fruit_radius = 10
    while len(fruits) < n:
        x = random.randint(0, 60) * 10
        y = random.randint(0, 61) * 10

        fruit = Fruit(x, y, fruit_radius)
        if is_colliding_walls(fruit, walls):
            continue
        fruits.append(fruit)

    return fruits


def draw_fruits():
    for fruit in fruits:
        draw_player(fruit, 10)


def draw_walls():
    glColor(1, 1, 1)  # Pink color
    for wall in walls:
        wall.draw()


def draw_game():
    global SCORE
    global player
    global ghosts
    global lives

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    # draw top ribbon
    glColor(0.5, 0.5, 0.5)  # Gray color
    ribbon = Rectangle(
        WINDOW_WIDTH / 2,
        WINDOW_HEIGHT - (RIBBON_HEIGHT / 2),
        WINDOW_WIDTH,
        RIBBON_HEIGHT,
    )
    draw_rectangle(ribbon)

    # Draw the score,best score and lives
    string = "SCORE : " + str(SCORE)
    draw_text(string, 10, 625)
    string = "LIVES : " + str(lives)
    draw_text(string, 490, 625)
    string = "BEST SCORE"
    draw_text(string, 230, 633)
    string = str(BEST_SCORE)
    draw_text(string, 265, 615)

    debug_player(player)
    draw_player(player, player.texture_ids)
    draw_fruits()
    draw_walls()

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
    if not is_colliding_walls(new_player, walls):
        if new_x - PLAYER_RADIUS / 2 > 0 and new_x + PLAYER_RADIUS / 2 < WINDOW_WIDTH:
            player.teleport(new_x, player.y_pos)

        if (
            new_y - PLAYER_RADIUS / 2 > 0
            and new_y + PLAYER_RADIUS / 2 < WINDOW_HEIGHT - RIBBON_HEIGHT
        ):
            player.teleport(player.x_pos, new_y)

    draw_player(ghosts[0], 8)
    draw_player(ghosts[1], 9)
    for ghost in ghosts:
        ghost.move()

        if is_colliding_rect(player.rect, ghost.rect):
            lives -= 1
            player.teleport(300, 300)
            if lives == 0:
                sys.exit(0)

    for fruit in fruits:
        if is_colliding_rect(player.rect, fruit.rect):
            fruits.remove(fruit)
            SCORE += 10

    player.end_frame()

    glutSwapBuffers()


def main():
    # Initialize the game window
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGBA)
    glutInitWindowSize(WINDOW_WIDTH, WINDOW_HEIGHT)
    glutInitWindowPosition(0, 0)
    glutCreateWindow(b"PacMan OpenGL")
    init()
    glutDisplayFunc(draw_game)
    glutTimerFunc(INTERVAL, game_timer, 1)
    glutKeyboardFunc(keyboard_callback)
    glutSpecialFunc(special_keys_callback)
    glutMainLoop()


if __name__ == "__main__":
    main()

import pygame
from OpenGL.GL import *
from OpenGL.GLUT import *

"""
Texture steps (init)
1) glEnable(GL_TEXTURE_2D)
2) pygame.image.load("1.png")
3) pygame.image.tostring(image, "RGBA", True)
4) glGenTextures(len(images), texture_names) # create identifiers for textures
5) glBindTexture(GL_TEXTURE_2D, texture_name) # modify THIS IDENTIFIER
6) glTexParameterf (many of those) # set the parameters
7) glTexImage2D # feed the binary image to opengl(Usage)
1) glBindTexture(GL_TEXTURE_2D, texture_name) # use THIS IDENTIFIER
2) glTexCoord(0, 0) repeat this
"""

ANIMATION_FRAME = 0
FRAME_DURATION = 10


def my_init():
    glClearColor(0.0, 0.0, 0.0, 0.0)
    glEnable(GL_TEXTURE_2D)
    glMatrixMode(GL_PROJECTION)  # ortho or perspective NO BRAINER
    glLoadIdentity()
    glOrtho(0, 500, 0, 500, 0, 1)  # l,r,b,t,n,f

    glMatrixMode(GL_MODELVIEW)
    loadTextures()


texture_names = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]  # TODO IMPORTANT must be numbers


def texture_setup(texture_image_binary, texture_name, width, height):
    """Assign texture attributes to specific images."""
    glBindTexture(GL_TEXTURE_2D, texture_name)  # texture init step [5]

    # texture init step [6]
    # affects the active selected texture which is identified by texture_name
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameterf(
        GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT
    )  # GL_MIRRORED_REPEAT , GL_CLAMP_TO_EDGE, GL_CLAMP_TO_BORDER
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
    # END: texture init step [6]

    glTexImage2D(
        GL_TEXTURE_2D,
        0,  # mipmap
        3,  # Bytes per pixel
        width,
        height,
        0,  # Texture border
        GL_RGBA,  # RGBA Exactly as in  pygame.image.tostring(image, "RGBA", True)
        GL_UNSIGNED_BYTE,
        texture_image_binary,
    )  # texture init step [7]


def load_and_setup(image_path, idx):
    # Load images from file system
    image = pygame.image.load(image_path)
    # Convert images to the type needed for textures
    texture = pygame.image.tostring(image, "RGBA", True)  # texture init step [3]
    texture_setup(texture, texture_names[idx], image.get_width(), image.get_height())


def loadTextures():
    """Open images and convert them to "raw" pixel maps and
    bind or associate each image with and integer refernece number.
    """
    glEnable(GL_TEXTURE_2D)  # texture init step 1

    # Generate textures names from array
    glGenTextures(len(texture_names), texture_names)  # texture init step [4]

    # Add textures to openGL [2, 3, 5 ,6 ,7]
    # pacman texture is [11 x 6] x 16 pixels
    load_and_setup("art/right_1.png", texture_names[0])
    load_and_setup("art/right_2.png", texture_names[1])
    load_and_setup("art/left_1.png", texture_names[2])
    load_and_setup("art/left_2.png", texture_names[3])
    load_and_setup("art/up_1.png", texture_names[4])
    load_and_setup("art/up_2.png", texture_names[5])
    load_and_setup("art/down_1.png", texture_names[6])
    load_and_setup("art/down_2.png", texture_names[7])
    load_and_setup("art/ghost_yellow.png", texture_names[8])
    load_and_setup("art/ghost_red.png", texture_names[9])
    load_and_setup("art/power_pellete.png", texture_names[10])


def draw_player(Player, texture_ids):
    # glClearColor(0, 0, 0, 0)
    rect = Player.rect
    # glClear(GL_COLOR_BUFFER_BIT)
    # glColor3f(1, 1, 1)  # TODO IMPORTANT
    # glLoadIdentity()
    global ANIMATION_FRAME
    global FRAME_DURATION
    texture = 0
    if type(texture_ids) == list:
        if Player.is_moving:
            if ANIMATION_FRAME < FRAME_DURATION:
                texture = texture_ids[0]
            elif ANIMATION_FRAME > FRAME_DURATION:
                texture = texture_ids[1]

            ANIMATION_FRAME = (
                ANIMATION_FRAME + 1 if ANIMATION_FRAME < 2 * FRAME_DURATION else 0
            )
        else:
            texture = texture_ids[0]

    else:
        texture = texture_ids

    glBindTexture(
        GL_TEXTURE_2D, texture_names[texture]
    )  # repeat this if you want to bind another texture

    glBegin(GL_QUADS)
    glTexCoord2f(0, 0)  # TODO IMPORTANT: glTexCoord2f must come first before glVertex2d
    glVertex2d(rect.left, rect.bottom)

    glTexCoord2f(1, 0)
    glVertex2d(rect.right, rect.bottom)

    glTexCoord2f(1, 1)
    glVertex2d(rect.right, rect.top)

    glTexCoord2f(0, 1)
    glVertex2d(rect.left, rect.top)

    glEnd()

    glBindTexture(GL_TEXTURE_2D, -1)

    # glutSwapBuffers()


def draw(Player):
    # glClearColor(0, 0, 0, 0)
    rect = Player.rect
    glClear(GL_COLOR_BUFFER_BIT)
    glColor3f(1, 1, 1)  # TODO IMPORTANT
    glLoadIdentity()

    glBindTexture(
        GL_TEXTURE_2D, texture_names[0]
    )  # repeat this if you want to bind another texture

    glBegin(GL_QUADS)
    glTexCoord2f(0, 0)  # TODO IMPORTANT: glTexCoord2f must come first before glVertex2d
    glVertex2d(rect.left, rect.bottom)

    glTexCoord2f(1, 0)
    glVertex2d(rect.right, rect.bottom)

    glTexCoord2f(1, 1)
    glVertex2d(rect.right, rect.top)

    glTexCoord2f(0, 1)
    glVertex2d(rect.left, rect.top)

    glEnd()

    glBindTexture(GL_TEXTURE_2D, -1)

    glutSwapBuffers()


def main():
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGBA)
    glutInitWindowSize(500, 500)
    glutCreateWindow(b"tex example")
    my_init()
    glutDisplayFunc(draw)
    glutMainLoop()


if __name__ == "__main__":
    main()

from OpenGL.GL import *
from OpenGL.GLUT import *
from PIL import Image


def load_texture(image_path):
    img = Image.open(image_path)
    img_data = img.tobytes("raw", "RGB", 0, -1)

    texture_id = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, texture_id)
    glTexImage2D(
        GL_TEXTURE_2D,
        0,
        GL_RGB,
        img.width,
        img.height,
        0,
        GL_RGB,
        GL_UNSIGNED_BYTE,
        img_data,
    )

    # Set the texture parameters
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)

    return texture_id


def draw():
    texture_id = load_texture("art/up_1.png")
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glBindTexture(GL_TEXTURE_2D, texture_id)
    glBegin(GL_QUADS)
    glTexCoord2f(0, 0)
    glVertex3f(-1, -1, 0)
    glTexCoord2f(1, 0)
    glVertex3f(1, -1, 0)
    glTexCoord2f(1, 1)
    glVertex3f(1, 1, 0)
    glTexCoord2f(0, 1)
    glVertex3f(-1, 1, 0)
    glEnd()
    glutSwapBuffers()


def draw_entity(entity, texture_id):
    rect = entity.rect

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glBindTexture(GL_TEXTURE_2D, texture_id)
    glBegin(GL_QUADS)
    glTexCoord2f(0, 0)
    glVertex3f(rect.left, rect.bottom, 0)
    glTexCoord2f(1, 0)
    glVertex3f(rect.right, rect.bottom, 0)
    glTexCoord2f(1, 1)
    glVertex3f(rect.right, rect.top, 0)
    glTexCoord2f(0, 1)
    glVertex3f(rect.left, rect.top, 0)
    glEnd()


# Initialize GLUT and create a window


def main():
    glutInit()
    glutInitDisplayMode(GLUT_RGB | GLUT_DOUBLE)
    glutInitWindowSize(480, 480)
    glutCreateWindow(b"OpenGL Window")

    # Enable 2D texturing
    glEnable(GL_TEXTURE_2D)
    texture_id = load_texture("art/up_1.png")
    # Load the texture
    # Set the draw function and start the main loop
    glutDisplayFunc(draw)
    glutIdleFunc(draw)  # Continuously redraw the scene
    glutMainLoop()


if __name__ == "__main__":
    main()

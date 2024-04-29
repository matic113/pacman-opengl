from math import cos, sin

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *


class Rectangle:
    def __init__(self, x, y, length, width):
        self.left = x - length / 2
        self.right = x + length / 2
        self.top = y + width / 2
        self.bottom = y - width / 2
        self.x = x
        self.y = y

    def draw(self):
        draw_rectangle(self)


class Circle:
    # noinspection PyShadowingNames
    def __init__(self, x, y, r):
        self.x = x
        self.y = y
        self.r = r


class Wall:
    def __init__(self, x, y, length, width):
        self.rect = Rectangle(x, y, length, width)
        self.texture = None

    def draw(self):
        self.rect.draw()


def draw_rectangle(rect):
    glLoadIdentity()
    glBegin(GL_QUADS)
    glVertex(rect.left, rect.bottom, 0)  # Left - Bottom
    glVertex(rect.right, rect.bottom, 0)
    glVertex(rect.right, rect.top, 0)
    glVertex(rect.left, rect.top, 0)
    glEnd()


def draw_circle(circle):
    glLoadIdentity()
    glBegin(GL_POLYGON)
    for i in range(360):
        angle = i * 3.14159 / 180
        x = circle.x + circle.r * cos(angle)
        y = circle.y + circle.r * sin(angle)
        glVertex(x, y, 0)
    glEnd()


def draw_cutout(circle, start_angle, end_angle):
    glLoadIdentity()
    glBegin(GL_POLYGON)
    starting_x = circle.x
    starting_y = circle.y
    glVertex(starting_x, starting_y, 0)
    for i in range(start_angle, end_angle + 1):
        angle = i * 3.14159 / 180
        x = circle.x + circle.r * cos(angle)
        y = circle.y + circle.r * sin(angle)
        glVertex(x, y, 0)
    glVertex(starting_x, starting_y, 0)
    glEnd()


def draw_triangle(triangle):
    glLoadIdentity()
    glBegin(GL_TRIANGLES)
    glVertex(triangle.x1, triangle.y1, 0)
    glVertex(triangle.x2, triangle.y2, 0)
    glVertex(triangle.x3, triangle.y3, 0)
    glEnd()

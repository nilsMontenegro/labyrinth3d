print "import OpenGL          ",
import OpenGL
import OpenGL.GL
import OpenGL.GLU
import pygame
print "done"


print "init grafic            ",
width  = 1024.0
height = 768.0

pygame.init()

screen = pygame.display.set_mode((int(width),int(height)),
    pygame.HWSURFACE | pygame.OPENGLBLIT | pygame.DOUBLEBUF, 24)    

OpenGL.GL.glClearColor(1.0, 1.0, 1.0, 1.0)
OpenGL.GL.glEnable(OpenGL.GL.GL_DEPTH_TEST)
OpenGL.GL.glShadeModel(OpenGL.GL.GL_FLAT)

fov_angle = 60.0
z_near    = 2.0
z_far     = 1000.0

OpenGL.GL.glMatrixMode(OpenGL.GL.GL_PROJECTION)
OpenGL.GL.glLoadIdentity()
OpenGL.GLU.gluPerspective( fov_angle,
    float(width)/float(height),
    z_near, z_far )

OpenGL.GL.glTranslate(0.0,  0.0, -40.0)

rotation_x = 20.0
rotation_y = 0.0

OpenGL.GL.glRotate(rotation_x, 1.0, 0.0, 0.0)
OpenGL.GL.glRotate(rotation_y, 0.0, 1.0, 0.0)

OpenGL.GL.glMatrixMode(OpenGL.GL.GL_MODELVIEW)

print "done"


def update_rotation(x, y):
    global rotation_x, rotation_y

    rotation_x_old = rotation_x
    rotation_y_old = rotation_y

    rotation_x += 1.0 * x
    rotation_y += 1.0 * y

    if rotation_x > 80.0:
        rotation_x = 80.0
    if rotation_x < -80.0:
        rotation_x = -80.0

    OpenGL.GL.glMatrixMode(OpenGL.GL.GL_PROJECTION)

    OpenGL.GL.glRotate(-rotation_y_old, 0.0, 1.0, 0.0)
    OpenGL.GL.glRotate(-rotation_x_old, 1.0, 0.0, 0.0)

    OpenGL.GL.glRotate(rotation_x, 1.0, 0.0, 0.0)
    OpenGL.GL.glRotate(rotation_y, 0.0, 1.0, 0.0)



def render_scene(labyrint):
    OpenGL.GL.glClear(OpenGL.GL.GL_COLOR_BUFFER_BIT | OpenGL.GL.GL_DEPTH_BUFFER_BIT)
    labyrint.render("truecolor")
    pygame.display.flip()

    OpenGL.GL.glClear(OpenGL.GL.GL_COLOR_BUFFER_BIT | OpenGL.GL.GL_DEPTH_BUFFER_BIT)
    labyrint.render("falsecolor")


def position_check(x, y_neg):
            color = OpenGL.GL.glReadPixels(x, height - y_neg,
                1, 1, OpenGL.GL.GL_RGB, OpenGL.GL.GL_BYTE)

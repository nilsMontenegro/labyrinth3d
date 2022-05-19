import OpenGL
import waysegment

size_x = 6 # +x = rigth
size_y = 2 # +y = up
size_z = 6 # +z = to viewer

segments = [ [ [ waysegment.Waysegment() for z in range(size_z) ] for y in range(size_y) ] for x in range(size_x) ]

spare_seg = waysegment.Waysegment()

def serialize():
    global size_x, size_y, size_z
    global spare_seg

    string = str(size_x) + ";" + str(size_y) + ";" + str(size_z) + ";"

    for x in range(size_x):
        for y in range(size_y):
            for z in range(size_z):
                string += segments[x][y][z].serialize()
                string += ";"
    string += spare_seg.serialize()

    return string

def deserialize(string):
    global size_x, size_y, size_z
    global spare_seg
    global segments

    params = string.split(";")

    size_x = int(params[0])
    size_y = int(params[1])
    size_z = int(params[2])

    segments = [ [ [ waysegment.Waysegment() for z in range(size_z) ] for y in range(size_y) ] for x in range(size_x) ]

    i = 4
    for x in range(size_x):
        for y in range(size_y):
            for z in range(size_z):
                segments[x][y][z].deserialize(params[i])
                i += 1
    spare_seg.deserialize(params[-1])


def render(mode):
    global size_x, size_y, size_z

    for x in range(size_x):
        for y in range(size_y):
            for z in range(size_z):

                OpenGL.GL.glMatrixMode(OpenGL.GL.GL_MODELVIEW)
                OpenGL.GL.glLoadIdentity()
                OpenGL.GL.glTranslate(x * 5.0 - size_x / 2.0 * 5.0,
                   y * 5.0 - size_y / 2.0 * 5.0,
                   z * 5.0 - size_z / 2.0 * 5.0)

                next_faces = segments[x][y][z].faces
                next_color = segments[x][y][z].color

                if mode == "falsecolor":
                    OpenGL.GL.glColor3b(x * 10, y * 10, z * 10); 
                    OpenGL.GL.glDrawElements(OpenGL.GL.GL_QUADS, len(next_faces), OpenGL.GL.GL_UNSIGNED_INT, next_faces)
                if mode == "truecolor":
                    OpenGL.GL.glColor3b(0, 0, 0);
                    OpenGL.GL.glPolygonMode(OpenGL.GL.GL_FRONT_AND_BACK, OpenGL.GL.GL_LINE)
                    OpenGL.GL.glDrawElements(OpenGL.GL.GL_QUADS, len(next_faces), OpenGL.GL.GL_UNSIGNED_INT, next_faces)

                    OpenGL.GL.glColor3bv(next_color);
                    OpenGL.GL.glPolygonMode(OpenGL.GL.GL_FRONT_AND_BACK, OpenGL.GL.GL_FILL)
                    OpenGL.GL.glDrawElements(OpenGL.GL.GL_QUADS, len(next_faces), OpenGL.GL.GL_UNSIGNED_INT, next_faces)

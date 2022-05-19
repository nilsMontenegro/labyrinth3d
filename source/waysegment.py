import random
import globalValues
if not globalValues.i_am_server:
    import OpenGL

small_cube_len = 1.0
s = small_cube_len / 2.0

big_cube_len = 5
b = big_cube_len / 2.0

points = [\
[-s, -s,  s],
[ s, -s,  s],
[ s,  s,  s],
[-s,  s,  s],

[-s, -s, -s],
[ s, -s, -s],
[ s,  s, -s],
[-s,  s, -s],

[-s, -s,  b],
[ s, -s,  b],
[ s,  s,  b],
[-s,  s,  b],

[-s, -s, -b],
[ s, -s, -b],
[ s,  s, -b],
[-s,  s, -b],

[ b,  s, -s],
[ b, -s, -s],
[ b, -s,  s],
[ b,  s,  s],

[-b,  s, -s],
[-b, -s, -s],
[-b, -s,  s],
[-b,  s,  s],

[-s, -b,  s],
[ s, -b,  s],
[ s, -b, -s],
[-s, -b, -s],

[-s,  b,  s],
[ s,  b,  s],
[ s,  b, -s],
[-s,  b, -s]
]

if not globalValues.i_am_server:
    OpenGL.GL.glEnableClientState(OpenGL.GL.GL_VERTEX_ARRAY);
    OpenGL.GL.glVertexPointer(3, OpenGL.GL.GL_DOUBLE, 0, points)

x_pos = 0
x_neg = 1
y_pos = 2
y_neg = 3
z_pos = 4
z_neg = 5


def rand_bool(prob):
    return random.random() < prob

class Waysegment:
    def generate_faces(self):

        self.faces = []

        if self.ways[z_pos]:
            self.faces.extend([8, 9, 10, 11])
            self.faces.extend([9, 1, 2, 10])
            self.faces.extend([10, 2, 3 ,11])
            self.faces.extend([11, 3, 0, 8])
            self.faces.extend([9, 1, 0, 8])
        else:
            self.faces.extend([0, 1, 2, 3])

        if self.ways[z_neg]:
            self.faces.extend([15, 14, 13, 12])
            self.faces.extend([14, 6, 5, 13  ])
            self.faces.extend([15, 7, 6, 14  ])
            self.faces.extend([7, 15, 12, 4  ])
            self.faces.extend([5, 4, 12, 13  ])
        else:
            self.faces.extend([7, 6, 5, 4])

        if self.ways[x_neg]:
            self.faces.extend([20, 21, 22, 23])
            self.faces.extend([23, 3, 7, 20  ])
            self.faces.extend([22, 0, 3, 23  ])
            self.faces.extend([4, 0, 22, 21  ])
            self.faces.extend([7, 4, 21, 20  ])
        else:
            self.faces.extend([0, 3, 7, 4])

        if self.ways[x_pos]:
            self.faces.extend([19, 18, 17, 16])
            self.faces.extend([19, 16, 6, 2  ])
            self.faces.extend([18, 19, 2, 1  ])
            self.faces.extend([17, 18, 1, 5  ])
            self.faces.extend([16, 17, 5, 6  ])
        else:
            self.faces.extend([5, 6, 2, 1    ])

        if self.ways[y_pos]:
            self.faces.extend([28, 29, 30, 31])
            self.faces.extend([29, 28, 3, 2  ])
            self.faces.extend([30, 29, 2, 6  ])
            self.faces.extend([31, 30, 6, 7  ])
            self.faces.extend([28, 31, 7, 3  ])
        else:
            self.faces.extend([3, 2, 6, 7    ])


        if self.ways[y_neg]:
            self.faces.extend([27, 26, 25, 24])
            self.faces.extend([24, 25, 1, 0  ])
            self.faces.extend([25, 26, 5, 1  ])
            self.faces.extend([4, 5, 26, 27  ])
            self.faces.extend([0 , 4, 27, 24 ])
        else:
            self.faces.extend([4, 5, 1, 0    ])



    def __init__(self):
        self.ways = [False] * 6

        for i in range(6):
            self.ways[i] = rand_bool(0.3)

        while sum(self.ways) < 3:
            i = int(random.random() * 6)
            self.ways[i] = True

        self.color = [
            int(random.random()*64),
            int(random.random()*64),
            int(random.random()*64 + 63)]

        if not globalValues.i_am_server:
            self.generate_faces()

    def serialize(self):
        bitmap = 0
        for i in range(6):
            if self.ways[i]:
                bitmap |= 1 << i

        color_str = str(self.color[0])\
            + "." + str(self.color[1])\
            + "." + str(self.color[2])

        return str(bitmap) + "." + color_str
 
    def deserialize(self, string):
        params = string.split(".")
        bitmap = int(params[0])
        self.ways = [False] * 6
        for i in range(6):
            self.ways[i] = (bitmap & (1 << i)) >> i
        if not globalValues.i_am_server:
            self.generate_faces()

        self.color = [int(params[1]), int(params[2]), int(params[3])]

    def rotate(self, direction):
        return # do it another time
        if direction == "clockwise":
            tmp = self.front
            self.front = self.left
            self.left  = self.back
            self.back  = self.rigth
            self.right = tmp
        if direction == "anticlockwise":
            self.rotate("clockwise")
            self.rotate("clockwise")
            self.rotate("clockwise")

        if not globalValues.i_am_server:
            self.generate_faces()

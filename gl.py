#Andrés Emilio Quinto Villagrán
#18288
#Lab 1 - point

import struct
def char(c):
    return struct.pack('=c' , c.encode('ascii'))

def word(c):
    return struct.pack('=h', c)

def dword(c):
    return struct.pack('=l', c)

def color(r, g, b):
    return bytes([b, g, r])

class Render(object):
    def __init__(self,):
        self.framebuffer = []

    def glinit(self, width, height,r, g, b):
    	self.glCreateWindow(width, height)
    	self.glClearColor(r, g, b)
    	self.glClear()

#Features gl
    #inicializa el frame buffer con un tamaño

    def glCreateWindow(self, width, height):
        self.width = width
        self.height = height

    #Inicializa el framebuffer con especificaciones sobre donde puede dibujar

    def glViewport(self, x, y, width, height):
        self.viewPortWidth = width
        self.viewPortHeight = height
        self.xViewPort = x
        self.yViewPort = y
    #llena el mapa de un solo color

    def  glClear(self):
        self.framebuffer =[
            [color(r, g, b) for x in range(self.width)]
            for y in range(self.height)
        ]

    #Funcion con la cual podemos cambiar el color de gl clear (solo numeros de 0 a 1)

    def glClearcolor(self, r, g, b):

        #evitamos que se obtengan valores decimales

        r = round(r*255)
        g = round(g*255)
        b = round(b*255)
        self.framebuffer = [
            [color(r, g, b) for x in range(self.width)]
            for y in range(self.height)
        ]
    #Función que nos permite cambiar el color de un punto en pantalla

    def glVertex(self, x,y):
        gX = round((x+1)*(self.viewPortWidth/2)+self.xViewPort)
        gY = round((y+1)*(self.viewPortHeight/2)+self.yViewPort)
        self.point(gX, gY)

    #Operacion la cual nos permite cambiar el color con el que funciona glVertex

    def glColor(self, r,g,b):
        r = round(r*255)
        g = round(g*255)
        b = round(b*255)
        return color(r, g, b)

    def glFinish(self, filename):
        f = open(filename, 'bw')

        #Header
        f.write(char('B'))
        f.write(char('M'))
        f.write(dword(14 + 40 + self.width * self.height * 3))
        f.write(dword(0))
        f.write(dword(14 + 40))

        #image header 
        f.write(dword(40))
        f.write(dword(self.width))
        f.write(dword(self.height))
        f.write(word(1))
        f.write(word(24))
        f.write(dword(0))
        f.write(dword(self.width * self.height * 3))
        f.write(dword(0))
        f.write(dword(0))
        f.write(dword(0))
        f.write(dword(0))

        #Pixel data

        for x in range(self.width):
                for y in range(self.height):
                        f.write(self.framebuffer[y][x])

        f.close()

#function dot
    def point(self, x, y):
        self.framebuffer[x][y] = self.glColor(1,1,0)

    def glCordX(self, x):
    	return round((x+1)*(self.viewPortWidth/2)+self.xViewPort)

    def glCordY(self, y):
    	return round((y+1)*(self.viewPortHeight/2)+self.yViewPort)

    def glpointi(self, x, y):
    	X = self.glCordX(x)
    	Y = self.glCordY(y)
    	self.point(X, Y)

   	#Implementacion del algoritmo visto en clase con Denn1s 
    def glLine(self, x0, y0, x1, y1):
        x0 = self.glCordX(x0)
        y0 = self.glCordY(y0)
        x1 = self.glCordX(x1)
        y1 = self.glCordY(y1)

        dy = abs(y1 - y0)
        dx = abs(x1 - x0)

        steep = dy > dx

        if steep:
            x0, y0 = y0, x0
            x1, y1 = y1, x1

        if x0 > x1:
            x0, x1 = x1, x0
            y0, y1 = y1, y0

        dy = abs(y1 - y0)
        dx = abs(x1 - x0)

        offset = 0 
        threshold =  dx
        y = y0
        inc = 1 if y1 > y0 else -1
        for x in range(x0, x1):
            if steep:
                self.point(y, x)
            else:
                self.point(x, y)

            offset += 2 * dy
            if offset >= threshold:
                y += inc
                threshold += 2 * dx



   
r = Render()
r.glCreateWindow(100, 100)
r.glClearcolor(0.14, 0.2018, 0.26)
r.glViewport(10, 00, 50, 50)
r.glColor(1, 1, 0)
r.glpointi(-0.5, 1)
r.glColor(0.9,0,0)
r.glLine(-1,-1,0,1)
r.glLine(0, 1, 1, -1)
r.glLine(1, -1, -1, -1)
#Triangulo de arriba
r.glLine(0, 1, -1, 2.8)
r.glLine(-1, 2.8, 1, 2.8)
r.glLine(1, 2.8, 0, 1)
r.glFinish('out.bmp')
#sad
import struct
import random

#Write utils
def char(c):
	# 1 byte
	return struct.pack('=c', c.encode('ascii'))

def word(w):
	# 2 bytes
	return struct.pack('=h', w)

def dword(d):
	# 4 bytes
	return struct.pack('=l', d)

def color(r, g, b):
	return bytes([b, g, r])

BLACK = color(0, 0, 0)
WHITE = color(255, 255, 255)

#importar esta clase en gllib
class Render(object):
	def __init__(self, width, height):
		self.width = width
		self.height = height
		self.clear()

	def clear(self):
		self.framebuffer = [
			[BLACK for x in range(self.width)]
			for y in range(self.height)
		]
		#print(self.framebuffer)

	#no se necesita nombre al escribir a memoria de video
	def write(self, filename):
		f = open(filename, 'bw')

		# pixel header
		f.write(char('B'))
		f.write(char('M'))

		# file size 
		f.write(dword(14 + 40 + self.width * self.height * 3))

		f.write(word(0))
		f.write(word(0))

		f.write(dword(14 + 40))

		# info header
		f.write(dword(40))
		f.write(dword(self.width))
		f.write(dword(self.height))
		f.write(word(1))
		# true color
		f.write(word(24))
		f.write(dword(0))
		f.write(dword(self.width * self.height * 3))
		f.write(dword(0))
		f.write(dword(0))
		f.write(dword(0))
		f.write(dword(0))

		# pixel data

		for x in range (self.height):
			for y in range(self.width):
				f.write(self.framebuffer[x][y])

		f.close()

	def point(self, x, y):
		if (0 < x < self.width and 0 < y < self.height):
			self.framebuffer[x][y] = WHITE

	def set_current_color(self, c):
		self.current_color = c


# gl init -> r = Render() por ejemplo, puede quedar vacio
'''
print(char('B'))
print(word(1))
print(dword(4))
print(dword(14 + 40 + 1024 * 1024 * 3))
print(color(234, 244, 2))
'''

class Obj(object):
	def __init__(self, filename):
		with open(filename) as f:
			#print(filename)
			self.lines = f.read().splitlines()
			self.vertices = []
			self.faces = []

			for line in self.lines:
				prefix, value = line.split(' ', 1)

				if prefix == 'v':
					self.vertices.append(list(map(float, value.split(' '))))
				if prefix == 'f':
					self.faces.append([
						list(map(int, face.split('/')))
							for face in value.split(' ')
					])
			#print(self.faces)


r = Render(300,300)

def line(p0, p1):
	for x in range(p0[0], p1[0]):
		for y in range(p0[1], p1[1]):
			if x == y:
				r.point(x, y)

def line2(p0, p1):
	'''
	x = x_0 + (p1[0] - p0[0]) * i
	y = y_0 + (p1[1] - p0[1]) * i
	i += 
	r.write(x, y)'''
	x0 = round(p0[0])
	x1 = round(p1[0])
	y0 = round(p0[1]) 
	y1 = round(p1[1])
	dy = abs(y1 - y0)
	dx = abs(x1 - x0)
	slope = dy

	# y = y0 + m * (x - x0)

	steep = dy > dx

	if steep:
		x0, y0 = y0, x0
		x1, y1 = y1, x1

	if x0 > x1:
		x0, x1 = x1, x0
		y0, y1 = y1, y0	

	dy = abs(y1 - y0)
	dx = abs(x1 - x0)

	offset = 0 * dx * 2
	threshold = dx

	y = y0
	for x in range(x0, x1 + 1):
		offset += dy * 2
		# y = y0 + round(offset)

		
		if steep:
			r.point(x, y)
		else:
			r.point(y, x)
		if offset >= threshold:
			y += 1 if y0 < y1 else -1
			threshold += 1 * dx * 2

#line2((20, 13), (40, 90))	
# line2((80, 40), (13, 20))

square = [
	(100, 100),
	(200, 100),
	(200, 200),
	(100, 200)
]

square_right = [
	(200, 100),
	(300, 100),
	(300, 200),
	(200, 200)
]

center = (150, 150)

square_large = [
	(
		((x-center[0]) * 1.5) + center[0], 
		((y-center[1]) * 0.5) + center[1]
	)
	for x, y in square
]

tsquare = square_large
last_point = tsquare[-1]
'''
for point in tsquare:
	line2(last_point, point)
	last_point = point
r.write('a.bmp')
'''
cube = Obj('cube.obj')
#print(cube.vertices)
# Obj propio archivo y transformacion dentro de render

def transform_vertex(vertex, scale, translate):
	return [
		(vertex[0] * scale[0]) + translate[0], 
			(vertex[1] * scale[1])	 + translate[1]
	]

scale_factor = (50, 50)
translate_factor = (150, 150)

for face in cube.faces:
	#print(face)
	f1 = face[0][0] - 1
	f2 = face[1][0] - 1
	f3 = face[2][0] - 1
	f4 = face[3][0] - 1

	v1 = transform_vertex(cube.vertices[f1], scale_factor, translate_factor)
	v2 = transform_vertex(cube.vertices[f2], scale_factor, translate_factor)
	v3 = transform_vertex(cube.vertices[f3], scale_factor, translate_factor)
	v4 = transform_vertex(cube.vertices[f4], scale_factor, translate_factor)

	#print(v1[0], v1[1], v2[0], v2[1])

	line2((v1[0], v1[1]), (v2[0], v2[1]))
	#line2((v2[0], v2[1]), (v3[0], v3[1]))
	#line2((v3[0], v3[1]), (v4[0], v4[1]))
	#line2((v4[0], v4[1]), (v1[0], v1[1]))
r.write('a.bmp')
'''
for x in range(0, 1024):
	for y in range(0, 1024):
		r.set_current_color(color(random.randint(0, 255), 100, 0))
		r.point(x, y)
r.write('a.bmp')
'''
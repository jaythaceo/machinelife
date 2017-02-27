import numpy as np
from PIL import Image
import math

epsilon = 1e-8

class Scene:
	def __init__(self, camera_position, camera_look_at, field_of_view=10.0, gamma=0.05, 
					focus=3.8, focal=7.5):
		self.objects = list()
		self.light_sources = list()
		self.ambient = RGB([100, 100, 100])
		self.gamma = gamma
		self.focus = focus
		self.focal = focal # High focal = better focus

		self.camera_position = np.array(camera_position)
		self.camera_look_at = np.array(camera_look_at)
		self.field_of_view = field_of_view

		self.camera_direction = self.camera_look_at - self.camera_position
		self.camera_direction = self.camera_direction / np.linalg.norm(self.camera_direction)

		### Temp: should be rotated not projected ###
		self.camera_up = np.cross(self.camera_direction, np.cross(np.array([0,0,1]), self.camera_direction))
		self.camera_up = self.camera_up / np.linalg.norm(self.camera_up)
		self.camera_right = np.cross(self.camera_direction, self.camera_up)
		#####

	def add_object(self, object):
		self.objects.append(object)

	def add_light(self, light):
		self.light_sources.append(light)

	def reflected_index(self, i, j, width, height):
		if i<0:
			i = -i
		if j<0:
			j = -j
		if i >= width:
			i = 2 * width - i - 1
		if j >= height:
			j = 2 * height - j - 1
		return (i,j)

	def DOF(self, pixels, Z, N=15, offset=5):
		inf = Z == -1
		m = np.max(Z)
		Z[inf] = m
		Z -= self.focus
		Z = 1.2 * N * np.abs(np.tanh(Z/self.focal))

		base = np.zeros((N,N))
		for x in xrange(N):
			for y in xrange(N):
				base[x,y] = (x-N/2)**2 + (y-N/2)**2

		width, height = Z.shape
		for x in xrange(width):
			print 'Depth of Field :', x/float(width) * 100, '%'
			for y in xrange(height):
				if Z[x,y] < offset:
					continue

				gauss = np.exp(-base/(Z[x,y]-offset))
				gauss /= np.sum(gauss)
				temp = [0]*3	


				for i in range(N):
					for j in xrange(N):
						for c in xrange(3):
							l, m = self.reflected_index(x + i - N/2, y + j - N/2, width, height)
							temp[c] += gauss[i,j] * pixels[l][m][c]

				pixels[x][y] = tuple(map(int,temp))

		return pixels
		

	def render(self, width=128, height=128, max_depth=2, DOF=True):
		pixels = [[0]*height for _ in xrange(width)]
		Z = np.zeros((width, height))
		for x in xrange(width):
			print 'Raytracing :', x/float(width) * 100, '%'
			for y in xrange(height):
				x_shift = (x - width/2.0)/width * self.field_of_view * self.camera_right
				y_shift = (y - height/2.0)/width * self.field_of_view * self.camera_up # normalized by width
				ray = Ray(origin=self.camera_position, direction=self.camera_look_at+x_shift+y_shift - self.camera_position)
				color, dist = self.trace(ray, max_depth=max_depth)
				pixels[x][y] = color.tuple
				Z[x][y] = dist

		# Depth of Field:
		if DOF:
			pixels = self.DOF(pixels, Z)

		img = Image.new("RGB",(width,height))
		for x in xrange(width):
			for y in xrange(height):
				img.putpixel((width - x - 1,height - y - 1), pixels[x][y])
		return img

	def find_ray_intersection(self, ray):
		smallest_distance = float('inf')
		first_intersection = None
		for obj in self.objects:
			intersection = obj.find_intersection(ray)
			if intersection.true_intersection and epsilon < intersection.distance < smallest_distance:
				first_intersection = intersection
				smallest_distance = intersection.distance
		return first_intersection

	def diffuse_to_light_sources(self, point, normal, obj):
		brightness = 0.0
		for light in self.light_sources:
			to_light = light.position - point
			ray = Ray(origin=point + epsilon*normal, direction=to_light)
			if self.find_ray_intersection(ray) == None:
				cosine = max([0, to_light.dot(normal) / (np.linalg.norm(to_light) * np.linalg.norm(normal))])
				intensity = 100 * light.intensity / sum(to_light**2)

				# Shading:
				brightness +=  intensity * cosine

				# Specular reflections:
				if obj.specular_level > 0:
					brightness += intensity * obj.specular_level * pow(cosine, obj.specular_falloff)

		return brightness + self.gamma

	def trace(self, ray, max_depth=2, depth=0):
		color = RGB([0.0, 0.0, 0.0])
		intersection = self.find_ray_intersection(ray)
		if intersection == None:
			return self.ambient, -1

		obj = intersection.object
		if depth == max_depth:
			return obj.color, 0

		refl_color = RGB([0, 0, 0])
		if obj.reflectivity > 0.0:
			reflected_ray_direction = ray.direction - \
					2 * intersection.normal * ray.direction.dot(intersection.normal)
			reflected_ray = Ray(intersection.point, reflected_ray_direction)
			refl_color, dummy = self.trace(reflected_ray, max_depth, depth+1)

		brightness = self.diffuse_to_light_sources(intersection.point, intersection.normal, intersection.object)
		return (refl_color * obj.reflectivity + obj.color * (1.0 - obj.reflectivity)) * brightness, intersection.distance

class RGB:
	def __init__(self, color):
		self.color = [0,0,0]
		for i in range(3):
			self.__setitem__(i, color[i])

	def __setitem__(self, i, value):
		self.color[i] = int(value)
		if self.color[i] < 0:
			self.color[i] = 0
		elif self.color[i] > 255:
			self.color[i] = 255

	def __getitem__(self, i):
		return self.color[i]

	def __add__(self, other):
		out = RGB([0,0,0])
		for i in range(3):
			out[i] = self[i] + other[i]
		return out

	def __mul__(self, other):
		out = RGB([0,0,0])
		for i in range(3):
			out[i] = other * self[i]
		return out

	def norm(self):
		return np.array(self.color) / np.linalg.norm(self.color)

	@property
	def tuple(self):
		return tuple(self.color)

class Plane:
	def __init__(self, center, normal, color):
		self.center = np.array(center)
		self.normal = np.array(normal)
		self.color = RGB(color)
		self.reflectivity = 0.3
		self.name = 'plane'
		self.specular_level = 0
		self.specular_falloff = 1

	def find_intersection(self, ray):
		dot = self.normal.dot(ray.direction)
		if dot == 0.0:
			return Intersection()
		else:
			inter = Intersection()
			inter.distance = (self.center - ray.origin).dot(self.normal)/dot
			if inter.distance < 0:
				return inter
			inter.point = ray.origin + inter.distance * ray.direction
			inter.normal = self.normal
			inter.object = self
			inter.true_intersection = True
			return inter

class Sphere:
	def __init__(self, center, radius, color):
		self.center = np.array(center)
		self.radius = radius
		self.color = RGB(color)
		self.reflectivity = 0.5
		self.name = 'sphere'
		self.specular_level = 2
		self.specular_falloff = 500

	def find_intersection(self, ray):
		l = ray.direction
		o = ray.origin
		c = self.center
		pre = l.dot(o - c)
		discriminant = pre**2 - l.dot(l) * ( (o-c).dot(o-c) - self.radius**2 )
		if discriminant <= 0: # fuck the edge
			return Intersection()
		else:
			discriminant = np.sqrt(discriminant)
			dist1 = -pre + discriminant
			dist2 = -pre - discriminant
			inter = Intersection()

			if dist1 <= 0:
				if dist2 <=0:
					return inter
				else:
					dist = dist2
			elif dist2 <= 0:
				dist = dist1
			else:
				dist = min([dist1, dist2])

			inter.object = self
			inter.distance = dist / l.dot(l)
			inter.point = o + l*inter.distance
			inter.normal = inter.point - c
			inter.normal = inter.normal / np.linalg.norm(inter.normal)
			inter.true_intersection = True
			return inter

class OmniLight:
	def __init__(self, position, intensity):
		self.position = position
		self.intensity = intensity

class Ray:
	def __init__(self, origin, direction):
		self.origin = np.array(origin)
		self.direction = np.array(direction / np.linalg.norm(direction))

class Intersection( object ):
	def __init__(self):
		self.point = np.array([0.0, 0.0, 0.0])
		self.distace = 0
		self.normal = np.array([0.0, 0.0, 0.0])
		self.object = None
		self.true_intersection = False

if __name__ == "__main__":
	scene = Scene((0.0, 0.0, 1.0), (1.0, 0.0, 1.0), field_of_view=1.0, 
					gamma=0.65, focus=9.5, focal=2.0)
	scene.ambient = RGB((105, 205, 255))

	floor = Plane((0.0, 0.0, 0.0), (0.0, 0.0, 1.0), color=(200, 200, 175))
	scene.add_object(floor)


	scene.add_object(Sphere((10, -0.5, 1.5), 1.5, color=(50, 190, 25)))
	
	scene.add_object(Sphere((12, -4.8, 2.15), 2.15, color=(255,128,0)))
	scene.add_object(Sphere((5.5, -2.6, 0.83), 0.83, color=(255,128,0)))
	scene.add_object(Sphere((6.6, 1, 0.5), 0.5, color=(255,128,0)))
	scene.add_object(Sphere((8.5, 2.2, 0.5), 0.5, color=(255,128,0)))
	scene.add_object(Sphere((4.6, 2.15, 0.9), 0.9, color=(255,128,0)))


	scene.add_light( OmniLight((6.5, -10.0, 5.0), 1.6) )

	img = scene.render(1024, 768, max_depth=3, DOF=True) # choose width, height (ie. quality) here
	img.save("rendered.bmp")
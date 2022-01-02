from IX import IX, getIdx

from physics import Physics
from constants import SIZE
from profile import profile
import numpy as np

class Container:

	def __init__ (self, dt, diff, visc):

		self.size = SIZE
		self.dt = dt
		self.diff = diff
		self.visc = visc

		self.px = self.InitArr(self.size)
		self.py = self.InitArr(self.size)
		self.x = self.InitArr(self.size)
		self.y = self.InitArr(self.size)
		self.previousDensity = self.InitArr(self.size)
		self.density = self.InitArr(self.size)
		self.physics = Physics()


	# def InitArr(self, size):
	# 	arr = []
	# 	for i in range(0,size+1,1):
	# 		arr.append(0)

	# 	return arr

	def InitArr(self, size):
		dictionary = {}

		for i in range(0,size+1,1):
			subdict = {}
			for j in range(0,size+1,1):
				subdict[j] = 0
			dictionary[i] = subdict
		return dictionary

	def AddDensity(self, x, y, amount):
		self.density[x][y] += amount
		# self.density[getIdx(x, y)] += amount


	def AddVelocity(self, x, y, px, py):
		idx = getIdx(x, y)

		# self.x[idx] += px
		# self.y[idx] += py
		self.x[x][y] += px
		self.y[x][y] += py


	def Step(self):
		self.physics.Diffuse(1, self.px, self.x, self.visc, self.dt, 16, self.size)
		self.physics.Diffuse(2, self.py, self.y, self.visc, self.dt, 16, self.size)
		self.physics.Diffuse(2, self.py, self.y, self.visc, self.dt, 16, self.size)

		self.physics.Project(self.px, self.py, self.x, self.y, 16, self.size)

		self.physics.Advect(1, self.x, self.px, self.px, self.py, self.dt, self.size)
		self.physics.Advect(1, self.y, self.py, self.px, self.py, self.dt, self.size)

		self.physics.Project(self.x, self.y, self.px, self.py, 16, self.size)

		self.physics.Diffuse(0, self.previousDensity, self.density, self.diff, self.dt, 16, self.size);	
		self.physics.Advect(0, self.density, self.previousDensity, self.x, self.y, self.dt, self.size);
		

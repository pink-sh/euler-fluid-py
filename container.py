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


	def InitArr(self, size):
		dictionary = {}

		for i in range(0,size+1,1):
			subdict = {}
			for j in range(0,size+1,1):
				subdict[j] = 0
			dictionary[i] = subdict
		return dictionary

	def AddDensity(self, x, y, amount):
		print("Adding density", amount, "to", x,y)
		self.density[x][y] += amount

	def FadeDensity(self, size):
		for i in range(0,size,1):
			for j in range(0,size,1):
				d = self.density[i][j]
				self.density[i][j] = 0 if (d - 0.05) < 0 else (d - 0.05)


	def AddVelocity(self, x, y, px, py):
		try:
			self.x[x][y] += px
			self.y[x][y] += py
		except:
			m = 0


	def Step(self):
		iterations = 8
		self.physics.Diffuse(1, self.px, self.x, self.visc, self.dt, iterations, self.size)
		self.physics.Diffuse(2, self.py, self.y, self.visc, self.dt, iterations, self.size)
		self.physics.Diffuse(2, self.py, self.y, self.visc, self.dt, iterations, self.size)

		self.physics.Project(self.px, self.py, self.x, self.y, iterations, self.size)

		self.physics.Advect(1, self.x, self.px, self.px, self.py, self.dt, self.size)
		self.physics.Advect(1, self.y, self.py, self.px, self.py, self.dt, self.size)

		self.physics.Project(self.x, self.y, self.px, self.py, iterations, self.size)

		self.physics.Diffuse(0, self.previousDensity, self.density, self.diff, self.dt, iterations, self.size);	
		self.physics.Advect(0, self.density, self.previousDensity, self.x, self.y, self.dt, self.size);
		

from IX import IX
from constants import SIZE

class FluidCube:

	def __init__(self, size, diffusion, viscosity, dt):
		self.size = size
		self.dt = dt
		self.diff = diffusion
		self.visc = viscosity

		self.s = []
		self.density = []
		self.Vx = []
		self.Vy = []
		self.Vz = []

		self.Vx0 = []
		self.Vy0 = []
		self.Vz0 = []


	def addDensity(x, y, z, amount):
		self.density[IX(x,y,z)] = self.density[IX(x,y,z)] + amount


	def addVelocity(x, y, z, amountX, amountY, amountZ):
		idx = IX(x,y,z)
		self.Vx[index] = self.Vx[index] + amountX
		self.Vy[index] = self.Vy[index] + amountY
		self.Vz[index] = self.Vz[index] + amountZ

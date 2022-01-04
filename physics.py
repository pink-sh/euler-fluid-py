from IX import IX, getIdx
import math
from constants import SIZE


class Physics:

	def SetBnd(self, b, x, N):
		for i in range(1,N-1,1):
			x[i][0] = -x[i][1] if b == 2 else x[i][1]
			x[i][N-1] = -x[i][N] if b == 2 else x[i][N];
		for j in range(1,N-1,1):
			x[0][j] = -x[1][j] if b == 1 else x[1][j]
			x[N-1][j] = -x[N-2][j] if b == 1 else x[N-2][j]


		x[0][0] = 0.33 * (x[1][0] + x[0][1] + x[0][0])
		x[0][N-1] = 0.33 * (x[1][N-1] + x[0][N-2] + x[0][N-1])
		x[N-1][0] = 0.33 * (x[N-2][0] + x[N-1][1] + x[N-1][0])

		x[N-1][N-1] = 0.33 * (x[N-2][N-1] + x[N-1][N-2] + x[N-1][N-1])


	def LinSolve(self, b, x, x0, a, c, iter, N):
		cRecip = 1.0 / c

		for k in range(0,iter-1,1):
			for j in range (1,N-2,1):
				for i in range(1,N-2,1):
					x[i][j] = (x0[i][j] + a *(x[i+1][j] + x[i-1][j] + x[i][j+1] + x[i][j-1] + x[i][j] + x[i][j] )) * cRecip
			self.SetBnd(b, x, N)


	def Diffuse(self, b, x, x0, diff, dt, iter, N):
		a = dt * diff * (N - 2) * (N - 2)
		self.LinSolve(b, x, x0, a, 1 + 6 * a, iter, N)



	def Project(self, vx, vy, p, div, iter, N):
		for j in range(1, N-2, 1):
			for i in range(1, N-2, 1):
				div[i][j] = -0.5 * ( vx[i+1][j] - vx[i-1][j] + vy[i][j+1] - vy[i][j-1] ) / N
				p[i][j] = 0

		self.SetBnd(0, div, N)
		self.SetBnd(0, p, N)
		self.LinSolve(0, p, div, 1, 6, iter, N)

		for j in range(1, N-2, 1):
			for i in range(1, N-2, 1):
				vx[i][j] -= 0.5 * (p[i+1][j] - p[i-1][j]) * N
				vy[i][j] -= 0.5 * (p[i][j+1] -p[i][j-1]) * N

		self.SetBnd(1, vx, N)
		self.SetBnd(2, vy, N)

	def Advect(self, b, d, d0, vx, vy, dt, N):
		Nfloat = N

		dtx = dt * (N - 2);
		dty = dt * (N - 2);

		jfloat = 1
		for j in range(1, N-2, 1):
			ifloat = 1
			for i in range(1, N-2, 1):
				tmp1 = dtx * vx[i][j]
				tmp2 = dty * vy[i][j]
				x = ifloat - tmp1
				y = jfloat - tmp2
                
				if (x < 0.5): 
					x = 0.5
				if (x > Nfloat + 0.5):
					x = Nfloat + 0.5

				i0 = math.floor(x)
				i1 = i0 + 1.0

				if (y < 0.5):
					y = 0.5
				if (y > Nfloat + 0.5):
					y = Nfloat + 0.5

				j0 = math.floor(y)
				j1 = j0 + 1.0;

				s1 = x - i0
				s0 = 1.0 - s1
				t1 = y - j0
				t0 = 1.0 - t1
                
				i0i = SIZE if SIZE < int(i0) else int(i0)
				i1i = SIZE if SIZE < int(i1) else int(i1)
				j0i = SIZE if SIZE < int(j0) else int(j0)
				j1i = SIZE if SIZE < int(j1) else int(j1)
                
				try:
					d[i][j] =  s0 * \
					(t0 * d0[i0i][j0i] + \
					t1 * \
					d0[i0i][j1i]) + \
					s1 * \
					(t0 * \
					d0[i1i][j0i] + \
						t1 * \
						d0[i1i][j1i])

				except:
					print(i1i, j0i)

				ifloat = ifloat + 1

			jfloat = jfloat + 1

		self.SetBnd(b, d, N)
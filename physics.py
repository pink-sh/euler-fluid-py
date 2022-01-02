from IX import IX, getIdx
import math

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


	# def SetBnd(self, b, x, N):
	# 	for i in range(1,N-1,1):
	# 		x[IX(i, 0, N)] = -x[IX(i, 1, N)] if b == 2 else x[IX(i, 1, N)]
	# 		x[IX(i, N-1, N)] = -x[IX(i, N-2, N)] if b == 2 else x[IX(i, N-2, N)];
	# 	for j in range(1,N-1,1):
	# 		x[IX(0, j, N)] = -x[IX(1, j, N)] if b == 1 else x[IX(1, j, N)]
	# 		x[IX(N-1, j, N)] = -x[IX(N-2, j, N)] if b == 1 else x[IX(N-2, j, N)]


	# 	x[IX(0, 0, N)] = 0.33 * (x[IX(1, 0, N)] + x[IX(0, 1, N)] + x[IX(0, 0, N)])
	# 	x[IX(0, N-1, N)] = 0.33 * (x[IX(1, N-1, N)] + x[IX(0, N-2, N)] + x[IX(0, N-1, N)])
	# 	x[IX(N-1, 0, N)] = 0.33 * (x[IX(N-2, 0, N)] + x[IX(N-1, 1, N)] + x[IX(N-1, 0, N)])

	# 	x[IX(N-1, N-1, N)] = 0.33 * (x[IX(N-2, N-1, N)] + x[IX(N-1, N-2, N)] + x[IX(N-1, N-1, N)])





	def LinSolve(self, b, x, x0, a, c, iter, N):
		cRecip = 1.0 / c

		for k in range(0,iter-1,1):
			for j in range (1,N-2,1):
				for i in range(1,N-2,1):
					x[i][j] = (x0[i][j] + a *(x[i+1][j] + x[i-1][j] + x[i][j+1] + x[i][j-1] + x[i][j] + x[i][j] )) * cRecip
			self.SetBnd(b, x, N)

	# def LinSolve(self, b, x, x0, a, c, iter, N):
	# 	cRecip = 1.0 / c

	# 	for k in range(0,iter-1,1):
	# 		for j in range (1,N-2,1):
	# 			for i in range(1,N-2,1):
	# 				x[IX(i, j, N)] = (x0[IX(i, j, N)] + a *(x[IX(i+1, j, N)] + x[IX(i-1, j, N)] + x[IX(i, j+1, N)] + x[IX(i, j-1, N)] + x[IX(i, j, N)] + x[IX(i, j, N)] )) * cRecip
	# 		self.SetBnd(b, x, N)


	# def LinSolve(self, b, x, x0, a, c, iter, N):
	# 	return


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

	# def Project(self, vx, vy, p, div, iter, N):
	# 	for j in range(1, N-2, 1):
	# 		for i in range(1, N-2, 1):
	# 			div[IX(i, j, N)] = -0.5 * ( vx[IX(i+1, j, N)] - vx[IX(i-1, j, N)] + vy[IX(i, j+1, N)] - vy[IX(i, j-1, N)] ) / N
	# 			p[IX(i, j, N)] = 0

	# 	self.SetBnd(0, div, N)
	# 	self.SetBnd(0, p, N)
	# 	self.LinSolve(0, p, div, 1, 6, iter, N)

	# 	for j in range(1, N-2, 1):
	# 		for i in range(1, N-2, 1):
	# 			vx[IX(i, j, N)] -= 0.5 * (p[IX(i+1, j, N)] - p[IX(i-1, j, N)]) * N
	# 			vy[IX(i, j, N)] -= 0.5 * (p[IX(i, j+1, N)] -p[IX(i, j-1, N)]) * N

	# 	self.SetBnd(1, vx, N)
	# 	self.SetBnd(2, vy, N)





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
                
				i0i = i0;
				i1i = i1;
				j0i = j0;
				j1i = j1;
                
				d[i][j] =  s0 * (t0 * d0[int(i0i)][int(j0i)] + t1 * d0[int(i0i)][int(j1i)]) + s1 * (t0 * d0[int(i1i)][int(j0i)] + t1 * d0[int(i1i)][int(j1i)])

				ifloat = ifloat + 1

			jfloat = jfloat + 1

		self.SetBnd(b, d, N)



	# def Advect(self, b, d, d0, vx, vy, dt, N):
	# 	Nfloat = N

	# 	dtx = dt * (N - 2);
	# 	dty = dt * (N - 2);

	# 	jfloat = 1
	# 	for j in range(1, N-2, 1):
	# 		ifloat = 1
	# 		for i in range(1, N-2, 1):
	# 			tmp1 = dtx * vx[IX(i, j, N)]
	# 			tmp2 = dty * vy[IX(i, j, N)]
	# 			x = ifloat - tmp1
	# 			y = jfloat - tmp2
                
	# 			if (x < 0.5): 
	# 				x = 0.5
	# 			if (x > Nfloat + 0.5):
	# 				x = Nfloat + 0.5

	# 			i0 = math.floor(x)
	# 			i1 = i0 + 1.0

	# 			if (y < 0.5):
	# 				y = 0.5
	# 			if (y > Nfloat + 0.5):
	# 				y = Nfloat + 0.5

	# 			j0 = math.floor(y)
	# 			j1 = j0 + 1.0;

	# 			s1 = x - i0
	# 			s0 = 1.0 - s1
	# 			t1 = y - j0
	# 			t0 = 1.0 - t1
                
	# 			i0i = i0;
	# 			i1i = i1;
	# 			j0i = j0;
	# 			j1i = j1;
                
	# 			d[IX(i, j, N)] =  s0 * (t0 * d0[IX(i0i, j0i, N)] + t1 * d0[IX(i0i, j1i, N)]) + s1 * (t0 * d0[IX(i1i, j0i, N)] + t1 * d0[IX(i1i, j1i, N)])

	# 			ifloat = ifloat + 1

	# 		jfloat = jfloat + 1

	# 	self.SetBnd(b, d, N)
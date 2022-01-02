import math

def IX(x, y, N):
	if (x < 0):
		x=0
	if  (x > N-1):
		x=N-1
	if (y < 0):
		y=0
	if (y > N-1):
		y=N-1
	# retVal = math.floor(((y*N)+x)-1)
	retVal = math.floor(((y*N)+x)-1)
	# print("IX returning (", x,y,N, ")", retVal)
	return retVal


def IXX(x,y,N,SIZE):
	xNorm = int(x/N)*SIZE
	yNorm = int(y/N)
	retVal = xNorm+yNorm
	print("IXX returning (", x,y,N,SIZE, ")", retVal)
	return retVal

def getIdx(x, y):
	idx = str(int(x)) + "_" + str(int(y))
	return idx


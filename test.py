import numpy as np



arr = np.full((5,5), 2)

def f(x):
	x = x +  1
	return x

ff = np.vectorize(f)

arr2 = ff(arr)

print (arr)

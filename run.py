import numpy as np

def test(size):
	# x = np.array([0 for col in range(size)] for row in range(size))
	x = np.zeros((size,size), dtype=int)
	print (x)



if __name__ == '__main__':
	test(100)
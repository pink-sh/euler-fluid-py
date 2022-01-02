import time

def profile(func, *args):
	now = round(time.time() * 1000)
	func(*args)
	print("Function took ", round(time.time() * 1000) - now)

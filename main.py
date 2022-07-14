def mul(x, y):
	return x*y

def mul(x, y):
	return x*y

def sum(x, y):
	return x+y
	

def sub(x, y):
	return x-y

def swapBytes(x):
	# 0x AA BB CC DD -> DD CC BB AA
	# 1 byte is shift of 8
	y1 = (x << 24) & 0xFF000000
	y2 = (x << 8) & 0x00FF0000
	y3 = (x >> 8) & 0x0000FF00
	y4 = (x >> 24) & 0x000000FF
	y = y1 | y2 | y3 | y4
	return y
# adding a comment here for test :)
def main():
	x = 0xAABBCCDD
	print("Little Endian: 0x%.8X" % x)
	x = swapBytes(x)
	print("   Big Endian: 0x%.8X" % x)
	return

if __name__ == "__main__":
	main()
def swapBytes(x):
	# 0x AA BB CC DD -> DD CC BB AA
	# 1 byte is shift of 8
	y1 = (x << 24) & 0xFF000000
	y2 = (x << 8) & 0x00FF0000
	y3 = (x >> 8) & 0x0000FF00
	y4 = (x >> 24) & 0x000000FF
	y = y1 | y2 | y3 | y4
	return y

def main():
	x = 0xAABBCCDD
	print("%.8x" % x)
	x = swapBytes(x)
	print("%.8x" % x)
	return

if __name__ == "__main__":
	main()
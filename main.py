def readInt(addr):
	return 0

# Motion Binary Class
class MOTA:
	def __int__(self, start, end):
		self.start_addr = start
		self.end_addr = end
		self.num_of_anims = readInt(start+16)
		
		return

def swapBytes(x):
	# 0x AA BB CC DD -> DD CC BB AA
	# 1 byte is shift of 8
	# y1 = (x << 24) & 0xFF000000
	# y2 = (x << 8) & 0x00FF0000
	# y3 = (x >> 8) & 0x0000FF00
	# y4 = (x >> 24) & 0x000000FF
	y = (x << 24) & 0xFF000000 | (x << 8) & 0x00FF0000 | (x >> 8) & 0x0000FF00 | (x >> 24) & 0x000000FF
	return y

# adding a comment here for test :)
def main():
	x = 0x80ED
	print("Little Endian: 0x%.8X" % x)
	x = swapBytes(x)
	print("   Big Endian: 0x%.8X" % x)
	return

if __name__ == "__main__":
	main()
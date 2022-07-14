def readInt(addr, endian):
	return 0

class ANIM:
	def __int__(self):
		self.type = 0
		self.bones = 0
		self.descriptors = []
		self.bytes = []
		return


class ANIM_0xC8(ANIM):
	def __int__(self):
		return

class ANIM_0x64(ANIM):
	def __int__(self):
		return
		

# Just Practising
# Motion Binary Class
class MOTA:
	def __int__(self, start, end):
		self.start_addr = start
		self.end_addr = end
		self.num_of_anims = readInt(start+16)
		self.endian = "little" if readInt(start+4) == 1 else "big"
		self.headers = [None] * self.num_of_anims
		self.readHeaders()
		return
	
	def readHeaders(self):
		start = self.start_addr
		for i in range(self.num_of_anims):
			self.headers[i] = readInt(start + 20 + i * 4) + start
		return

	def readAnims(self):
		
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
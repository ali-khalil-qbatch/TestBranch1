from binreader import BinaryReader

class MOTA:
	# Attribute: parent is either binary file reader
	# Or Process handle attached to the game
	def __init__(self, start, end, parent):
		self.start_addr = start
		self.end_addr = end
		self.parent = parent
		self.header = parent.readString(0, 4)
		self.endian = self.checkEndian()
		self.anims = parent.readUInt32(12, self.endian)
		self.animHeaders = []
		self.animBytes = []
		self.readHeaders()
		self.readAnims()
		# print('all read')
	
	def getHeader(self):
		return self.header

	def getAnimHeaders(self):
		return self.animHeaders

	def checkEndian(self):
		endian_bytes = self.parent.readInt(4)
		return "big" if endian_bytes == 256 else "little"

	def readHeaders(self):
		start = self.start_addr
		for i in range(self.anims):
			self.animHeaders.append(self.parent.readInt(20 + i * 4, self.endian) + start)
		return

	def readAnims(self):
		start = 0
		end = 0
		for i in range(self.anims):
			start = self.animHeaders[i]
			try:
				end = self.animHeaders[i+1]
			except Exception:
				end = self.end_addr
			self.readAnim(start)
			
	# temporary functions
	def readAnim(self, addr):
		signatureByte = self.parent.readShort(addr, self.endian)
		if signatureByte == 0x64:
			self.readAnim_64(addr)
		elif signatureByte == 0xC8:
			self.readAnim_C8(addr)

	def readAnim_64(self, addr):
		bones = self.parent.readShort(addr+2, self.endian)
		desc = [0] * bones
		for i in range(bones):
			temp = addr + 4 + i * 2
			desc[i] = self.parent.readShort(temp, self.endian)
		frames = self.parent.readShort(temp+2, self.endian)

		# Printing
		str = "0x64. Bones: %-3d Frames: %-5d Descriptors: " % (bones, frames)
		for i in range(bones):
			str += "%-3d " % desc[i]
		self.animBytes.append(str)
		return

	def readAnim_C8(self, addr):
		bones = self.parent.readShort(addr+2, self.endian)
		frames = self.parent.readInt(addr+4, self.endian)
		desc = [0] * bones
		for i in range(bones):
			temp = addr + 8 + i * 4
			desc[i] = self.parent.readShort(temp, self.endian)
		
		# Printing
		str = "0xC8. Bones: %-3d Frames: %-10d Descriptors: " % (bones, frames)
		for i in range(bones):
			str += "%-3d " % desc[i]
		self.animBytes.append(str)

		return
	
	def print(self):
		print(self.header)
		print("Endian Order:", self.endian)
		print("Animations: %d" % self.anims)
		print("Animation Headers")
		for i in range(self.anims):
			print("%-3d = 0x%.8x = %-10d: %s" % (i, self.animHeaders[i], self.animHeaders[i], self.animBytes[i]))

# END OF CLASS
	

def main():
	br = BinaryReader("mota_5.bin", True)
	if not br.isOpen():
		print("File Not Found")
		return
	mota = MOTA(0, br.getFileSize()-1, br)
	br.closeFile()
	mota.print()
	return

if __name__ == "__main__":
	main()
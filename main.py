from base64 import decode
import os
import struct

# File Descriptor
fd = None

def mergeTwo(x, y):
    # x = 0x00C8
    # y = 0x0004
    # z = 
    z = (x << 16) & 0xFFFF0000 | y & 0x0000FFFF
    return z

def swapBytesInt16(x):
    y = (x << 8) & 0xFF00 | (x >> 8) & 0x00FF
    return y


def swapBytesInt32(x):
    y = (x << 24) & 0xFF000000 | (x << 8) & 0x00FF0000 | (
        x >> 8) & 0x0000FF00 | (x >> 24) & 0x000000FF
    return y


def read(addr=None, base=0, size=4, endian='little'):
    original_position = fd.tell()
    if size != 2 and size != 4 and size != 8:
        raise
    if addr == None:
        addr = original_position
    fd.seek(addr+base)
    try:
        val = int.from_bytes(fd.read(size), endian)
    except Exception: # raise Exception
        val = None
    fd.seek(original_position)
    return val


def readShort(addr=None, endian='little', base=0):
    return read(addr, base, 2, endian)


def readInt(addr=None, endian='little', base=0):
    return read(addr, base, 4, endian)


def readLong(addr=None, endian='little', base=0):
    return read(addr, base, 8, endian)


def readFloat(addr=None, endian='little', base=0):
    original_position = fd.tell()
    if addr == None:
        addr = original_position
    fd.seek(addr+base)
    str = '>f' if endian == 'big' else '<f'
    try:
        val = struct.unpack(str, fd.read(4))[0]
    except Exception:
        val = None
    fd.seek(original_position)
    return val


def readBytes(addr, bytes_length):
    fd.seek(addr)
    return fd.read(bytes_length)


def readString(addr):
    offset = 0
    while readInt(addr + offset, 1) != 0:
        offset += 1
    return readBytes(addr, offset).decode("ascii")


class ANIM:
    def __init__(self, start, end, endian="little"):
        self.start_addr = start
        self.end_addr = end
        self.endian = endian
        self.type = 0
        self.bones = 0
        self.frames = 0
        self.descriptors = []
        self.bytes = []
        return

    def readData(self):
        self.type = readInt(self.start_addr)
        self.bones = readInt(self.start_addr+2)
        return

    def print(self):
        print("PARENT PRINT")
        return


class ANIM_0xC8(ANIM):
    def __init__(self, start, end, endian="little"):
        super().__init__(start, end, endian)
        self.readData()
        return

    def readData(self):
        self.type = readShort(self.start_addr, self.endian)
        self.bones = readShort(self.start_addr+2, self.endian)
        self.frames = readInt(self.start_addr+4, self.endian)

        for i in range(self.bones):
            self.descriptors.append(readInt(self.start_addr + 8 + i * 4, self.endian))

        # addr = self.start_addr + self.bones * 4 + 8
        # i = 0
        # while (addr < self.end_addr):
        #     self.bytes.append(readFloat(addr, self.endian))
        #     i += 1
        #     addr += 4
        return

    def print(self):
        x = mergeTwo(self.type, self.bones)
        print("%.8x" % x)
        print("%.8x" % self.frames)
        for i in range(self.bones):
            x = self.descriptors[i]
            print("%.8x" % x)
        return


class ANIM_0x64(ANIM):
    def __int__(self, start, end, endian="little"):
        super().__init__(self, start, end, endian)
        self.readData()
        return

    def readData(self):
        self.type = readShort(self.start_addr, self.endian)
        self.bones = readShort(self.start_addr+2, self.endian)

        for i in range(self.bones):
            self.descriptors.append(readInt(self.start_addr + 4 + i * 4, self.endian))

        self.frames = self.start_addr + self.bones * 4 + 4

        addr = self.start_addr + self.bones * 2 + 4
        # i = 0
        # while (addr < self.end_addr):
        #     self.bytes.append(readFloat(addr, self.endian))
        #     i += 1
        #     addr += 4
        return

    def print(self):
        x = mergeTwo(self.type, self.bones)
        print("%.8x" % x)
        return


# Just Practising
# Motion Binary Class
class MOTA:
    def __init__(self, start, end):
        self.start_addr = start
        self.end_addr = end
        self.header = fd.read(4).decode('ascii')
        self.endian = self.checkEndian()
        self.num_of_anims = readInt(addr=start+12, endian=self.endian)
        self.headers = [None] * self.num_of_anims
        self.anims = [None] * self.num_of_anims
        self.readHeaders()
        self.readAnims()
        return

    def header(self):
        return self.header

    def print(self):
        print(self.header)
        print("Endian Order:", self.endian)
        print("Animations: %d" % self.num_of_anims)
        print("Animation Headers")
        for i in range(self.num_of_anims):
            print("%-3d = 0x%.8x = %d" % (i, self.headers[i], self.headers[i]))

        for i in range(self.num_of_anims):
            if isinstance(self.anims[i], ANIM_0xC8):
                self.anims[i].print()
        return

    def checkEndian(self):
        endian_bytes = readInt(addr=4)
        return "big" if endian_bytes == 256 else "little"

    def readHeaders(self):
        start = self.start_addr
        for i in range(self.num_of_anims):
            self.headers[i] = readInt(20 + i * 4, endian=self.endian) + start
        return

    def readAnims(self):
        start = 0
        end = 0
        for i in range(self.num_of_anims):
            start = self.headers[i]
            try:
                end = self.headers[i+1]
            except Exception:
                end = self.end_addr
            signatureByte = readShort(start)
            if signatureByte == 0xC8:
                self.anims[i] = ANIM_0xC8(start, end, self.endian)
                self.anims[i].readData()
            elif signatureByte == 0x64:
                self.anims[i] = ANIM_0x64(start, end, self.endian)
                self.anims[i].readData()
            else:
                print("Invalid Anim Byte for anim # %d. Skipping this" % (i+1))
                self.anims[i] = None
        return

# adding a comment here for test :)


def main():
    # x = 0x00C8
    # y = 0x0004
    # z = mergeTwo(x, y)
    # print("0x%.8x" % z)
    # x = 0x80ED
    # print("Little Endian: 0x%.4X" % x)
    # x = swapBytesInt16(x)
    # print("   Big Endian: 0x%.4X" % x)
    global fd
    filename = "mota_9.bin"
    fd = open(filename, 'rb')
    if fd == None:
        print(f'Unable to open {filename}. Program closed.')
        return
    size = os.path.getsize(filename)
    # print(size)

    pathname, extension = os.path.splitext(filename)
    org_name = pathname.split('/')[-1]
    mota_file = MOTA(fd.tell(), size)
    mota_file.print()
    fd.close()
    return


if __name__ == "__main__":
    main()

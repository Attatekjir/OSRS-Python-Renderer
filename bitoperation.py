import numpy as np
from numba import jit
from MathUtills import nextPowerOfTwo, unsignedrshift
from MathUtills import integerdivide

@jit(nopython=True, cache=True)
def readUnsignedByte(buffer, index):
    out = buffer[index] & 255
    return out, index + 1

@jit(nopython=True, cache=True)
def readByte(buffer, index):
    out = buffer[index]
    return out, index + 1

@jit(nopython=True, cache=True)
def readStringIntParameters(buffer, index, hashTable):

    # We are not using the results of this operation. Just running it to clear the buffer

    var2, index = readUnsignedByte(buffer, index)
    if(hashTable == None):
        var3 = nextPowerOfTwo(var2)
        # new IterableHashTable(var3)
        hashTable = "SpoofReadStringIntParametersSpoof"

    for var3 in range(0, var2):
        var9999, index = readUnsignedByte(buffer, index)
        var4 = var9999 == 1
        var5, index = read24BitInt(buffer, index)
        if(var4):
            # new ObjectNode(buffer.readString())
            var6, index = readString(buffer, index)
        else:
            # new IntegerNode(buffer.readInt())
            var6, index = readInt(buffer, index)

    return hashTable

@jit(nopython=True, cache=True)
def putInt(buffer, index, var1):
    buffer[index] = np.byte(var1 >> 24)
    index += 1
    buffer[index] = np.byte(var1 >> 16)
    index += 1
    buffer[index] = np.byte(var1 >> 8)
    index += 1
    buffer[index] = np.byte(var1)
    index += 1
    return index

@jit(nopython=True, cache=True)
def readUnsignedShort(buffer, index):
    index += 2
    out = ((buffer[index - 2] & 255) << 8) + (buffer[index - 1] & 255)
    return out, index

@jit(nopython=True, cache=True)
def readShort(buffer, index):
    index += 2
    var1 = (buffer[index - 1] & 255) + ((buffer[index - 2] & 255) << 8)
    if(var1 > 32767):
        var1 -= 65536

    return var1, index

@jit(nopython=True, cache=True)
def read24BitInt(buffer, index):
    index += 3
    out = ((buffer[index - 3] & 255) << 16) + \
        (buffer[index - 1] & 255) + ((buffer[index - 2] & 255) << 8)
    return out, index

@jit(nopython=True, cache=True)
def readInt(buffer, index):
    index += 4
    out = np.int32(((buffer[index - 3] & 255) << 16) + (buffer[index - 1] & 255) +
                   ((buffer[index - 2] & 255) << 8) + ((buffer[index - 4] & 255) << 24))
    return out, index

@jit(nopython=True, cache=True)
def readUnsignedByteAsBool(buffer, index):

    var1, index = readUnsignedByte(buffer, index)
    out = (var1  & 1) == 1

    return out, index

@jit(nopython=True, cache=True)
def readString(buffer, index):
    result = ""

    while (True):

        ch, index = readUnsignedByte(buffer, index)
        if ch == 0:
            break

        if (ch >= 128 and ch < 160):
            #var7 = CHARACTERS[ch - 128]
            # if (var7 == 0):
            #ch = '?'
            result += chr(ch)
        else:
            result += chr(ch)

    return result, index

@jit(nopython=True, cache=True)
def readBytes(buffer, index, var2, var3):

    out = buffer[index + var2: index + var2 + var3]
    # for var4 in range(var2, var3 + var2):
    #     var1[var4] = buffer[index]
    #     index += 1

    index += var3

    return out, index

@jit(nopython=True, cache=True)
def getLength(buffer):
    return len(buffer)

@jit(nopython=True, cache=True)
def readShortSmart(buffer, index):

    # Peak first...
    var1 = np.int32(buffer[index] & 0xFF)

    if var1 < 128:
        result, index = readUnsignedByte(buffer, index)
        result -= 64
    else:
        result, index = readUnsignedShort(buffer, index)
        result -= 0xc000

    return result, index

@jit(nopython=True, cache=True)
def getUSmart(buffer, index):

    # Peek first
    var1 = buffer[index] & 255

    # return var1 < 128?readUnsignedByte():readUnsignedShort() - 32768
    if var1 < 128:
        return readUnsignedByte(buffer, index)
    else:
        var9999, index = readUnsignedShort(buffer, index)
        out = var9999 - 32768
        return out, index

    


@jit(nopython=True, cache=True)
def getIntFromBuffer(buffer, index):

    output = \
        ((buffer[index + 0] & 255) << 24) +\
        ((buffer[index + 1] & 255) << 16) +\
        ((buffer[index + 2] & 255) << 8) +\
        (buffer[index + 3] & 255)

    return output, index + 4


@jit(nopython=True, cache=True)
def getShortFromBuffer(buffer, index):

    output = ((buffer[index + 0] & 255) << 8) + (buffer[index + 1] & 255)
    if(output > 32767):
        output -= 65536
    output = output & 0xFFFF

    return output, index + 2


@jit(nopython=True, cache=True)
def getMediumFromBuffer(buffer, index):

    output = \
        ((buffer[index + 0] & 0xFF) << 16) | \
        ((buffer[index + 1] & 0xFF) << 8) | \
        (buffer[index + 2] & 0xFF)

    return output, index + 3


@jit(nopython=True, cache=True)
def getFromBuffer(buffer, index):

    output = buffer[index]

    return output, index + 1


@jit(nopython=True, cache=True)
def putIntToBuffer(buffer, index, value):

    buffer[index + 0] = np.byte(value >> 24)
    buffer[index + 1] = np.byte(value >> 16)
    buffer[index + 2] = np.byte(value >> 8)
    buffer[index + 3] = np.byte(value)

    return buffer, index + 4

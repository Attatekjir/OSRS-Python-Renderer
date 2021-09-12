from fileCounts import FILECOUNTS195
from bitoperation import getIntFromBuffer, getShortFromBuffer, getMediumFromBuffer, getFromBuffer, putIntToBuffer
from Buffer import Buffer
from regionIdTomapindex import regionIdToMapIndex, objectMapIDtoRegionID
import MathUtills
from MathUtills import integerdivide
import numpy as np
import zlib
import os
import json
import bz2
from numba import jit
import numba
from numba import int32, int64, float32, int8   # import the types


class FileStore():

    # FileStoreOpen
    def __init__(self, cache_folder):

        cache_path = cache_folder + "cache/"
        self.regionIdToXTEAkeys = numba.typed.Dict.empty(
            key_type=int64, value_type=int64[:])
        with open(cache_folder + "xteas.json") as json_file:
            data = json.load(json_file)
            for entry in data:
                self.regionIdToXTEAkeys[entry['mapsquare']] = np.asarray(
                    entry['key'], dtype=np.int64)

        # rb <- b stands for that reading shall remain in binary and not converted to string
        f = open(cache_path + "main_file_cache.dat2", mode='rb')
        dataChannel = np.array(bytearray(f.read()), dtype=np.byte)

        indexChannels = numba.typed.Dict.empty(
            key_type=int64, value_type=int8[:])  # []
        for i in range(0, 255):

            if not os.path.exists(cache_path + "main_file_cache.idx" + str(i)):
                continue

            if i != len(indexChannels):
                raise Exception("should not happen, should be serial idxs")

            f = open(cache_path + "main_file_cache.idx" + str(i), mode='rb')
            outputi = np.array(bytearray(f.read()), dtype=np.byte)

            indexChannels[i] = outputi  # .append(outputi)

        f = open(cache_path + "main_file_cache.idx255", mode='rb')
        metaChannel = np.array(bytearray(f.read()), dtype=np.byte)

        self.dataChannel = dataChannel
        self.indexChannels = indexChannels
        self.metaChannel = metaChannel

        self.objectMapIDtoRegionID = numba.typed.Dict.empty(
            key_type=int64, value_type=int64)
        for regionID, (floorMapID, objectMapID) in regionIdToMapIndex.items():
            self.objectMapIDtoRegionID[objectMapID] = regionID

    def FileStoreRead(self, typu, id):

        data = self.RetreiveDataFromCache(typu, id)

        xteaKeys = np.zeros(shape=(4), dtype=np.int32)  # [0, 0, 0, 0]

        # Does it concern map data and is it objectmap data == uneven id
        if typu == 5 and id % 2 == 1:
            regionId = self.objectMapIDtoRegionID[id]
            xteaKeys = self.regionIdToXTEAkeys[regionId]

        assert len(xteaKeys) == 4, "need 4 keys"

        decodedData = Decode(data, xteaKeys)

        return decodedData

    def GetIDCount(self, typu):
        INDEXSIZE = 6
        return np.int32(len(self.indexChannels[typu]) / INDEXSIZE)

    def getFileCount(self, typu):

        INDEXSIZE = 6

        if typu == 255:
            return int(len(self.metaChannel) / INDEXSIZE)
        else:
            return int(len(self.indexChannels[typu]) / INDEXSIZE)

    # Not worth to JIT, slower even
    def RetreiveDataFromCache(self, typu, id):

        if typu == 255:
            indexChannel = self.metaChannel
        else:
            indexChannel = self.indexChannels[typu]

        INDEXSIZE = 6
        ptr = id * INDEXSIZE

        if ptr < 0 or ptr >= len(indexChannel):
            raise TypeError("IndexChannel does not exist")

        buf = indexChannel[ptr: ptr + INDEXSIZE]

        # "Index"
        size = ((buf[0] & 0xFF) << 16) | (
            (buf[1] & 0xFF) << 8) | (buf[2] & 0xFF)
        sector = ((buf[3] & 0xFF) << 16) | (
            (buf[4] & 0xFF) << 8) | (buf[5] & 0xFF)

        buf = None  # clear bffr

        SECTORSIZE = 520
        chunk, remaining = 0, size
        ptr = sector * SECTORSIZE

        data = np.empty(shape=(remaining), dtype=np.byte)

        while (True):

            buf = self.dataChannel[ptr: ptr + SECTORSIZE]
            ptr += SECTORSIZE

            extended = id > 0xFFFF
            if extended:

                index = 0
                sectorid, index = getIntFromBuffer(buf, index)

                sectorchunk, index = getShortFromBuffer(buf, index)
                sectorchunk = sectorchunk & 0xFFFF

                sectornextSector, index = getMediumFromBuffer(buf, index)
                sectortype, index = getFromBuffer(buf, index)
                sectortype = sectortype & 0xFF

                sectordata = buf

            else:

                index = 0
                sectorid, index = getShortFromBuffer(buf, index)
                sectorid = sectorid & 0xFFFF

                sectorchunk, index = getShortFromBuffer(buf, index)
                sectorchunk = sectorchunk & 0xFFFF

                sectornextSector, index = getMediumFromBuffer(buf, index)
                sectortype, index = getFromBuffer(buf, index)
                sectortype = sectortype & 0xFF

                sectordata = buf

            if extended:
                dataSize = 510  # Sector.EXTENDED_DATA_SIZE
            else:
                dataSize = 512  # Sector.DATA_SIZE

            if (remaining > dataSize):

                data[-remaining: -remaining + dataSize] = sectordata[0 +
                                                                     index:dataSize + index].copy()
                remaining -= dataSize

                if (sectortype != typu):
                    raise Exception("read the cache wrong")

                if (sectorid != id):
                    raise Exception("read the cache wrong")

                if (sectorchunk != chunk):
                    raise Exception("read the cache wrong")

                chunk += 1

                ptr = sectornextSector * SECTORSIZE

            else:

                # Top-off the data array
                data[-remaining:] = sectordata[0 +
                                               index: remaining + index].copy()
                remaining = 0

            if remaining < 1:
                break

        return data

# Numpy.int32 to be compatible with java implementation

@jit(nopython=True, cache=False)
def decipher(buffer, start, end, keys):
    # if len(keys) != 4:
    #    raise KeyError("Keys need to be array of length 4")

    GOLDEN_RATIO = np.int32(0x9E3779B9)
    ROUNDS = np.int32(32)

    numQuads = integerdivide(end - start, 8)
    for i in range(0, numQuads):
        sum = np.int32(GOLDEN_RATIO * ROUNDS)
        v0, _ = getIntFromBuffer(buffer, start + i * 8)
        v1, _ = getIntFromBuffer(buffer, start + i * 8 + 4)

        v0 = np.int32(v0)
        v1 = np.int32(v1)

        for j in range(0, ROUNDS):

            v1 -= (((v0 << 4) ^ (MathUtills.unsignedrshift(v0, 5))) +
                   v0) ^ (sum + keys[(MathUtills.unsignedrshift(sum, 11)) & 3])
            v1 = np.int32(v1)

            sum = np.int32(sum - GOLDEN_RATIO)

            v0 -= (((v1 << 4) ^ (MathUtills.unsignedrshift(v1, 5))) +
                   v1) ^ (sum + keys[sum & 3])
            v0 = np.int32(v0)

        putIntToBuffer(buffer, start + i * 8, v0)
        putIntToBuffer(buffer, start + i * 8 + 4, v1)

    return buffer


# https://rationalpie.wordpress.com/2010/06/02/python-streaming-gzip-decompression/


class GzipInputStream(object):
    def __init__(self, data):
        self.compressedData = data

        # this magic number can be inferred from the structure of a gzip file
        self.decompressor = zlib.decompressobj(16+zlib.MAX_WBITS)
        self.curr = 0

    def read(self, block_size=64 * 1024):
        if block_size <= len(self.compressedData):
            raise Exception("Bruh!")

        if self.curr >= len(self.compressedData):
            raise Exception("Already read the file")

        # IF ERROR; THEN XTEA KEYS WERE PROBABLY WRONG
        compressedData_ = self.compressedData[self.curr: self.curr + block_size]
        uncompressedData = self.decompressor.decompress(compressedData_)

        # From bytearray to numpy
        uncompressedData = np.frombuffer(uncompressedData, dtype=np.byte)

        self.curr += block_size

        return uncompressedData


# https://gist.github.com/dirtysalt/d6c9f1fc74f1c9527bc3
def Decode(bffr, keys):

    index = 0
    typeOfCompression, index = getFromBuffer(bffr, index)
    typeOfCompression = typeOfCompression & 0xFF
    length, index = getIntFromBuffer(bffr, index)

    if typeOfCompression == 0:
        plus = 5
    else:
        plus = 9

    if (keys[0] != 0 or keys[1] != 0 or keys[2] != 0 or keys[3] != 0):
        bffr = decipher(bffr, start=5, end=length + plus, keys=keys)

    if typeOfCompression == 0:

        # /* simply grab the data and wrap it in a buffer */
        compressed = bffr[index: index + length]
        index += length
        uncompressed = compressed #.copy()

        version = -1
        if len(bffr) - index >= 2:
            version, index = getShortFromBuffer(bffr, index)

    else:

        # grab the length of the uncompressed data
        uncompressedLength, index = getIntFromBuffer(bffr, index)

        # grab the data
        compressed = bffr[index: index + length]

        # uncompress it
        if typeOfCompression == 1:  # bunzip2

            # BZh9 is added to the front of buffer as header, necessary for decompression
            bzipHeader = np.array([66, 90, 104, 57], dtype=np.byte)
            compressed = np.concatenate((bzipHeader, compressed), axis=0)
            compressed = bytearray(compressed)
            uncompressed = bz2.decompress(compressed)

            # From bytearray to np.byte array
            uncompressed = np.frombuffer(uncompressed, dtype=np.byte)

        elif (typeOfCompression == 2):

            # IF ERROR; THEN XTEA KEYS WERE PROBABLY WRONG
            gzipstream = GzipInputStream(compressed)
            uncompressed = gzipstream.read()

        else:
            raise Exception("Invalid compression type")

        # /* check if the lengths are equal */
        if len(uncompressed) != uncompressedLength:
            raise Exception(
                "Length mismatch. [ " + uncompressed.length + ", " + uncompressedLength + " ]")

        # /* decode the version if present */
        #version = -1
        # if buffer.remaining() >= 2:
        #    version = buffer.getShort()

    return uncompressed


# Runelite method
@jit(nopython=True, cache=False)
def loadContents(data, filesCount):

    stream = Buffer(data)
    stream.setOffset(stream.getLength() - 1)
    chunks = stream.readUnsignedByte()

    # -1 for chunks count + one int per file slot per chunk
    stream.setOffset(stream.getLength() - 1 - chunks * filesCount * 4)
    chunkSizes = np.zeros(shape = (filesCount, chunks), dtype = np.int32) 
    filesSize = np.zeros(shape=(filesCount), dtype=np.int32)

    for chunk in range(0, chunks):
        chunkSize = 0
        for id in range(0, filesCount):
            delta = stream.readInt()
            chunkSize += delta  # size of this chunk
            chunkSizes[id][chunk] = chunkSize  # store size of chunk
            filesSize[id] += chunkSize  # add chunk size to file size

    #fileContents = [None] * filesCount
    fileOffsets = np.zeros(shape=(filesCount), dtype=np.int32)

    fileContents = [np.zeros(shape=(filesSize[i]), dtype=np.byte)
                             for i in range(0, filesCount)]

    # for i in range(0, filesCount):
    #     fileContents[i] = np.zeros(shape=(filesSize[i]), dtype=np.byte)

    # the file data is at the beginning of the stream
    stream.setOffset(0)

    for chunk in range(0, chunks):
        for id in range(0, filesCount):
            chunkSize = chunkSizes[id][chunk]
            stream.readBytes(fileContents[id], fileOffsets[id], chunkSize)
            fileOffsets[id] += chunkSize

    return fileContents



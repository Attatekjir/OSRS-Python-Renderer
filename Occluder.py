from numba import int32, float32, boolean, short, int64
from numba.experimental import jitclass

@jitclass()
class Occluder:

    minTileX : int32
    maxTIleX : int32
    minTileZ : int32
    maxTileZ : int32
    type : int32
    minX : int32
    maxX : int32
    minZ : int32
    maxZ : int32
    minY : int32
    maxY : int32
    testDirection : int32
    field2089 : int32
    field2088 : int32
    minNormalX : int32
    maxNormalX : int32
    minNormalY : int32
    maxNormalY : int32

    def __init__(self):

        pass

        # self.minTileX = 0
        # self.maxTIleX = 0
        # self.minTileZ = 0
        # self.maxTileZ = 0
        # self.type = 0
        # self.minX = 0
        # self.maxX = 0
        # self.minZ = 0
        # self.maxZ = 0
        # self.minY = 0
        # self.maxY = 0
        # self.testDirection = 0
        # self.field2089 = 0
        # self.field2088 = 0
        # self.minNormalX = 0
        # self.maxNormalX = 0
        # self.minNormalY = 0
        # self.maxNormalY = 0

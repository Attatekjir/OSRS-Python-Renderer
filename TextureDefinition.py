from numba import int32, float32   # import the types
from SpriteDefinition import normalizeSprite
import numba
from cacheUtills import loadContents
from numba import jit
from fileCounts import FILECOUNTS195
from utills import adjustRGB
import numpy as np
from Buffer import Buffer
from numba.experimental import jitclass
from numba import int32, float32, boolean

spec1 = [
    ('id', int32),

    ('field1801', int32[:]),
    ('field1803', int32),
    ('field1806', boolean),
    ('field1807', int32[:]),
    ('field1808', int32[:]),
    ('field1809', int32),
    ('field1810', int32),

    ('fileIds', int32[:]),
    ('pixels', int32[:]),
]


@jitclass(spec1)
class TextureDefinition:

    def __init__(self, id, field1801, field1803, field1806, field1807,
                 field1808, field1809, field1810, fileIds):

        self.id = id
        self.field1801 = field1801
        self.field1803 = field1803
        self.field1806 = field1806
        self.field1807 = field1807
        self.field1808 = field1808
        self.field1809 = field1809
        self.field1810 = field1810

        self.fileIds = fileIds
        self.pixels = np.empty(shape=(1), dtype=np.int32)


@jit(nopython=True, cache=False)
def method2680(texture, brightness, width, spriteProvider):
    var5 = width * width
    texture.pixels = np.zeros(shape=(var5), dtype=np.int32)

    for var6 in range(0, len(texture.fileIds)):

        # Select random sprite from the list of sprites (gathered from a dict)
        var9999 = spriteProvider[texture.fileIds[var6]]
        var7 = var9999[np.random.choice(len(var9999), 1)[0]]
        normalizeSprite(var7)
        var8 = var7.pixelIdx
        var9 = var7.palette
        var10 = texture.field1808[var6]

        if ((var10 & -16777216) == 50331648):
            var11 = var10 & 16711935
            var12 = var10 >> 8 & 255
            for var13 in range(0, len(var9)):
                var14 = var9[var13]
                if (var14 >> 8 == (var14 & 65535)):
                    var14 &= 255
                    var9[var13] = var11 * \
                        var14 >> 8 & 16711935 | var12 * var14 & 65280

        for var11 in range(0, len(var9)):
            var9[var11] = adjustRGB(var9[var11], brightness)

        if (var6 == 0):
            var11 = 0
        else:
            var11 = texture.field1801[var6 - 1]

        if (var11 == 0):
            if (width == var7.maxWidth):
                for var12 in range(0, var5):
                    texture.pixels[var12] = var9[var8[var12] & 255]
            elif (var7.maxWidth == 64 and width == 128):
                var12 = 0
                for var13 in range(0, width):
                    for var14 in range(0, width):
                        texture.pixels[var12] = var9[var8[(
                            var13 >> 1 << 6) + (var14 >> 1)] & 255]
                        var12 += 1
            else:
                if (var7.maxWidth != 128 or width != 64):
                    raise Exception("except")
                var12 = 0
                for var13 in range(0, width):
                    for var14 in range(0, width):
                        texture.pixels[var12] = var9[var8[(
                            var14 << 1) + (var13 << 1 << 7)] & 255]
                        var12 += 1

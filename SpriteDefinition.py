from numba import jit
from Buffer import Buffer
import numpy as np
from numba.experimental import jitclass
from numba import int32, float32, boolean, int8
from numba import int64, types, typed


spec1 = [
    ('id', int32),
    ('frame', int32),
    ('offsetX', int32),
    ('offsetY', int32),
    ('width', int32),
    ('height', int32),
    ('pixels', int32[:]),
    ('maxWidth', int32),
    ('maxHeight', int32),
    ('pixelIdx', int8[:]),
    ('palette', int32[:]),
]


@jitclass(spec1)
class SpriteDefinition:

    def __init__(self, id, frameid, maxwidth, maxheight):

        self.id = id
        self.frame = frameid
        self.offsetX = 0
        self.offsetY = 0
        self.width = 0
        self.height = 0
        self.pixels = np.empty(shape=(1), dtype=np.int32)
        self.maxWidth = maxwidth
        self.maxHeight = maxheight

        self.pixelIdx = np.empty(shape=(1), dtype=np.byte)
        self.palette = np.empty(shape=(1), dtype=np.int32)


@jit(nopython=True, cache=True)
def normalizeSprite(sprite):
    if (sprite.width != sprite.maxWidth or sprite.height != sprite.maxHeight):
        var1 = np.zeros(
            shape=(sprite.maxWidth * sprite.maxHeight), dtype=np.byte)
        var2 = 0

        for var3 in range(0, sprite.height):
            for var4 in range(0, sprite.width):
                var1[var4 + (var3 + sprite.offsetY) * sprite.maxWidth +
                     sprite.offsetX] = sprite.pixelIdx[var2]
                var2 += 1

        sprite.pixelIdx = var1
        sprite.width = sprite.maxWidth
        sprite.height = sprite.maxHeight
        sprite.offsetX = 0
        sprite.offsetY = 0


@jit(nopython=True, cache= True)
def loadSprite(id, data, ci):

    FLAG_VERTICAL = 0b01
    FLAG_ALPHA = 0b10

    stream = Buffer(data)

    stream.setOffset(stream.getLength() - 2)
    spriteCount = stream.readUnsignedShort()

    # 2 for size
    # 5 for width, height, palette length
    # + 8 bytes per sprite for offset x/y, width, and height
    stream.setOffset(stream.getLength() - 7 - spriteCount * 8)

    # max width and height
    maxwidth = stream.readUnsignedShort()
    maxheight = stream.readUnsignedShort()
    paletteLength = stream.readUnsignedByte() + 1

    #sprites = [SpriteDefinition(id, i, maxwidth, maxheight) for i in range(0, spriteCount)]

    sprites = typed.List.empty_list(ci)
    for frameid in range(0, spriteCount):
        sprite_ = SpriteDefinition(id, frameid, maxwidth, maxheight)
        sprites.append(sprite_)

    for frameid in range(0, spriteCount):
        sprites[frameid].offsetX = stream.readUnsignedShort()

    for frameid in range(0, spriteCount):
        sprites[frameid].offsetY = stream.readUnsignedShort()

    for frameid in range(0, spriteCount):
        sprites[frameid].width = stream.readUnsignedShort()

    for frameid in range(0, spriteCount):
        sprites[frameid].height = stream.readUnsignedShort()

    # same as above + 3 bytes for each palette entry, except for the first one (which stream transparent)
    stream.setOffset(stream.getLength() - 7 - spriteCount *
                     8 - (paletteLength - 1) * 3)
    palette = np.zeros(shape=(paletteLength), dtype=np.int32)

    for i in range(1, paletteLength):
        palette[i] = stream.read24BitInt()
        if (palette[i] == 0):
            palette[i] = 1

    stream.setOffset(0)

    for frameid in range(0, spriteCount):
        spritedef = sprites[frameid]
        spriteWidth = spritedef.width
        spriteHeight = spritedef.height
        dimension = spriteWidth * spriteHeight
        pixelPaletteIndicies = np.zeros(shape=(dimension), dtype=np.byte)
        pixelAlphas = np.zeros(shape=(dimension), dtype=np.byte)
        spritedef.pixelIdx = pixelPaletteIndicies
        spritedef.palette = palette  # .copy()

        flags = stream.readUnsignedByte()

        if ((flags & FLAG_VERTICAL) == 0):  # read horizontally
            for j in range(0, dimension):
                pixelPaletteIndicies[j] = stream.readByte()
        else:  # read vertically
            for j in range(0, spriteWidth):
                for k in range(0, spriteHeight):
                    pixelPaletteIndicies[spriteWidth *
                                         k + j] = stream.readByte()

        if ((flags & FLAG_ALPHA) != 0):  # read alphas
            if ((flags & FLAG_VERTICAL) == 0):  # read horizontally
                for j in range(0, dimension):
                    pixelAlphas[j] = stream.readByte()
            else:  # read vertically
                for j in range(0, spriteWidth):
                    for k in range(0, spriteHeight):
                        pixelAlphas[spriteWidth * k + j] = stream.readByte()

        else:  # everything non-zero stream opaque
            for j in range(0, dimension):
                index = pixelPaletteIndicies[j]
                if (index != 0):
                    pixelAlphas[j] = np.byte(0xFF)

        pixels = np.zeros(shape=(dimension), dtype=np.int32)

        # build argb pixels from palette/alphas
        for j in range(0, dimension):
            index = pixelPaletteIndicies[j] & 0xFF
            pixels[j] = palette[index] | (pixelAlphas[j] << 24)

        spritedef.pixels = pixels

    return sprites

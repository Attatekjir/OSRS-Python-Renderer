from numba import jit

@jit(nopython=True, cache=False)
def adjustRGB(var0, var1):

    var3 = (var0 >> 16) / 256.0
    var5 = (var0 >> 8 & 255) / 256.0
    var7 = (var0 & 255) / 256.0
    var3 = pow(var3, var1)
    var5 = pow(var5, var1)
    var7 = pow(var7, var1)
    var9 = int(var3 * 256.0)
    var10 = int(var5 * 256.0)
    var11 = int(var7 * 256.0)

    return var11 + (var10 << 8) + (var9 << 16)

@jit(nopython=True, cache=False)
def hslToRGB(pixelvalue):
    
    r = (pixelvalue >> 16 & 255)
    g = (pixelvalue >> 8 & 255)
    b = (pixelvalue & 255)

    return r,g,b

@jit(nopython=True, cache=False)
def getTile(var1, var2, var3, tiles):

    # 104 is max of var2 and var3
    index =  (var1 * 104 * 104) + (var2 * 104) + var3
    tile = tiles[index]
    return tile

@jit(nopython=True, cache=False)
def getTileID(tile):

    # 104 is max of var2 and var3
    index =  (tile.plane * 104 * 104) + (tile.x * 104) + tile.y
    return index

@jit(nopython=True, cache=False)
def putTile(tile, var1, var2, var3, tiles):
    
    # 104 is max of var2 and var3
    index =  (var1 * 104 * 104) + (var2 * 104) + var3
    tiles[index] = tile
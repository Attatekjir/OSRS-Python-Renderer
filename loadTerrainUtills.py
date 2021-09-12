import numba
from GroundObject import GroundObject
from utills import getTile
from WallObject import WallObject
from DecorativeObject import DecorativeObject
from expModel import method2693
from numba import jit
from Buffer import Buffer
import numpy as np
from MathUtills import integerdivide
from MathUtills import Graphics3DCOSINE
from expObjectDefinition import getModel
from Region import method2862


@jit(nopython=True, cache=True)
def method2246(var0, var1, var2, var3):
    var10 = integerdivide(var2 * 1024, var3)
    cosineValue = Graphics3DCOSINE(var10)
    var4 = 65536 - cosineValue >> 1
    return np.int32(((65536 - var4) * var0 >> 16) + (var4 * var1 >> 16))


@jit(nopython=True, cache=True)
def method2544(var0, var1):
    var2 = var1 * 57 + var0
    var2 ^= var2 << 13

    i1 = np.int32((var2 * var2 * 15731 + 789221) * var2)
    i2 = np.int32(i1 + 1376312589)
    i3 = np.int32(i2 & 2147483647)
    i4 = np.int32(i3 >> 19)
    return i4 & 255


@jit(nopython=True, cache=True)
def getSmoothNoise2D(var0, var1):
    var2 = method2544(var0 - 1, var1 - 1) + method2544(var0 + 1, var1 - 1) + \
        method2544(var0 - 1, var1 + 1) + method2544(1 + var0, 1 + var1)
    var3 = method2544(var0 - 1, var1) + method2544(var0 + 1, var1) + \
        method2544(var0, var1 - 1) + method2544(var0, var1 + 1)
    var4 = method2544(var0, var1)
    return integerdivide(var2, 16) + integerdivide(var3, 8) + integerdivide(var4, 4)





@jit(nopython=True, cache=True)
def getSmoothNoise(var0, var1, var2):
    var3 = integerdivide(var0, var2)
    var4 = var0 & var2 - 1
    var5 = integerdivide(var1, var2)
    var6 = var1 & var2 - 1
    var7 = getSmoothNoise2D(var3, var5)
    var8 = getSmoothNoise2D(var3 + 1, var5)
    var9 = getSmoothNoise2D(var3, var5 + 1)
    var10 = getSmoothNoise2D(var3 + 1, var5 + 1)
    var11 = method2246(var7, var8, var4, var2)
    var12 = method2246(var9, var10, var4, var2)
    return method2246(var11, var12, var6, var2)




@jit(nopython=True, cache=False)
def method1131(var0, var1):
    var2 = getSmoothNoise(var0 + 45365, var1 + 91923, 4) - 128 + \
       (getSmoothNoise(10294 + var0, 37821 + var1, 2) - 128 >> 1) + \
       (getSmoothNoise(var0, var1, 1) - 128 >> 2)

    var2 = np.int32(0.3 * var2) + 35
    #var2 = 40

    # It can not be less than 10, nor higher than 60
    var2 = min(max(var2, 10), 60)

    return var2

@jit(nopython=True, cache=False)
def method2868(var1, var2, var3, var4, tiles):
    var5 = getTile(var1, var2, var3, tiles)  # tiles[var1][var2][var3]
    if(var5 is not None):
        var6 = var5.decorativeObject
        if(var6 is not None):
            var6.offsetX = integerdivide(var4 * var6.offsetX, 16)
            var6.offsetY = integerdivide(var4 * var6.offsetY, 16)

@jit(nopython=True, cache=False)
def groundObjectSpawned(var1, var2, var3, var4, var5, var6, var7, tiles):

    if(var5 is not None):

        floor = var4
        x = var2 * 128 + 64
        y = var3 * 128 + 64
        renderable = var5
        hash = var6
        renderInfoBitPacked = var7

        var8 = GroundObject(floor, x, y, renderable, hash, renderInfoBitPacked)

        # Tiles already exist...
        # if(tiles[var1][var2][var3] is None):
        #    tiles[var1][var2][var3] = Tile(var1, var2, var3)

        tile_ = getTile(var1, var2, var3, tiles)
        tile_.groundObject = var8

        #tiles[var1][var2][var3].groundObject = var8


# public void addItemPile(var1, var2, var3, var4, final Renderable var5, var6, final Renderable var7, final Renderable var8) :
# final ItemLayer var9 = new ItemLayer()
# var9.bottom = var5
# var9.x = var2 * 128 + 64
# var9.y = var3 * 128 + 64
# var9.hash = var4
# var9.flags = var6
# var9.middle = var7
# var9.top = var8
# int var10 = 0
# final Tile var11 = tiles[var1][var2][var3]
# if(var11 is not None) :
# for(int var12 = 0 var12 < var11.entityCount ++var12) :
# if((var11.objects[var12].flags & 256) == 256 and var11.objects[var12].renderable instanceof Model) :
# final Model var13 = (Model)var11.objects[var12].renderable
# var13.calculateBoundsCylinder()
# if(var13.modelHeight > var10) :
# var10 = var13.modelHeight


# var9.height = var10
# if(tiles[var1][var2][var3] is None) :
# tiles[var1][var2][var3] = new Tile(var1, var2, var3)


# tiles[var1][var2][var3].itemLayer = var9


@jit(nopython=True, cache=False)
def addBoundary(var1, var2, var3, var4, var5, var6, var7, var8, var9, var10, tiles):
    if(var5 is not None or var6 is not None):
        var11 = WallObject(var5, var6)
        var11.hash = var9
        var11.config = var10
        var11.x = var2 * 128 + 64
        var11.y = var3 * 128 + 64
        var11.floor = var4
        #var11.renderable1 = var5
        #var11.renderable2 = var6
        var11.orientationA = var7
        var11.orientationB = var8

        # Tiles already exist...
        # var12 = var1
        # while var12 >= 0:
        #     if(tiles[var12][var2][var3] is None):
        #         tiles[var12][var2][var3] = Tile(var12, var2, var3)
        #     var12 -= 1

        tile_ = getTile(var1, var2, var3, tiles)
        tile_.wallObject = var11
        #tiles[var1][var2][var3].wallObject = var11


@jit(nopython=True, cache=False)
def addBoundaryDecoration(var1, var2, var3, var4, var5, var6, var7, var8, var9, var10, var11, var12, tiles):
    if(var5 is not None):
        var13 = DecorativeObject(var5, var6)
        var13.hash = var11
        var13.renderInfoBitPacked = var12
        var13.x = var2 * 128 + 64
        var13.y = var3 * 128 + 64
        var13.floor = var4
        # var13.renderable1 = var5
        # var13.renderable2 = var6
        var13.renderFlag = var7
        var13.rotation = var8
        var13.offsetX = var9
        var13.offsetY = var10

        # Tiles already exist...
        # var14 = var1
        # while var14 >= 0:
        #     if(tiles[var14][var2][var3] is None):
        #         tiles[var14][var2][var3] = Tile(var14, var2, var3)
        #     var14 -= 1

        tile_ = getTile(var1, var2, var3, tiles)
        tile_.decorativeObject = var13
        #tiles[var1][var2][var3].decorativeObject = var13


@jit(nopython=True, cache=False)
def loadTerrain(var0, var1, var2, var3, var4, var5, var6, tileSettings, tileHeights, tileOverlayIds, tileUnderlayIds, tileOverlayPath, overlayRotations):

    # if(var2 >= 0 and var2 < 104 and var3 >= 0 and var3 < 104):
    if max(var2, var3) < 104 and min(var2, var3) >= 0:

        tileSettings[var1][var2][var3] = 0

        while(True):
            var7 = var0.readUnsignedByte()

            if(var7 == 0):
                if(var1 == 0):
                    tileHeights[0][var2][var3] = -method1131(var2 + 932731 + var4,
                                   var5 + 556238 + var3) * 8
                else:
                    tileHeights[var1][var2][var3] = tileHeights[var1 -
                                                                1][var2][var3] - 240
                break

            if(var7 == 1):
                var8 = var0.readUnsignedByte()
                if(var8 == 1):
                    var8 = 0
                if(var1 == 0):
                    tileHeights[0][var2][var3] = -var8 * 8
                else:
                    tileHeights[var1][var2][var3] = tileHeights[var1 -
                                                                1][var2][var3] - var8 * 8
                break

            if(var7 <= 49):
                tileOverlayIds[var1][var2][var3] = var0.readByte()
                tileOverlayPath[var1][var2][var3] = np.byte(
                    integerdivide((var7 - 2), 4))
                overlayRotations[var1][var2][var3] = np.byte(
                    var7 - 2 + var6 & 3)
            elif(var7 <= 81):
                tileSettings[var1][var2][var3] = np.byte(var7 - 49)
            else:
                tileUnderlayIds[var1][var2][var3] = np.byte(var7 - 81)

    else:
        while(True):
            var7 = var0.readUnsignedByte()
            if(var7 == 0):
                break

            if(var7 == 1):
                var0.readUnsignedByte()
                break

            if(var7 <= 49):
                var0.readUnsignedByte()


@jit(nopython=True, cache=False)
def loadTerrainFloor(decodedFloorMapBffr, eastadjust, xlocal, northadjust, ylocal,
                     tileSettings, tileHeights,
                     tileOverlayIds, tileUnderlayIds,
                     tileOverlayPath, overlayRotations):

    # First load terrain, because tileHeights is used when placing objects
    # Values taken from rebotted2006
    ScriptStatefield761 = 406 * 8 - 48
    GrandExchangeEventfield301 = 427 * 8 - 48

    # USED FOR SOME RANDOM SMOOTH FUNCTION
    var7, var73 = ScriptStatefield761, GrandExchangeEventfield301
    var55 = Buffer(decodedFloorMapBffr)
    for var11 in range(0, 4):
        for var12 in range(0 + eastadjust + xlocal, 64 + eastadjust + xlocal):
            for var75 in range(0 + northadjust + ylocal, 64 + northadjust + ylocal):
                loadTerrain(var55, var11, var12, var75, var7, var73, 0,
                            tileSettings, tileHeights,
                            tileOverlayIds, tileUnderlayIds,
                            tileOverlayPath, overlayRotations)


@numba.jit(nopython=True, cache=False)
def addObject(uncryptedModelContents, regionobjects, field2025, regionvars, maxYregion, maxXregion, maxZregion, var0, var1, var2, var3, var4, var5, var7, field2520, field3831, tileSettings, objectDefinitions,
              field749, field746, field738, field740, field752, field750, tileHeights, tiles):

    ClientlowMemory = False

    if(not ClientlowMemory or (tileSettings[0][var1][var2] & 2) != 0 or (tileSettings[var0][var1][var2] & 16) == 0):
        # if(var0 < field747):
        #    field747 = var0

        var8 = objectDefinitions[var3]

        # There is no models for this object...so no point trying to render it
        if var8.objectModels is None:
            return

        #print("In here boys", var8.name, var8.id, var5)

        if(var4 != 1 and var4 != 3):
            var9 = var8.width
            var10 = var8.length
        else:
            var9 = var8.length
            var10 = var8.width

        if(var9 + var1 <= 104):
            var11 = (var9 >> 1) + var1
            var12 = (var9 + 1 >> 1) + var1
        else:
            var11 = var1
            var12 = var1 + 1

        if(var10 + var2 <= 104):
            var13 = (var10 >> 1) + var2
            var14 = var2 + (var10 + 1 >> 1)
        else:
            var13 = var2
            var14 = var2 + 1

        var15 = tileHeights[var0]

        var16 = var15[var12][var13] + var15[var11][var13] + \
            var15[var11][var14] + var15[var12][var14] >> 2

        var17 = (var1 << 7) + (var9 << 6)
        var18 = (var2 << 7) + (var10 << 6)
        var19 = (var3 << 14) + (var2 << 7) + var1 + 1073741824
        if(var8.int1 == 0):
            # yes, minus a minus value
            var19 = np.int32(var19 - -2147483648)  # Integer.MIN_VALUE

        var20 = var5 + (var4 << 6)
        if(var8.supportItems == 1):
            var20 += 256

        # The object is a random piece of rock/dirt on the floor, mostly unnamed or unexaminable
        if(var5 == 22):

            if(not ClientlowMemory or var8.int1 != 0 or var8.clipType == 1 or var8.obstructsGround):
                var30 = getModel(uncryptedModelContents, var8,
                                 22, var4, var15, var17, var16, var18)

                groundObjectSpawned(
                    var0, var1, var2, var16, var30, var19, var20, tiles)

                #if var8.clipType == 1 and var7 is not None:
                #    var7.method3385(var1, var2)
                

        elif(var5 != 10 and var5 != 11):

            if(var5 >= 12):
                # if(var8.animationId == -1 and var8.impostorIds is None):
                var30 = getModel(uncryptedModelContents, var8,
                                 var5, var4, var15, var17, var16, var18)
                # else:
                #     var30 = DynamicObject(var3, var5, var4, var0, var1, var2, var8.animationId, True, None,
                #                             cacheStore_, Graphics3D_)

                method2862(regionobjects, field2025, regionvars, maxYregion, maxXregion, maxZregion, var0, var1, var2, var16, 1,
                           1, var30, 0, var19, var20, tiles)
                if(var5 >= 12 and var5 <= 17 and var5 != 13 and var0 > 0):
                    field2520[var0][var1][var2] |= 2340

                # if(var8.clipType != 0 and var7 is not None):
                #    var7.addObject(var1, var2, var9, var10,
                #                   var8.blocksProjectile)

            elif(var5 == 0):

                # if(var8.animationId == -1 and var8.impostorIds is None):
                var30 = getModel(uncryptedModelContents, var8,
                                 0, var4, var15, var17, var16, var18)
                # else:
                #     var30 = DynamicObject(var3, 0, var4, var0, var1, var2, var8.animationId, True, None,
                #                             cacheStore_, Graphics3D_)

                addBoundary(var0, var1, var2, var16, var30, None,
                            field749[var4], 0, var19, var20, tiles)
                if(var4 == 0):
                    if(var8.clipped):
                        field3831[var0][var1][var2] = 50
                        field3831[var0][var1][var2 + 1] = 50

                    if(var8.modelClipped):
                        field2520[var0][var1][var2] |= 585

                elif(var4 == 1):
                    if(var8.clipped):
                        field3831[var0][var1][var2 + 1] = 50
                        field3831[var0][var1 +
                                        1][var2 + 1] = 50

                    if(var8.modelClipped):
                        field2520[var0][var1][1 + var2] |= 1170

                elif(var4 == 2):
                    if(var8.clipped):
                        field3831[var0][var1 + 1][var2] = 50
                        field3831[var0][var1 +
                                        1][var2 + 1] = 50

                    if(var8.modelClipped):
                        field2520[var0][var1 +
                                        1][var2] |= 585

                elif(var4 == 3):
                    if(var8.clipped):
                        field3831[var0][var1][var2] = 50
                        field3831[var0][var1 + 1][var2] = 50

                    if(var8.modelClipped):
                        field2520[var0][var1][var2] |= 1170

                # if(var8.clipType != 0 and var7 is not None):
                #    var7.method3391(var1, var2, var5, var4,
                #                    var8.blocksProjectile)

                if(var8.decorDisplacement != 16):
                    method2868(var0, var1, var2,
                               var8.decorDisplacement, tiles)

            elif(var5 == 1):

                # if(var8.animationId == -1 and var8.impostorIds is None):
                var30 = getModel(uncryptedModelContents, var8,
                                 1, var4, var15, var17, var16, var18)
                # else:
                #     var30 = DynamicObject(var3, 1, var4, var0, var1, var2, var8.animationId, True, None,
                #                             cacheStore_, Graphics3D_)

                addBoundary(var0, var1, var2, var16, var30, None,
                            field746[var4], 0, var19, var20, tiles)
                if(var8.clipped):
                    if(var4 == 0):
                        field3831[var0][var1][var2 + 1] = 50
                    elif(var4 == 1):
                        field3831[var0][var1 +
                                        1][var2 + 1] = 50
                    elif(var4 == 2):
                        field3831[var0][var1 + 1][var2] = 50
                    elif(var4 == 3):
                        field3831[var0][var1][var2] = 50

                # if(var8.clipType != 0 and var7 is not None):
                #    var7.method3391(var1, var2, var5, var4,
                #                    var8.blocksProjectile)

            else:
                if(var5 == 2):
                    var26 = var4 + 1 & 3

                    # if(var8.animationId == -1 and var8.impostorIds is None):
                    var27 = getModel(uncryptedModelContents, var8,
                                     2, var4 + 4, var15, var17, var16, var18)
                    var28 = getModel(uncryptedModelContents, var8,
                                     2, var26, var15, var17, var16, var18)
                    # else:
                    #     var27 = DynamicObject(var3, 2, var4 + 4, var0, var1, var2, var8.animationId, True, None,
                    #                             cacheStore_, Graphics3D_)
                    #     var28 = DynamicObject(var3, 2, var26, var0, var1, var2, var8.animationId, True, None,
                    #                             cacheStore_, Graphics3D_)

                    addBoundary(var0, var1, var2, var16, var27, var28,
                                field749[var4], field749[var26], var19, var20, tiles)
                    if(var8.modelClipped):
                        if(var4 == 0):
                            field2520[var0][var1][var2] |= 585
                            field2520[var0][var1][var2 + 1] |= 1170
                        elif(var4 == 1):
                            field2520[var0][var1][1 + var2] |= 1170
                            field2520[var0][var1 +
                                            1][var2] |= 585
                        elif(var4 == 2):
                            field2520[var0][var1 +
                                            1][var2] |= 585
                            field2520[var0][var1][var2] |= 1170
                        elif(var4 == 3):
                            field2520[var0][var1][var2] |= 1170
                            field2520[var0][var1][var2] |= 585

                    # if(var8.clipType != 0 and var7 is not None):
                    #    var7.method3391(var1, var2, var5,
                    #                    var4, var8.blocksProjectile)

                    if(var8.decorDisplacement != 16):
                        method2868(var0, var1, var2,
                                   var8.decorDisplacement, tiles)

                elif(var5 == 3):

                    # if(var8.animationId == -1 and var8.impostorIds is None):
                    var30 = getModel(uncryptedModelContents, var8,
                                     3, var4, var15, var17, var16, var18)
                    # else:
                    #     var30 = DynamicObject(var3, 3, var4, var0, var1, var2, var8.animationId, True, None,
                    #                             cacheStore_, Graphics3D_)

                    addBoundary(
                        var0, var1, var2, var16, var30, None, field746[var4], 0, var19, var20, tiles)
                    if(var8.clipped):
                        if(var4 == 0):
                            field3831[var0][var1][var2 + 1] = 50
                        elif(var4 == 1):
                            field3831[var0][var1 + 1][var2 + 1] = 50
                        elif(var4 == 2):
                            field3831[var0][var1 + 1][var2] = 50
                        elif(var4 == 3):
                            field3831[var0][var1][var2] = 50

                    # if(var8.clipType != 0 and var7 is not None):
                    #    var7.method3391(var1, var2, var5,
                    #                    var4, var8.blocksProjectile)

                elif(var5 == 9):

                    # if(var8.animationId == -1 and var8.impostorIds is None):
                    var30 = getModel(uncryptedModelContents, var8,
                                     var5, var4, var15, var17, var16, var18)
                    # else:
                    #     var30 = DynamicObject(var3, var5, var4, var0, var1, var2, var8.animationId, True, None,
                    #                             cacheStore_, Graphics3D_)

                    method2862(regionobjects, field2025, regionvars, maxYregion, maxXregion, maxZregion, var0, var1, var2, var16,
                               1, 1, var30, 0, var19, var20, tiles)
                    # if(var8.clipType != 0 and var7 is not None):
                    #    var7.addObject(var1, var2, var9,
                    #                   var10, var8.blocksProjectile)

                    if(var8.decorDisplacement != 16):
                        method2868(var0, var1, var2,
                                   var8.decorDisplacement, tiles)

                elif(var5 == 4):

                    # if(var8.animationId == -1 and var8.impostorIds is None):
                    var30 = getModel(uncryptedModelContents, var8,
                                     4, var4, var15, var17, var16, var18)
                    # else:
                    #     var30 = DynamicObject(var3, 4, var4, var0, var1, var2, var8.animationId, True, None,
                    #                             cacheStore_, Graphics3D_)

                    addBoundaryDecoration(
                        var0, var1, var2, var16, var30, None, field749[var4], 0, 0, 0, var19, var20, tiles)

                elif(var5 == 5):
                    var26 = 16
                    var22 = getWallObjectHash(var0, var1, var2, tiles)
                    if(var22 != 0):
                        #var26 = self.GameCanvas_.getObjectDefinition(var22 >> 14 & 32767).decorDisplacement
                        var26 = objectDefinitions[var22 >>
                                                  14 & 32767].decorDisplacement

                    # if(var8.animationId == -1 and var8.impostorIds is None):
                    var28 = getModel(uncryptedModelContents, var8,
                                     4, var4, var15, var17, var16, var18)
                    # else:
                    #     var28 = DynamicObject(var3, 4, var4, var0, var1, var2, var8.animationId, True, None,
                    #                             cacheStore_, Graphics3D_)

                    addBoundaryDecoration(var0, var1, var2, var16, var28, None, field749[
                        var4], 0, var26 * field738[var4], var26 * field740[var4], var19, var20, tiles)

                elif(var5 == 6):
                    var26 = 8
                    var22 = getWallObjectHash(var0, var1, var2, tiles)
                    if(var22 != 0):
                        #var26 = self.GameCanvas_.getObjectDefinition(var22 >> 14 & 32767).decorDisplacement / 2
                        var26 = integerdivide(
                            objectDefinitions[var22 >> 14 & 32767].decorDisplacement, 2)

                    # if(var8.animationId == -1 and var8.impostorIds is None):
                    var28 = getModel(uncryptedModelContents, var8,
                                     4, var4 + 4, var15, var17, var16, var18)
                    # else:
                    #     var28 = DynamicObject(var3, 4, var4 + 4, var0, var1, var2, var8.animationId, True, None,
                    #                             cacheStore_, Graphics3D_)

                    addBoundaryDecoration(var0, var1, var2, var16, var28, None, 256, var4, var26 *
                                          field752[var4], var26 * field750[var4], var19, var20, tiles)

                elif(var5 == 7):
                    var22 = var4 + 2 & 3

                    # if(var8.animationId == -1 and var8.impostorIds is None):
                    var30 = getModel(uncryptedModelContents, var8,
                                     4, var22 + 4, var15, var17, var16, var18)
                    # else:
                    #     var30 = DynamicObject(var3, 4, var22 + 4, var0, var1, var2, var8.animationId, True, None,
                    #                             cacheStore_, Graphics3D_)

                    addBoundaryDecoration(
                        var0, var1, var2, var16, var30, None, 256, var22, 0, 0, var19, var20, tiles)

                elif(var5 == 8):
                    var26 = 8
                    var22 = getWallObjectHash(var0, var1, var2, tiles)
                    if(var22 != 0):
                        #var26 = self.GameCanvas_.getObjectDefinition(var22 >> 14 & 32767).decorDisplacement / 2
                        var26 = integerdivide(
                            objectDefinitions[var22 >> 14 & 32767].decorDisplacement, 2)

                    var25 = var4 + 2 & 3

                    # if(var8.animationId == -1 and var8.impostorIds is None):
                    var28 = getModel(uncryptedModelContents, var8,
                                     4, var4 + 4, var15, var17, var16, var18)
                    var29 = getModel(uncryptedModelContents, var8,
                                     4, var25 + 4, var15, var17, var16, var18)
                    # else:
                    #     var28 = DynamicObject(var3, 4, var4 + 4, var0, var1, var2, var8.animationId, True, None,
                    #                             cacheStore_, Graphics3D_)
                    #     var29 = DynamicObject(var3, 4, var25 + 4, var0, var1, var2, var8.animationId, True, None,
                    #                             cacheStore_, Graphics3D_)

                    addBoundaryDecoration(var0, var1, var2, var16, var28, var29, 256, var4, var26 *
                                          field752[var4], var26 * field750[var4], var19, var20, tiles)

        else:  # var5 == 10 or var5 == 11

            # if(var8.animationId == -1 and var8.impostorIds is None):
            var30 = getModel(uncryptedModelContents, var8,
                             10, var4, var15, var17, var16, var18)
            # else:
            #     var30 = DynamicObject(var3, 10, var4, var0, var1, var2, var8.animationId, True, None,
            #                             cacheStore_, Graphics3D_)

            # var5 == 11?256:0
            customvar = 0
            if var5 == 11:
                customvar = 256

            modelsuccesfullygotten = method2862(regionobjects, field2025, regionvars, maxYregion, maxXregion, maxZregion,
                                                var0, var1, var2, var16, var9, var10, var30, customvar, var19, var20, tiles)
            if(var30 is not None and modelsuccesfullygotten and var8.clipped):
                var22 = 15
                #  var30 instanceof Model
                # if(isinstance(var30, Model)):
                #     var22 = integerdivide(var30.method2693(), 4)
                #     if(var22 > 30):
                #         var22 = 30
                var22 = integerdivide(method2693(var30), 4)
                if(var22 > 30):
                    var22 = 30

                # else:
                #    This does happen...Like in Lumbridge

                for var23 in range(0, var9 + 1):
                    for var24 in range(0, var10 + 1):
                        if(var22 > field3831[var0][var23 + var1][var24 + var2]):
                            field3831[var0][var23 +
                                            var1][var24 + var2] = np.byte(var22)

            # if(var8.clipType != 0 and var7 is not None):
            #    var7.addObject(var1, var2, var9, var10,
            #                   var8.blocksProjectile)


@numba.jit(nopython=True, cache=False)
def loadTerrainObjects(uncryptedModelContents, regionobjects, field2025, regionvars, maxYregion, maxXregion, maxZregion, decodedObjectMapBffr, eastadjust, xlocal, northadjust, ylocal, field2520, field3831, tileSettings, objectDefinitions,
                       field749, field746, field738, field740, field752, field750, tileHeights, tiles):

    var5 = Buffer(decodedObjectMapBffr)
    var6 = -1
    while(True):
        var7 = var5.getUSmart()
        if(var7 == 0):
            break

        var6 += var7
        var8 = 0


        while(True):
            var9 = var5.getUSmart()
            if(var9 == 0):
                break

            var8 += var9 - 1
            var10 = var8 & 63
            var11 = var8 >> 6 & 63
            var12 = var8 >> 12
            var13 = var5.readUnsignedByte()
            var14 = var13 >> 2
            var15 = var13 & 3  # orientation
            var16 = var11 + eastadjust + xlocal
            var17 = var10 + northadjust + ylocal

            #if var16 < 35 or var16 > 36 or var17 < 51 or var17 > 52:
            #    continue

            if(var16 > 0 and var17 > 0 and var16 < 103 and var17 < 103):

                addObject(uncryptedModelContents, regionobjects, field2025, regionvars, maxYregion, maxXregion, maxZregion, var12, var16, var17,
                          var6, var15, var14, None, field2520, field3831, tileSettings, objectDefinitions,
                          field749, field746, field738, field740, field752, field750, tileHeights, tiles)


@jit(nopython=True, cache=False)
def getWallObjectHash(var1, var2, var3, tiles):
    var4 = getTile(var1, var2, var3, tiles)  # tiles[var1][var2][var3]

    # return var4 is not None and var4.wallObject is not None?var4.wallObject.hash:0
    if var4 is not None and var4.wallObject is not None:
        return var4.wallObject.hash
    else:
        return 0


@jit(nopython=True, cache=False)
def xyposToRegionID(x, y):

    regionX = x >> 6
    regionY = y >> 6
    regionId = regionX * 256 + regionY

    return regionId

import time

# @numba.jit(nopython=True, cache=False)
def loadChunk(uncryptedModelContents, regionobjects, field2025, regionvars, maxYregion, maxXregion, maxZregion, x, y, FileStore_, field2520, field3831, objectDefinitions,
              field749, field746, field738, field740, field752, field750, tileSettings, tileHeights,
              tileOverlayIds, tileUnderlayIds, tileOverlayPath, overlayRotations, regionIdToMapIndex, tiles):

    isDynamicRegion = False

    if(not isDynamicRegion):
        xlocal = 0  # -16  # -32
        ylocal = 0 #24 #0  # -16  # -32
        for eastadjust, northadjust in zip([-64, -64, -64, 0, 0, 0, 64, 64, 64], [-64, 0, 64, -64, 0, 64, -64, 0, 64]):
        #for eastadjust, northadjust in zip([0], [0]):
        #for eastadjust, northadjust in zip([0], [0]):
            x_ = x + eastadjust
            y_ = y + northadjust

            regionId = xyposToRegionID(x_, y_)
            floorMapId, objectMapId = regionIdToMapIndex[regionId]

            decodedObjectMapBffr = FileStore_.FileStoreRead(5, objectMapId)
            decodedFloorMapBffr = FileStore_.FileStoreRead(5, floorMapId)

            # # First load terrain, because tileHeights is used when placing objects
            loadTerrainFloor(decodedFloorMapBffr, eastadjust, xlocal, northadjust, ylocal,
                             tileSettings, tileHeights,
                             tileOverlayIds, tileUnderlayIds,
                             tileOverlayPath, overlayRotations)

            # Load objects onto terrain
            loadTerrainObjects(uncryptedModelContents, regionobjects, field2025, regionvars, maxYregion, maxXregion, maxZregion, decodedObjectMapBffr,
                              eastadjust, xlocal, northadjust, ylocal, field2520, field3831, tileSettings, objectDefinitions,
                              field749, field746, field738, field740, field752, field750, tileHeights, tiles)
                              
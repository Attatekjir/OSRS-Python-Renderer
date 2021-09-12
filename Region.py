from Tile import Tile
from utills import getTileID
from enum import Enum
from MathUtills import Graphics3DSINE, Graphics3DCOSINE
from numba import jit
from MathUtills import Graphics3DCOSINE, Graphics3DSINE
from MathUtills import integerdivide
from Occluder import Occluder
from SceneTilePaint import SceneTilePaint
import numpy as np
from SceneTileModel import SceneTileModel
from GameObject import GameObject
from expModel import drawModel
from utills import getTile, putTile
# How many files are there in a (uncompressed) data in cache
from Graphics3D import rasterTexture, rasterGouraud
from numba import int32, float32, boolean, short, int64
from numba.experimental import jitclass
from numba import jit

@jit(nopython=True, cache=False)
def method2897(var0, var1):

    var1 = (var0 & 127) * var1 >> 7

    if(var1 < 2):
        var1 = 2
    elif(var1 > 126):
        var1 = 126

    out = (var0 & 65408) + var1

    return out


@jitclass()
class Region:

    # SELF INIT
    cycle: int32
    screenCenterX: int32
    screenCenterZ: int32
    cameraX2: int32
    cameraY2: int32
    pitchSin: int32
    pitchCos: int32
    yawSin: int32
    yawCos: int32
    entityCount: int32
    tileUpdateCount: int32
    Scene_plane: int32
    field2013: int32
    minTileX: int32
    minTileZ: int32
    maxTileX: int32
    maxTileZ: int32
    cameraZ2: int32
    field1981: int32
    tileIDQueueSize: int32

    def __init__(self):

        pass

        # self.cycle = 0
        # self.screenCenterX = 0
        # self.screenCenterZ = 0
        # self.cameraX2 = 0
        # self.cameraY2 = 0
        # self.pitchSin = 0
        # self.pitchCos = 0
        # self.yawSin = 0
        # self.yawCos = 0
        # self.entityCount = 0
        # self.tileUpdateCount = 0
        # self.Scene_plane = 0
        # self.field2013 = 0
        # self.minTileX = 0
        # self.minTileZ = 0
        # self.maxTileX = 0
        # self.maxTileZ = 0
        # self.cameraZ2 = 0
        # self.field1981 = 0
        # self.tileIDQueueSize = 0

    def reset(self):

        self.cycle = 0
        self.screenCenterX = 0
        self.screenCenterZ = 0
        self.cameraX2 = 0
        self.cameraY2 = 0
        self.pitchSin = 0
        self.pitchCos = 0
        self.yawSin = 0
        self.yawCos = 0
        self.entityCount = 0
        self.tileUpdateCount = 0
        self.Scene_plane = 0
        self.field2013 = 0
        self.minTileX = 0
        self.minTileZ = 0
        self.maxTileX = 0
        self.maxTileZ = 0
        self.cameraZ2 = 0
        self.field1981 = 0
        self.tileIDQueueSize = 0


@jit(nopython=True, cache=False)
def drawRegion(colorPalette, field2027, field2040, TILE_WALL_DRAW_FLAGS_1, WALL_UNCULL_FLAGS_0, WALL_UNCULL_FLAGS_1, WALL_UNCULL_FLAGS_2, WALL_UNCULL_FLAGS_3,
               entityBuffer, visibilityMaps, field2025, regionvars, staticModel_, Deque_, tileCycles, minLevel, maxYregion, maxXregion, maxZregion, levelOccluders, levelOccluderCount, vertexSceneX, vertexSceneY, vertexSceneZ, tmpScreenX, tmpScreenY, var1, var2, var3, var4, var5, var6, Graphics3D_, tileHeights, tiles, textures, objectDefinitions):

    if(var1 < 0):
        var1 = 0
    elif(var1 >= maxXregion * 128):
        var1 = maxXregion * 128 - 1

    if(var3 < 0):
        var3 = 0
    elif(var3 >= maxZregion * 128):
        var3 = maxZregion * 128 - 1

    if(var4 < 128):
        var4 = 128
    elif(var4 > 383):
        var4 = 383

    regionvars.cycle += 1
    regionvars.pitchSin = Graphics3DSINE(var4)
    regionvars.pitchCos = Graphics3DCOSINE(var4)
    regionvars.yawSin = Graphics3DSINE(var5)
    regionvars.yawCos = Graphics3DCOSINE(var5)
    renderArea = visibilityMaps[integerdivide(
        var4 - 128, 32)][integerdivide(var5, 64)]
    regionvars.cameraX2 = var1
    regionvars.cameraY2 = var2
    regionvars.cameraZ2 = var3
    regionvars.screenCenterX = integerdivide(var1, 128)
    regionvars.screenCenterZ = integerdivide(var3, 128)
    regionvars.Scene_plane = var6
    regionvars.minTileX = regionvars.screenCenterX - 25
    if(regionvars.minTileX < 0):
        regionvars.minTileX = 0

    regionvars.minTileZ = regionvars.screenCenterZ - 25
    if(regionvars.minTileZ < 0):
        regionvars.minTileZ = 0

    regionvars.maxTileX = regionvars.screenCenterX + 25
    if(regionvars.maxTileX > maxXregion):
        regionvars.maxTileX = maxXregion

    regionvars.maxTileZ = regionvars.screenCenterZ + 25
    if(regionvars.maxTileZ > maxZregion):
        regionvars.maxTileZ = maxZregion

    updateOccluders(renderArea, field2025, regionvars,
                    levelOccluders, levelOccluderCount)
    regionvars.tileUpdateCount = 0

    for var7 in range(minLevel, maxYregion):
        for var9 in range(regionvars.minTileX, regionvars.maxTileX):
            for var10 in range(regionvars.minTileZ, regionvars.maxTileZ):
                var11 = getTile(var7, var9, var10, tiles)

                # var9 > 55 works, var9 > 60 does not
                # var10 > 40 works
                #tempbool = (var7 == 0 and var9 > 55 and var9 < 58 and var10 == 42)
                #tempbool = (var7 == 0 and var9 == 56 and var10 == 42)

                if(var11.physicalLevel <= var6 and (renderArea[var9 - regionvars.screenCenterX + 25][var10 - regionvars.screenCenterZ + 25] or tileHeights[var7][var9][var10] - var2 >= 2000)):

                    # minus999 = 1
                    # if var7 != 0 or var9 < 35 or var9 > 36 or var10 < 51 or var10 > 52 + minus999:
                    #     ##print("CHANGED THIS HERE, WHOLE IF STATEMENT")
                    #     var11.draw = False
                    #     var11.visible = False
                    #     var11.wallCullDirection = 0
                    #     continue

                    var11.draw = True
                    var11.visible = True
                    var11.drawEntities = var11.entityCount > 0

                    ##print("Init drawEntities: ", var11.drawEntities, var11.entityCount, var11.entityCount > 0)

                    regionvars.tileUpdateCount += 1

                    #print(var7, var9, var10)

                else:

                    var11.draw = False
                    var11.visible = False
                    var11.wallCullDirection = 0

    #print("TILEUPDATECOUNT", regionvars.tileUpdateCount)

    for var7 in range(minLevel, maxYregion):

        for var9 in range(-25, 1):
            var10 = var9 + regionvars.screenCenterX
            var16 = regionvars.screenCenterX - var9

            if(var10 >= regionvars.minTileX or var16 < regionvars.maxTileX):

                for var12 in range(-25, 1):
                    var13 = var12 + regionvars.screenCenterZ
                    var14 = regionvars.screenCenterZ - var12

                    if(var10 >= regionvars.minTileX):
                        if(var13 >= regionvars.minTileZ):
                            # tiles[var7][var10][var13]
                            var15 = getTile(var7, var10, var13, tiles)

                            if(var15.draw):
                                #print("1 draw")
                                draw(colorPalette, field2027, field2040, TILE_WALL_DRAW_FLAGS_1, WALL_UNCULL_FLAGS_0, WALL_UNCULL_FLAGS_1, WALL_UNCULL_FLAGS_2, WALL_UNCULL_FLAGS_3,
                                     entityBuffer, field2025, regionvars, staticModel_, Deque_, tileCycles, maxYregion, maxXregion, maxZregion, vertexSceneX, vertexSceneY, vertexSceneZ, tmpScreenX, tmpScreenY,
                                     var15, True, Graphics3D_, tileHeights, tiles, textures, objectDefinitions)

                        if(var14 < regionvars.maxTileZ):
                            # tiles[var7][var10][var14]
                            var15 = getTile(var7, var10, var14, tiles)
                            if(var15.draw):
                                #print("2 draw")
                                draw(colorPalette, field2027, field2040, TILE_WALL_DRAW_FLAGS_1, WALL_UNCULL_FLAGS_0, WALL_UNCULL_FLAGS_1, WALL_UNCULL_FLAGS_2, WALL_UNCULL_FLAGS_3,
                                     entityBuffer, field2025, regionvars, staticModel_, Deque_, tileCycles, maxYregion, maxXregion, maxZregion, vertexSceneX, vertexSceneY, vertexSceneZ, tmpScreenX, tmpScreenY,
                                     var15, True, Graphics3D_, tileHeights, tiles, textures, objectDefinitions)

                    if(var16 < regionvars.maxTileX):
                        if(var13 >= regionvars.minTileZ):
                            # tiles[var7][var16][var13]
                            var15 = getTile(var7, var16, var13, tiles)
                            if(var15.draw):
                                #print("3 draw")
                                draw(colorPalette, field2027, field2040, TILE_WALL_DRAW_FLAGS_1, WALL_UNCULL_FLAGS_0, WALL_UNCULL_FLAGS_1, WALL_UNCULL_FLAGS_2, WALL_UNCULL_FLAGS_3,
                                     entityBuffer, field2025, regionvars, staticModel_, Deque_, tileCycles, maxYregion, maxXregion, maxZregion, vertexSceneX, vertexSceneY, vertexSceneZ, tmpScreenX, tmpScreenY,
                                     var15, True, Graphics3D_, tileHeights, tiles, textures, objectDefinitions)

                        if(var14 < regionvars.maxTileZ):
                            # tiles[var7][var16][var14]
                            var15 = getTile(var7, var16, var14, tiles)
                            if(var15.draw):
                                #print("4 draw")
                                draw(colorPalette, field2027, field2040, TILE_WALL_DRAW_FLAGS_1, WALL_UNCULL_FLAGS_0, WALL_UNCULL_FLAGS_1, WALL_UNCULL_FLAGS_2, WALL_UNCULL_FLAGS_3,
                                     entityBuffer, field2025, regionvars, staticModel_, Deque_, tileCycles, maxYregion, maxXregion, maxZregion, vertexSceneX, vertexSceneY, vertexSceneZ, tmpScreenX, tmpScreenY,
                                     var15, True, Graphics3D_, tileHeights, tiles, textures, objectDefinitions)

                    if(regionvars.tileUpdateCount == 0):
                        #print("Done Drawing1")
                        checkClick = False
                        return

    for var7 in range(minLevel, maxYregion):

        for var9 in range(-25, 1):
            var10 = var9 + regionvars.screenCenterX
            var16 = regionvars.screenCenterX - var9
            if(var10 >= regionvars.minTileX or var16 < regionvars.maxTileX):

                for var12 in range(-25, 1):
                    var13 = var12 + regionvars.screenCenterZ
                    var14 = regionvars.screenCenterZ - var12
                    if(var10 >= regionvars.minTileX):
                        if(var13 >= regionvars.minTileZ):
                            # tiles[var7][var10][var13]
                            var15 = getTile(var7, var10, var13, tiles)
                            if(var15.draw):
                                #print("5 draw")
                                draw(colorPalette, field2027, field2040, TILE_WALL_DRAW_FLAGS_1, WALL_UNCULL_FLAGS_0, WALL_UNCULL_FLAGS_1, WALL_UNCULL_FLAGS_2, WALL_UNCULL_FLAGS_3,
                                     entityBuffer, field2025, regionvars, staticModel_, Deque_, tileCycles, maxYregion, maxXregion, maxZregion, vertexSceneX, vertexSceneY, vertexSceneZ, tmpScreenX, tmpScreenY, var15, False,
                                     Graphics3D_, tileHeights, tiles, textures, objectDefinitions)

                        if(var14 < regionvars.maxTileZ):
                            # tiles[var7][var10][var14]
                            var15 = getTile(var7, var10, var14, tiles)
                            if(var15.draw):
                                #print("6 draw")
                                draw(colorPalette, field2027, field2040, TILE_WALL_DRAW_FLAGS_1, WALL_UNCULL_FLAGS_0, WALL_UNCULL_FLAGS_1, WALL_UNCULL_FLAGS_2, WALL_UNCULL_FLAGS_3,
                                     entityBuffer, field2025, regionvars, staticModel_, Deque_, tileCycles, maxYregion, maxXregion, maxZregion, vertexSceneX, vertexSceneY, vertexSceneZ, tmpScreenX, tmpScreenY, var15, False,
                                     Graphics3D_, tileHeights, tiles, textures, objectDefinitions)

                    if(var16 < regionvars.maxTileX):
                        if(var13 >= regionvars.minTileZ):
                            # tiles[var7][var16][var13]
                            var15 = getTile(var7, var16, var13, tiles)
                            if(var15.draw):
                                #print("7 draw")
                                draw(colorPalette, field2027, field2040, TILE_WALL_DRAW_FLAGS_1, WALL_UNCULL_FLAGS_0, WALL_UNCULL_FLAGS_1, WALL_UNCULL_FLAGS_2, WALL_UNCULL_FLAGS_3,
                                     entityBuffer, field2025, regionvars, staticModel_, Deque_, tileCycles, maxYregion, maxXregion, maxZregion, vertexSceneX, vertexSceneY, vertexSceneZ, tmpScreenX, tmpScreenY, var15, False,
                                     Graphics3D_, tileHeights, tiles, textures, objectDefinitions)

                        if(var14 < regionvars.maxTileZ):
                            # tiles[var7][var16][var14]
                            var15 = getTile(var7, var16, var14, tiles)
                            if(var15.draw):
                                #print("8 draw")
                                draw(colorPalette, field2027, field2040, TILE_WALL_DRAW_FLAGS_1, WALL_UNCULL_FLAGS_0, WALL_UNCULL_FLAGS_1, WALL_UNCULL_FLAGS_2, WALL_UNCULL_FLAGS_3,
                                     entityBuffer, field2025, regionvars, staticModel_, Deque_, tileCycles, maxYregion, maxXregion, maxZregion, vertexSceneX, vertexSceneY, vertexSceneZ, tmpScreenX, tmpScreenY, var15, False,
                                     Graphics3D_, tileHeights, tiles, textures, objectDefinitions)

                    if(regionvars.tileUpdateCount == 0):
                        #print("Done Drawing2")
                        checkClick = False
                        return

    #print("Done Drawing3")

    checkClick = False

    # Is put in the other isOccluded function
    # def isOccluded(field2025, regionvars, self, var1,  var2,  var3,  var4):
    #     if(not isTileOccluded(field2025, regionvars, tileCycles, var1, var2, var3)):
    #         return False
    #     else:
    #         var5 = var2 << 7
    #         var6 = var3 << 7
    #         return isOccluded(field2025, regionvars, var5 + 1, tileHeights[var1][var2][var3] - var4, var6 + 1) and \
    #             isOccluded(field2025, regionvars, var5 + 128 - 1, tileHeights[var1][var2 + 1][var3] - var4, var6 + 1) and \
    #             isOccluded(field2025, regionvars, var5 + 128 - 1, tileHeights[var1][var2 + 1][var3 + 1] - var4, var6 + 128 - 1) and \
    #             isOccluded(field2025, regionvars, var5 + 1, tileHeights[var1][var2][var3 + 1] -
    #                             var4, var6 + 128 - 1)


# public boolean method2863(var1, var2, var3, var4, var5, final Renderable var6, var7, var8, final boolean var9) :
# if(var6 is None) :
# return True
# else :
# int var10 = var2 - var5
# int var11 = var3 - var5
# int var12 = var5 + var2
# int var13 = var3 + var5
# if(var9) :
# if(var7 > 640 and var7 < 1408) :
# var13 += 128


# if(var7 > 1152 and var7 < 1920) :
# var12 += 128


# if(var7 > 1664 or var7 < 384) :
# var11 -= 128


# if(var7 > 128 and var7 < 896) :
# var10 -= 128


# var10 /= 128
# var11 /= 128
# var12 /= 128
# var13 /= 128
# return addEntityMarker(var1, var10, var11, var12 - var10 + 1, var13 - var11 + 1, var2, var3, var4, var6, var7, True, var8, 0)


# public boolean method2871(var1, var2, var3, var4, final Renderable var6, var7, var8, var9, var10, var11, var12) :
# return var6 is None or addEntityMarker(var1, var9, var10, var11 - var9 + 1, var12 - var10 + 1, var2, var3, var4, var6, var7, True, var8, 0)

    # def clearEntities(self, field2025, regionvars, tiles):
    #     for var1 in range(0, regionvars.entityCount):
    #         var2 = regionobjects[var1]
    #         removeEntity(var2, tiles)
    #         regionobjects[var1] = None

    #     regionvars.entityCount = 0

    # def method2868(self, var1, var2, var3, var4, tiles):
    #     var5 = getTile(var1, var2, var3, tiles) #tiles[var1][var2][var3]
    #     if(var5 is not None):
    #         var6 = var5.decorativeObject
    #         if(var6 is not None):
    #             var6.offsetX = integerdivide(var4 * var6.offsetX, 16)
    #             var6.offsetY = integerdivide(var4 * var6.offsetY, 16)


# public void removeBoundaryObject(var1, var2, var3) :
# final Tile var4 = tiles[var1][var2][var3]
# if(var4 is not None) :
# var4.wallObject = None


# public void removeWallDecoration(var1, var2, var3) :
# final Tile var4 = tiles[var1][var2][var3]
# if(var4 is not None) :
# var4.decorativeObject = None


# public void method3035(var1, var2, var3) :
# final Tile var4 = tiles[var1][var2][var3]
# if(var4 is not None) :
# for(int var5 = 0 var5 < var4.entityCount ++var5) :
# final GameObject var6 = var4.objects[var5]
# if((var6.hash >> 29 & 3) == 2 and var2 == var6.relativeX and var3 == var6.relativeY) :
# self.removeEntity(var6)
# return


# public void removeFloorDecoration(var1, var2, var3) :
# final Tile var4 = tiles[var1][var2][var3]
# if(var4 is not None) :
# var4.groundObject = None


# public void removeGroundItemPile(var1, var2, var3) :
# final Tile var4 = tiles[var1][var2][var3]
# if(var4 is not None) :
# var4.itemLayer = None


# public WallObject method2874(var1, var2, var3) :
# final Tile var4 = tiles[var1][var2][var3]
# return var4 is None?null:var4.wallObject


# public DecorativeObject method2928(var1, var2, var3) :
# final Tile var4 = tiles[var1][var2][var3]
# return var4 is None?null:var4.decorativeObject


# public GameObject method2876(var1, var2, var3) :
# final Tile var4 = tiles[var1][var2][var3]
# if (var4 is not None) :
# for (int var5 = 0 var5 < var4.entityCount ++var5) :
# final GameObject var6 = var4.objects[var5]
# if ((var6.hash >> 29 & 3) == 2 and var2 == var6.relativeX and var3 == var6.relativeY) :
# return var6


# return None


# public GroundObject getFloorDecoration(var1, var2, var3) :
# final Tile var4 = tiles[var1][var2][var3]
# return var4 is not None and var4.groundObject is not None?var4.groundObject:null

    # def getWallObjectHash(self, var1, var2, var3, tiles):
    #     var4 = tiles[var1][var2][var3]

    #     # return var4 is not None and var4.wallObject is not None?var4.wallObject.hash:0
    #     if var4 is not None and var4.wallObject is not None:
    #         return var4.wallObject.hash
    #     else:
    #         return 0


# public int method2879(var1, var2, var3) :
# final Tile var4 = tiles[var1][var2][var3]
# return var4 is not None and var4.decorativeObject is not None?var4.decorativeObject.hash:0


# public int method2888(var1, var2, var3) :
# final Tile var4 = tiles[var1][var2][var3]
# if (var4 is not None) :
# for (int var5 = 0 var5 < var4.entityCount ++var5) :
# final GameObject var6 = var4.objects[var5]
# if ((var6.hash >> 29 & 3) == 2 and var2 == var6.relativeX and var3 == var6.relativeY) :
# return var6.hash


# return 0


# public int getGroundObjectHash(var1, var2, var3) :
# final Tile var4 = tiles[var1][var2][var3]
# return var4 is not None and var4.groundObject is not None?var4.groundObject.hash:0


# public int getObjectFlags(var1, var2, var3, var4) :
# final Tile var5 = tiles[var1][var2][var3]
# if(var5 is None) :
# return -1
# else if(var5.wallObject is not None and var5.wallObject.hash == var4) :
# return var5.wallObject.config & 255
# else if(var5.decorativeObject is not None and var5.decorativeObject.hash == var4) :
# return var5.decorativeObject.renderInfoBitPacked & 255
# else if(var5.groundObject is not None and var5.groundObject.hash == var4) :
# return var5.groundObject.renderInfoBitPacked & 255
# else :
# for(int var6 = 0 var6 < var5.entityCount ++var6) :
# if(var4 == var5.objects[var6].hash) :
# return var5.objects[var6].flags & 255


# return -1

    # # So basically we have already lighted the model when we loaded it...
    # # So no need to do this as it expects ModelData instead of Models (which it is currently)
    # def applyLighting(self, var1, var2, var3, tileHeights, tiles):

    #     for var4 in range(0, maxYregion):
    #         for var5 in range(0, maxXregion):
    #             for var6 in range(0, maxZregion):
    #                 var7 = getTile(var4, var5, var6, tiles) # tiles[var4][var5][var6]
    #                 if(var7 is not None):
    #                     var8 = var7.wallObject
    #                     if var8 is not None: #and isinstance(var8.renderable1, ModelData):
    #                         var9 = var8.renderable1 #ModelData(var8.renderable1)

    #                         self.method2894(var9, var4, var5, var6, 1, 1, tileHeights, tiles)

    #                         #if(isinstance(var8.renderable2, ModelData)):
    #                         var10 = var8.renderable2 #ModelData(var8.renderable2)
    #                         self.method2894(var10, var4, var5, var6, 1, 1, tileHeights, tiles)
    #                         method2608(staticModelData_, var9, var10, 0, 0, 0, False)

    #                         var8.renderable2 = light(var10,
    #                             var10.field1731, var10.contrast, var1, var2, var3)

    #                         var8.renderable1 = light(var9,
    #                             var9.field1731, var9.contrast, var1, var2, var3)

    #                         #print("Ever?>")

    #                     # for(int var12 = 0 var12 < var7.entityCount ++var12) :
    #                     for var12 in range(0, var7.entityCount):
    #                         #print("EVER?")
    #                         var14 = var7.objects[var12]
    #                         #if(var14 is not None and isinstance(var14.renderable, ModelData)):
    #                         var11 = var14.renderable #ModelData(var14.renderable)
    #                         self.method2894(var11, var4, var5, var6, var14.offsetX -
    #                                         var14.relativeX + 1, var14.offsetY - var14.relativeY + 1, tileHeights, tiles)
    #                         var14.renderable = light(var11,
    #                             var11.field1731, var11.contrast, var1, var2, var3)

    #                     var13 = var7.groundObject
    #                     if(var13 is not None):
    #                         #print("EVER?!!!!")
    #                         # ModelData(var13.renderable)
    #                         var10 = var13.renderable

    #                         self.method2966(var10, var4, var5, var6, tiles)
    #                         var13.renderable = light(var10,
    #                             var10.field1731, var10.contrast, var1, var2, var3)

    # These two

    # def method2966(self, staticModelData_, maxYregion, maxXregion, maxZregion, var1, var2, var3, var4, tiles):
    #     if(var3 < maxXregion):
    #         # tiles[var2][var3 + 1][var4]
    #         var5 = getTile(var2, var3 + 1, var4, tiles)
    #         if(var5 is not None and var5.groundObject is not None):
    #             var6 = var5.groundObject.renderable
    #             #self.ModelData_.method2608(var1, var6, 128, 0, 0, True)
    #             method2608(staticModelData_, var1, var6, 128, 0, 0, True)

    #     if(var4 < maxXregion):
    #         # tiles[var2][var3][var4 + 1]
    #         var5 = getTile(var2, var3, var4 + 1, tiles)
    #         if(var5 is not None and var5.groundObject is not None):
    #             var6 = var5.groundObject.renderable
    #             #self.ModelData_.method2608(var1, var6, 0, 0, 128, True)
    #             method2608(staticModelData_, var1, var6, 0, 0, 128, True)

    #     if(var3 < maxXregion and var4 < maxZregion):
    #         # tiles[var2][var3 + 1][var4 + 1]
    #         var5 = getTile(var2, var3 + 1, var4 + 1, tiles)
    #         if(var5 is not None and var5.groundObject is not None):
    #             var6 = var5.groundObject.renderable
    #             #self.ModelData_.method2608(var1, var6, 128, 0, 128, True)
    #             method2608(staticModelData_, var1, var6, 0, 0, 128, True)

    #     if(var3 < maxXregion and var4 > 0):
    #         # tiles[var2][var3 + 1][var4 - 1]
    #         var5 = getTile(var2, var3 + 1, var4 - 1, tiles)
    #         if(var5 is not None and var5.groundObject is not None):
    #             var6 = var5.groundObject.renderable
    #             #self.ModelData_.method2608(var1, var6, 128, 0, -128, True)
    #             method2608(staticModelData_, var1, var6, 0, 0, 128, True)

    # def method2894(self, staticModelData_, maxYregion, maxXregion, maxZregion, var1, var2, var3, var4, var5, var6, tileHeights, tiles):
    #     var7 = True
    #     var8 = var3
    #     var9 = var3 + var5
    #     var10 = var4 - 1
    #     var11 = var4 + var6

    #     for var12 in range(var2, var2 + 2):
    #         if(var12 != maxYregion):
    #             for var13 in range(var8, var9 + 1):
    #                 if(var13 >= 0 and var13 < maxXregion):
    #                     for var14 in range(var10, var11 + 1):
    #                         if(var14 >= 0 and var14 < maxZregion and (var7 is False or var13 >= var9 or var14 >= var11 or var14 < var4 and var3 != var13)):
    #                             # tiles[var12][var13][var14]
    #                             var15 = getTile(var12, var13, var14, tiles)
    #                             if(var15 is not None):
    #                                 var16 = integerdivide((tileHeights[var12][var13 + 1][var14] + tileHeights[var12][var13 + 1][var14 + 1] + tileHeights[var12][var13][var14] + tileHeights[var12][var13][var14 + 1]), 4) - \
    #                                     integerdivide((tileHeights[var2][var3 + 1][var4] + tileHeights[var2][var3][var4] +
    #                                                   tileHeights[var2][var3 + 1][var4 + 1] + tileHeights[var2][var3][var4 + 1]), 4)
    #                                 var17 = var15.wallObject
    #                                 if(var17 is not None):
    #                                     # if(isinstance(var17.renderable1, ModelData)):
    #                                     #     var18 = ModelData(
    #                                     #         var17.renderable1)
    #                                     #     method2608(staticModelData_, var1, var18, (1 - var5) * 64 + (
    #                                     #         var13 - var3) * 128, var16, (var14 - var4) * 128 + (1 - var6) * 64, var7)
    #                                     var18 = var17.renderable1
    #                                     method2608(staticModelData_, var1, var18, (1 - var5) * 64 + (
    #                                         var13 - var3) * 128, var16, (var14 - var4) * 128 + (1 - var6) * 64, var7)

    #                                     # if(isinstance(var17.renderable2, ModelData)):
    #                                     #     var18 = ModelData(var17.renderable2)
    #                                     #     method2608(staticModelData_, var1, var18, (1 - var5) * 64 + (
    #                                     #         var13 - var3) * 128, var16, (var14 - var4) * 128 + (1 - var6) * 64, var7)
    #                                     var18 = var17.renderable2
    #                                     method2608(staticModelData_, var1, var18, (1 - var5) * 64 + (
    #                                         var13 - var3) * 128, var16, (var14 - var4) * 128 + (1 - var6) * 64, var7)

    #                                 for var23 in range(0, var15.entityCount):
    #                                     var19 = var15.objects[var23]
    #                                     # and isinstance(var19.renderable, ModelData)):
    #                                     if(var19 is not None):
    #                                         #var20 = ModelData(var19.renderable)
    #                                         var20 = var19.renderable
    #                                         var21 = var19.offsetX - var19.relativeX + 1
    #                                         var22 = var19.offsetY - var19.relativeY + 1
    #                                         method2608(staticModelData_, var1, var20, (var21 - var5) * 64 + (
    #                                             var19.relativeX - var3) * 128, var16, (var19.relativeY - var4) * 128 + (var22 - var6) * 64, var7)

    #             var8 -= 1
    #             var7 = False

    # def drawTile(self, var1, var2, var3, var4, var5, var6, tiles):

    #     var7 = getTile(var4, var5, var6, tiles) #tiles[var4][var5][var6]
    #     if(var7 is not None):
    #         var8 = var7.paint
    #         if(var8 is not None):
    #             var9 = var8.rgb
    #             if(var9 != 0):
    #                 for var10 in range(0, 4):
    #                     var1[var2] = var9
    #                     var1[var2 + 1] = var9
    #                     var1[var2 + 2] = var9
    #                     var1[var2 + 3] = var9
    #                     var2 += var3

    #         else:
    #             var18 = var7.overlay
    #             if(var18 is not None):
    #                 var10 = var18.shape
    #                 var11 = var18.rotation
    #                 var12 = var18.underlay
    #                 var13 = var18.overlay
    #                 var14 = self.TILE_MASK_2D[var10]
    #                 var15 = self.TILE_ROTATION_2D[var11]
    #                 var16 = 0
    #                 if(var12 != 0):
    #                     for var17 in range(0, 4):

    #                         # var1[var2] = var14[var15[var16++]] == 0?var12:var13
    #                         if var14[var15[var16]] == 0:
    #                             var1[var2] = var12
    #                         else:
    #                             var1[var2] = var13
    #                         var16 += 1

    #                         # var1[var2 + 1] = var14[var15[var16++]] == 0?var12:var13
    #                         if var14[var15[var16]] == 0:
    #                             var1[var2 + 1] = var12
    #                         else:
    #                             var1[var2 + 1] = var13
    #                         var16 += 1

    #                         # var1[var2 + 2] = var14[var15[var16++]] == 0?var12:var13
    #                         if var14[var15[var16]] == 0:
    #                             var1[var2 + 2] = var12
    #                         else:
    #                             var1[var2 + 2] = var13
    #                         var16 += 1

    #                         # var1[var2 + 3] = var14[var15[var16++]] == 0?var12:var13
    #                         if var14[var15[var16]] == 0:
    #                             var1[var2 + 3] = var12
    #                         else:
    #                             var1[var2 + 3] = var13
    #                         var16 += 1

    #                         var2 += var3

    #                 else:

    #                     for var17 in range(0, 4):
    #                         if(var14[var15[var16]] != 0):
    #                             var16 += 1
    #                             var1[var2] = var13

    #                         if(var14[var15[var16]] != 0):
    #                             var16 += 1
    #                             var1[var2 + 1] = var13

    #                         if(var14[var15[var16]] != 0):
    #                             var16 += 1
    #                             var1[var2 + 2] = var13

    #                         if(var14[var15[var16]] != 0):
    #                             var16 += 1
    #                             var1[var2 + 3] = var13

    #                         var2 += var3

    # def method2889(self, var1, var2, var3, var4):
    #     if(self.method2906() is False or var4):
    #         self.checkClick = True
    #         self.viewportWalking = var4
    #         regionvars.field2013 = var1
    #         self.mouseX2 = var2
    #         self.mouseY2 = var3
    #         self.selectedRegionTileX = -1
    #         self.selectedRegionTileY = -1

    # def method2997(self):
    #     self.viewportWalking = True


# public static boolean method2906() :
# return viewportWalking and selectedRegionTileX != -1


# public static void method2892() :
# selectedRegionTileX = -1
# viewportWalking = False


# private static int method2897(var0, int var1) :
# var1 = (var0 & 127) * var1 >> 7
# if(var1 < 2) :
# var1 = 2
# else if(var1 > 126) :
# var1 = 126


# return (var0 & 65408) + var1


# private static boolean method2898(var0, var1, var2, var3, var4, var5, var6, var7) :
# if(var1 < var2 and var1 < var3 and var1 < var4) :
# return False
# else if(var1 > var2 and var1 > var3 and var1 > var4) :
# return False
# else if(var0 < var5 and var0 < var6 and var0 < var7) :
# return False
# else if(var0 > var5 and var0 > var6 and var0 > var7) :
# return False
# else :
# var8 = (var1 - var2) * (var6 - var5) - (var0 - var5) * (var3 - var2)
# var9 = (var7 - var6) * (var1 - var3) - (var0 - var6) * (var4 - var3)
# var10 = (var5 - var7) * (var1 - var4) - (var2 - var4) * (var0 - var7)
# return var8 == 0?(var9 == 0 or (var9 < 0 ? var10 <= 0 : var10 >= 0)):(var8 < 0?var9 <= 0 and var10 <= 0:var9 >= 0 and var10 >= 0)


# public static int[] method2905(int var0, var1, int var2) :
# int var3 = var0 * yawCos + var2 * yawSin >> 16
# var2 = var2 * yawCos - var0 * yawSin >> 16
# var0 = var3
# var3 = pitchCos * var1 - var2 * pitchSin >> 16
# var2 = pitchSin * var1 + var2 * pitchCos >> 16
# var2 |= 1
# var4 = var0 * Graphics3D_.Rasterizer3D_zoom / var2 + Graphics3D_.centerX + Rasterizer2D.draw_region_x
# var5 = Graphics3D_.Rasterizer3D_zoom * var3 / var2 + Graphics3D_.centerY + Rasterizer2D.drawingAreaTop
# return new int[]:var4, var5

@jit(nopython=True, cache=False)
def setBridge(var1, var2, tiles):
    var3 = getTile(0, var1, var2, tiles)  # tiles[0][var1][var2]

    for var4 in range(0, 3):
        tile_ = getTile(var4 + 1, var1, var2, tiles)
        putTile(tile_, var4, var1, var2, tiles)
        # tiles[var4][var1][var2] # tiles[var4 + 1][var1][var2]
        # getTile(var4, var1, var2, tiles) # tiles[var4][var1][var2]
        var5 = tile_
        if(var5 is not None):
            var5.plane -= 1

            for var6 in range(0, var5.entityCount):
                var7 = var5.objects[var6]
                if((var7.hash >> 29 & 3) == 2 and var7.relativeX == var1 and var2 == var7.relativeY):
                    var7.plane -= 1

    # if(tiles[0][var1][var2] is None):
    #    pass
    #    #tiles[0][var1][var2] = Tile(0, var1, var2)

    tile_ = getTile(0, var1, var2, tiles)
    tile_.bridge = var3
    #tiles[0][var1][var2].bridge = var3
    #tiles[3][var1][var2] = None


@jit(nopython=True, cache=False)
def removeEntity(var1, tiles):

    for var2 in range(var1.relativeX, var1.offsetX + 1):
        for var3 in range(var1.relativeY, var1.offsetY + 1):
            # tiles[var1.plane][var2][var3]
            var4 = getTile(var1.plane, var2, var3, tiles)
            if(var4 is not None):
                for var5 in range(0, var4.entityCount):
                    if(var4.objects[var5] == var1):
                        var4.entityCount -= 1

                        for var6 in range(var5, var4.entityCount):
                            var4.objects[var6] = var4.objects[var6 + 1]
                            var4.entityFlags[var6] = var4.entityFlags[var6 + 1]

                        var4.objects[var4.entityCount] = None
                        break

                var4.flags = 0

                for var5 in range(0, var4.entityCount):
                    var4.flags |= var4.entityFlags[var5]


@jit(nopython=True, cache=False)
def addTile(field1790, field1791, var1, var2, var3, var4, var5, var6, var7, var8, var9,
            var10, var11, var12, var13, var14, var15,
            var16, var17, var18, var19, var20, tiles):

    tile_ = getTile(var1, var2, var3, tiles)

    if(var4 == 0):

        var21 = SceneTilePaint(var11, var12, var13,
                               var14, -1, var19, False)

        # Tiles already exist...
        # var22 = var1
        # while var22 >= 0:
        #     if(tiles[var22][var2][var3] is None):
        #         tiles[var22][var2][var3] = Tile(var22, var2, var3)

        #     var22 -= 1

        #tiles[var1][var2][var3].paint = var21
        tile_.paint = var21

    elif(var4 != 1):
        var23 = SceneTileModel(field1790, field1791, var4, var5, var6, var2, var3, var7, var8, var9, var10,
                               var11, var12, var13, var14, var15, var16, var17, var18, var19, var20)

        # Tiles already exist...
        # var22 = var1
        # while var22 >= 0:
        #     if(tiles[var22][var2][var3] is None):
        #         tiles[var22][var2][var3] = Tile(var22, var2, var3)
        #     var22 -= 1

        #tiles[var1][var2][var3].overlay = var23
        tile_.overlay = var23

    else:  # var4 == 1
        var21 = SceneTilePaint(var15, var16, var17, var18, var6,
                               var20, var8 == var7 and var7 == var9 and var10 == var7)

        # Tiles already exist...
        # var22 = var1
        # while var22 >= 0:
        #     if(tiles[var22][var2][var3] is None):
        #         tiles[var22][var2][var3] = Tile(var22, var2, var3)
        #     var22 -= 1

        #tiles[var1][var2][var3].paint = var21
        tile_.paint = var21


@jit(nopython=True, cache=False)
def method2936(var0, var1, var2, yawSin, yawCos, pitchSin, pitchCos, field2042, field2041, field1999, field2043, field1996, field2039):
    var3 = var0 * yawCos + var2 * yawSin >> 16
    var4 = var2 * yawCos - var0 * yawSin >> 16
    var5 = var4 * pitchCos + pitchSin * var1 >> 16
    var6 = pitchCos * var1 - var4 * pitchSin >> 16
    if(var5 >= 50 and var5 <= 3500):
        var7 = integerdivide(var3 * 390, var5) + field1996
        var8 = integerdivide(var6 * 390, var5) + field2039
        return var7 >= field2042 and var7 <= field1999 and var8 >= field2041 and var8 <= field2043
    else:
        return False


@jit(nopython=True, cache=False)
def buildVisibilityMaps(var1, var2, var3, var4):

    field2042 = 0 # static
    field2041 = 0 # static
    field1999 = var3
    field2043 = var4
    field1996 = integerdivide(var3, 2)
    field2039 = integerdivide(var4, 2)

    # This for loop normally outside of function, passed through var0
    var0 = np.zeros(shape=(9), dtype=np.int32)  # [0] * 9
    for var10 in range(0, 9):
        var11 = var10 * 32 + 15 + 128
        var12 = var11 * 3 + 600
        var13 = Graphics3DSINE(var11)
        var0[var10] = var13 * var12 >> 16

    var5 = np.zeros(shape=(9, 32, 53, 53), dtype=np.bool8)
    visibilityMaps = np.zeros(shape=(9, 32, 51, 51), dtype=np.bool8)

    for var6 in range(128, 384 + 1, 32):
        for var7 in range(0, 2048, 64):
            pitchSin = Graphics3DSINE(var6)
            pitchCos = Graphics3DCOSINE(var6)
            yawSin = Graphics3DSINE(var7)
            yawCos = Graphics3DCOSINE(var7)
            var8 = integerdivide(var6 - 128, 32)
            var9 = integerdivide(var7, 64)

            for var10 in range(-26, 26 + 1):
                for var11 in range(-26, 26 + 1):
                    var12 = var10 * 128
                    var13 = var11 * 128
                    var14 = False

                    for var15 in range(-var1, var2 + 1, 128):
                        if(method2936(var12, var0[var8] + var15, var13, yawSin, yawCos, pitchSin, pitchCos, field2042, field2041, field1999, field2043, field1996, field2039)):
                            var14 = True
                            break

                    var5[var8][var9][var10 + 1 +
                                     25][var11 + 1 + 25] = var14

    for var6 in range(0, 8):
        for var7 in range(0, 32):
            for var8 in range(-25, 25):
                for var9 in range(-25, 25):
                    var16 = False

                    breaklabel76 = False
                    for var11 in range(-1, 1 + 1):
                        for var12 in range(-1, 1 + 1):
                            if(var5[var6][var7][var8 + var11 + 1 + 25][var9 + var12 + 1 + 25]):
                                var16 = True
                                breaklabel76 = True
                                break

                            if(var5[var6][(var7 + 1) % 31][var8 + var11 + 1 + 25][var9 + var12 + 1 + 25]):
                                var16 = True
                                breaklabel76 = True
                                break

                            if(var5[var6 + 1][var7][var8 + var11 + 1 + 25][var9 + var12 + 1 + 25]):
                                var16 = True
                                breaklabel76 = True
                                break

                            if(var5[var6 + 1][(var7 + 1) % 31][var8 + var11 + 1 + 25][var9 + var12 + 1 + 25]):
                                var16 = True
                                breaklabel76 = True
                                break

                        if breaklabel76:
                            break

                    visibilityMaps[var6][var7][var8 + 25][var9 + 25] = var16

    return visibilityMaps


@jit(nopython=True, cache=False)
def addOcclude(levelOccluders, levelOccluderCount, var0, var1, var2, var3, var4, var5, var6, var7):
    var8 = Occluder()
    var8.minTileX = integerdivide(var2, 128)
    var8.maxTIleX = integerdivide(var3, 128)
    var8.minTileZ = integerdivide(var4, 128)
    var8.maxTileZ = integerdivide(var5, 128)
    var8.type = var1
    var8.minX = var2
    var8.maxX = var3
    var8.minZ = var4
    var8.maxZ = var5
    var8.minY = var6
    var8.maxY = var7
    levelOccluders[var0][levelOccluderCount[var0]] = var8
    levelOccluderCount[var0] += 1


@jit(nopython=True, cache=False)
def isOccluded(field2025, regionvars, var1, var2, var3):

    # Is in another function isOccluded4
    # if var4 is not None:
    #     if(not isTileOccluded(field2025, regionvars, tileCycles, var1, var2, var3)):
    #         return False
    #     else:
    #         var5 = var2 << 7
    #         var6 = var3 << 7
    #         return isOccluded(field2025, regionvars, var5 + 1, tileHeights[var1][var2][var3] - var4, var6 + 1) and \
    #             isOccluded(field2025, regionvars, var5 + 128 - 1, tileHeights[var1][var2 + 1][var3] - var4, var6 + 1) and \
    #             isOccluded(field2025, regionvars, var5 + 128 - 1, tileHeights[var1][var2 + 1][var3 + 1] - var4, var6 + 128 - 1) and \
    #             isOccluded(field2025, regionvars, var5 + 1, tileHeights[var1][var2][var3 + 1] -
    #                             var4, var6 + 128 - 1)

    # else:
    for var4 in range(0, regionvars.field1981):
        var5 = field2025[var4]
        if(var5.testDirection == 1):
            var6 = var5.minX - var1
            if(var6 > 0):
                var7 = (var6 * var5.minNormalX >> 8) + var5.minZ
                var8 = (var6 * var5.maxNormalX >> 8) + var5.maxZ
                var9 = (var6 * var5.minNormalY >> 8) + var5.minY
                var10 = (var6 * var5.maxNormalY >> 8) + var5.maxY
                if(var3 >= var7 and var3 <= var8 and var2 >= var9 and var2 <= var10):
                    return True

        elif(var5.testDirection == 2):
            var6 = var1 - var5.minX
            if(var6 > 0):
                var7 = (var6 * var5.minNormalX >> 8) + var5.minZ
                var8 = (var6 * var5.maxNormalX >> 8) + var5.maxZ
                var9 = (var6 * var5.minNormalY >> 8) + var5.minY
                var10 = (var6 * var5.maxNormalY >> 8) + var5.maxY
                if(var3 >= var7 and var3 <= var8 and var2 >= var9 and var2 <= var10):
                    return True

        elif(var5.testDirection == 3):
            var6 = var5.minZ - var3
            if(var6 > 0):
                var7 = (var6 * var5.field2089 >> 8) + var5.minX
                var8 = (var6 * var5.field2088 >> 8) + var5.maxX
                var9 = (var6 * var5.minNormalY >> 8) + var5.minY
                var10 = (var6 * var5.maxNormalY >> 8) + var5.maxY
                if(var1 >= var7 and var1 <= var8 and var2 >= var9 and var2 <= var10):
                    return True

        elif(var5.testDirection == 4):
            var6 = var3 - var5.minZ
            if(var6 > 0):
                var7 = (var6 * var5.field2089 >> 8) + var5.minX
                var8 = (var6 * var5.field2088 >> 8) + var5.maxX
                var9 = (var6 * var5.minNormalY >> 8) + var5.minY
                var10 = (var6 * var5.maxNormalY >> 8) + var5.maxY
                if(var1 >= var7 and var1 <= var8 and var2 >= var9 and var2 <= var10):
                    return True

        elif(var5.testDirection == 5):
            var6 = var2 - var5.minY
            if(var6 > 0):
                var7 = (var6 * var5.field2089 >> 8) + var5.minX
                var8 = (var6 * var5.field2088 >> 8) + var5.maxX
                var9 = (var6 * var5.minNormalX >> 8) + var5.minZ
                var10 = (var6 * var5.maxNormalX >> 8) + var5.maxZ
                if(var1 >= var7 and var1 <= var8 and var3 >= var9 and var3 <= var10):
                    return True

    return False


@jit(nopython=True, cache=False)
def isTileOccluded(field2025, regionvars, tileCycles, var1, var2, var3, tileHeights):

    var4 = tileCycles[var1][var2][var3]

    if(var4 == -regionvars.cycle):
        return False

    elif(var4 == regionvars.cycle):
        return True

    else:
        var5 = var2 << 7
        var6 = var3 << 7

        if(isOccluded(field2025, regionvars, var5 + 1, tileHeights[var1][var2][var3], var6 + 1) and
            isOccluded(field2025, regionvars, var5 + 128 - 1, tileHeights[var1][var2 + 1][var3], var6 + 1) and
                isOccluded(field2025, regionvars, var5 + 128 - 1, tileHeights[var1][var2 + 1][var3 + 1], var6 + 128 - 1) and
           isOccluded(field2025, regionvars, var5 + 1, tileHeights[var1][var2][var3 + 1], var6 + 128 - 1)):
            tileCycles[var1][var2][var3] = regionvars.cycle
            return True
        else:
            tileCycles[var1][var2][var3] = -regionvars.cycle
            return False


@jit(nopython=True, cache=False)
def isWallOccluded(field2025, regionvars, tileCycles, var1,  var2,  var3,  var4, tileHeights):
    if(not isTileOccluded(field2025, regionvars, tileCycles, var1, var2, var3, tileHeights)):
        return False
    else:
        var5 = var2 << 7
        var6 = var3 << 7
        var7 = tileHeights[var1][var2][var3] - 1
        var8 = var7 - 120
        var9 = var7 - 230
        var10 = var7 - 238
        if(var4 < 16):
            if(var4 == 1):
                if(var5 > regionvars.cameraX2):
                    if(not isOccluded(field2025, regionvars, var5, var7, var6)):
                        return False

                    if(not isOccluded(field2025, regionvars, var5, var7, var6 + 128)):
                        return False

                if(var1 > 0):
                    if(not isOccluded(field2025, regionvars, var5, var8, var6)):
                        return False

                    if(not isOccluded(field2025, regionvars, var5, var8, var6 + 128)):
                        return False

                if(not isOccluded(field2025, regionvars, var5, var9, var6)):
                    return False

                return isOccluded(field2025, regionvars, var5, var9, var6 + 128)

            if(var4 == 2):
                if(var6 < regionvars.cameraZ2):
                    if(not isOccluded(field2025, regionvars, var5, var7, var6 + 128)):
                        return False

                    if(not isOccluded(field2025, regionvars, var5 + 128, var7, var6 + 128)):
                        return False

                if(var1 > 0):
                    if(not isOccluded(field2025, regionvars, var5, var8, var6 + 128)):
                        return False

                    if(not isOccluded(field2025, regionvars, var5 + 128, var8, var6 + 128)):
                        return False

                if(not isOccluded(field2025, regionvars, var5, var9, var6 + 128)):
                    return False

                return isOccluded(field2025, regionvars, var5 + 128, var9, var6 + 128)

            if(var4 == 4):
                if(var5 < regionvars.cameraX2):
                    if(not isOccluded(field2025, regionvars, var5 + 128, var7, var6)):
                        return False

                    if(not isOccluded(field2025, regionvars, var5 + 128, var7, var6 + 128)):
                        return False

                if(var1 > 0):
                    if(not isOccluded(field2025, regionvars, var5 + 128, var8, var6)):
                        return False

                    if(not isOccluded(field2025, regionvars, var5 + 128, var8, var6 + 128)):
                        return False

                if(not isOccluded(field2025, regionvars, var5 + 128, var9, var6)):
                    return False

                return isOccluded(field2025, regionvars, var5 + 128, var9, var6 + 128)

            if(var4 == 8):
                if(var6 > regionvars.cameraZ2):
                    if(not isOccluded(field2025, regionvars, var5, var7, var6)):
                        return False

                    if(not isOccluded(field2025, regionvars, var5 + 128, var7, var6)):
                        return False

                if(var1 > 0):
                    if(not isOccluded(field2025, regionvars, var5, var8, var6)):
                        return False

                    if(not isOccluded(field2025, regionvars, var5 + 128, var8, var6)):
                        return False

                if(not isOccluded(field2025, regionvars, var5, var9, var6)):
                    return False

                return isOccluded(field2025, regionvars, var5 + 128, var9, var6)

        # WHAT IS A ? : Operation?
        # return var8 == 0?(var9 == 0 or (var9 < 0 ? var10 <= 0 : var10 >= 0)):(var8 < 0?var9 <= 0 and var10 <= 0:var9 >= 0 and var10 >= 0)
        # int a = (b < 4)? 7: 8 // if b < 4, set a to 7, else set a to 8
        # WHAT IS A ? : Operation?

        if var4 == 16:

            out = isOccluded(field2025, regionvars, var5, var9, var6 + 128)

        else:

            if var4 == 32:

                out = isOccluded(field2025, regionvars,
                                 var5 + 128, var9, var6 + 128)

            else:

                if var4 == 64:

                    out = isOccluded(field2025, regionvars,
                                     var5 + 128, var9, var6)

                else:

                    if var4 == 128:

                        out = isOccluded(
                            field2025, regionvars, var5, var9, var6)

                    else:

                        out = True

        return isOccluded(field2025, regionvars, var5 + 64, var10, var6 + 64) and out
        # return isOccluded(field2025, regionvars, var5 + 64, var10, var6 + 64) and (var4 == 16 ? isOccluded(field2025, regionvars, var5, var9, var6 + 128): (var4 == 32 ? isOccluded(field2025, regionvars, var5 + 128, var9, var6 + 128): (var4 == 64 ? isOccluded(field2025, regionvars, var5 + 128, var9, var6): (var4 == 128 ? isOccluded(field2025, regionvars, var5, var9, var6): True))))


@jit(nopython=True, cache=False)
def updateOccluders(renderArea, field2025, regionvars, levelOccluders, levelOccluderCount):
    var1 = levelOccluderCount[regionvars.Scene_plane]
    var2 = levelOccluders[regionvars.Scene_plane]
    regionvars.field1981 = 0

    for var3 in range(0, var1):
        var4 = var2[var3]
        if(var4.type == 1):
            var5 = var4.minTileX - regionvars.screenCenterX + 25
            if(var5 >= 0 and var5 <= 50):
                var6 = var4.minTileZ - \
                    regionvars.screenCenterZ + 25
                if(var6 < 0):
                    var6 = 0

                var7 = var4.maxTileZ - \
                    regionvars.screenCenterZ + 25
                if(var7 > 50):
                    var7 = 50

                var13 = False

                while(var6 <= var7):
                    if(renderArea[var5][var6]):
                        var13 = True
                        var6 += 1
                        break
                    var6 += 1

                if(var13):
                    var9 = regionvars.cameraX2 - var4.minX
                    if(var9 > 32):
                        var4.testDirection = 1
                    else:
                        if(var9 >= -32):
                            continue

                        var4.testDirection = 2
                        var9 = -var9

                    var4.minNormalX = integerdivide(
                        (var4.minZ - regionvars.cameraZ2 << 8), var9)
                    var4.maxNormalX = integerdivide(
                        (var4.maxZ - regionvars.cameraZ2 << 8), var9)
                    var4.minNormalY = integerdivide(
                        (var4.minY - regionvars.cameraY2 << 8), var9)
                    var4.maxNormalY = integerdivide(
                        (var4.maxY - regionvars.cameraY2 << 8), var9)
                    field2025[regionvars.field1981] = var4
                    regionvars.field1981 += 1

        elif(var4.type == 2):
            var5 = var4.minTileZ - regionvars.screenCenterZ + 25
            if(var5 >= 0 and var5 <= 50):
                var6 = var4.minTileX - \
                    regionvars.screenCenterX + 25
                if(var6 < 0):
                    var6 = 0

                var7 = var4.maxTIleX - \
                    regionvars.screenCenterX + 25
                if(var7 > 50):
                    var7 = 50

                var13 = False

                while(var6 <= var7):
                    if(renderArea[var6][var5]):
                        var13 = True
                        var6 += 1
                        break

                    var6 += 1

                if(var13):
                    var9 = regionvars.cameraZ2 - var4.minZ
                    if(var9 > 32):
                        var4.testDirection = 3
                    else:
                        if(var9 >= -32):
                            continue

                        var4.testDirection = 4
                        var9 = -var9

                    var4.field2089 = integerdivide(
                        (var4.minX - regionvars.cameraX2 << 8), var9)
                    var4.field2088 = integerdivide(
                        (var4.maxX - regionvars.cameraX2 << 8), var9)
                    var4.minNormalY = integerdivide(
                        (var4.minY - regionvars.cameraY2 << 8), var9)
                    var4.maxNormalY = integerdivide(
                        (var4.maxY - regionvars.cameraY2 << 8), var9)
                    field2025[regionvars.field1981] = var4
                    regionvars.field1981 += 1

        elif(var4.type == 4):
            var5 = var4.minY - regionvars.cameraY2
            if(var5 > 128):
                var6 = var4.minTileZ - \
                    regionvars.screenCenterZ + 25
                if(var6 < 0):
                    var6 = 0

                var7 = var4.maxTileZ - \
                    regionvars.screenCenterZ + 25
                if(var7 > 50):
                    var7 = 50

                if(var6 <= var7):
                    var8 = var4.minTileX - \
                        regionvars.screenCenterX + 25
                    if(var8 < 0):
                        var8 = 0

                    var9 = var4.maxTIleX - \
                        regionvars.screenCenterX + 25
                    if(var9 > 50):
                        var9 = 50

                    var10 = False

                    breaknestedforloop = False
                    for var11 in range(var8, var9 + 1):
                        for var12 in range(var6, var7 + 1):
                            if(renderArea[var11][var12]):
                                var10 = True
                                breaknestedforloop = True
                                break
                        if breaknestedforloop == True:
                            break

                    if(var10):
                        var4.testDirection = 5
                        var4.field2089 = integerdivide(
                            (var4.minX - regionvars.cameraX2 << 8), var5)
                        var4.field2088 = integerdivide(
                            (var4.maxX - regionvars.cameraX2 << 8), var5)
                        var4.minNormalX = integerdivide(
                            (var4.minZ - regionvars.cameraZ2 << 8), var5)
                        var4.maxNormalX = integerdivide(
                            (var4.maxZ - regionvars.cameraZ2 << 8), var5)
                        field2025[regionvars.field1981] = var4
                        regionvars.field1981 += 1


@jit(nopython=True, cache=False)
def isAreaOccluded(field2025, regionvars, tileCycles, var1, var2, var3, var4, var5, var6, tileHeights):
    if(var3 == var2 and var5 == var4):
        if(not isTileOccluded(field2025, regionvars, tileCycles, var1, var2, var4, tileHeights)):
            return False
        else:
            var7 = var2 << 7
            var8 = var4 << 7
            return isOccluded(field2025, regionvars, var7 + 1, tileHeights[var1][var2][var4] - var6, var8 + 1) and isOccluded(field2025, regionvars, var7 + 128 - 1, tileHeights[var1][var2 + 1][var4] - var6, var8 + 1) and isOccluded(field2025, regionvars, var7 + 128 - 1, tileHeights[var1][var2 + 1][var4 + 1] - var6, var8 + 128 - 1) and isOccluded(field2025, regionvars, var7 + 1, tileHeights[var1][var2][var4 + 1] - var6, var8 + 128 - 1)

    else:
        for var7 in range(var2, var3 + 1):
            for var8 in range(var4, var5 + 1):
                if(tileCycles[var1][var7][var8] == -regionvars.cycle):
                    return False

    var7 = (var2 << 7) + 1
    var8 = (var4 << 7) + 2
    var9 = tileHeights[var1][var2][var4] - var6
    if(not isOccluded(field2025, regionvars, var7, var9, var8)):
        return False
    else:
        var10 = (var3 << 7) - 1
        if(not isOccluded(field2025, regionvars, var10, var9, var8)):
            return False
        else:
            var11 = (var5 << 7) - 1
            if(not isOccluded(field2025, regionvars, var7, var9, var11)):
                return False
            else:
                return isOccluded(field2025, regionvars, var10, var9, var11)


@jit(nopython=True, cache=False)
def isOccluded4(field2025, regionvars, tileCycles, var1, var2, var3, var4, tileHeights):

    if(not isTileOccluded(field2025, regionvars, tileCycles, var1, var2, var3, tileHeights)):
        return False
    else:
        var5 = var2 << 7
        var6 = var3 << 7
        return isOccluded(field2025, regionvars, var5 + 1, tileHeights[var1][var2][var3] - var4, var6 + 1) and \
            isOccluded(field2025, regionvars, var5 + 128 - 1, tileHeights[var1][var2 + 1][var3] - var4, var6 + 1) and \
            isOccluded(field2025, regionvars, var5 + 128 - 1, tileHeights[var1][var2 + 1][var3 + 1] - var4, var6 + 128 - 1) and \
            isOccluded(field2025, regionvars,
                       var5 + 1, tileHeights[var1][var2][var3 + 1] - var4, var6 + 128 - 1)


@jit(nopython=True, cache=False)
def drawTileUnderlay(colorPalette, field2025, regionvars, Graphics3D_, var1,  var2,  var3,  var4,  var5,  var6,  var7,  var8, tileHeights, textures, objectDefinitions):

    selfregionLowMemory = False

    # Tile obviously does not have objectID...so do == 0 for now
    tileunderlayObjectID = 0

    var10 = var9 = (var7 << 7) - regionvars.cameraX2
    var12 = var11 = (var8 << 7) - regionvars.cameraZ2
    var14 = var13 = var10 + 128
    var16 = var15 = var12 + 128
    var17 = tileHeights[var2][var7][var8] - regionvars.cameraY2
    var18 = tileHeights[var2][var7 + 1][var8] - \
        regionvars.cameraY2
    var19 = tileHeights[var2][var7 + 1][var8 + 1] - \
        regionvars.cameraY2
    var20 = tileHeights[var2][var7][var8 + 1] - \
        regionvars.cameraY2
    var21 = var10 * var6 + var5 * var12 >> 16
    var12 = var12 * var6 - var5 * var10 >> 16
    var10 = var21
    var21 = var17 * var4 - var3 * var12 >> 16
    var12 = var3 * var17 + var12 * var4 >> 16
    var17 = var21
    if(var12 >= 50):
        var21 = var14 * var6 + var5 * var11 >> 16
        var11 = var11 * var6 - var5 * var14 >> 16
        var14 = var21
        var21 = var18 * var4 - var3 * var11 >> 16
        var11 = var3 * var18 + var11 * var4 >> 16
        var18 = var21
        if(var11 >= 50):
            var21 = var13 * var6 + var5 * var16 >> 16
            var16 = var16 * var6 - var5 * var13 >> 16
            var13 = var21
            var21 = var19 * var4 - var3 * var16 >> 16
            var16 = var3 * var19 + var16 * var4 >> 16
            var19 = var21
            if(var16 >= 50):
                var21 = var9 * var6 + var5 * var15 >> 16
                var15 = var15 * var6 - var5 * var9 >> 16
                var9 = var21
                var21 = var20 * var4 - var3 * var15 >> 16
                var15 = var3 * var20 + var15 * var4 >> 16
                if(var15 >= 50):

                    var22 = integerdivide(
                        var10 * Graphics3D_.Rasterizer3D_zoom, var12) + Graphics3D_.centerX
                    var23 = integerdivide(
                        var17 * Graphics3D_.Rasterizer3D_zoom, var12) + Graphics3D_.centerY
                    var24 = integerdivide(
                        var14 * Graphics3D_.Rasterizer3D_zoom, var11) + Graphics3D_.centerX
                    var25 = integerdivide(
                        var18 * Graphics3D_.Rasterizer3D_zoom, var11) + Graphics3D_.centerY
                    var26 = integerdivide(
                        var13 * Graphics3D_.Rasterizer3D_zoom, var16) + Graphics3D_.centerX
                    var27 = integerdivide(
                        var19 * Graphics3D_.Rasterizer3D_zoom, var16) + Graphics3D_.centerY
                    var28 = integerdivide(
                        var9 * Graphics3D_.Rasterizer3D_zoom, var15) + Graphics3D_.centerX
                    var29 = integerdivide(
                        var21 * Graphics3D_.Rasterizer3D_zoom, var15) + Graphics3D_.centerY
                    Graphics3D_.rasterAlpha = 0

                    if((var26 - var28) * (var25 - var29) - (var27 - var29) * (var24 - var28) > 0):
                        Graphics3D_.rasterClipEnable = var26 < 0 or var28 < 0 or var24 < 0 or var26 > Graphics3D_.rasterClipX or var28 > Graphics3D_.rasterClipX or var24 > Graphics3D_.rasterClipX

                        # if(checkClick and method2898(mouseX2, mouseY2, var27, var29, var25, var26, var28, var24)):
                        #     selectedRegionTileX = var7
                        #     selectedRegionTileY = var8

                        if(var1.texture == -1):
                            if(var1.neColor != 12345678):

                                
                                rasterGouraud(colorPalette, Graphics3D_, tileunderlayObjectID,
                                              var27, var29, var25, var26, var28, var24, var1.neColor, var1.nwColor, var1.seColor)

                        elif(not selfregionLowMemory):
                            if(var1.flatShade):

                                rasterTexture(colorPalette, Graphics3D_, tileunderlayObjectID,
                                              var27, var29, var25, var26, var28, var24, var1.neColor, var1.nwColor,
                                              var1.seColor, var10, var14, var9, var17, var18, var21, var12, var11, var15, var1.texture, textures)
                            else:

                                rasterTexture(colorPalette, Graphics3D_, tileunderlayObjectID,
                                              var27, var29, var25, var26, var28, var24, var1.neColor, var1.nwColor,
                                              var1.seColor, var13, var9, var14, var19, var21, var18, var16, var15, var11, var1.texture, textures)

                        else:

                            var30 = Graphics3D_.textureLoader.getAverageTextureRGB(
                                var1.texture)

                            rasterGouraud(colorPalette, Graphics3D_, tileunderlayObjectID,
                                          var27, var29, var25, var26, var28, var24, method2897(
                                              var30, var1.neColor), method2897(var30, var1.nwColor), method2897(var30, var1.seColor))

                    if((var22 - var24) * (var29 - var25) - (var23 - var25) * (var28 - var24) > 0):
                        Graphics3D_.rasterClipEnable = var22 < 0 or var24 < 0 or var28 < 0 or var22 > Graphics3D_.rasterClipX or var24 > Graphics3D_.rasterClipX or var28 > Graphics3D_.rasterClipX

                        # if(checkClick and method2898(mouseX2, mouseY2, var23, var25, var29, var22, var24, var28)):
                        #     selectedRegionTileX = var7
                        #     selectedRegionTileY = var8

                        if(var1.texture == -1):
                            if(var1.swColor != 12345678):

                                rasterGouraud(colorPalette, Graphics3D_, tileunderlayObjectID,
                                              var23, var25, var29, var22, var24, var28, var1.swColor, var1.seColor, var1.nwColor)

                        elif(not selfregionLowMemory):

                            rasterTexture(colorPalette, Graphics3D_, tileunderlayObjectID,
                                          var23, var25, var29, var22, var24, var28, var1.swColor, var1.seColor,
                                          var1.nwColor, var10, var14, var9, var17, var18, var21, var12, var11, var15, var1.texture, textures)
                        else:

                            var30 = Graphics3D_.textureLoader.getAverageTextureRGB(
                                var1.texture)

                            rasterGouraud(colorPalette, Graphics3D_, tileunderlayObjectID,
                                          var23, var25, var29, var22, var24, var28, method2897(
                                              var30, var1.swColor), method2897(var30, var1.seColor), method2897(var30, var1.nwColor))


@jit(nopython=True, cache=False)
def drawTileOverlay(colorPalette, field2025, regionvars, vertexSceneX, vertexSceneY, vertexSceneZ, tmpScreenX, tmpScreenY, Graphics3D_, var1, var2, var3, var4, var5, var6, var7, textures):

    selfregionLowMemory = False

    # Tile obviously does not have objectID...so do == 0 for now
    tileOverlayObjectID = 0

    var8 = len(var1.vertexX)

    for var9 in range(0, var8):
        var10 = var1.vertexX[var9] - regionvars.cameraX2
        var11 = var1.vertexY[var9] - regionvars.cameraY2
        var12 = var1.vertexZ[var9] - regionvars.cameraZ2
        var13 = var12 * var4 + var5 * var10 >> 16
        var12 = var5 * var12 - var10 * var4 >> 16
        var10 = var13
        var13 = var3 * var11 - var12 * var2 >> 16
        var12 = var11 * var2 + var3 * var12 >> 16
        if(var12 < 50):
            return

        if(var1.triangleTextureId is not None):
            vertexSceneX[var9] = var10
            vertexSceneY[var9] = var13
            vertexSceneZ[var9] = var12

        tmpScreenX[var9] = integerdivide(
            var10 * Graphics3D_.Rasterizer3D_zoom, var12) + Graphics3D_.centerX
        tmpScreenY[var9] = integerdivide(
            var13 * Graphics3D_.Rasterizer3D_zoom, var12) + Graphics3D_.centerY

    Graphics3D_.rasterAlpha = 0
    var8 = len(var1.field1772)

    for var9 in range(0, var8):
        var10 = var1.field1772[var9]
        var11 = var1.field1774[var9]
        var12 = var1.field1778[var9]
        var13 = tmpScreenX[var10]
        var14 = tmpScreenX[var11]
        var15 = tmpScreenX[var12]
        var16 = tmpScreenY[var10]
        var17 = tmpScreenY[var11]
        var18 = tmpScreenY[var12]
        if((var13 - var14) * (var18 - var17) - (var16 - var17) * (var15 - var14) > 0):
            Graphics3D_.rasterClipEnable = var13 < 0 or var14 < 0 or var15 < 0 or var13 > Graphics3D_.rasterClipX or var14 > Graphics3D_.rasterClipX or var15 > Graphics3D_.rasterClipX

            # if(checkClick and method2898(mouseX2, mouseY2, var16, var17, var18, var13, var14, var15)):
            #     selectedRegionTileX = var6
            #     selectedRegionTileY = var7

            if(var1.triangleTextureId is not None and var1.triangleTextureId[var9] != -1):
                if(not selfregionLowMemory):
                    if(var1.flatShade):
                        rasterTexture(colorPalette, Graphics3D_, tileOverlayObjectID,
                                      var16, var17, var18, var13, var14, var15, var1.triangleColorA[var9], var1.triangleColorB[var9], var1.triangleColorC[var9], vertexSceneX[0], vertexSceneX[1], vertexSceneX[
                                          3], vertexSceneY[0], vertexSceneY[1], vertexSceneY[3], vertexSceneZ[0], vertexSceneZ[1], vertexSceneZ[3], var1.triangleTextureId[var9], textures)
                    else:
                        rasterTexture(colorPalette, Graphics3D_, tileOverlayObjectID,
                                      var16, var17, var18, var13, var14, var15, var1.triangleColorA[var9], var1.triangleColorB[var9], var1.triangleColorC[var9], vertexSceneX[var10], vertexSceneX[var11], vertexSceneX[
                                          var12], vertexSceneY[var10], vertexSceneY[var11], vertexSceneY[var12], vertexSceneZ[var10], vertexSceneZ[var11], vertexSceneZ[var12], var1.triangleTextureId[var9], textures)

                else:

                    var19 = Graphics3D_.textureLoader.getAverageTextureRGB(
                        var1.triangleTextureId[var9])
                    rasterGouraud(colorPalette, Graphics3D_, tileOverlayObjectID,
                                  var16, var17, var18, var13, var14, var15, method2897(var19, var1.triangleColorA[var9]), method2897(
                                      var19, var1.triangleColorB[var9]), method2897(var19, var1.triangleColorC[var9]))

            elif(var1.triangleColorA[var9] != 12345678):
                rasterGouraud(colorPalette, Graphics3D_, tileOverlayObjectID,
                              var16, var17, var18, var13, var14, var15,
                              var1.triangleColorA[var9], var1.triangleColorB[var9], var1.triangleColorC[var9])


@jit(nopython=True, cache=False)
def setPhysicalLevel(var1, var2, var3, var4, tiles):
    var5 = getTile(var1, var2, var3, tiles)  # tiles[var1][var2][var3]
    # if(var5 is not None):
    #tiles[var1][var2][var3].physicalLevel = var4
    var5.physicalLevel = var4  # Never not None


@jit(nopython=True, cache=False)
def addEntityMarker(regionobjects, field2025, regionvars, maxYregion, maxXregion, maxZregion, var1, var2, var3, var4, var5, var6, var7, var8, var9, var10, var11, var12, var13, tiles):

    for var14 in range(var2, var2 + var4):
        for var15 in range(var3, var3 + var5):
            if(var14 < 0 or var15 < 0 or var14 >= maxXregion or var15 >= maxZregion):
                return False

            # tiles[var1][var14][var15]
            var21 = getTile(var1, var14, var15, tiles)

            # var21 is not None and
            if(var21.entityCount >= 5):
                return False

    var20 = GameObject()  # (var9)
    var20.hash = var12
    var20.flags = var13
    var20.plane = var1
    var20.x = var6
    var20.y = var7
    var20.height = var8
    var20.renderable = var9

    var20.orientation = var10
    var20.relativeX = var2
    var20.relativeY = var3
    var20.offsetX = var2 + var4 - 1
    var20.offsetY = var3 + var5 - 1

    for var15 in range(var2, var2 + var4):
        for var16 in range(var3, var3 + var5):
            var17 = 0
            if(var15 > var2):
                var17 += 1

            if(var15 < var2 + var4 - 1):
                var17 += 4

            if(var16 > var3):
                var17 += 8

            if(var16 < var3 + var5 - 1):
                var17 += 2

            # Tiles already exist...
            # var18 = var1
            # while var18 >= 0:
            #     if(tiles[var18][var15][var16] is None):
            #         tiles[var18][var15][var16] = Tile(
            #             var18, var15, var16)

            #     var18 -= 1

            # tiles[var1][var15][var16]
            var22 = getTile(var1, var15, var16, tiles)
            var22.objects[var22.entityCount] = var20
            var22.entityFlags[var22.entityCount] = var17
            var22.flags |= var17
            var22.entityCount += 1

    if var11:
        #print("Yeah added NPC")
        regionobjects[regionvars.entityCount] = var20
        regionvars.entityCount += 1

    return True


@jit(nopython=True, cache=False)
def method2862(regionobjects, field2025, regionvars, maxYregion, maxXregion, maxZregion, var1, var2, var3, var4, var5, var6, var7, var8, var9, var10, tiles):

    if(var7 is None):
        return True
    else:
        var11 = var5 * 64 + var2 * 128
        var12 = var6 * 64 + var3 * 128
        return addEntityMarker(regionobjects, field2025, regionvars, maxYregion, maxXregion, maxZregion, var1, var2, var3, var5, var6, var11, var12, var4, var7, var8, False, var9, var10, tiles)


@jit(nopython=True, cache=False)
def draw(colorPalette, field2027, field2040, TILE_WALL_DRAW_FLAGS_1, WALL_UNCULL_FLAGS_0, WALL_UNCULL_FLAGS_1, WALL_UNCULL_FLAGS_2, WALL_UNCULL_FLAGS_3,
         entityBuffer, field2025, regionvars, staticModel_, Deque_, tileCycles, maxYregion,
         maxXregion, maxZregion, vertexSceneX, vertexSceneY, vertexSceneZ, tmpScreenX,
         tmpScreenY, var1, var2, Graphics3D_, tileHeights, tiles, textures, objectDefinitions):

    selfcheckClick = False

    # tileIDQueue.addFront(var1)
    # tileIDQueue[regionvars.tileIDQueueSize] = getTileID(var1)
    # regionvars.tileIDQueueSize += 1

    # tileIDQueueList.append(getTileID(var1))

    Deque_.addFront(getTileID(var1))

    while(True):

        currTile = Tile(-9999, -9999, -9999)
        var4 = 0
        var5 = 0
        var6 = 0
        var7 = 0
        var8plane = 0  # var8
        var9 = Tile(-9999, -9999, -9999)
        var11 = 0
        var14 = 0
        var15 = 0
        var16 = 0
        var24 = 0
        var25 = 0

        while (True):
            while (True):
                while (True):
                    while(True):
                        while(True):
                            while (True):

                                while(True):

                                    while(True):

                                        ###################
                                        while (True):

                                            # Is empty!
                                            currTileID = Deque_.popFront()
                                            if currTileID == -1:
                                                return
                                            ##print("Would have been tileID", currTileID)

                                            currTile = tiles[currTileID]

                                            #print("------------CurrTile: ", currTile.plane, currTile.x, currTile.y, currTile.visible, currTile.draw)

                                            # A tile that should be drone, break the search and lets get to drawing
                                            if currTile.visible:
                                                break
                                        ####################

                                        var4 = currTile.x
                                        var5 = currTile.y
                                        var6 = currTile.plane
                                        var7 = currTile.renderLevel
                                        var8plane = var6

                                        if(not currTile.draw):
                                            break

                                        if var2:
                                            if(var6 > 0):
                                                var9 = getTile(
                                                    var6 - 1, var4, var5, tiles)
                                                if(var9.visible):
                                                    continue

                                            if(var4 <= regionvars.screenCenterX and var4 > regionvars.minTileX):
                                                var9 = getTile(
                                                    var8plane, var4 - 1, var5, tiles)
                                                if(var9.visible and (var9.draw or (currTile.flags & 1) == 0)):
                                                    continue

                                            if(var4 >= regionvars.screenCenterX and var4 < regionvars.maxTileX - 1):
                                                var9 = getTile(
                                                    var8plane, var4 + 1, var5, tiles)
                                                if(var9.visible and (var9.draw or (currTile.flags & 4) == 0)):
                                                    continue

                                            if(var5 <= regionvars.screenCenterZ and var5 > regionvars.minTileZ):
                                                var9 = getTile(
                                                    var8plane, var4, var5 - 1, tiles)
                                                if(var9.visible and (var9.draw or (currTile.flags & 8) == 0)):
                                                    continue

                                            if(var5 >= regionvars.screenCenterZ and var5 < regionvars.maxTileZ - 1):
                                                var9 = getTile(
                                                    var8plane, var4, var5 + 1, tiles)
                                                if(var9.visible and (var9.draw or (currTile.flags & 2) == 0)):
                                                    continue

                                        else:
                                            var2 = True

                                        currTile.draw = False
                                        if(currTile.bridge is not None):
                                            var9 = currTile.bridge
                                            if(var9.paint is not None):
                                                if(not isTileOccluded(field2025, regionvars, tileCycles, 0, var4, var5, tileHeights)):

                                                    drawTileUnderlay(colorPalette, field2025, regionvars, Graphics3D_,
                                                                     var9.paint, 0, regionvars.pitchSin, regionvars.pitchCos, regionvars.yawSin, regionvars.yawCos, var4, var5, tileHeights, textures, objectDefinitions)

                                            elif(var9.overlay is not None and not isTileOccluded(field2025, regionvars, tileCycles, 0, var4, var5, tileHeights)):

                                                drawTileOverlay(colorPalette, field2025, regionvars, vertexSceneX, vertexSceneY, vertexSceneZ, tmpScreenX, tmpScreenY, Graphics3D_,
                                                                var9.overlay, regionvars.pitchSin, regionvars.pitchCos, regionvars.yawSin, regionvars.yawCos, var4, var5, textures)

                                            var10 = var9.wallObject
                                            if(var10 is not None):
                                                ##print("BRIDGE: There is a wallObject that needs to be drawn")
                                                drawModel(colorPalette, staticModel_, var10.renderable1, 0, regionvars.pitchSin, regionvars.pitchCos, regionvars.yawSin, regionvars.yawCos, var10.x -
                                                          regionvars.cameraX2, var10.floor - regionvars.cameraY2, var10.y - regionvars.cameraZ2, var10.hash, Graphics3D_, tileHeights, textures, objectDefinitions)

                                            for var11 in range(0, var9.entityCount):
                                                ##print("BRIDGE: There is an entity that needs to be drawn")
                                                var12 = var9.objects[var11]
                                                if(var12 is not None):
                                                    drawModel(colorPalette, staticModel_, var12.renderable, var12.orientation, regionvars.pitchSin, regionvars.pitchCos, regionvars.yawSin, regionvars.yawCos, var12.x -
                                                              regionvars.cameraX2, var12.height - regionvars.cameraY2, var12.y - regionvars.cameraZ2, var12.hash, Graphics3D_, tileHeights, textures, objectDefinitions)

                                        var20 = False
                                        if(currTile.paint is not None):
                                            if(not isTileOccluded(field2025, regionvars, tileCycles, var7, var4, var5, tileHeights)):
                                                var20 = True
                                                if(currTile.paint.neColor != 12345678 or selfcheckClick and var6 <= regionvars.field2013):

                                                    drawTileUnderlay(colorPalette, field2025, regionvars, Graphics3D_,
                                                                     currTile.paint, var7, regionvars.pitchSin, regionvars.pitchCos, regionvars.yawSin, regionvars.yawCos, var4, var5, tileHeights, textures, objectDefinitions)

                                        elif(currTile.overlay is not None and not isTileOccluded(field2025, regionvars, tileCycles, var7, var4, var5, tileHeights)):
                                            var20 = True

                                            drawTileOverlay(colorPalette, field2025, regionvars, vertexSceneX, vertexSceneY, vertexSceneZ, tmpScreenX, tmpScreenY, Graphics3D_,
                                                            currTile.overlay, regionvars.pitchSin, regionvars.pitchCos, regionvars.yawSin, regionvars.yawCos, var4, var5, textures)

                                        var21 = 0
                                        var11 = 0
                                        var31 = currTile.wallObject
                                        var13 = currTile.decorativeObject
                                        if(var31 is not None or var13 is not None):

                                            if(var4 == regionvars.screenCenterX):
                                                var21 += 1
                                            elif(regionvars.screenCenterX < var4):
                                                var21 += 2

                                            if(var5 == regionvars.screenCenterZ):
                                                var21 += 3
                                            elif(regionvars.screenCenterZ > var5):
                                                var21 += 6

                                            var11 = field2027[var21]

                                            currTile.wallDrawFlags = TILE_WALL_DRAW_FLAGS_1[var21]

                                        if(var31 is not None):
                                            if((var31.orientationA & field2040[var21]) != 0):
                                                if(var31.orientationA == 16):
                                                    currTile.wallCullDirection = 3
                                                    currTile.wallUncullDirection = WALL_UNCULL_FLAGS_0[
                                                        var21]
                                                    currTile.wallCullOppositeDirection = 3 - currTile.wallUncullDirection
                                                elif(var31.orientationA == 32):
                                                    currTile.wallCullDirection = 6
                                                    currTile.wallUncullDirection = WALL_UNCULL_FLAGS_1[
                                                        var21]
                                                    currTile.wallCullOppositeDirection = 6 - currTile.wallUncullDirection
                                                elif(var31.orientationA == 64):
                                                    currTile.wallCullDirection = 12
                                                    currTile.wallUncullDirection = WALL_UNCULL_FLAGS_2[
                                                        var21]
                                                    currTile.wallCullOppositeDirection = 12 - currTile.wallUncullDirection
                                                else:
                                                    currTile.wallCullDirection = 9
                                                    currTile.wallUncullDirection = WALL_UNCULL_FLAGS_3[
                                                        var21]
                                                    currTile.wallCullOppositeDirection = 9 - currTile.wallUncullDirection

                                            else:
                                                currTile.wallCullDirection = 0

                                            wallAOccluded = isWallOccluded(field2025, regionvars, tileCycles,
                                                                           var7, var4, var5, var31.orientationA, tileHeights)
                                            if wallAOccluded:
                                                raise Exception(
                                                    "Wow actually True")
                                            firstStatementA = (
                                                var31.orientationA & var11) != 0

                                            if(firstStatementA and not wallAOccluded):

                                                drawModel(colorPalette, staticModel_, var31.renderable1, 0, regionvars.pitchSin, regionvars.pitchCos, regionvars.yawSin, regionvars.yawCos, var31.x - regionvars.cameraX2,
                                                          var31.floor - regionvars.cameraY2, var31.y - regionvars.cameraZ2, var31.hash, Graphics3D_, tileHeights, textures, objectDefinitions)

                                            if((var31.orientationB & var11) != 0 and not isWallOccluded(field2025, regionvars, tileCycles, var7, var4, var5, var31.orientationB, tileHeights)):

                                                drawModel(colorPalette, staticModel_, var31.renderable2, 0, regionvars.pitchSin, regionvars.pitchCos, regionvars.yawSin, regionvars.yawCos, var31.x - regionvars.cameraX2,
                                                          var31.floor - regionvars.cameraY2, var31.y - regionvars.cameraZ2, var31.hash, Graphics3D_, tileHeights, textures, objectDefinitions)

                                        if(var13 is not None and not isOccluded4(field2025, regionvars, tileCycles, var7, var4, var5, var13.renderable1.modelHeight, tileHeights)):
                                            if((var13.renderFlag & var11) != 0):
                                                drawModel(colorPalette, staticModel_, var13.renderable1, 0, regionvars.pitchSin, regionvars.pitchCos, regionvars.yawSin, regionvars.yawCos, var13.x - regionvars.cameraX2 + var13.offsetX,
                                                          var13.floor - regionvars.cameraY2, var13.y - regionvars.cameraZ2 + var13.offsetY, var13.hash, Graphics3D_, tileHeights, textures, objectDefinitions)
                                            elif(var13.renderFlag == 256):
                                                var14 = var13.x - \
                                                    regionvars.cameraX2
                                                var15 = var13.floor - \
                                                    regionvars.cameraY2
                                                var16 = var13.y - \
                                                    regionvars.cameraZ2
                                                var17 = var13.rotation
                                                if(var17 != 1 and var17 != 2):
                                                    var18 = var14
                                                else:
                                                    var18 = -var14

                                                if(var17 != 2 and var17 != 3):
                                                    var19 = var16
                                                else:
                                                    var19 = -var16

                                                if(var19 < var18):

                                                    drawModel(colorPalette, staticModel_, var13.renderable1, 0, regionvars.pitchSin, regionvars.pitchCos, regionvars.yawSin, regionvars.yawCos, var14 +
                                                              var13.offsetX, var15, var16 + var13.offsetY, var13.hash, Graphics3D_, tileHeights, textures, objectDefinitions)

                                                    # var13.renderable1.draw(0, regionvars.pitchSin, regionvars.pitchCos, regionvars.yawSin, regionvars.yawCos, var14 +
                                                    #                       var13.offsetX, var15, var16 + var13.offsetY, var13.hash, Graphics3D_, tileHeights, textures, objectDefinitions)
                                                elif(var13.renderable2 is not None):
                                                    drawModel(colorPalette, staticModel_, var13.renderable2,
                                                              0, regionvars.pitchSin, regionvars.pitchCos, regionvars.yawSin, regionvars.yawCos, var14, var15, var16, var13.hash, Graphics3D_, tileHeights, textures, objectDefinitions)
                                                    # var13.renderable2.draw(
                                                    #    0, regionvars.pitchSin, regionvars.pitchCos, regionvars.yawSin, regionvars.yawCos, var14, var15, var16, var13.hash, Graphics3D_, tileHeights, textures, objectDefinitions)

                                        if var20:

                                            # Random small rocks on the floor
                                            var22 = currTile.groundObject
                                            if(var22 is not None):
                                                drawModel(colorPalette, staticModel_, var22.renderable, 0, regionvars.pitchSin, regionvars.pitchCos, regionvars.yawSin, regionvars.yawCos, var22.x - regionvars.cameraX2,
                                                          var22.floor - regionvars.cameraY2, var22.y - regionvars.cameraZ2, var22.hash, Graphics3D_, tileHeights, textures, objectDefinitions)
                                                # var22.renderable.draw(0, regionvars.pitchSin, regionvars.pitchCos, regionvars.yawSin, regionvars.yawCos, var22.x - regionvars.cameraX2,
                                                #                      var22.floor - regionvars.cameraY2, var22.y - regionvars.cameraZ2, var22.hash, Graphics3D_, tileHeights, textures, objectDefinitions)

                                            # var23 = currTile.itemLayer
                                            # if(var23 is not None and var23.height == 0):

                                            #     raise Exception("For ")

                                            #     if(var23.middle is not None):
                                            #         var23.middle.draw(0, regionvars.pitchSin, regionvars.pitchCos, regionvars.yawSin, regionvars.yawCos, var23.x - regionvars.cameraX2,
                                            #                           var23.hash - regionvars.cameraY2, var23.y - regionvars.cameraZ2, var23.flags, Graphics3D_, tileHeights, textures, objectDefinitions)

                                            #     if(var23.top is not None):
                                            #         var23.top.draw(0, regionvars.pitchSin, regionvars.pitchCos, regionvars.yawSin, regionvars.yawCos, var23.x - regionvars.cameraX2,
                                            #                        var23.hash - regionvars.cameraY2, var23.y - regionvars.cameraZ2, var23.flags, Graphics3D_, tileHeights, textures, objectDefinitions)

                                            #     if(var23.bottom is not None):
                                            #         var23.bottom.draw(0, regionvars.pitchSin, regionvars.pitchCos, regionvars.yawSin, regionvars.yawCos, var23.x - regionvars.cameraX2,
                                            #                           var23.hash - regionvars.cameraY2, var23.y - regionvars.cameraZ2, var23.flags, Graphics3D_, tileHeights, textures, objectDefinitions)

                                        var14 = currTile.flags
                                        if(var14 != 0):
                                            if(var4 < regionvars.screenCenterX and (var14 & 4) != 0):
                                                # tiles[var6][var4 + 1][var5]
                                                var36 = getTile(
                                                    var8plane, var4 + 1, var5, tiles)
                                                if(var36 is not None and var36.visible):

                                                    #print("Flags readd1: ", var14, var8plane, var4 + 1, var5)

                                                    Deque_.addFront(
                                                        getTileID(var36))

                                            if(var5 < regionvars.screenCenterZ and (var14 & 2) != 0):
                                                # tiles[var6][var4][var5 + 1]
                                                var36 = getTile(
                                                    var8plane, var4, var5 + 1, tiles)
                                                if(var36 is not None and var36.visible):

                                                    #print("Flags readd2: ", var14, var8plane, var4, var5 + 1)

                                                    Deque_.addFront(
                                                        getTileID(var36))

                                            if(var4 > regionvars.screenCenterX and (var14 & 1) != 0):
                                                # tiles[var6][var4 - 1][var5]
                                                var36 = getTile(
                                                    var8plane, var4 - 1, var5, tiles)
                                                if(var36 is not None and var36.visible):

                                                    #print("Flags readd3: ", var14, var8plane, var4 - 1, var5)
                                                    Deque_.addFront(
                                                        getTileID(var36))

                                            if(var5 > regionvars.screenCenterZ and (var14 & 8) != 0):
                                                # tiles[var6][var4][var5 - 1]
                                                var36 = getTile(
                                                    var8plane, var4, var5 - 1, tiles)
                                                if(var36 is not None and var36.visible):

                                                    #print("Flags readd4: ", var14, var8plane, var4, var5 - 1)
                                                    Deque_.addFront(
                                                        getTileID(var36))

                                        break

                                    if(currTile.wallCullDirection != 0):
                                        var20 = True

                                        for var21 in range(0, currTile.entityCount):
                                            if(currTile.objects[var21].cycle != regionvars.cycle and (currTile.entityFlags[var21] & currTile.wallCullDirection) == currTile.wallUncullDirection):
                                                var20 = False
                                                break

                                        if var20 == True:
                                            var10 = currTile.wallObject
                                            if(not isWallOccluded(field2025, regionvars, tileCycles, var7, var4, var5, var10.orientationA, tileHeights)):
                                                drawModel(colorPalette, staticModel_, var10.renderable1, 0, regionvars.pitchSin, regionvars.pitchCos, regionvars.yawSin, regionvars.yawCos, var10.x - regionvars.cameraX2,
                                                          var10.floor - regionvars.cameraY2, var10.y - regionvars.cameraZ2, var10.hash, Graphics3D_, tileHeights, textures, objectDefinitions)

                                            currTile.wallCullDirection = 0

                                    #print("EntityCount: ", currTile.entityCount)
                                    if(not currTile.drawEntities):
                                        #print("Break at drawEntities")
                                        break

                                    var34 = currTile.entityCount
                                    currTile.drawEntities = False
                                    var21 = 0

                                    for var11 in range(0, var34):

                                        continuelabel563 = False
                                        var12 = currTile.objects[var11]
                                        if(var12.cycle != regionvars.cycle):
                                            for var24 in range(var12.relativeX, var12.offsetX + 1):
                                                for var14 in range(var12.relativeY, var12.offsetY + 1):
                                                    # tiles[var6][var24][var14]
                                                    var36 = getTile(
                                                        var8plane, var24, var14, tiles)
                                                    if(var36.draw):
                                                        #print("Set drawEntities to true1")
                                                        currTile.drawEntities = True
                                                        continuelabel563 = True
                                                        break

                                                    if(var36.wallCullDirection != 0):
                                                        var16 = 0
                                                        if(var24 > var12.relativeX):
                                                            var16 += 1

                                                        if(var24 < var12.offsetX):
                                                            var16 += 4

                                                        if(var14 > var12.relativeY):
                                                            var16 += 8

                                                        if(var14 < var12.offsetY):
                                                            var16 += 2

                                                        if((var16 & var36.wallCullDirection) == currTile.wallCullOppositeDirection):
                                                            #print("Set drawEntities to true2")
                                                            currTile.drawEntities = True
                                                            continuelabel563 = True
                                                            break

                                                if continuelabel563 is True:
                                                    break

                                            if continuelabel563 is True:
                                                continue

                                            entityBuffer[var21] = var12
                                            var21 += 1
                                            var24 = regionvars.screenCenterX - \
                                                var12.relativeX
                                            var14 = var12.offsetX - \
                                                regionvars.screenCenterX
                                            if(var14 > var24):
                                                var24 = var14

                                            var15 = regionvars.screenCenterZ - \
                                                var12.relativeY
                                            var16 = var12.offsetY - \
                                                regionvars.screenCenterZ
                                            if(var16 > var15):
                                                var12.drawPriority = var24 + var16
                                            else:
                                                var12.drawPriority = var24 + var15

                                    # While (True)..., but only initiate when there are var21 (>0) entities in buffer
                                    while(var21 > 0):
                                        var11 = -50
                                        var25 = -1

                                        for var24 in range(0, var21):
                                            var35 = entityBuffer[var24]
                                            if(var35.cycle != regionvars.cycle):
                                                if(var35.drawPriority > var11):
                                                    var11 = var35.drawPriority
                                                    var25 = var24
                                                elif(var11 == var35.drawPriority):
                                                    var15 = var35.x - \
                                                        regionvars.cameraX2
                                                    var16 = var35.y - \
                                                        regionvars.cameraZ2
                                                    var17 = entityBuffer[var25].x - \
                                                        regionvars.cameraX2
                                                    var18 = entityBuffer[var25].y - \
                                                        regionvars.cameraZ2
                                                    if(var15 * var15 + var16 * var16 > var17 * var17 + var18 * var18):
                                                        var25 = var24

                                        if(var25 == -1):
                                            break

                                        var33 = entityBuffer[var25]
                                        var33.cycle = regionvars.cycle
                                        if(not isAreaOccluded(field2025, regionvars, tileCycles, var7, var33.relativeX, var33.offsetX, var33.relativeY, var33.offsetY, var33.renderable.modelHeight, tileHeights)):

                                            intermediatex = var33.x - \
                                                regionvars.cameraX2
                                            intermediatey = var33.height - \
                                                regionvars.cameraY2
                                            intermediatez = var33.y - \
                                                regionvars.cameraZ2

                                            drawModel(colorPalette, staticModel_, var33.renderable, var33.orientation, regionvars.pitchSin, regionvars.pitchCos, regionvars.yawSin, regionvars.yawCos,
                                                      intermediatex, intermediatey, intermediatez, var33.hash, Graphics3D_, tileHeights, textures, objectDefinitions)

                                        for var14 in range(var33.relativeX, var33.offsetX + 1):
                                            for var15 in range(var33.relativeY, var33.offsetY + 1):
                                                # tiles[var6][var14][var15]
                                                var26 = getTile(
                                                    var8plane, var14, var15, tiles)
                                                if(var26.wallCullDirection != 0):

                                                    #print("Wallcull1", var8plane, var14, var15)

                                                    Deque_.addFront(
                                                        getTileID(var26))

                                                elif((var14 != var4 or var15 != var5) and var26.visible):

                                                    #print("Wallcull2", var8plane, var14, var15)

                                                    Deque_.addFront(
                                                        getTileID(var26))

                                    if(not currTile.drawEntities):
                                        #print("breaked on drawEntities")
                                        break
                                    # print("SANITYCHECK2")

                                #print("what the fuck ever here?", currTile.visible)

                                if currTile.visible:
                                    break

                            # print("break0")

                            if not currTile.wallCullDirection != 0:
                                break

                        #print("break1", var4, regionvars.screenCenterX, regionvars.minTileX)

                        if(var4 > regionvars.screenCenterX or var4 <= regionvars.minTileX):
                            # print("break2")
                            break

                        var9 = getTile(var8plane, var4 - 1, var5, tiles)

                        if not var9.visible:
                            break

                    # print("break3")

                    if(var4 < regionvars.screenCenterX or var4 >= regionvars.maxTileX - 1):
                        # print("break4")
                        break

                    var9 = getTile(var8plane, var4 + 1, var5, tiles)

                    if not var9.visible:
                        break

                # print("break5")

                if(var5 > regionvars.screenCenterZ or var5 <= regionvars.minTileZ):
                    # print("break6")
                    break

                var9 = getTile(var8plane, var4, var5 - 1, tiles)

                if not var9.visible:
                    break

            # print("break7")

            if(var5 < regionvars.screenCenterZ or var5 >= regionvars.maxTileZ - 1):
                # print("break8")
                break

            var9 = getTile(var8plane, var4, var5 + 1, tiles)
            if not var9.visible:
                break

        # print("break9")

        #print("End of massive whiles")

        currTile.visible = False
        regionvars.tileUpdateCount -= 1
        # var32 = currTile.itemLayer
        # if(var32 != None and var32.height != 0):
        #     if(var32.middle != None) :
        #         var32.middle.draw(0, regionvars.pitchSin, regionvars.pitchCos, regionvars.yawSin, regionvars.yawCos, var32.x - regionvars.cameraX2, var32.hash - regionvars.cameraY2 - var32.height, var32.y - regionvars.cameraZ2, var32.flags)

        #     if(var32.top != None) :
        #         var32.top.draw(0, regionvars.pitchSin, regionvars.pitchCos, regionvars.yawSin, regionvars.yawCos, var32.x - regionvars.cameraX2, var32.hash - regionvars.cameraY2 - var32.height, var32.y - regionvars.cameraZ2, var32.flags)

        #     if(var32.bottom != None) :
        #         var32.bottom.draw(0, regionvars.pitchSin, regionvars.pitchCos, regionvars.yawSin, regionvars.yawCos, var32.x - regionvars.cameraX2, var32.hash - regionvars.cameraY2 - var32.height, var32.y - regionvars.cameraZ2, var32.flags)

        if(currTile.wallDrawFlags != 0):
            var29 = currTile.decorativeObject

            if(var29 is not None and not isOccluded4(field2025, regionvars, tileCycles, var7, var4, var5, var29.renderable1.modelHeight, tileHeights)):
                if((var29.renderFlag & currTile.wallDrawFlags) != 0):
                    # var29.renderable1.draw(0, regionvars.pitchSin, regionvars.pitchCos, regionvars.yawSin, regionvars.yawCos, var29.x - regionvars.cameraX2 +
                    #                       var29.offsetX, var29.floor - regionvars.cameraY2, var29.y - regionvars.cameraZ2 + var29.offsetY, var29.hash)
                    drawModel(colorPalette, staticModel_, var29.renderable1, 0, regionvars.pitchSin, regionvars.pitchCos, regionvars.yawSin, regionvars.yawCos, var29.x - regionvars.cameraX2 +
                              var29.offsetX, var29.floor - regionvars.cameraY2, var29.y - regionvars.cameraZ2 + var29.offsetY, var29.hash, Graphics3D_, tileHeights, textures, objectDefinitions)
                elif(var29.renderFlag == 256):
                    var11 = var29.x - regionvars.cameraX2
                    var25 = var29.floor - regionvars.cameraY2
                    var24 = var29.y - regionvars.cameraZ2
                    var14 = var29.rotation
                    if(var14 != 1 and var14 != 2):
                        var15 = var11
                    else:
                        var15 = -var11

                    if(var14 != 2 and var14 != 3):
                        var16 = var24
                    else:
                        var16 = -var24

                    if(var16 >= var15):
                        # var29.renderable1.draw(0, regionvars.pitchSin, regionvars.pitchCos, regionvars.yawSin, regionvars.yawCos,
                        #                       var11 + var29.offsetX, var25, var24 + var29.offsetY, var29.hash)
                        drawModel(colorPalette, staticModel_, var29.renderable1, 0, regionvars.pitchSin, regionvars.pitchCos, regionvars.yawSin, regionvars.yawCos,
                                  var11 + var29.offsetX, var25, var24 + var29.offsetY, var29.hash, Graphics3D_, tileHeights, textures, objectDefinitions)
                    elif(var29.renderable2 is not None):
                        # var29.renderable2.draw(
                        #    0, regionvars.pitchSin, regionvars.pitchCos, regionvars.yawSin, regionvars.yawCos, var11, var25, var24, var29.hash)
                        drawModel(colorPalette, staticModel_, var29.renderable2, 0, regionvars.pitchSin, regionvars.pitchCos, regionvars.yawSin, regionvars.yawCos,
                                  var11, var25, var24, var29.hash, Graphics3D_, tileHeights, textures, objectDefinitions)

            var27 = currTile.wallObject
            if(var27 is not None):
                if((var27.orientationB & currTile.wallDrawFlags) != 0 and not isWallOccluded(field2025, regionvars, tileCycles, var7, var4, var5, var27.orientationB, tileHeights)):
                    # var27.renderable2.draw(0, regionvars.pitchSin, regionvars.pitchCos, regionvars.yawSin, regionvars.yawCos, var27.x -
                    #                       regionvars.cameraX2, var27.floor - regionvars.cameraY2, var27.y - regionvars.cameraZ2, var27.hash)
                    drawModel(colorPalette, staticModel_, var27.renderable2, 0, regionvars.pitchSin, regionvars.pitchCos, regionvars.yawSin, regionvars.yawCos, var27.x -
                              regionvars.cameraX2, var27.floor - regionvars.cameraY2, var27.y - regionvars.cameraZ2, var27.hash, Graphics3D_, tileHeights, textures, objectDefinitions)

                if((var27.orientationA & currTile.wallDrawFlags) != 0 and not isWallOccluded(field2025, regionvars, tileCycles, var7, var4, var5, var27.orientationA, tileHeights)):
                    # var27.renderable1.draw(0, regionvars.pitchSin, regionvars.pitchCos, regionvars.yawSin, regionvars.yawCos, var27.x -
                    #                       regionvars.cameraX2, var27.floor - regionvars.cameraY2, var27.y - regionvars.cameraZ2, var27.hash)

                    drawModel(colorPalette, staticModel_, var27.renderable1, 0, regionvars.pitchSin, regionvars.pitchCos, regionvars.yawSin, regionvars.yawCos, var27.x -
                              regionvars.cameraX2, var27.floor - regionvars.cameraY2, var27.y - regionvars.cameraZ2, var27.hash, Graphics3D_, tileHeights, textures, objectDefinitions)

        if(var6 < maxYregion - 1):
            # tiles[var6 + 1][var4][var5]
            var30 = getTile(var6 + 1, var4, var5, tiles)
            if(var30.visible):
                #print("Endcull1", var6 + 1, var4, var5)

                Deque_.addFront(getTileID(var30))

        if(var4 < regionvars.screenCenterX):
            # tiles[var6][var4 + 1][var5]
            var30 = getTile(var8plane, var4 + 1, var5, tiles)
            if(var30.visible):
                #print("Endcull2", var8plane, var4 + 1, var5)

                Deque_.addFront(getTileID(var30))

        if(var5 < regionvars.screenCenterZ):
            # tiles[var6][var4][var5 + 1]
            var30 = getTile(var8plane, var4, var5 + 1, tiles)
            if(var30.visible):
                #print("Endcull3", var8plane, var4, var5 + 1)

                Deque_.addFront(getTileID(var30))

        if(var4 > regionvars.screenCenterX):
            # tiles[var6][var4 - 1][var5]
            var30 = getTile(var8plane, var4 - 1, var5, tiles)
            if(var30.visible):
                #print("Endcull4", var8plane, var4 - 1, var5)

                Deque_.addFront(getTileID(var30))

        if(var5 > regionvars.screenCenterZ):
            # tiles[var6][var4][var5 - 1]
            var30 = getTile(var8plane, var4, var5 - 1, tiles)
            if(var30.visible):
                #print("Endcull5", var8plane, var4, var5 - 1)

                Deque_.addFront(getTileID(var30))

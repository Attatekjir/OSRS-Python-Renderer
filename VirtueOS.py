# %%
from __future__ import print_function, absolute_import
import sys
import PyQt5
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from colorPalette import initiateColorPalette
from Region import Region
from Deque import Deque
from wdfisthis import tst
from GameObject import GameObject
from fileCounts import FILECOUNTS195
from expModel import staticModel
from Occluder import Occluder
import numpy as np

from loadTerrainUtills import loadChunk
from Region import buildVisibilityMaps
import numba
from numba import typed
from numba import jit
from random import random
import time
from numba import int32, float32   # import the types
from cacheStore import cacheStore
from utills import hslToRGB
from regionIdTomapindex import regionIdToMapIndex
from Graphics3D import Graphics3D

from Tile import Tile
from cacheUtills import FileStore
from MathUtills import integerdivide
import time
import matplotlib.pyplot as plt
from Region import drawRegion
from MathUtills import Graphics3DCOSINE

# %%

cache_folder = "/home/atta/Desktop/cache195/"


# %%

FileStore_ = FileStore(cache_folder)

starttime = time.time()

# Statics
field1790listed = [[1, 3, 5, 7], [1, 3, 5, 7], [1, 3, 5, 7], [1, 3, 5, 7, 6], [1, 3, 5, 7, 6],
                   [1, 3, 5, 7, 6], [1, 3, 5, 7, 6], [1, 3, 5, 7, 2, 6],
                   [1, 3, 5, 7, 2, 8], [1, 3, 5, 7, 2, 8], [1, 3, 5, 7, 11, 12],
                   [1, 3, 5, 7, 11, 12], [1, 3, 5, 7, 13, 14]]

npint32type = numba.typeof(np.empty(shape=(0), dtype=np.int32))
field1790 = numba.typed.List.empty_list(npint32type)
for lst in field1790listed:
    lstasnumpy = np.asarray(lst, dtype=np.int32)
    field1790.append(lstasnumpy)

field1791listed = [[0, 1, 2, 3, 0, 0, 1, 3], [1, 1, 2, 3, 1, 0, 1, 3], [0, 1, 2, 3, 1, 0, 1, 3], [0, 0, 1, 2, 0, 0, 2, 4, 1, 0, 4, 3],
                   [0, 0, 1, 4, 0, 0, 4, 3, 1, 1, 2, 4],
                   [0, 0, 4, 3, 1, 0, 1, 2, 1, 0, 2, 4],
                   [0, 1, 2, 4, 1, 0, 1, 4, 1, 0, 4, 3],
                   [0, 4, 1, 2, 0, 4, 2, 5, 1, 0, 4, 5, 1, 0, 5, 3],
                   [0, 4, 1, 2, 0, 4, 2, 3, 0, 4, 3, 5, 1, 0, 4, 5],
                   [0, 0, 4, 5, 1, 4, 1, 2, 1, 4, 2, 3, 1, 4, 3, 5],
                   [0, 0, 1, 5, 0, 1, 4, 5, 0, 1, 2, 4, 1,
                       0, 5, 3, 1, 5, 4, 3, 1, 4, 2, 3],
                   [1, 0, 1, 5, 1, 1, 4, 5, 1, 1, 2, 4, 0,
                       0, 5, 3, 0, 5, 4, 3, 0, 4, 2, 3],
                   [1, 0, 5, 4, 1, 0, 1, 5, 0, 0, 4, 3, 0, 4, 5, 3, 0, 5, 2, 3, 0, 1, 2, 5]]

field1791 = numba.typed.List.empty_list(npint32type)
for lst in field1791listed:
    lstasnumpy = np.asarray(lst, dtype=np.int32)
    field1791.append(lstasnumpy)

ci = numba.typeof(np.zeros(shape=(0), dtype=np.int8))
uncryptedModelContents = typed.List.empty_list(ci)
for ide in range(FILECOUNTS195.MODELS.value):
    uncryptedModelContents.append(FileStore_.FileStoreRead(7, ide))

cacheStore_ = cacheStore(FileStore_)
sprites = cacheStore_.getAllSprites()
textures = cacheStore_.getAllTextures()
npcDefinitions = cacheStore_.getAllNpcDefinitions()
objectDefinitions = cacheStore_.getAllObjectDefinitions()
underlayDefinitions = cacheStore_.getAllUnderlayDefinitions()
overlayDefinitions = cacheStore_.getAllOverlayDefinitions()

field747 = np.int32(99)
field749 = np.array([1, 2, 4, 8], dtype=np.int32)
field746 = np.array([16, 32, 64, 128], dtype=np.int32)
field738 = np.array([1, 0, -1, 0], dtype=np.int32)
field740 = np.array([0, -1, 0, 1], dtype=np.int32)
field752 = np.array([1, -1, -1, 1], dtype=np.int32)
field750 = np.array([-1, -1, 1, 1], dtype=np.int32)

field2027 = np.asarray(
    [19, 55, 38, 155, 255, 110, 137, 205, 76], dtype=np.int32)
field2040 = np.asarray(
    [160, 192, 80, 96, 0, 144, 80, 48, 160], dtype=np.int32)

TILE_WALL_DRAW_FLAGS_1 = np.asarray(
    [76, 8, 137, 4, 0, 1, 38, 2, 19], dtype=np.int32)
WALL_UNCULL_FLAGS_0 = np.asarray(
    [0, 0, 2, 0, 0, 2, 1, 1, 0], dtype=np.int32)
WALL_UNCULL_FLAGS_1 = np.asarray(
    [2, 0, 0, 2, 0, 0, 0, 4, 4], dtype=np.int32)
WALL_UNCULL_FLAGS_2 = np.asarray(
    [0, 4, 4, 8, 0, 0, 8, 0, 0], dtype=np.int32)
WALL_UNCULL_FLAGS_3 = np.asarray(
    [1, 1, 0, 0, 0, 8, 0, 0, 8], dtype=np.int32)


print("Initiated static variables", time.time() - starttime)


# %%

starttime = time.time()

ci = Occluder.class_type.instance_type
field2025 = numba.typed.List.empty_list(ci)
for var3 in range(0, 500):
    field2025.append(Occluder())

ci = GameObject.class_type.instance_type
regionobjects = numba.typed.List.empty_list(ci)
for i in range(5000):
    regionobjects.append(GameObject())

entityBuffer = numba.typed.List.empty_list(ci)  # [None] * 100
for i in range(100):
    entityBuffer.append(GameObject())

ci = Occluder.class_type.instance_type
lci = numba.typed.List.empty_list(ci)
lci_type = numba.typeof(lci)

MAX_OCCLUDER_LEVELS = 4
levelOccluders = numba.typed.List.empty_list(lci_type)
for var2 in range(0, MAX_OCCLUDER_LEVELS):
    lci = numba.typed.List.empty_list(ci)
    for var3 in range(0, 500):
        lci.append(Occluder())
    levelOccluders.append(lci)

graphics3d = Graphics3D()
staticModel_ = staticModel()
Deque_ = Deque()
regionvars = Region()
maxYregion, maxXregion, maxZregion = 4, 104, 104
tiles = numba.typed.List.empty_list(Tile.class_type.instance_type)
for k in range(maxYregion):
    for l in range(maxXregion):
        for m in range(maxZregion):
            tiles.append(Tile(k, l, m))

tileHeights = np.empty(shape=(4, 105, 105), dtype=np.int32)
tileSettings = np.empty(shape=(4, 104, 104), dtype=np.byte)
tileUnderlayIds = np.empty(shape=(4, 104, 104), dtype=np.byte)
tileOverlayIds = np.empty(shape=(4, 104, 104), dtype=np.byte)
tileOverlayPath = np.empty(shape=(4, 104, 104), dtype=np.byte)
overlayRotations = np.empty(shape=(4, 104, 104), dtype=np.byte)
field2520 = np.empty(shape=(4, 105, 105), dtype=np.int32)
field3831 = np.empty(shape=(4, 105, 105), dtype=np.byte)

tmpScreenX = np.empty(shape=(6), dtype=np.int32)
tmpScreenY = np.empty(shape=(6), dtype=np.int32)
vertexSceneX = np.empty(shape=(6), dtype=np.int32)
vertexSceneY = np.empty(shape=(6), dtype=np.int32)
vertexSceneZ = np.empty(shape=(6), dtype=np.int32)

levelOccluderCount = np.empty(shape=(MAX_OCCLUDER_LEVELS), dtype=np.int32)
tileCycles = np.empty(shape=(maxYregion, maxXregion + 1,
                      maxZregion + 1), dtype=np.int32)

# Will get filled with zeros anyway
floorSaturations = np.empty(shape=(104), dtype=np.int32)
floorHues = np.empty(shape=(104), dtype=np.int32)
floorMultiplier = np.empty(shape=(104), dtype=np.int32)
field3314 = np.empty(shape=(104), dtype=np.int32)
field1356 = np.empty(shape=(104), dtype=np.int32)

# Need to be zeros
field1354 = np.empty(shape=(105, 105), dtype=np.int32)

colorPalette = np.empty(shape=(65536), dtype=np.int32)

print("Initiated variables which fill get reset every run", time.time() - starttime)

# %%


tileHeights.fill(0)
tileSettings.fill(0)
tileUnderlayIds.fill(0)
tileOverlayIds.fill(0)
tileOverlayPath.fill(0)
overlayRotations.fill(0)
field2520.fill(0)
field3831.fill(0)


regionvars.reset()

for tile in tiles:
    tile.reset()

# %%


starttime = time.time()

x = 3300  # 3250  # 3250  # 3250  # 3300
y = 2900  # 3250  # 3250  # 3420  # 3300
loadChunk(uncryptedModelContents, regionobjects, field2025, regionvars, maxYregion, maxXregion, maxZregion, x, y, FileStore_, field2520, field3831, objectDefinitions,
          field749, field746, field738, field740, field752, field750, tileSettings, tileHeights,
          tileOverlayIds, tileUnderlayIds, tileOverlayPath, overlayRotations, regionIdToMapIndex, tiles)

print("LoadChunk: ", time.time() - starttime)


# %%

levelOccluderCount.fill(0)

field751 = np.int32(random() * 17.0 - 8)
field745 = np.int32(random() * 33.0 - 16)

brightness = 0.6
colorPalette = initiateColorPalette(colorPalette, brightness)

starttime = time.time()

tst(floorSaturations, floorHues, floorMultiplier, field3314, field1356, field1354,
    colorPalette, field2520, field3831, tileHeights, tileUnderlayIds, underlayDefinitions, tileSettings,
    tiles, tileOverlayIds, levelOccluders, levelOccluderCount, field751, tileOverlayPath,
    overlayDefinitions, field745, field1790, field1791, textures, overlayRotations)

print(time.time() - starttime)


# %%


# def determineRenderTillLevel():
#     BoundingBox3DDrawModeplane = 0
#     ClientlocalPlayery = 0  # 1000 #7616 #25 * 64 * 2
#     ClientlocalPlayerx = 0  # 1000 #3776 #40 * 64 * 2
#     field578 = -ClientlocalPlayery  # localPlayer.y
#     field2228 = ClientlocalPlayerx  # localPlayer.x
#     field960 = 1  # or 0
#     var6 = 3
#     if(cameraPitch < 310):
#         if(field960 == 1):
#             var7 = field2228 >> 7
#             var8 = field578 >> 7
#         else:
#             var7 = ClientlocalPlayerx >> 7
#             var8 = ClientlocalPlayery >> 7

#         var9 = PlayercameraX >> 7
#         var10 = PlayercameraY >> 7
#         if(var9 < 0 or var10 < 0 or var9 >= 104 or var10 >= 104):
#             var5 = BoundingBox3DDrawModeplane
#             return var5

#         if(var7 < 0 or var8 < 0 or var7 >= 104 or var8 >= 104):
#             var5 = BoundingBox3DDrawModeplane
#             return var5

#         if((tileSettings[BoundingBox3DDrawModeplane][var9][var10] & 4) != 0):
#             var6 = BoundingBox3DDrawModeplane

#         if(var7 > var9):
#             var11 = var7 - var9
#         else:
#             var11 = var9 - var7

#         if(var8 > var10):
#             var12 = var8 - var10
#         else:
#             var12 = var10 - var8

#         if(var11 > var12):
#             var13 = integerdivide(var12 * 65536, var11)
#             var14 = 32768

#             while(var7 != var9):
#                 if(var9 < var7):
#                     var9 += 1
#                 elif(var9 > var7):
#                     var9 -= 1

#                 if((tileSettings[BoundingBox3DDrawModeplane][var9][var10] & 4) != 0):
#                     var6 = BoundingBox3DDrawModeplane

#                 var14 += var13
#                 if(var14 >= 65536):
#                     var14 -= 65536
#                     if(var10 < var8):
#                         var10 += 1
#                     elif(var10 > var8):
#                         var10 -= 1

#                     if((tileSettings[BoundingBox3DDrawModeplane][var9][var10] & 4) != 0):
#                         var6 = BoundingBox3DDrawModeplane

#         elif(var12 > 0):
#             var13 = integerdivide(var11 * 65536, var12)
#             var14 = 32768

#             while(var10 != var8):
#                 if(var10 < var8):
#                     var10 += 1
#                 elif(var10 > var8):
#                     var10 -= 1

#                 if((tileSettings[BoundingBox3DDrawModeplane][var9][var10] & 4) != 0):
#                     var6 = BoundingBox3DDrawModeplane

#                 var14 += var13
#                 if(var14 >= 65536):
#                     var14 -= 65536
#                     if(var9 < var7):
#                         var9 += 1
#                     elif(var9 > var7):
#                         var9 -= 1

#                     if((tileSettings[BoundingBox3DDrawModeplane][var9][var10] & 4) != 0):
#                         var6 = BoundingBox3DDrawModeplane

#     if(ClientlocalPlayerx >= 0 and ClientlocalPlayery >= 0 and ClientlocalPlayerx < 13312 and ClientlocalPlayery < 13312):
#         if((tileSettings[BoundingBox3DDrawModeplane][ClientlocalPlayerx >> 7][ClientlocalPlayery >> 7] & 4) != 0):
#             var6 = BoundingBox3DDrawModeplane
#         var5 = var6
#     else:
#         var5 = BoundingBox3DDrawModeplane

#     return var5


# %%

# Set to 0 if inside, or camera near building
renderTillLevel = 0  # 3 == ALL
minLevel = 0

canvaswidth = 1500  # 512
canvasheight = 1200  # 334

# Need function around it
visibilityMaps = buildVisibilityMaps(
    500, 800, canvaswidth, canvasheight)


graphics3d.reset(canvaswidth, canvasheight)
staticModel_.reset()

tileCycles.fill(0)
tmpScreenX.fill(0)
tmpScreenY.fill(0)
vertexSceneX.fill(0)
vertexSceneY.fill(0)
vertexSceneZ.fill(0)


cameraPitch = 310  # 310 >= different behavior
PlayercameraX = 70 * 64 * 2  # 50 # drawRegion
PlayercameraY = (65 - 24) * 64 * 2  # drawRegion

print("Lets draw region")
starttime = time.time()


#class255region.drawRegion(20 * 64 * 2, -1500, 23 * 64 * 2, 383, 1, renderTillLevel, graphics3d)
drawRegion(colorPalette, field2027, field2040, TILE_WALL_DRAW_FLAGS_1, WALL_UNCULL_FLAGS_0, WALL_UNCULL_FLAGS_1, WALL_UNCULL_FLAGS_2, WALL_UNCULL_FLAGS_3,
           entityBuffer, visibilityMaps, field2025, regionvars, staticModel_, Deque_, tileCycles, minLevel, maxYregion,
           maxXregion, maxZregion, levelOccluders, levelOccluderCount, vertexSceneX, vertexSceneY, vertexSceneZ, tmpScreenX, tmpScreenY, PlayercameraX, -1200, PlayercameraY,
           cameraPitch, 1, renderTillLevel, graphics3d, tileHeights, tiles, textures, objectDefinitions)

print("drawRegion in: ", time.time() - starttime)

# %%


@jit(nopython=True, cache=False)
def oke(graphicsPixels, canvasheight, canvaswidth):

    canvas = np.zeros(shape=(canvasheight, canvaswidth, 3), dtype=np.uint8)
    cntr = 0
    for h in range(0, canvasheight):
        for w in range(0, canvaswidth):

            pixel = graphicsPixels[cntr]
            r, g, b = hslToRGB(pixel)

            canvas[h, w, 0:3] = r, g, b
            cntr += 1

    return canvas


canvas = oke(graphics3d.graphicsPixels, canvasheight, canvaswidth)
rnds = np.random.randint(low=0, high=256, size=(66000, 3))


@jit(nopython=True, cache=False)
def MkAnnotationCanvas(annotationCanvas, canvasheight, canvaswidth, rnds):

    canvas = np.empty(shape=(canvasheight, canvaswidth, 3), dtype=np.uint8)

    cntr = 0
    for h in range(0, canvasheight):
        for w in range(0, canvaswidth):

            pixel = annotationCanvas[cntr]
            if pixel == 0:
                canvas[h, w, 0:3] = 0
            else:
                canvas[h, w, 0:3] = rnds[pixel, :]

            cntr += 1

    return canvas


gameCanvas = oke(graphics3d.graphicsPixels, canvasheight, canvaswidth)

plt.imshow(canvas)
plt.show()


annotationCanvas = MkAnnotationCanvas(
    graphics3d.annotationCanvas, canvasheight, canvaswidth, rnds)

plt.imshow(annotationCanvas)
plt.show()


# %%


class Canvas(QPlainTextEdit):
    def __init__(self):
        super().__init__()
        self.keyspressed = set()
        self.xcoordCamera = 50
        self.ycoordCamera = 50
        self.zcoordCamera = -1200
        self.displaychannel = 1
        self.pitchCamera = 310
        self.rotate = 1
        self.xregion = 3300
        self.yregion = 2900

        self.loadChunk(self.xregion, self.yregion)

    def keyReleaseEvent(self, event):
        self.keyspressed.remove(event.key())

    def keyPressEvent(self, event):
        self.keyspressed.add(event.key())

        for eventkey in self.keyspressed:

            if eventkey == Qt.Key_1:
                self.displaychannel = 1
            elif eventkey == Qt.Key_2:
                self.displaychannel = 2

            elif eventkey == Qt.Key_Up:
                self.pitchCamera = min(self.pitchCamera + 5, 400)
            elif eventkey == Qt.Key_Down:
                self.pitchCamera = max(self.pitchCamera - 5, 1)

            elif eventkey == Qt.Key_Left:
                self.rotate = min(self.rotate + 10, 65536)
            elif eventkey == Qt.Key_Right:
                self.rotate = max(self.rotate - 10, -65536)

            elif eventkey == Qt.Key_A:
                self.xcoordCamera = min(max(self.xcoordCamera - 1, 0), 103)
            elif eventkey == Qt.Key_D:
                self.xcoordCamera = min(max(self.xcoordCamera + 1, 0), 103)
            elif eventkey == Qt.Key_S:
                self.ycoordCamera = min(max(self.ycoordCamera - 1, 0), 103)
            elif eventkey == Qt.Key_W:
                self.ycoordCamera = min(max(self.ycoordCamera + 1, 0), 103)
            elif eventkey == Qt.Key_Space:
                self.zcoordCamera = min(max(self.zcoordCamera - 10, -4000), 0)
            elif eventkey == Qt.Key_C:
                self.zcoordCamera = min(max(self.zcoordCamera + 10, -4000), 0)

        self.viewport().update()

    def loadChunk(self, x, y):
        tileHeights.fill(0)
        tileSettings.fill(0)
        tileUnderlayIds.fill(0)
        tileOverlayIds.fill(0)
        tileOverlayPath.fill(0)
        overlayRotations.fill(0)
        field2520.fill(0)
        field3831.fill(0)

        regionvars.reset()

        for tile in tiles:
            tile.reset()

        #x = 3300  # 3250  # 3250  # 3250  # 3300
        #y = 2900  # 3250  # 3250  # 3420  # 3300
        loadChunk(uncryptedModelContents, regionobjects, field2025, regionvars, maxYregion, maxXregion, maxZregion, x, y, FileStore_, field2520, field3831, objectDefinitions,
                  field749, field746, field738, field740, field752, field750, tileSettings, tileHeights,
                  tileOverlayIds, tileUnderlayIds, tileOverlayPath, overlayRotations, regionIdToMapIndex, tiles)

    def mousePressEvent(self, event):

        print(event.pos())

        self.viewport().update()

    def paintEvent(self, event):
        super().paintEvent(event)
        self.refreshCanvas()

    def refreshCanvas(self):

        levelOccluderCount.fill(0)
        field751 = np.int32(random() * 17.0 - 8)
        field745 = np.int32(random() * 33.0 - 16)

        brightness = 0.6
        colorPalette = np.empty(shape=(65536), dtype=np.int32)
        colorPalette = initiateColorPalette(colorPalette, brightness)

        tst(floorSaturations, floorHues, floorMultiplier, field3314, field1356, field1354,
            colorPalette, field2520, field3831, tileHeights, tileUnderlayIds, underlayDefinitions, tileSettings,
            tiles, tileOverlayIds, levelOccluders, levelOccluderCount, field751, tileOverlayPath,
            overlayDefinitions, field745, field1790, field1791, textures, overlayRotations)

        # Set to 0 if inside, or camera near building
        renderTillLevel = 0  # 3 == ALL
        minLevel = 0

        canvaswidth = max(self.width(), 512)  # 1500  # 512
        canvasheight = max(self.height(), 334)  # 1200  # 334

        # Need function around it
        visibilityMaps = buildVisibilityMaps(
            500, 800, canvaswidth, canvasheight)

        graphics3d.reset(canvaswidth, canvasheight)
        staticModel_.reset()

        tileCycles.fill(0)
        tmpScreenX.fill(0)
        tmpScreenY.fill(0)
        vertexSceneX.fill(0)
        vertexSceneY.fill(0)
        vertexSceneZ.fill(0)

        cameraPitch = self.pitchCamera  # 310 >= different behavior
        PlayercameraX = self.xcoordCamera * 64 * 2  # 50 # drawRegion
        PlayercameraY = self.ycoordCamera * 64 * 2  # drawRegion

        #print("Lets draw region")
        #starttime = time.time()

        #class255region.drawRegion(20 * 64 * 2, -1500, 23 * 64 * 2, 383, 1, renderTillLevel, graphics3d)
        drawRegion(colorPalette, field2027, field2040, TILE_WALL_DRAW_FLAGS_1, WALL_UNCULL_FLAGS_0, WALL_UNCULL_FLAGS_1, WALL_UNCULL_FLAGS_2, WALL_UNCULL_FLAGS_3,
                   entityBuffer, visibilityMaps, field2025, regionvars, staticModel_, Deque_, tileCycles, minLevel, maxYregion,
                   maxXregion, maxZregion, levelOccluders, levelOccluderCount, vertexSceneX, vertexSceneY, vertexSceneZ, tmpScreenX, tmpScreenY, PlayercameraX, self.zcoordCamera, PlayercameraY,
                   cameraPitch, self.rotate, renderTillLevel, graphics3d, tileHeights, tiles, textures, objectDefinitions)

        #print("drawRegion in: ", time.time() - starttime)

        if self.displaychannel == 2:
            canvas_ = MkAnnotationCanvas(
                graphics3d.annotationCanvas, canvasheight, canvaswidth, rnds)

        else:  # self.displaychannel == 1:
            canvas_ = oke(graphics3d.graphicsPixels, canvasheight, canvaswidth)

        cvImg = canvas_
        #cvImg = np.random.randint(low = 0, high = 255, size = (100, 150, 4), dtype = np.uint8)

        height, width, channel = cvImg.shape
        #bytesPerLine = 4 * width
        #qImg = QImage(cvImg.data, width, height, bytesPerLine, QImage.Format_RGBA8888)

        bytesPerLine = 3 * width
        qImg = QImage(cvImg.data, width, height,
                      bytesPerLine, QImage.Format_RGB888)

        xd = QPixmap(qImg)

        #rndom = np.random.randint(low = 0, high = 255, size = (2), dtype = np.uint8)
        painter = QPainter(self.viewport())
        painter.drawPixmap(QPoint(0, 40), xd)  # hole_pos - _offset, _bullet)


# Construct the QApplication before a QWidget
app = QApplication(sys.argv)
app.setCursorFlashTime(1000)
# app.setObjectName("GfG")
app.setApplicationName("ApplicationName")
app.beep()


# The rest of the code is as for the normal version of the text editor.


class MainWindow(QMainWindow):

    def closeEvent(self, event):

        answer = QMessageBox.question(window, None,
                                      "Bruh, u sure to exit?",
                                      QMessageBox.Save | QMessageBox.Discard | QMessageBox.Cancel | QMessageBox.No
                                      )
        if answer & QMessageBox.Cancel:
            event.ignore()
        elif answer & QMessageBox.Save:
            self.save()
        else:  # QMessageBox.Discard
            return

    def save(self):

        print('saved btw')
        # if file_path is None:
        #     save_as()
        # else:
        #     with open(file_path, "w") as f:
        #         f.write(text.toPlainText())
        #     text.document().setModified(False)


window = MainWindow()


# Add a
text = Canvas()
text.setPlainText("Sample PlainText")
window.setCentralWidget(text)

file_menu = window.menuBar().addMenu("&File")
close = QAction("&Close")
close.triggered.connect(window.close)
file_menu.addAction(close)

help_menu = window.menuBar().addMenu("&Help")
about_action = QAction("&About")
help_menu.addAction(about_action)


def show_about_dialog():
    text = 'Lol if u press the help button u see this'

    QMessageBox.about(window, "About Text Editor", text)
    QMessageBox.warning(window, "About Text Editor", text)
    QMessageBox.information(window, "About Text Editor", text)


about_action.triggered.connect(show_about_dialog)

window.show()
app.exec_()

# %%

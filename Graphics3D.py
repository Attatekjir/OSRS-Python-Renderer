from numba import jit
from MathUtills import integerdivide
import numpy as np
import MathUtills
from TextureProvider import TextureLoaderGetAverageTextureRGB, TextureLoaderLoad, TextureLoaderVmethod3069, TextureLoaderIsLowMem
from numba import int32, float32, boolean, short, int64
from numba.experimental import jitclass
from colorPalette import initiateColorPalette


@jitclass()
class Graphics3D:

    # SELF INIT
    centerX: int32
    centerY: int32
    rasterClipX: int32
    Rasterizer3D_clipHeight: int32
    Rasterizer3D_clipNegativeMidX: int32
    Rasterizer3D_clipMidX2: int32
    Rasterizer3D_clipNegativeMidY: int32
    Rasterizer3D_clipMidY2: int32

    rasterAlpha: int32
    Rasterizer3D_zoom: int32

    graphicsPixelsWidth: int32
    graphicsPixelsHeight: int32
    draw_region_x: int32
    drawingAreaTop: int32
    drawingAreaBottom: int32
    drawingAreaRight: int32

    # # FROM OFFICIAL STATIC INIT
    rasterClipEnable: boolean
    field1944: boolean
    lowMem: boolean
    rasterGouraudLowRes: boolean

    rasterClipY: int32[:]
    #colorPalette: int32[:]
    #field1960 : int32[:]
    field1952: int32[:]

    annotationCanvas: int32[:]  # numba.optional(int32[:])
    graphicsPixels: int32[:]  # numba.optional(int32[:])

    def __init__(self):

        # # SELF INIT
        # self.centerX = 0
        # self.centerY = 0
        # self.rasterClipX = 0
        # self.Rasterizer3D_clipHeight = 0
        # self.Rasterizer3D_clipNegativeMidX = 0
        # self.Rasterizer3D_clipMidX2 = 0
        # self.Rasterizer3D_clipNegativeMidY = 0
        # self.Rasterizer3D_clipMidY2 = 0
        # self.rasterAlpha = 0
        # self.Rasterizer3D_zoom = 390  # 512 #492
        # self.graphicsPixelsWidth = 0
        # self.graphicsPixelsHeight = 0
        # self.draw_region_x = 0
        # self.drawingAreaTop = 0
        # self.drawingAreaBottom = 0
        # self.drawingAreaRight = 0

        # self.rasterClipEnable = False
        # self.field1944 = False
        # self.lowMem = False
        # self.rasterGouraudLowRes = True

        # gets set in reset
        self.rasterClipY = np.empty(shape=(1024), dtype=np.int32)

        

        # self.field1960 = np.empty(shape=(512), dtype=np.int32)
        # self.field1960[0] = 0
        # for var0 in range(1, 512):
        #     self.field1960[var0] = integerdivide(32768, var0)

        self.field1952 = np.empty(shape=(2048), dtype=np.int32)
        self.field1952[0] = 0
        for var0 in range(1, 2048):
            self.field1952[var0] = integerdivide(65536, var0)

        #self.reset(canvaswidth, canvasheight)


    def reset(self, canvaswidth, canvasheight):

        # SELF INIT
        self.centerX = 0
        self.centerY = 0
        self.rasterClipX = 0
        self.Rasterizer3D_clipHeight = 0
        self.Rasterizer3D_clipNegativeMidX = 0
        self.Rasterizer3D_clipMidX2 = 0
        self.Rasterizer3D_clipNegativeMidY = 0
        self.Rasterizer3D_clipMidY2 = 0
        self.rasterAlpha = 0
        self.Rasterizer3D_zoom = 390  # 512 #492
        self.graphicsPixelsWidth = 0
        self.graphicsPixelsHeight = 0
        self.draw_region_x = 0
        self.drawingAreaTop = 0
        self.drawingAreaBottom = 0
        self.drawingAreaRight = 0

        self.rasterClipEnable = False
        self.field1944 = False
        self.lowMem = False
        self.rasterGouraudLowRes = True

        self.rasterClipY.fill(0)

        

        self.setRasterBuffer(canvaswidth, canvasheight)
        self.Rasterizer3D_method1()


    def Rasterizer3D_method1(self):
        self.setRasterClipping(self.draw_region_x, self.drawingAreaTop,
                               self.drawingAreaBottom, self.drawingAreaRight)

    def setRasterClipping(self, var0,  var1,  var2,  var3):
        self.rasterClipX = var2 - var0
        self.Rasterizer3D_clipHeight = var3 - var1
        self.Rasterizer3D_method3()
        if(len(self.rasterClipY) < self.Rasterizer3D_clipHeight):
            self.rasterClipY = np.zeros(shape=(MathUtills.nextPowerOfTwo(
                self.Rasterizer3D_clipHeight)), dtype=np.int32)

        var4 = var0 + \
            self.graphicsPixelsWidth * var1
        for var5 in range(0, self.Rasterizer3D_clipHeight):
            self.rasterClipY[var5] = var4
            var4 += self.graphicsPixelsWidth

    def Rasterizer3D_method3(self):
        self.centerX = integerdivide(
            self.rasterClipX, 2)
        self.centerY = integerdivide(
            self.Rasterizer3D_clipHeight, 2)
        self.Rasterizer3D_clipNegativeMidX = - \
            self.centerX
        self.Rasterizer3D_clipMidX2 = self.rasterClipX - \
            self.centerX
        self.Rasterizer3D_clipNegativeMidY = - \
            self.centerY
        self.Rasterizer3D_clipMidY2 = self.Rasterizer3D_clipHeight - \
            self.centerY

    def setRasterBuffer(self, canvaswidth, canvasheight):

        # Canvas to draw the "game" on
        self.graphicsPixels = np.zeros(
            shape=(canvaswidth * canvasheight), dtype=np.int32)
        self.graphicsPixelsWidth = canvaswidth
        self.graphicsPixelsHeight = canvasheight

        # Canvas to paint the annotations of the models on
        self.annotationCanvas = np.zeros(
            shape=(canvaswidth * canvasheight), dtype=np.int32)

        self.setDrawRegion(0, 0, canvaswidth, canvasheight)

    def setDrawRegion(self, var0, var1, var2, var3):
        if(var0 < 0):
            var0 = 0

        if(var1 < 0):
            var1 = 0

        if(var2 > self.graphicsPixelsWidth):
            var2 = self.graphicsPixelsWidth

        if(var3 > self.graphicsPixelsHeight):
            var3 = self.graphicsPixelsHeight

        self.draw_region_x = var0
        self.drawingAreaTop = var1
        self.drawingAreaBottom = var2
        self.drawingAreaRight = var3


@jit(nopython=True, cache=False)
def rasterTextureAffine(colorPalette, graphicsobj, objectID, var0, var1, var2, var3, var4, var5, var6, var7, var8,  var9, var10, var11,  var12, var13, var14,  var15, var16, var17,  var18, textures):

    # var19 = graphicsobj.textureLoader.load(var18)
    var19 = TextureLoaderLoad(textures, var18)

    if(var19 is None):
        var20 = TextureLoaderGetAverageTextureRGB(textures, var18)
        rasterGouraud(colorPalette, graphicsobj, objectID, var0, var1, var2, var3, var4, var5, method2797(
            var20, var6), method2797(var20, var7), method2797(var20, var8))
    else:
        graphicsobj.lowMem = TextureLoaderIsLowMem(textures, var18)
        graphicsobj.field1944 = TextureLoaderVmethod3069(textures, var18)
        var20 = var4 - var3
        var21 = var1 - var0
        var22 = var5 - var3
        var23 = var2 - var0
        var24 = var7 - var6
        var25 = var8 - var6
        var26 = 0
        if(var0 != var1):
            var26 = integerdivide((var4 - var3 << 14), (var1 - var0))

        var27 = 0
        if(var2 != var1):
            var27 = integerdivide((var5 - var4 << 14), (var2 - var1))

        var28 = 0
        if(var0 != var2):
            var28 = integerdivide((var3 - var5 << 14), (var0 - var2))

        var29 = var20 * var23 - var22 * var21
        if(var29 != 0):
            var30 = integerdivide(
                (var24 * var23 - var25 * var21 << 9), var29)
            var31 = integerdivide(
                (var25 * var20 - var24 * var22 << 9), var29)
            var10 = var9 - var10
            var13 = var12 - var13
            var16 = var15 - var16
            var11 -= var9
            var14 -= var12
            var17 -= var15
            var32 = var11 * var12 - var9 * var14 << 14
            var33 = np.int32(
                integerdivide(
                    ((var15 * var14 - var17 * var12) << 3 << 14), graphicsobj.Rasterizer3D_zoom))
            var34 = np.int32(
                integerdivide(((var17 * var9 - var11 * var15) << 14), graphicsobj.Rasterizer3D_zoom))
            var35 = var10 * var12 - var13 * var9 << 14
            var36 = np.int32(
                integerdivide(
                    ((var13 * var15 - var16 * var12)
                        << 3 << 14), graphicsobj.Rasterizer3D_zoom))
            var37 = np.int32(
                integerdivide(
                    ((var16 * var9 - var10 * var15) << 14), graphicsobj.Rasterizer3D_zoom))
            var38 = var13 * var11 - var10 * var14 << 14
            var39 = np.int32(
                integerdivide(
                    ((var16 * var14 - var13 * var17)
                        << 3 << 14), graphicsobj.Rasterizer3D_zoom))
            var40 = np.int32(
                integerdivide(
                    ((var17 * var10 - var11 * var16) << 14), graphicsobj.Rasterizer3D_zoom))
            if(var0 <= var1 and var0 <= var2):
                if(var0 < graphicsobj.Rasterizer3D_clipHeight):
                    if(var1 > graphicsobj.Rasterizer3D_clipHeight):
                        var1 = graphicsobj.Rasterizer3D_clipHeight

                    if(var2 > graphicsobj.Rasterizer3D_clipHeight):
                        var2 = graphicsobj.Rasterizer3D_clipHeight

                    var6 = var30 + ((var6 << 9) - var3 * var30)
                    if(var1 < var2):
                        var3 <<= 14
                        var5 = var3
                        if(var0 < 0):
                            var5 -= var0 * var28
                            var3 -= var0 * var26
                            var6 -= var0 * var31
                            var0 = 0

                        var4 <<= 14
                        if(var1 < 0):
                            var4 -= var27 * var1
                            var1 = 0

                        var41 = var0 - \
                            graphicsobj.centerY
                        var32 += var34 * var41
                        var35 += var37 * var41
                        var38 += var40 * var41
                        if((var0 == var1 or var28 >= var26) and (var0 != var1 or var28 <= var27)):
                            var2 -= var1
                            var1 -= var0
                            var0 = graphicsobj.rasterClipY[var0]

                            while(True):
                                var1 -= 1
                                if(var1 < 0):
                                    while(True):
                                        var2 -= 1
                                        if(var2 < 0):
                                            return

                                        method2844(objectID, graphicsobj.annotationCanvas, graphicsobj.graphicsPixels, var19, var0, var4 >> 14,
                                                   var5 >> 14, var6, var30, var32, var35, var38, var33, var36, var39,
                                                   graphicsobj.rasterClipEnable, graphicsobj.rasterClipX, graphicsobj.lowMem, graphicsobj.centerX, graphicsobj.field1944)
                                        var5 += var28
                                        var4 += var27
                                        var6 += var31
                                        var0 += graphicsobj.graphicsPixelsWidth
                                        var32 += var34
                                        var35 += var37
                                        var38 += var40

                                method2844(objectID, graphicsobj.annotationCanvas, graphicsobj.graphicsPixels, var19, var0, var3 >> 14,
                                           var5 >> 14, var6, var30, var32, var35, var38, var33, var36, var39,
                                           graphicsobj.rasterClipEnable, graphicsobj.rasterClipX, graphicsobj.lowMem, graphicsobj.centerX, graphicsobj.field1944)
                                var5 += var28
                                var3 += var26
                                var6 += var31
                                var0 += graphicsobj.graphicsPixelsWidth
                                var32 += var34
                                var35 += var37
                                var38 += var40

                        else:
                            var2 -= var1
                            var1 -= var0
                            var0 = graphicsobj.rasterClipY[var0]

                            while(True):
                                var1 -= 1
                                if(var1 < 0):
                                    while(True):
                                        var2 -= 1
                                        if(var2 < 0):
                                            return

                                        method2844(objectID, graphicsobj.annotationCanvas, graphicsobj.graphicsPixels, var19, var0, var5 >> 14,
                                                   var4 >> 14, var6, var30, var32, var35, var38, var33, var36, var39,
                                                   graphicsobj.rasterClipEnable, graphicsobj.rasterClipX, graphicsobj.lowMem, graphicsobj.centerX, graphicsobj.field1944)
                                        var5 += var28
                                        var4 += var27
                                        var6 += var31
                                        var0 += graphicsobj.graphicsPixelsWidth
                                        var32 += var34
                                        var35 += var37
                                        var38 += var40

                                method2844(objectID, graphicsobj.annotationCanvas, graphicsobj.graphicsPixels, var19, var0, var5 >> 14,
                                           var3 >> 14, var6, var30, var32, var35, var38, var33, var36, var39,
                                           graphicsobj.rasterClipEnable, graphicsobj.rasterClipX, graphicsobj.lowMem, graphicsobj.centerX, graphicsobj.field1944)
                                var5 += var28
                                var3 += var26
                                var6 += var31
                                var0 += graphicsobj.graphicsPixelsWidth
                                var32 += var34
                                var35 += var37
                                var38 += var40

                    else:
                        var3 <<= 14
                        var4 = var3
                        if(var0 < 0):
                            var4 -= var0 * var28
                            var3 -= var0 * var26
                            var6 -= var0 * var31
                            var0 = 0

                        var5 <<= 14
                        if(var2 < 0):
                            var5 -= var27 * var2
                            var2 = 0

                        var41 = var0 - \
                            graphicsobj.centerY
                        var32 += var34 * var41
                        var35 += var37 * var41
                        var38 += var40 * var41
                        if(var0 != var2 and var28 < var26 or var0 == var2 and var27 > var26):
                            var1 -= var2
                            var2 -= var0
                            var0 = graphicsobj.rasterClipY[var0]

                            while(True):
                                var2 -= 1
                                if(var2 < 0):
                                    while(True):
                                        var1 -= 1
                                        if(var1 < 0):
                                            return

                                        method2844(objectID, graphicsobj.annotationCanvas, graphicsobj.graphicsPixels, var19, var0, var5 >> 14,
                                                   var3 >> 14, var6, var30, var32, var35, var38, var33, var36, var39,
                                                   graphicsobj.rasterClipEnable, graphicsobj.rasterClipX, graphicsobj.lowMem, graphicsobj.centerX, graphicsobj.field1944)
                                        var5 += var27
                                        var3 += var26
                                        var6 += var31
                                        var0 += graphicsobj.graphicsPixelsWidth
                                        var32 += var34
                                        var35 += var37
                                        var38 += var40

                                method2844(objectID, graphicsobj.annotationCanvas, graphicsobj.graphicsPixels, var19, var0, var4 >> 14,
                                           var3 >> 14, var6, var30, var32, var35, var38, var33, var36, var39,
                                           graphicsobj.rasterClipEnable, graphicsobj.rasterClipX, graphicsobj.lowMem, graphicsobj.centerX, graphicsobj.field1944)
                                var4 += var28
                                var3 += var26
                                var6 += var31
                                var0 += graphicsobj.graphicsPixelsWidth
                                var32 += var34
                                var35 += var37
                                var38 += var40

                        else:
                            var1 -= var2
                            var2 -= var0
                            var0 = graphicsobj.rasterClipY[var0]

                            while(True):
                                var2 -= 1
                                if(var2 < 0):
                                    while(True):
                                        var1 -= 1
                                        if(var1 < 0):
                                            return

                                        method2844(objectID, graphicsobj.annotationCanvas, graphicsobj.graphicsPixels, var19, var0, var3 >> 14,
                                                   var5 >> 14, var6, var30, var32, var35, var38, var33, var36, var39,
                                                   graphicsobj.rasterClipEnable, graphicsobj.rasterClipX, graphicsobj.lowMem, graphicsobj.centerX, graphicsobj.field1944)
                                        var5 += var27
                                        var3 += var26
                                        var6 += var31
                                        var0 += graphicsobj.graphicsPixelsWidth
                                        var32 += var34
                                        var35 += var37
                                        var38 += var40

                                method2844(objectID, graphicsobj.annotationCanvas, graphicsobj.graphicsPixels, var19, var0, var3 >> 14,
                                           var4 >> 14, var6, var30, var32, var35, var38, var33, var36, var39,
                                           graphicsobj.rasterClipEnable, graphicsobj.rasterClipX, graphicsobj.lowMem, graphicsobj.centerX, graphicsobj.field1944)
                                var4 += var28
                                var3 += var26
                                var6 += var31
                                var0 += graphicsobj.graphicsPixelsWidth
                                var32 += var34
                                var35 += var37
                                var38 += var40

            elif(var1 <= var2):
                if(var1 < graphicsobj.Rasterizer3D_clipHeight):
                    if(var2 > graphicsobj.Rasterizer3D_clipHeight):
                        var2 = graphicsobj.Rasterizer3D_clipHeight

                    if(var0 > graphicsobj.Rasterizer3D_clipHeight):
                        var0 = graphicsobj.Rasterizer3D_clipHeight

                    var7 = var30 + ((var7 << 9) - var30 * var4)
                    if(var2 < var0):
                        var4 <<= 14
                        var3 = var4
                        if(var1 < 0):
                            var3 -= var26 * var1
                            var4 -= var27 * var1
                            var7 -= var31 * var1
                            var1 = 0

                        var5 <<= 14
                        if(var2 < 0):
                            var5 -= var28 * var2
                            var2 = 0

                        var41 = var1 - \
                            graphicsobj.centerY
                        var32 += var34 * var41
                        var35 += var37 * var41
                        var38 += var40 * var41
                        if((var2 == var1 or var26 >= var27) and (var2 != var1 or var26 <= var28)):
                            var0 -= var2
                            var2 -= var1
                            var1 = graphicsobj.rasterClipY[var1]

                            while(True):
                                var2 -= 1
                                if(var2 < 0):
                                    while(True):
                                        var0 -= 1
                                        if(var0 < 0):
                                            return

                                        method2844(objectID, graphicsobj.annotationCanvas, graphicsobj.graphicsPixels, var19, var1, var5 >> 14,
                                                   var3 >> 14, var7, var30, var32, var35, var38, var33, var36, var39,
                                                   graphicsobj.rasterClipEnable, graphicsobj.rasterClipX, graphicsobj.lowMem, graphicsobj.centerX, graphicsobj.field1944)
                                        var3 += var26
                                        var5 += var28
                                        var7 += var31
                                        var1 += graphicsobj.graphicsPixelsWidth
                                        var32 += var34
                                        var35 += var37
                                        var38 += var40

                                method2844(objectID, graphicsobj.annotationCanvas, graphicsobj.graphicsPixels, var19, var1, var4 >> 14,
                                           var3 >> 14, var7, var30, var32, var35, var38, var33, var36, var39,
                                           graphicsobj.rasterClipEnable, graphicsobj.rasterClipX, graphicsobj.lowMem, graphicsobj.centerX, graphicsobj.field1944)
                                var3 += var26
                                var4 += var27
                                var7 += var31
                                var1 += graphicsobj.graphicsPixelsWidth
                                var32 += var34
                                var35 += var37
                                var38 += var40

                        else:
                            var0 -= var2
                            var2 -= var1
                            var1 = graphicsobj.rasterClipY[var1]

                            while(True):
                                var2 -= 1
                                if(var2 < 0):
                                    while(True):
                                        var0 -= 1
                                        if(var0 < 0):
                                            return

                                        method2844(objectID, graphicsobj.annotationCanvas, graphicsobj.graphicsPixels, var19, var1, var3 >> 14,
                                                   var5 >> 14, var7, var30, var32, var35, var38, var33, var36, var39,
                                                   graphicsobj.rasterClipEnable, graphicsobj.rasterClipX, graphicsobj.lowMem, graphicsobj.centerX, graphicsobj.field1944)
                                        var3 += var26
                                        var5 += var28
                                        var7 += var31
                                        var1 += graphicsobj.graphicsPixelsWidth
                                        var32 += var34
                                        var35 += var37
                                        var38 += var40

                                method2844(objectID, graphicsobj.annotationCanvas, graphicsobj.graphicsPixels, var19, var1, var3 >> 14,
                                           var4 >> 14, var7, var30, var32, var35, var38, var33, var36, var39,
                                           graphicsobj.rasterClipEnable, graphicsobj.rasterClipX, graphicsobj.lowMem, graphicsobj.centerX, graphicsobj.field1944)
                                var3 += var26
                                var4 += var27
                                var7 += var31
                                var1 += graphicsobj.graphicsPixelsWidth
                                var32 += var34
                                var35 += var37
                                var38 += var40

                    else:
                        var4 <<= 14
                        var5 = var4
                        if(var1 < 0):
                            var5 -= var26 * var1
                            var4 -= var27 * var1
                            var7 -= var31 * var1
                            var1 = 0

                        var3 <<= 14
                        if(var0 < 0):
                            var3 -= var0 * var28
                            var0 = 0

                        var41 = var1 - \
                            graphicsobj.centerY
                        var32 += var34 * var41
                        var35 += var37 * var41
                        var38 += var40 * var41
                        if(var26 < var27):
                            var2 -= var0
                            var0 -= var1
                            var1 = graphicsobj.rasterClipY[var1]

                            while(True):
                                var0 -= 1
                                if(var0 < 0):
                                    while(True):
                                        var2 -= 1
                                        if(var2 < 0):
                                            return

                                        method2844(objectID, graphicsobj.annotationCanvas, graphicsobj.graphicsPixels, var19, var1, var3 >> 14,
                                                   var4 >> 14, var7, var30, var32, var35, var38, var33, var36, var39,
                                                   graphicsobj.rasterClipEnable, graphicsobj.rasterClipX, graphicsobj.lowMem, graphicsobj.centerX, graphicsobj.field1944)
                                        var3 += var28
                                        var4 += var27
                                        var7 += var31
                                        var1 += graphicsobj.graphicsPixelsWidth
                                        var32 += var34
                                        var35 += var37
                                        var38 += var40

                                method2844(objectID, graphicsobj.annotationCanvas, graphicsobj.graphicsPixels, var19, var1, var5 >> 14,
                                           var4 >> 14, var7, var30, var32, var35, var38, var33, var36, var39,
                                           graphicsobj.rasterClipEnable, graphicsobj.rasterClipX, graphicsobj.lowMem, graphicsobj.centerX, graphicsobj.field1944)
                                var5 += var26
                                var4 += var27
                                var7 += var31
                                var1 += graphicsobj.graphicsPixelsWidth
                                var32 += var34
                                var35 += var37
                                var38 += var40

                        else:
                            var2 -= var0
                            var0 -= var1
                            var1 = graphicsobj.rasterClipY[var1]

                            while(True):
                                var0 -= 1
                                if(var0 < 0):
                                    while(True):
                                        var2 -= 1
                                        if(var2 < 0):
                                            return

                                        method2844(objectID, graphicsobj.annotationCanvas, graphicsobj.graphicsPixels, var19, var1, var4 >> 14,
                                                   var3 >> 14, var7, var30, var32, var35, var38, var33, var36, var39,
                                                   graphicsobj.rasterClipEnable, graphicsobj.rasterClipX, graphicsobj.lowMem, graphicsobj.centerX, graphicsobj.field1944)
                                        var3 += var28
                                        var4 += var27
                                        var7 += var31
                                        var1 += graphicsobj.graphicsPixelsWidth
                                        var32 += var34
                                        var35 += var37
                                        var38 += var40

                                method2844(objectID, graphicsobj.annotationCanvas, graphicsobj.graphicsPixels, var19, var1, var4 >> 14,
                                           var5 >> 14, var7, var30, var32, var35, var38, var33, var36, var39,
                                           graphicsobj.rasterClipEnable, graphicsobj.rasterClipX, graphicsobj.lowMem, graphicsobj.centerX, graphicsobj.field1944)
                                var5 += var26
                                var4 += var27
                                var7 += var31
                                var1 += graphicsobj.graphicsPixelsWidth
                                var32 += var34
                                var35 += var37
                                var38 += var40

            elif(var2 < graphicsobj.Rasterizer3D_clipHeight):
                if(var0 > graphicsobj.Rasterizer3D_clipHeight):
                    var0 = graphicsobj.Rasterizer3D_clipHeight

                if(var1 > graphicsobj.Rasterizer3D_clipHeight):
                    var1 = graphicsobj.Rasterizer3D_clipHeight

                var8 = (var8 << 9) - var5 * var30 + var30
                if(var0 < var1):
                    var5 <<= 14
                    var4 = var5
                    if(var2 < 0):
                        var4 -= var27 * var2
                        var5 -= var28 * var2
                        var8 -= var31 * var2
                        var2 = 0

                    var3 <<= 14
                    if(var0 < 0):
                        var3 -= var0 * var26
                        var0 = 0

                    var41 = var2 - \
                        graphicsobj.centerY
                    var32 += var34 * var41
                    var35 += var37 * var41
                    var38 += var40 * var41
                    if(var27 < var28):
                        var1 -= var0
                        var0 -= var2
                        var2 = graphicsobj.rasterClipY[var2]

                        while(True):
                            var0 -= 1
                            if(var0 < 0):
                                while(True):
                                    var1 -= 1
                                    if(var1 < 0):
                                        return

                                    method2844(objectID, graphicsobj.annotationCanvas, graphicsobj.graphicsPixels, var19, var2, var4 >> 14,
                                               var3 >> 14, var8, var30, var32, var35, var38, var33, var36, var39,
                                               graphicsobj.rasterClipEnable, graphicsobj.rasterClipX, graphicsobj.lowMem, graphicsobj.centerX, graphicsobj.field1944)
                                    var4 += var27
                                    var3 += var26
                                    var8 += var31
                                    var2 += graphicsobj.graphicsPixelsWidth
                                    var32 += var34
                                    var35 += var37
                                    var38 += var40

                            method2844(objectID, graphicsobj.annotationCanvas, graphicsobj.graphicsPixels, var19, var2, var4 >> 14,
                                       var5 >> 14, var8, var30, var32, var35, var38, var33, var36, var39,
                                       graphicsobj.rasterClipEnable, graphicsobj.rasterClipX, graphicsobj.lowMem, graphicsobj.centerX, graphicsobj.field1944)
                            var4 += var27
                            var5 += var28
                            var8 += var31
                            var2 += graphicsobj.graphicsPixelsWidth
                            var32 += var34
                            var35 += var37
                            var38 += var40

                    else:
                        var1 -= var0
                        var0 -= var2
                        var2 = graphicsobj.rasterClipY[var2]

                        while(True):
                            var0 -= 1
                            if(var0 < 0):
                                while(True):
                                    var1 -= 1
                                    if(var1 < 0):
                                        return

                                    method2844(objectID, graphicsobj.annotationCanvas, graphicsobj.graphicsPixels, var19, var2, var3 >> 14,
                                               var4 >> 14, var8, var30, var32, var35, var38, var33, var36, var39,
                                               graphicsobj.rasterClipEnable, graphicsobj.rasterClipX, graphicsobj.lowMem, graphicsobj.centerX, graphicsobj.field1944)
                                    var4 += var27
                                    var3 += var26
                                    var8 += var31
                                    var2 += graphicsobj.graphicsPixelsWidth
                                    var32 += var34
                                    var35 += var37
                                    var38 += var40

                            method2844(objectID, graphicsobj.annotationCanvas, graphicsobj.graphicsPixels, var19, var2, var5 >> 14,
                                       var4 >> 14, var8, var30, var32, var35, var38, var33, var36, var39,
                                       graphicsobj.rasterClipEnable, graphicsobj.rasterClipX, graphicsobj.lowMem, graphicsobj.centerX, graphicsobj.field1944)
                            var4 += var27
                            var5 += var28
                            var8 += var31
                            var2 += graphicsobj.graphicsPixelsWidth
                            var32 += var34
                            var35 += var37
                            var38 += var40

                else:
                    var5 <<= 14
                    var3 = var5
                    if(var2 < 0):
                        var3 -= var27 * var2
                        var5 -= var28 * var2
                        var8 -= var31 * var2
                        var2 = 0

                    var4 <<= 14
                    if(var1 < 0):
                        var4 -= var26 * var1
                        var1 = 0

                    var41 = var2 - \
                        graphicsobj.centerY
                    var32 += var34 * var41
                    var35 += var37 * var41
                    var38 += var40 * var41
                    if(var27 < var28):
                        var0 -= var1
                        var1 -= var2
                        var2 = graphicsobj.rasterClipY[var2]

                        while(True):
                            var1 -= 1
                            if(var1 < 0):
                                while(True):
                                    var0 -= 1
                                    if(var0 < 0):
                                        return

                                    method2844(objectID, graphicsobj.annotationCanvas, graphicsobj.graphicsPixels, var19, var2, var4 >> 14,
                                               var5 >> 14, var8, var30, var32, var35, var38, var33, var36, var39,
                                               graphicsobj.rasterClipEnable, graphicsobj.rasterClipX, graphicsobj.lowMem, graphicsobj.centerX, graphicsobj.field1944)
                                    var4 += var26
                                    var5 += var28
                                    var8 += var31
                                    var2 += graphicsobj.graphicsPixelsWidth
                                    var32 += var34
                                    var35 += var37
                                    var38 += var40

                            method2844(objectID, graphicsobj.annotationCanvas, graphicsobj.graphicsPixels, var19, var2, var3 >> 14,
                                       var5 >> 14, var8, var30, var32, var35, var38, var33, var36, var39,
                                       graphicsobj.rasterClipEnable, graphicsobj.rasterClipX, graphicsobj.lowMem, graphicsobj.centerX, graphicsobj.field1944)
                            var3 += var27
                            var5 += var28
                            var8 += var31
                            var2 += graphicsobj.graphicsPixelsWidth
                            var32 += var34
                            var35 += var37
                            var38 += var40

                    else:
                        var0 -= var1
                        var1 -= var2
                        var2 = graphicsobj.rasterClipY[var2]

                        while(True):
                            var1 -= 1
                            if(var1 < 0):
                                while(True):
                                    var0 -= 1
                                    if(var0 < 0):
                                        return

                                    method2844(objectID, graphicsobj.annotationCanvas, graphicsobj.graphicsPixels, var19, var2, var5 >> 14,
                                               var4 >> 14, var8, var30, var32, var35, var38, var33, var36, var39,
                                               graphicsobj.rasterClipEnable, graphicsobj.rasterClipX, graphicsobj.lowMem, graphicsobj.centerX, graphicsobj.field1944)
                                    var4 += var26
                                    var5 += var28
                                    var8 += var31
                                    var2 += graphicsobj.graphicsPixelsWidth
                                    var32 += var34
                                    var35 += var37
                                    var38 += var40

                            method2844(objectID, graphicsobj.annotationCanvas, graphicsobj.graphicsPixels, var19, var2, var5 >> 14,
                                       var3 >> 14, var8, var30, var32, var35, var38, var33, var36, var39,
                                       graphicsobj.rasterClipEnable, graphicsobj.rasterClipX, graphicsobj.lowMem, graphicsobj.centerX, graphicsobj.field1944)
                            var3 += var27
                            var5 += var28
                            var8 += var31
                            var2 += graphicsobj.graphicsPixelsWidth
                            var32 += var34
                            var35 += var37
                            var38 += var40


@jit(nopython=True, cache=False)
def rasterFlat(graphicsobj, objectID, var0, var1, var2, var3, var4, var5, var6):
    var7 = 0
    if(var0 != var1):
        var7 = integerdivide((var4 - var3 << 14), (var1 - var0))

    var8 = 0
    if(var2 != var1):
        var8 = integerdivide((var5 - var4 << 14), (var2 - var1))

    var9 = 0
    if(var0 != var2):
        var9 = integerdivide((var3 - var5 << 14), (var0 - var2))

    if(var0 <= var1 and var0 <= var2):
        if(var0 < graphicsobj.Rasterizer3D_clipHeight):
            if(var1 > graphicsobj.Rasterizer3D_clipHeight):
                var1 = graphicsobj.Rasterizer3D_clipHeight

            if(var2 > graphicsobj.Rasterizer3D_clipHeight):
                var2 = graphicsobj.Rasterizer3D_clipHeight

            if(var1 < var2):
                var3 <<= 14
                var5 = var3
                if(var0 < 0):
                    var5 -= var0 * var9
                    var3 -= var0 * var7
                    var0 = 0

                var4 <<= 14
                if(var1 < 0):
                    var4 -= var8 * var1
                    var1 = 0

                if(var0 != var1 and var9 < var7 or var0 == var1 and var9 > var8):
                    var2 -= var1
                    var1 -= var0
                    var0 = graphicsobj.rasterClipY[var0]

                    while(True):
                        var1 -= 1
                        if(var1 < 0):
                            while(True):
                                var2 -= 1
                                if(var2 < 0):
                                    return

                                method2826(objectID, graphicsobj.annotationCanvas,
                                           graphicsobj.graphicsPixels, var0, var6, var5 >> 14, var4 >> 14,
                                           graphicsobj.rasterClipEnable, graphicsobj.rasterClipX, graphicsobj.rasterAlpha)
                                var5 += var9
                                var4 += var8
                                var0 += graphicsobj.graphicsPixelsWidth

                        method2826(objectID, graphicsobj.annotationCanvas,
                                   graphicsobj.graphicsPixels, var0, var6, var5 >> 14, var3 >> 14,
                                   graphicsobj.rasterClipEnable, graphicsobj.rasterClipX, graphicsobj.rasterAlpha)
                        var5 += var9
                        var3 += var7
                        var0 += graphicsobj.graphicsPixelsWidth

                else:
                    var2 -= var1
                    var1 -= var0
                    var0 = graphicsobj.rasterClipY[var0]

                    while(True):
                        var1 -= 1
                        if(var1 < 0):
                            while(True):
                                var2 -= 1
                                if(var2 < 0):
                                    return

                                method2826(objectID, graphicsobj.annotationCanvas,
                                           graphicsobj.graphicsPixels, var0, var6, var4 >> 14, var5 >> 14,
                                           graphicsobj.rasterClipEnable, graphicsobj.rasterClipX, graphicsobj.rasterAlpha)
                                var5 += var9
                                var4 += var8
                                var0 += graphicsobj.graphicsPixelsWidth

                        method2826(objectID, graphicsobj.annotationCanvas,
                                   graphicsobj.graphicsPixels, var0, var6, var3 >> 14, var5 >> 14,
                                   graphicsobj.rasterClipEnable, graphicsobj.rasterClipX, graphicsobj.rasterAlpha)
                        var5 += var9
                        var3 += var7
                        var0 += graphicsobj.graphicsPixelsWidth

            else:
                var3 <<= 14
                var4 = var3
                if(var0 < 0):
                    var4 -= var0 * var9
                    var3 -= var0 * var7
                    var0 = 0

                var5 <<= 14
                if(var2 < 0):
                    var5 -= var8 * var2
                    var2 = 0

                if(var0 != var2 and var9 < var7 or var0 == var2 and var8 > var7):
                    var1 -= var2
                    var2 -= var0
                    var0 = graphicsobj.rasterClipY[var0]

                    while(True):
                        var2 -= 1
                        if(var2 < 0):
                            while(True):
                                var1 -= 1
                                if(var1 < 0):
                                    return

                                method2826(objectID, graphicsobj.annotationCanvas,
                                           graphicsobj.graphicsPixels, var0, var6, var5 >> 14, var3 >> 14,
                                           graphicsobj.rasterClipEnable, graphicsobj.rasterClipX, graphicsobj.rasterAlpha)
                                var5 += var8
                                var3 += var7
                                var0 += graphicsobj.graphicsPixelsWidth

                        method2826(objectID, graphicsobj.annotationCanvas,
                                   graphicsobj.graphicsPixels, var0, var6, var4 >> 14, var3 >> 14,
                                   graphicsobj.rasterClipEnable, graphicsobj.rasterClipX, graphicsobj.rasterAlpha)
                        var4 += var9
                        var3 += var7
                        var0 += graphicsobj.graphicsPixelsWidth

                else:
                    var1 -= var2
                    var2 -= var0
                    var0 = graphicsobj.rasterClipY[var0]

                    while(True):
                        var2 -= 1
                        if(var2 < 0):
                            while(True):
                                var1 -= 1
                                if(var1 < 0):
                                    return

                                method2826(objectID, graphicsobj.annotationCanvas,
                                           graphicsobj.graphicsPixels, var0, var6, var3 >> 14, var5 >> 14,
                                           graphicsobj.rasterClipEnable, graphicsobj.rasterClipX, graphicsobj.rasterAlpha)
                                var5 += var8
                                var3 += var7
                                var0 += graphicsobj.graphicsPixelsWidth

                        method2826(objectID, graphicsobj.annotationCanvas,
                                   graphicsobj.graphicsPixels, var0, var6, var3 >> 14, var4 >> 14,
                                   graphicsobj.rasterClipEnable, graphicsobj.rasterClipX, graphicsobj.rasterAlpha)
                        var4 += var9
                        var3 += var7
                        var0 += graphicsobj.graphicsPixelsWidth

    elif(var1 <= var2):
        if(var1 < graphicsobj.Rasterizer3D_clipHeight):
            if(var2 > graphicsobj.Rasterizer3D_clipHeight):
                var2 = graphicsobj.Rasterizer3D_clipHeight

            if(var0 > graphicsobj.Rasterizer3D_clipHeight):
                var0 = graphicsobj.Rasterizer3D_clipHeight

            if(var2 < var0):
                var4 <<= 14
                var3 = var4
                if(var1 < 0):
                    var3 -= var7 * var1
                    var4 -= var8 * var1
                    var1 = 0

                var5 <<= 14
                if(var2 < 0):
                    var5 -= var9 * var2
                    var2 = 0

                if((var2 == var1 or var7 >= var8) and (var2 != var1 or var7 <= var9)):
                    var0 -= var2
                    var2 -= var1
                    var1 = graphicsobj.rasterClipY[var1]

                    while(True):
                        var2 -= 1
                        if(var2 < 0):
                            while(True):
                                var0 -= 1
                                if(var0 < 0):
                                    return

                                method2826(objectID, graphicsobj.annotationCanvas,
                                           graphicsobj.graphicsPixels, var1, var6, var5 >> 14, var3 >> 14,
                                           graphicsobj.rasterClipEnable, graphicsobj.rasterClipX, graphicsobj.rasterAlpha)
                                var3 += var7
                                var5 += var9
                                var1 += graphicsobj.graphicsPixelsWidth

                        method2826(objectID, graphicsobj.annotationCanvas,
                                   graphicsobj.graphicsPixels, var1, var6, var4 >> 14, var3 >> 14,
                                   graphicsobj.rasterClipEnable, graphicsobj.rasterClipX, graphicsobj.rasterAlpha)
                        var3 += var7
                        var4 += var8
                        var1 += graphicsobj.graphicsPixelsWidth

                else:
                    var0 -= var2
                    var2 -= var1
                    var1 = graphicsobj.rasterClipY[var1]

                    while(True):
                        var2 -= 1
                        if(var2 < 0):
                            while(True):
                                var0 -= 1
                                if(var0 < 0):
                                    return

                                method2826(objectID, graphicsobj.annotationCanvas,
                                           graphicsobj.graphicsPixels, var1, var6, var3 >> 14, var5 >> 14,
                                           graphicsobj.rasterClipEnable, graphicsobj.rasterClipX, graphicsobj.rasterAlpha)
                                var3 += var7
                                var5 += var9
                                var1 += graphicsobj.graphicsPixelsWidth

                        method2826(objectID, graphicsobj.annotationCanvas,
                                   graphicsobj.graphicsPixels, var1, var6, var3 >> 14, var4 >> 14,
                                   graphicsobj.rasterClipEnable, graphicsobj.rasterClipX, graphicsobj.rasterAlpha)
                        var3 += var7
                        var4 += var8
                        var1 += graphicsobj.graphicsPixelsWidth

            else:
                var4 <<= 14
                var5 = var4
                if(var1 < 0):
                    var5 -= var7 * var1
                    var4 -= var8 * var1
                    var1 = 0

                var3 <<= 14
                if(var0 < 0):
                    var3 -= var0 * var9
                    var0 = 0

                if(var7 < var8):
                    var2 -= var0
                    var0 -= var1
                    var1 = graphicsobj.rasterClipY[var1]

                    while(True):
                        var0 -= 1
                        if(var0 < 0):
                            while(True):
                                var2 -= 1
                                if(var2 < 0):
                                    return

                                method2826(objectID, graphicsobj.annotationCanvas,
                                           graphicsobj.graphicsPixels, var1, var6, var3 >> 14, var4 >> 14,
                                           graphicsobj.rasterClipEnable, graphicsobj.rasterClipX, graphicsobj.rasterAlpha)
                                var3 += var9
                                var4 += var8
                                var1 += graphicsobj.graphicsPixelsWidth

                        method2826(objectID, graphicsobj.annotationCanvas,
                                   graphicsobj.graphicsPixels, var1, var6, var5 >> 14, var4 >> 14,
                                   graphicsobj.rasterClipEnable, graphicsobj.rasterClipX, graphicsobj.rasterAlpha)
                        var5 += var7
                        var4 += var8
                        var1 += graphicsobj.graphicsPixelsWidth

                else:
                    var2 -= var0
                    var0 -= var1
                    var1 = graphicsobj.rasterClipY[var1]

                    while(True):
                        var0 -= 1
                        if(var0 < 0):
                            while(True):
                                var2 -= 1
                                if(var2 < 0):
                                    return

                                method2826(objectID, graphicsobj.annotationCanvas,
                                           graphicsobj.graphicsPixels, var1, var6, var4 >> 14, var3 >> 14,
                                           graphicsobj.rasterClipEnable, graphicsobj.rasterClipX, graphicsobj.rasterAlpha)
                                var3 += var9
                                var4 += var8
                                var1 += graphicsobj.graphicsPixelsWidth

                        method2826(objectID, graphicsobj.annotationCanvas,
                                   graphicsobj.graphicsPixels, var1, var6, var4 >> 14, var5 >> 14,
                                   graphicsobj.rasterClipEnable, graphicsobj.rasterClipX, graphicsobj.rasterAlpha)
                        var5 += var7
                        var4 += var8
                        var1 += graphicsobj.graphicsPixelsWidth

    elif(var2 < graphicsobj.Rasterizer3D_clipHeight):
        if(var0 > graphicsobj.Rasterizer3D_clipHeight):
            var0 = graphicsobj.Rasterizer3D_clipHeight

        if(var1 > graphicsobj.Rasterizer3D_clipHeight):
            var1 = graphicsobj.Rasterizer3D_clipHeight

        if(var0 < var1):
            var5 <<= 14
            var4 = var5
            if(var2 < 0):
                var4 -= var8 * var2
                var5 -= var9 * var2
                var2 = 0

            var3 <<= 14
            if(var0 < 0):
                var3 -= var0 * var7
                var0 = 0

            if(var8 < var9):
                var1 -= var0
                var0 -= var2
                var2 = graphicsobj.rasterClipY[var2]

                while(True):
                    var0 -= 1
                    if(var0 < 0):
                        while(True):
                            var1 -= 1
                            if(var1 < 0):
                                return

                            method2826(objectID, graphicsobj.annotationCanvas,
                                       graphicsobj.graphicsPixels, var2, var6, var4 >> 14, var3 >> 14,
                                       graphicsobj.rasterClipEnable, graphicsobj.rasterClipX, graphicsobj.rasterAlpha)
                            var4 += var8
                            var3 += var7
                            var2 += graphicsobj.graphicsPixelsWidth

                    method2826(objectID, graphicsobj.annotationCanvas,
                               graphicsobj.graphicsPixels, var2, var6, var4 >> 14, var5 >> 14,
                               graphicsobj.rasterClipEnable, graphicsobj.rasterClipX, graphicsobj.rasterAlpha)
                    var4 += var8
                    var5 += var9
                    var2 += graphicsobj.graphicsPixelsWidth

            else:
                var1 -= var0
                var0 -= var2
                var2 = graphicsobj.rasterClipY[var2]

                while(True):
                    var0 -= 1
                    if(var0 < 0):
                        while(True):
                            var1 -= 1
                            if(var1 < 0):
                                return

                            method2826(objectID, graphicsobj.annotationCanvas,
                                       graphicsobj.graphicsPixels, var2, var6, var3 >> 14, var4 >> 14,
                                       graphicsobj.rasterClipEnable, graphicsobj.rasterClipX, graphicsobj.rasterAlpha)
                            var4 += var8
                            var3 += var7
                            var2 += graphicsobj.graphicsPixelsWidth

                    method2826(objectID, graphicsobj.annotationCanvas,
                               graphicsobj.graphicsPixels, var2, var6, var5 >> 14, var4 >> 14,
                               graphicsobj.rasterClipEnable, graphicsobj.rasterClipX, graphicsobj.rasterAlpha)
                    var4 += var8
                    var5 += var9
                    var2 += graphicsobj.graphicsPixelsWidth

        else:
            var5 <<= 14
            var3 = var5
            if(var2 < 0):
                var3 -= var8 * var2
                var5 -= var9 * var2
                var2 = 0

            var4 <<= 14
            if(var1 < 0):
                var4 -= var7 * var1
                var1 = 0

            if(var8 < var9):
                var0 -= var1
                var1 -= var2
                var2 = graphicsobj.rasterClipY[var2]

                while(True):
                    var1 -= 1
                    if(var1 < 0):
                        while(True):
                            var0 -= 1
                            if(var0 < 0):
                                return

                            method2826(objectID, graphicsobj.annotationCanvas,
                                       graphicsobj.graphicsPixels, var2, var6, var4 >> 14, var5 >> 14,
                                       graphicsobj.rasterClipEnable, graphicsobj.rasterClipX, graphicsobj.rasterAlpha)
                            var4 += var7
                            var5 += var9
                            var2 += graphicsobj.graphicsPixelsWidth

                    method2826(objectID, graphicsobj.annotationCanvas,
                               graphicsobj.graphicsPixels, var2, var6, var3 >> 14, var5 >> 14,
                               graphicsobj.rasterClipEnable, graphicsobj.rasterClipX, graphicsobj.rasterAlpha)
                    var3 += var8
                    var5 += var9
                    var2 += graphicsobj.graphicsPixelsWidth

            else:
                var0 -= var1
                var1 -= var2
                var2 = graphicsobj.rasterClipY[var2]

                while(True):
                    var1 -= 1
                    if(var1 < 0):
                        while(True):
                            var0 -= 1
                            if(var0 < 0):
                                return

                            method2826(objectID, graphicsobj.annotationCanvas,
                                       graphicsobj.graphicsPixels, var2, var6, var5 >> 14, var4 >> 14,
                                       graphicsobj.rasterClipEnable, graphicsobj.rasterClipX, graphicsobj.rasterAlpha)
                            var4 += var7
                            var5 += var9
                            var2 += graphicsobj.graphicsPixelsWidth

                    method2826(objectID, graphicsobj.annotationCanvas,
                               graphicsobj.graphicsPixels, var2, var6, var5 >> 14, var3 >> 14,
                               graphicsobj.rasterClipEnable, graphicsobj.rasterClipX, graphicsobj.rasterAlpha)
                    var3 += var8
                    var5 += var9
                    var2 += graphicsobj.graphicsPixelsWidth


@jit(nopython=True, cache=False)
def rasterGouraud(colorPalette, graphicsobj, objectID, var0, var1, var2, var3, var4, var5, var6, var7, var8):

    var9 = var4 - var3
    var10 = var1 - var0
    var11 = var5 - var3
    var12 = var2 - var0
    var13 = var7 - var6
    var14 = var8 - var6

    if(var2 != var1):
        var15 = integerdivide((var5 - var4 << 14), (var2 - var1))
    else:
        var15 = 0

    if(var0 != var1):
        var16 = integerdivide((var9 << 14), var10)
    else:
        var16 = 0

    if(var0 != var2):
        var17 = integerdivide((var11 << 14), var12)
    else:
        var17 = 0

    var18 = var9 * var12 - var11 * var10

    if(var18 != 0):

        var19 = integerdivide((var13 * var12 - var14 * var10 << 8), var18)
        var20 = integerdivide((var14 * var9 - var13 * var11 << 8), var18)
        if(var0 <= var1 and var0 <= var2):

            if(var0 < graphicsobj.Rasterizer3D_clipHeight):
                if(var1 > graphicsobj.Rasterizer3D_clipHeight):
                    var1 = graphicsobj.Rasterizer3D_clipHeight

                if(var2 > graphicsobj.Rasterizer3D_clipHeight):
                    var2 = graphicsobj.Rasterizer3D_clipHeight

                var6 = var19 + ((var6 << 8) - var3 * var19)
                if(var1 < var2):
                    var3 <<= 14
                    var5 = var3
                    if(var0 < 0):
                        var5 -= var0 * var17
                        var3 -= var0 * var16
                        var6 -= var0 * var20
                        var0 = 0

                    var4 <<= 14
                    if(var1 < 0):
                        var4 -= var15 * var1
                        var1 = 0

                    if(var0 != var1 and var17 < var16 or var0 == var1 and var17 > var15):
                        var2 -= var1
                        var1 -= var0
                        var0 = graphicsobj.rasterClipY[var0]

                        while(True):
                            var1 -= 1
                            if(var1 < 0):
                                while(True):
                                    var2 -= 1
                                    if(var2 < 0):
                                        return

                                    method2790(objectID, graphicsobj.annotationCanvas,
                                               graphicsobj.graphicsPixels, var0, var5 >> 14, var4 >> 14, var6, var19,
                                               graphicsobj.rasterClipEnable, graphicsobj.rasterClipX, graphicsobj.rasterGouraudLowRes, graphicsobj.rasterAlpha, colorPalette)
                                    var5 += var17
                                    var4 += var15
                                    var6 += var20
                                    var0 += graphicsobj.graphicsPixelsWidth

                            method2790(objectID, graphicsobj.annotationCanvas,
                                       graphicsobj.graphicsPixels, var0, var5 >> 14, var3 >> 14, var6, var19,
                                       graphicsobj.rasterClipEnable, graphicsobj.rasterClipX, graphicsobj.rasterGouraudLowRes, graphicsobj.rasterAlpha, colorPalette)
                            var5 += var17
                            var3 += var16
                            var6 += var20
                            var0 += graphicsobj.graphicsPixelsWidth

                    else:
                        var2 -= var1
                        var1 -= var0
                        var0 = graphicsobj.rasterClipY[var0]

                        while(True):
                            var1 -= 1
                            if(var1 < 0):
                                while(True):
                                    var2 -= 1
                                    if(var2 < 0):
                                        return

                                    method2790(objectID, graphicsobj.annotationCanvas,
                                               graphicsobj.graphicsPixels, var0, var4 >> 14, var5 >> 14, var6, var19,
                                               graphicsobj.rasterClipEnable, graphicsobj.rasterClipX, graphicsobj.rasterGouraudLowRes, graphicsobj.rasterAlpha, colorPalette)
                                    var5 += var17
                                    var4 += var15
                                    var6 += var20
                                    var0 += graphicsobj.graphicsPixelsWidth

                            method2790(objectID, graphicsobj.annotationCanvas,
                                       graphicsobj.graphicsPixels, var0, var3 >> 14, var5 >> 14, var6, var19,
                                       graphicsobj.rasterClipEnable, graphicsobj.rasterClipX, graphicsobj.rasterGouraudLowRes, graphicsobj.rasterAlpha, colorPalette)
                            var5 += var17
                            var3 += var16
                            var6 += var20
                            var0 += graphicsobj.graphicsPixelsWidth

                else:
                    var3 <<= 14
                    var4 = var3
                    if(var0 < 0):
                        var4 -= var0 * var17
                        var3 -= var0 * var16
                        var6 -= var0 * var20
                        var0 = 0

                    var5 <<= 14
                    if(var2 < 0):
                        var5 -= var15 * var2
                        var2 = 0

                    if((var0 == var2 or var17 >= var16) and (var0 != var2 or var15 <= var16)):
                        var1 -= var2
                        var2 -= var0
                        var0 = graphicsobj.rasterClipY[var0]

                        while(True):
                            var2 -= 1
                            if(var2 < 0):
                                while(True):
                                    var1 -= 1
                                    if(var1 < 0):
                                        return

                                    method2790(objectID, graphicsobj.annotationCanvas,
                                               graphicsobj.graphicsPixels, var0, var3 >> 14, var5 >> 14, var6, var19,
                                               graphicsobj.rasterClipEnable, graphicsobj.rasterClipX, graphicsobj.rasterGouraudLowRes, graphicsobj.rasterAlpha, colorPalette)
                                    var5 += var15
                                    var3 += var16
                                    var6 += var20
                                    var0 += graphicsobj.graphicsPixelsWidth

                            method2790(objectID, graphicsobj.annotationCanvas,
                                       graphicsobj.graphicsPixels, var0, var3 >> 14, var4 >> 14, var6, var19,
                                       graphicsobj.rasterClipEnable, graphicsobj.rasterClipX, graphicsobj.rasterGouraudLowRes, graphicsobj.rasterAlpha, colorPalette)
                            var4 += var17
                            var3 += var16
                            var6 += var20
                            var0 += graphicsobj.graphicsPixelsWidth

                    else:
                        var1 -= var2
                        var2 -= var0
                        var0 = graphicsobj.rasterClipY[var0]

                        while(True):
                            var2 -= 1
                            if(var2 < 0):
                                while(True):
                                    var1 -= 1
                                    if(var1 < 0):
                                        return

                                    method2790(objectID, graphicsobj.annotationCanvas,
                                               graphicsobj.graphicsPixels, var0, var5 >> 14, var3 >> 14, var6, var19,
                                               graphicsobj.rasterClipEnable, graphicsobj.rasterClipX, graphicsobj.rasterGouraudLowRes, graphicsobj.rasterAlpha, colorPalette)
                                    var5 += var15
                                    var3 += var16
                                    var6 += var20
                                    var0 += graphicsobj.graphicsPixelsWidth

                            method2790(objectID, graphicsobj.annotationCanvas,
                                       graphicsobj.graphicsPixels, var0, var4 >> 14, var3 >> 14, var6, var19,
                                       graphicsobj.rasterClipEnable, graphicsobj.rasterClipX, graphicsobj.rasterGouraudLowRes, graphicsobj.rasterAlpha, colorPalette)
                            var4 += var17
                            var3 += var16
                            var6 += var20
                            var0 += graphicsobj.graphicsPixelsWidth

        elif(var1 <= var2):

            if(var1 < graphicsobj.Rasterizer3D_clipHeight):
                if(var2 > graphicsobj.Rasterizer3D_clipHeight):
                    var2 = graphicsobj.Rasterizer3D_clipHeight

                if(var0 > graphicsobj.Rasterizer3D_clipHeight):
                    var0 = graphicsobj.Rasterizer3D_clipHeight

                var7 = var19 + ((var7 << 8) - var19 * var4)
                if(var2 < var0):
                    var4 <<= 14
                    var3 = var4

                    if(var1 < 0):
                        var3 -= var16 * var1
                        var4 -= var15 * var1
                        var7 -= var20 * var1
                        var1 = 0

                    var5 <<= 14
                    if(var2 < 0):
                        var5 -= var17 * var2
                        var2 = 0

                    if(var2 != var1 and var16 < var15 or var2 == var1 and var16 > var17):
                        var0 -= var2
                        var2 -= var1
                        var1 = graphicsobj.rasterClipY[var1]

                        while(True):
                            var2 -= 1
                            if(var2 < 0):
                                while(True):
                                    var0 -= 1
                                    if(var0 < 0):
                                        return

                                    method2790(objectID, graphicsobj.annotationCanvas,
                                               graphicsobj.graphicsPixels, var1, var3 >> 14, var5 >> 14, var7, var19,
                                               graphicsobj.rasterClipEnable, graphicsobj.rasterClipX, graphicsobj.rasterGouraudLowRes, graphicsobj.rasterAlpha, colorPalette)
                                    var3 += var16
                                    var5 += var17
                                    var7 += var20
                                    var1 += graphicsobj.graphicsPixelsWidth

                            method2790(objectID, graphicsobj.annotationCanvas,
                                       graphicsobj.graphicsPixels, var1, var3 >> 14, var4 >> 14, var7, var19,
                                       graphicsobj.rasterClipEnable, graphicsobj.rasterClipX, graphicsobj.rasterGouraudLowRes, graphicsobj.rasterAlpha, colorPalette)
                            var3 += var16
                            var4 += var15
                            var7 += var20
                            var1 += graphicsobj.graphicsPixelsWidth

                    else:
                        var0 -= var2
                        var2 -= var1
                        var1 = graphicsobj.rasterClipY[var1]

                        while(True):
                            var2 -= 1
                            if(var2 < 0):
                                while(True):
                                    var0 -= 1
                                    if(var0 < 0):
                                        return

                                    method2790(objectID, graphicsobj.annotationCanvas,
                                               graphicsobj.graphicsPixels, var1, var5 >> 14, var3 >> 14, var7, var19,
                                               graphicsobj.rasterClipEnable, graphicsobj.rasterClipX, graphicsobj.rasterGouraudLowRes, graphicsobj.rasterAlpha, colorPalette)
                                    var3 += var16
                                    var5 += var17
                                    var7 += var20
                                    var1 += graphicsobj.graphicsPixelsWidth

                            method2790(objectID, graphicsobj.annotationCanvas,
                                       graphicsobj.graphicsPixels, var1, var4 >> 14, var3 >> 14, var7, var19,
                                       graphicsobj.rasterClipEnable, graphicsobj.rasterClipX, graphicsobj.rasterGouraudLowRes, graphicsobj.rasterAlpha, colorPalette)
                            var3 += var16
                            var4 += var15
                            var7 += var20
                            var1 += graphicsobj.graphicsPixelsWidth

                else:

                    var4 <<= 14
                    var5 = var4
                    if(var1 < 0):
                        var5 -= var16 * var1
                        var4 -= var15 * var1
                        var7 -= var20 * var1
                        var1 = 0

                    var3 <<= 14
                    if(var0 < 0):
                        var3 -= var0 * var17
                        var0 = 0

                    if(var16 < var15):
                        var2 -= var0
                        var0 -= var1
                        var1 = graphicsobj.rasterClipY[var1]

                        while(True):
                            var0 -= 1
                            if(var0 < 0):
                                while(True):
                                    var2 -= 1
                                    if(var2 < 0):
                                        return

                                    method2790(objectID, graphicsobj.annotationCanvas,
                                               graphicsobj.graphicsPixels, var1, var3 >> 14, var4 >> 14, var7, var19,
                                               graphicsobj.rasterClipEnable, graphicsobj.rasterClipX, graphicsobj.rasterGouraudLowRes, graphicsobj.rasterAlpha, colorPalette)
                                    var3 += var17
                                    var4 += var15
                                    var7 += var20
                                    var1 += graphicsobj.graphicsPixelsWidth

                            method2790(objectID, graphicsobj.annotationCanvas,
                                       graphicsobj.graphicsPixels, var1, var5 >> 14, var4 >> 14, var7, var19,
                                       graphicsobj.rasterClipEnable, graphicsobj.rasterClipX, graphicsobj.rasterGouraudLowRes, graphicsobj.rasterAlpha, colorPalette)
                            var5 += var16
                            var4 += var15
                            var7 += var20
                            var1 += graphicsobj.graphicsPixelsWidth

                    else:

                        var2 -= var0
                        var0 -= var1
                        var1 = graphicsobj.rasterClipY[var1]

                        while(True):
                            var0 -= 1
                            if(var0 < 0):
                                while(True):
                                    var2 -= 1
                                    if(var2 < 0):
                                        return

                                    method2790(objectID, graphicsobj.annotationCanvas,
                                               graphicsobj.graphicsPixels, var1, var4 >> 14, var3 >> 14, var7, var19,
                                               graphicsobj.rasterClipEnable, graphicsobj.rasterClipX, graphicsobj.rasterGouraudLowRes, graphicsobj.rasterAlpha, colorPalette)
                                    var3 += var17
                                    var4 += var15
                                    var7 += var20
                                    var1 += graphicsobj.graphicsPixelsWidth

                            method2790(objectID, graphicsobj.annotationCanvas,
                                       graphicsobj.graphicsPixels, var1, var4 >> 14, var5 >> 14, var7, var19,
                                       graphicsobj.rasterClipEnable, graphicsobj.rasterClipX, graphicsobj.rasterGouraudLowRes, graphicsobj.rasterAlpha, colorPalette)
                            var5 += var16
                            var4 += var15
                            var7 += var20
                            var1 += graphicsobj.graphicsPixelsWidth

        elif(var2 < graphicsobj.Rasterizer3D_clipHeight):
            if(var0 > graphicsobj.Rasterizer3D_clipHeight):
                var0 = graphicsobj.Rasterizer3D_clipHeight

            if(var1 > graphicsobj.Rasterizer3D_clipHeight):
                var1 = graphicsobj.Rasterizer3D_clipHeight

            var8 = var19 + ((var8 << 8) - var5 * var19)
            if(var0 < var1):
                var5 <<= 14
                var4 = var5
                if(var2 < 0):
                    var4 -= var15 * var2
                    var5 -= var17 * var2
                    var8 -= var20 * var2
                    var2 = 0

                var3 <<= 14
                if(var0 < 0):
                    var3 -= var0 * var16
                    var0 = 0

                if(var15 < var17):
                    var1 -= var0
                    var0 -= var2
                    var2 = graphicsobj.rasterClipY[var2]

                    while(True):
                        var0 -= 1
                        if(var0 < 0):
                            while(True):
                                var1 -= 1
                                if(var1 < 0):
                                    return

                                method2790(objectID, graphicsobj.annotationCanvas,
                                           graphicsobj.graphicsPixels, var2, var4 >> 14, var3 >> 14, var8, var19,
                                           graphicsobj.rasterClipEnable, graphicsobj.rasterClipX, graphicsobj.rasterGouraudLowRes, graphicsobj.rasterAlpha, colorPalette)
                                var4 += var15
                                var3 += var16
                                var8 += var20
                                var2 += graphicsobj.graphicsPixelsWidth

                        method2790(objectID, graphicsobj.annotationCanvas,
                                   graphicsobj.graphicsPixels, var2, var4 >> 14, var5 >> 14, var8, var19,
                                   graphicsobj.rasterClipEnable, graphicsobj.rasterClipX, graphicsobj.rasterGouraudLowRes, graphicsobj.rasterAlpha, colorPalette)
                        var4 += var15
                        var5 += var17
                        var8 += var20
                        var2 += graphicsobj.graphicsPixelsWidth

                else:
                    var1 -= var0
                    var0 -= var2
                    var2 = graphicsobj.rasterClipY[var2]

                    while(True):
                        var0 -= 1
                        if(var0 < 0):
                            while(True):
                                var1 -= 1
                                if(var1 < 0):
                                    return

                                method2790(objectID, graphicsobj.annotationCanvas,
                                           graphicsobj.graphicsPixels, var2, var3 >> 14, var4 >> 14, var8, var19,
                                           graphicsobj.rasterClipEnable, graphicsobj.rasterClipX, graphicsobj.rasterGouraudLowRes, graphicsobj.rasterAlpha, colorPalette)
                                var4 += var15
                                var3 += var16
                                var8 += var20
                                var2 += graphicsobj.graphicsPixelsWidth

                        method2790(objectID, graphicsobj.annotationCanvas,
                                   graphicsobj.graphicsPixels, var2, var5 >> 14, var4 >> 14, var8, var19,
                                   graphicsobj.rasterClipEnable, graphicsobj.rasterClipX, graphicsobj.rasterGouraudLowRes, graphicsobj.rasterAlpha, colorPalette)
                        var4 += var15
                        var5 += var17
                        var8 += var20
                        var2 += graphicsobj.graphicsPixelsWidth

            else:
                var5 <<= 14
                var3 = var5
                if(var2 < 0):
                    var3 -= var15 * var2
                    var5 -= var17 * var2
                    var8 -= var20 * var2
                    var2 = 0

                var4 <<= 14
                if(var1 < 0):
                    var4 -= var16 * var1
                    var1 = 0

                if(var15 < var17):
                    var0 -= var1
                    var1 -= var2
                    var2 = graphicsobj.rasterClipY[var2]

                    while(True):
                        var1 -= 1
                        if(var1 < 0):
                            while(True):
                                var0 -= 1
                                if(var0 < 0):
                                    return

                                method2790(objectID, graphicsobj.annotationCanvas,
                                           graphicsobj.graphicsPixels, var2, var4 >> 14, var5 >> 14, var8, var19,
                                           graphicsobj.rasterClipEnable, graphicsobj.rasterClipX, graphicsobj.rasterGouraudLowRes, graphicsobj.rasterAlpha, colorPalette)
                                var4 += var16
                                var5 += var17
                                var8 += var20
                                var2 += graphicsobj.graphicsPixelsWidth

                        method2790(objectID, graphicsobj.annotationCanvas,
                                   graphicsobj.graphicsPixels, var2, var3 >> 14, var5 >> 14, var8, var19,
                                   graphicsobj.rasterClipEnable, graphicsobj.rasterClipX, graphicsobj.rasterGouraudLowRes, graphicsobj.rasterAlpha, colorPalette)
                        var3 += var15
                        var5 += var17
                        var8 += var20
                        var2 += graphicsobj.graphicsPixelsWidth

                else:
                    var0 -= var1
                    var1 -= var2
                    var2 = graphicsobj.rasterClipY[var2]

                    while(True):
                        var1 -= 1
                        if(var1 < 0):
                            while(True):
                                var0 -= 1
                                if(var0 < 0):
                                    return

                                method2790(objectID, graphicsobj.annotationCanvas,
                                           graphicsobj.graphicsPixels, var2, var5 >> 14, var4 >> 14, var8, var19,
                                           graphicsobj.rasterClipEnable, graphicsobj.rasterClipX, graphicsobj.rasterGouraudLowRes, graphicsobj.rasterAlpha, colorPalette)
                                var4 += var16
                                var5 += var17
                                var8 += var20
                                var2 += graphicsobj.graphicsPixelsWidth

                        method2790(objectID, graphicsobj.annotationCanvas,
                                   graphicsobj.graphicsPixels, var2, var5 >> 14, var3 >> 14, var8, var19,
                                   graphicsobj.rasterClipEnable, graphicsobj.rasterClipX, graphicsobj.rasterGouraudLowRes, graphicsobj.rasterAlpha, colorPalette)
                        var3 += var15
                        var5 += var17
                        var8 += var20
                        var2 += graphicsobj.graphicsPixelsWidth


@jit(nopython=True, cache=False)
def rasterTexture(colorPalette, graphicsobj, objectID, var0, var1, var2, var3, var4, var5, var6, var7, var8,  var9, var10, var11,  var12, var13, var14,  var15, var16, var17, var18, textures):
    # graphicsobj.textureLoader.load(var18)
    var19 = TextureLoaderLoad(textures, var18)

    if(var19 is None):
        # graphicsobj.textureLoader.getAverageTextureRGB(var18)
        var20 = TextureLoaderGetAverageTextureRGB(textures, var18)
        rasterGouraud(colorPalette, graphicsobj, objectID, var0, var1, var2, var3, var4, var5, method2797(
            var20, var6), method2797(var20, var7), method2797(var20, var8))
    else:
        # graphicsobj.textureLoader.isLowMem(var18)
        graphicsobj.lowMem = TextureLoaderIsLowMem(textures, var18)
        # graphicsobj.textureLoader.vmethod3069(var18)
        graphicsobj.field1944 = TextureLoaderVmethod3069(textures, var18)
        var20 = var4 - var3
        var21 = var1 - var0
        var22 = var5 - var3
        var23 = var2 - var0
        var24 = var7 - var6
        var25 = var8 - var6
        var26 = 0
        if(var0 != var1):
            var26 = integerdivide((var4 - var3 << 14), (var1 - var0))

        var27 = 0
        if(var2 != var1):
            var27 = integerdivide((var5 - var4 << 14), (var2 - var1))

        var28 = 0
        if(var0 != var2):
            var28 = integerdivide((var3 - var5 << 14), (var0 - var2))

        var29 = var20 * var23 - var22 * var21
        if(var29 != 0):
            var30 = integerdivide(
                (var24 * var23 - var25 * var21 << 9), var29)
            var31 = integerdivide(
                (var25 * var20 - var24 * var22 << 9), var29)
            var10 = var9 - var10
            var13 = var12 - var13
            var16 = var15 - var16
            var11 -= var9
            var14 -= var12
            var17 -= var15
            var32 = var11 * var12 - var9 * var14 << 14
            var33 = np.int32(
                integerdivide(
                    ((var15 * var14 - var17 * var12) << 14), graphicsobj.Rasterizer3D_zoom))
            var34 = np.int32(
                integerdivide(((var17 * var9 - var11 * var15) << 14), graphicsobj.Rasterizer3D_zoom))
            var35 = var10 * var12 - var13 * var9 << 14
            var36 = np.int32(
                integerdivide(
                    ((var13 * var15 - var16 * var12) << 14), graphicsobj.Rasterizer3D_zoom))
            var37 = np.int32(
                integerdivide(
                    ((var16 * var9 - var10 * var15) << 14), graphicsobj.Rasterizer3D_zoom))
            var38 = var13 * var11 - var10 * var14 << 14
            var39 = np.int32(
                integerdivide(
                    ((var16 * var14 - var13 * var17) << 14), graphicsobj.Rasterizer3D_zoom))
            var40 = np.int32(
                integerdivide(
                    ((var17 * var10 - var11 * var16) << 14), graphicsobj.Rasterizer3D_zoom))
            if(var0 <= var1 and var0 <= var2):
                if(var0 < graphicsobj.Rasterizer3D_clipHeight):
                    if(var1 > graphicsobj.Rasterizer3D_clipHeight):
                        var1 = graphicsobj.Rasterizer3D_clipHeight

                    if(var2 > graphicsobj.Rasterizer3D_clipHeight):
                        var2 = graphicsobj.Rasterizer3D_clipHeight

                    var6 = var30 + ((var6 << 9) - var3 * var30)
                    if(var1 < var2):
                        var3 <<= 14
                        var5 = var3
                        if(var0 < 0):
                            var5 -= var0 * var28
                            var3 -= var0 * var26
                            var6 -= var0 * var31
                            var0 = 0

                        var4 <<= 14
                        if(var1 < 0):
                            var4 -= var27 * var1
                            var1 = 0

                        var41 = var0 - \
                            graphicsobj.centerY
                        var32 += var34 * var41
                        var35 += var37 * var41
                        var38 += var40 * var41
                        if((var0 == var1 or var28 >= var26) and (var0 != var1 or var28 <= var27)):
                            var2 -= var1
                            var1 -= var0
                            var0 = graphicsobj.rasterClipY[var0]

                            while(True):
                                var1 -= 1
                                if(var1 < 0):
                                    while(True):
                                        var2 -= 1
                                        if(var2 < 0):
                                            return

                                        method2796(objectID, graphicsobj.annotationCanvas, graphicsobj.graphicsPixels, var19, var0, var4 >> 14,
                                                   var5 >> 14, var6, var30, var32, var35, var38, var33, var36, var39, graphicsobj.rasterClipEnable, graphicsobj.rasterClipX, graphicsobj.lowMem, graphicsobj.centerX, graphicsobj.field1944)
                                        var5 += var28
                                        var4 += var27
                                        var6 += var31
                                        var0 += graphicsobj.graphicsPixelsWidth
                                        var32 += var34
                                        var35 += var37
                                        var38 += var40

                                method2796(objectID, graphicsobj.annotationCanvas, graphicsobj.graphicsPixels, var19, var0, var3 >> 14,
                                           var5 >> 14, var6, var30, var32, var35, var38, var33, var36, var39, graphicsobj.rasterClipEnable, graphicsobj.rasterClipX, graphicsobj.lowMem, graphicsobj.centerX, graphicsobj.field1944)
                                var5 += var28
                                var3 += var26
                                var6 += var31
                                var0 += graphicsobj.graphicsPixelsWidth
                                var32 += var34
                                var35 += var37
                                var38 += var40

                        else:
                            var2 -= var1
                            var1 -= var0
                            var0 = graphicsobj.rasterClipY[var0]

                            while(True):
                                var1 -= 1
                                if(var1 < 0):
                                    while(True):
                                        var2 -= 1
                                        if(var2 < 0):
                                            return

                                        method2796(objectID, graphicsobj.annotationCanvas, graphicsobj.graphicsPixels, var19, var0, var5 >> 14,
                                                   var4 >> 14, var6, var30, var32, var35, var38, var33, var36, var39, graphicsobj.rasterClipEnable, graphicsobj.rasterClipX, graphicsobj.lowMem, graphicsobj.centerX, graphicsobj.field1944)
                                        var5 += var28
                                        var4 += var27
                                        var6 += var31
                                        var0 += graphicsobj.graphicsPixelsWidth
                                        var32 += var34
                                        var35 += var37
                                        var38 += var40

                                method2796(objectID, graphicsobj.annotationCanvas, graphicsobj.graphicsPixels, var19, var0, var5 >> 14,
                                           var3 >> 14, var6, var30, var32, var35, var38, var33, var36, var39, graphicsobj.rasterClipEnable, graphicsobj.rasterClipX, graphicsobj.lowMem, graphicsobj.centerX, graphicsobj.field1944)
                                var5 += var28
                                var3 += var26
                                var6 += var31
                                var0 += graphicsobj.graphicsPixelsWidth
                                var32 += var34
                                var35 += var37
                                var38 += var40

                    else:
                        var3 <<= 14
                        var4 = var3
                        if(var0 < 0):
                            var4 -= var0 * var28
                            var3 -= var0 * var26
                            var6 -= var0 * var31
                            var0 = 0

                        var5 <<= 14
                        if(var2 < 0):
                            var5 -= var27 * var2
                            var2 = 0

                        var41 = var0 - \
                            graphicsobj.centerY
                        var32 += var34 * var41
                        var35 += var37 * var41
                        var38 += var40 * var41
                        if(var0 != var2 and var28 < var26 or var0 == var2 and var27 > var26):
                            var1 -= var2
                            var2 -= var0
                            var0 = graphicsobj.rasterClipY[var0]

                            while(True):
                                var2 -= 1
                                if(var2 < 0):
                                    while(True):
                                        var1 -= 1
                                        if(var1 < 0):
                                            return

                                        method2796(objectID, graphicsobj.annotationCanvas, graphicsobj.graphicsPixels, var19, var0, var5 >> 14,
                                                   var3 >> 14, var6, var30, var32, var35, var38, var33, var36, var39, graphicsobj.rasterClipEnable, graphicsobj.rasterClipX, graphicsobj.lowMem, graphicsobj.centerX, graphicsobj.field1944)
                                        var5 += var27
                                        var3 += var26
                                        var6 += var31
                                        var0 += graphicsobj.graphicsPixelsWidth
                                        var32 += var34
                                        var35 += var37
                                        var38 += var40

                                method2796(objectID, graphicsobj.annotationCanvas, graphicsobj.graphicsPixels, var19, var0, var4 >> 14,
                                           var3 >> 14, var6, var30, var32, var35, var38, var33, var36, var39, graphicsobj.rasterClipEnable, graphicsobj.rasterClipX, graphicsobj.lowMem, graphicsobj.centerX, graphicsobj.field1944)
                                var4 += var28
                                var3 += var26
                                var6 += var31
                                var0 += graphicsobj.graphicsPixelsWidth
                                var32 += var34
                                var35 += var37
                                var38 += var40

                        else:
                            var1 -= var2
                            var2 -= var0
                            var0 = graphicsobj.rasterClipY[var0]

                            while(True):
                                var2 -= 1
                                if(var2 < 0):
                                    while(True):
                                        var1 -= 1
                                        if(var1 < 0):
                                            return

                                        method2796(objectID, graphicsobj.annotationCanvas, graphicsobj.graphicsPixels, var19, var0, var3 >> 14,
                                                   var5 >> 14, var6, var30, var32, var35, var38, var33, var36, var39, graphicsobj.rasterClipEnable, graphicsobj.rasterClipX, graphicsobj.lowMem, graphicsobj.centerX, graphicsobj.field1944)
                                        var5 += var27
                                        var3 += var26
                                        var6 += var31
                                        var0 += graphicsobj.graphicsPixelsWidth
                                        var32 += var34
                                        var35 += var37
                                        var38 += var40

                                method2796(objectID, graphicsobj.annotationCanvas, graphicsobj.graphicsPixels, var19, var0, var3 >> 14,
                                           var4 >> 14, var6, var30, var32, var35, var38, var33, var36, var39, graphicsobj.rasterClipEnable, graphicsobj.rasterClipX, graphicsobj.lowMem, graphicsobj.centerX, graphicsobj.field1944)
                                var4 += var28
                                var3 += var26
                                var6 += var31
                                var0 += graphicsobj.graphicsPixelsWidth
                                var32 += var34
                                var35 += var37
                                var38 += var40

            elif(var1 <= var2):
                if(var1 < graphicsobj.Rasterizer3D_clipHeight):
                    if(var2 > graphicsobj.Rasterizer3D_clipHeight):
                        var2 = graphicsobj.Rasterizer3D_clipHeight

                    if(var0 > graphicsobj.Rasterizer3D_clipHeight):
                        var0 = graphicsobj.Rasterizer3D_clipHeight

                    var7 = var30 + ((var7 << 9) - var30 * var4)
                    if(var2 < var0):
                        var4 <<= 14
                        var3 = var4
                        if(var1 < 0):
                            var3 -= var26 * var1
                            var4 -= var27 * var1
                            var7 -= var31 * var1
                            var1 = 0

                        var5 <<= 14
                        if(var2 < 0):
                            var5 -= var28 * var2
                            var2 = 0

                        var41 = var1 - \
                            graphicsobj.centerY
                        var32 += var34 * var41
                        var35 += var37 * var41
                        var38 += var40 * var41
                        if((var2 == var1 or var26 >= var27) and (var2 != var1 or var26 <= var28)):
                            var0 -= var2
                            var2 -= var1
                            var1 = graphicsobj.rasterClipY[var1]

                            while(True):
                                var2 -= 1
                                if(var2 < 0):
                                    while(True):
                                        var0 -= 1
                                        if(var0 < 0):
                                            return

                                        method2796(objectID, graphicsobj.annotationCanvas, graphicsobj.graphicsPixels, var19, var1, var5 >> 14,
                                                   var3 >> 14, var7, var30, var32, var35, var38, var33, var36, var39, graphicsobj.rasterClipEnable, graphicsobj.rasterClipX, graphicsobj.lowMem, graphicsobj.centerX, graphicsobj.field1944)
                                        var3 += var26
                                        var5 += var28
                                        var7 += var31
                                        var1 += graphicsobj.graphicsPixelsWidth
                                        var32 += var34
                                        var35 += var37
                                        var38 += var40

                                method2796(objectID, graphicsobj.annotationCanvas, graphicsobj.graphicsPixels, var19, var1, var4 >> 14,
                                           var3 >> 14, var7, var30, var32, var35, var38, var33, var36, var39, graphicsobj.rasterClipEnable, graphicsobj.rasterClipX, graphicsobj.lowMem, graphicsobj.centerX, graphicsobj.field1944)
                                var3 += var26
                                var4 += var27
                                var7 += var31
                                var1 += graphicsobj.graphicsPixelsWidth
                                var32 += var34
                                var35 += var37
                                var38 += var40

                        else:
                            var0 -= var2
                            var2 -= var1
                            var1 = graphicsobj.rasterClipY[var1]

                            while(True):
                                var2 -= 1
                                if(var2 < 0):
                                    while(True):
                                        var0 -= 1
                                        if(var0 < 0):
                                            return

                                        method2796(objectID, graphicsobj.annotationCanvas, graphicsobj.graphicsPixels, var19, var1, var3 >> 14,
                                                   var5 >> 14, var7, var30, var32, var35, var38, var33, var36, var39, graphicsobj.rasterClipEnable, graphicsobj.rasterClipX, graphicsobj.lowMem, graphicsobj.centerX, graphicsobj.field1944)
                                        var3 += var26
                                        var5 += var28
                                        var7 += var31
                                        var1 += graphicsobj.graphicsPixelsWidth
                                        var32 += var34
                                        var35 += var37
                                        var38 += var40

                                method2796(objectID, graphicsobj.annotationCanvas, graphicsobj.graphicsPixels, var19, var1, var3 >> 14,
                                           var4 >> 14, var7, var30, var32, var35, var38, var33, var36, var39, graphicsobj.rasterClipEnable, graphicsobj.rasterClipX, graphicsobj.lowMem, graphicsobj.centerX, graphicsobj.field1944)
                                var3 += var26
                                var4 += var27
                                var7 += var31
                                var1 += graphicsobj.graphicsPixelsWidth
                                var32 += var34
                                var35 += var37
                                var38 += var40

                    else:
                        var4 <<= 14
                        var5 = var4
                        if(var1 < 0):
                            var5 -= var26 * var1
                            var4 -= var27 * var1
                            var7 -= var31 * var1
                            var1 = 0

                        var3 <<= 14
                        if(var0 < 0):
                            var3 -= var0 * var28
                            var0 = 0

                        var41 = var1 - \
                            graphicsobj.centerY
                        var32 += var34 * var41
                        var35 += var37 * var41
                        var38 += var40 * var41
                        if(var26 < var27):
                            var2 -= var0
                            var0 -= var1
                            var1 = graphicsobj.rasterClipY[var1]

                            while(True):
                                var0 -= 1
                                if(var0 < 0):
                                    while(True):
                                        var2 -= 1
                                        if(var2 < 0):
                                            return

                                        method2796(objectID, graphicsobj.annotationCanvas, graphicsobj.graphicsPixels, var19, var1, var3 >> 14,
                                                   var4 >> 14, var7, var30, var32, var35, var38, var33, var36, var39, graphicsobj.rasterClipEnable, graphicsobj.rasterClipX, graphicsobj.lowMem, graphicsobj.centerX, graphicsobj.field1944)
                                        var3 += var28
                                        var4 += var27
                                        var7 += var31
                                        var1 += graphicsobj.graphicsPixelsWidth
                                        var32 += var34
                                        var35 += var37
                                        var38 += var40

                                method2796(objectID, graphicsobj.annotationCanvas, graphicsobj.graphicsPixels, var19, var1, var5 >> 14,
                                           var4 >> 14, var7, var30, var32, var35, var38, var33, var36, var39, graphicsobj.rasterClipEnable, graphicsobj.rasterClipX, graphicsobj.lowMem, graphicsobj.centerX, graphicsobj.field1944)
                                var5 += var26
                                var4 += var27
                                var7 += var31
                                var1 += graphicsobj.graphicsPixelsWidth
                                var32 += var34
                                var35 += var37
                                var38 += var40

                        else:
                            var2 -= var0
                            var0 -= var1
                            var1 = graphicsobj.rasterClipY[var1]

                            while(True):
                                var0 -= 1
                                if(var0 < 0):
                                    while(True):
                                        var2 -= 1
                                        if(var2 < 0):
                                            return

                                        method2796(objectID, graphicsobj.annotationCanvas, graphicsobj.graphicsPixels, var19, var1, var4 >> 14,
                                                   var3 >> 14, var7, var30, var32, var35, var38, var33, var36, var39, graphicsobj.rasterClipEnable, graphicsobj.rasterClipX, graphicsobj.lowMem, graphicsobj.centerX, graphicsobj.field1944)
                                        var3 += var28
                                        var4 += var27
                                        var7 += var31
                                        var1 += graphicsobj.graphicsPixelsWidth
                                        var32 += var34
                                        var35 += var37
                                        var38 += var40

                                method2796(objectID, graphicsobj.annotationCanvas, graphicsobj.graphicsPixels, var19, var1, var4 >> 14,
                                           var5 >> 14, var7, var30, var32, var35, var38, var33, var36, var39, graphicsobj.rasterClipEnable, graphicsobj.rasterClipX, graphicsobj.lowMem, graphicsobj.centerX, graphicsobj.field1944)
                                var5 += var26
                                var4 += var27
                                var7 += var31
                                var1 += graphicsobj.graphicsPixelsWidth
                                var32 += var34
                                var35 += var37
                                var38 += var40

            elif(var2 < graphicsobj.Rasterizer3D_clipHeight):
                if(var0 > graphicsobj.Rasterizer3D_clipHeight):
                    var0 = graphicsobj.Rasterizer3D_clipHeight

                if(var1 > graphicsobj.Rasterizer3D_clipHeight):
                    var1 = graphicsobj.Rasterizer3D_clipHeight

                var8 = (var8 << 9) - var5 * var30 + var30
                if(var0 < var1):
                    var5 <<= 14
                    var4 = var5
                    if(var2 < 0):
                        var4 -= var27 * var2
                        var5 -= var28 * var2
                        var8 -= var31 * var2
                        var2 = 0

                    var3 <<= 14
                    if(var0 < 0):
                        var3 -= var0 * var26
                        var0 = 0

                    var41 = var2 - \
                        graphicsobj.centerY
                    var32 += var34 * var41
                    var35 += var37 * var41
                    var38 += var40 * var41
                    if(var27 < var28):
                        var1 -= var0
                        var0 -= var2
                        var2 = graphicsobj.rasterClipY[var2]

                        while(True):
                            var0 -= 1
                            if(var0 < 0):
                                while(True):
                                    var1 -= 1
                                    if(var1 < 0):
                                        return

                                    method2796(objectID, graphicsobj.annotationCanvas, graphicsobj.graphicsPixels, var19, var2, var4 >> 14,
                                               var3 >> 14, var8, var30, var32, var35, var38, var33, var36, var39, graphicsobj.rasterClipEnable, graphicsobj.rasterClipX, graphicsobj.lowMem, graphicsobj.centerX, graphicsobj.field1944)
                                    var4 += var27
                                    var3 += var26
                                    var8 += var31
                                    var2 += graphicsobj.graphicsPixelsWidth
                                    var32 += var34
                                    var35 += var37
                                    var38 += var40

                            method2796(objectID, graphicsobj.annotationCanvas, graphicsobj.graphicsPixels, var19, var2, var4 >> 14,
                                       var5 >> 14, var8, var30, var32, var35, var38, var33, var36, var39, graphicsobj.rasterClipEnable, graphicsobj.rasterClipX, graphicsobj.lowMem, graphicsobj.centerX, graphicsobj.field1944)
                            var4 += var27
                            var5 += var28
                            var8 += var31
                            var2 += graphicsobj.graphicsPixelsWidth
                            var32 += var34
                            var35 += var37
                            var38 += var40

                    else:
                        var1 -= var0
                        var0 -= var2
                        var2 = graphicsobj.rasterClipY[var2]

                        while(True):
                            var0 -= 1
                            if(var0 < 0):
                                while(True):
                                    var1 -= 1
                                    if(var1 < 0):
                                        return

                                    method2796(objectID, graphicsobj.annotationCanvas, graphicsobj.graphicsPixels, var19, var2, var3 >> 14,
                                               var4 >> 14, var8, var30, var32, var35, var38, var33, var36, var39, graphicsobj.rasterClipEnable, graphicsobj.rasterClipX, graphicsobj.lowMem, graphicsobj.centerX, graphicsobj.field1944)
                                    var4 += var27
                                    var3 += var26
                                    var8 += var31
                                    var2 += graphicsobj.graphicsPixelsWidth
                                    var32 += var34
                                    var35 += var37
                                    var38 += var40

                            method2796(objectID, graphicsobj.annotationCanvas, graphicsobj.graphicsPixels, var19, var2, var5 >> 14,
                                       var4 >> 14, var8, var30, var32, var35, var38, var33, var36, var39, graphicsobj.rasterClipEnable, graphicsobj.rasterClipX, graphicsobj.lowMem, graphicsobj.centerX, graphicsobj.field1944)
                            var4 += var27
                            var5 += var28
                            var8 += var31
                            var2 += graphicsobj.graphicsPixelsWidth
                            var32 += var34
                            var35 += var37
                            var38 += var40

                else:
                    var5 <<= 14
                    var3 = var5
                    if(var2 < 0):
                        var3 -= var27 * var2
                        var5 -= var28 * var2
                        var8 -= var31 * var2
                        var2 = 0

                    var4 <<= 14
                    if(var1 < 0):
                        var4 -= var26 * var1
                        var1 = 0

                    var41 = var2 - \
                        graphicsobj.centerY
                    var32 += var34 * var41
                    var35 += var37 * var41
                    var38 += var40 * var41
                    if(var27 < var28):
                        var0 -= var1
                        var1 -= var2
                        var2 = graphicsobj.rasterClipY[var2]

                        while(True):
                            var1 -= 1
                            if(var1 < 0):
                                while(True):
                                    var0 -= 1
                                    if(var0 < 0):
                                        return

                                    method2796(objectID, graphicsobj.annotationCanvas, graphicsobj.graphicsPixels, var19, var2, var4 >> 14,
                                               var5 >> 14, var8, var30, var32, var35, var38, var33, var36, var39, graphicsobj.rasterClipEnable, graphicsobj.rasterClipX, graphicsobj.lowMem, graphicsobj.centerX, graphicsobj.field1944)
                                    var4 += var26
                                    var5 += var28
                                    var8 += var31
                                    var2 += graphicsobj.graphicsPixelsWidth
                                    var32 += var34
                                    var35 += var37
                                    var38 += var40

                            method2796(objectID, graphicsobj.annotationCanvas, graphicsobj.graphicsPixels, var19, var2, var3 >> 14,
                                       var5 >> 14, var8, var30, var32, var35, var38, var33, var36, var39, graphicsobj.rasterClipEnable, graphicsobj.rasterClipX, graphicsobj.lowMem, graphicsobj.centerX, graphicsobj.field1944)
                            var3 += var27
                            var5 += var28
                            var8 += var31
                            var2 += graphicsobj.graphicsPixelsWidth
                            var32 += var34
                            var35 += var37
                            var38 += var40

                    else:
                        var0 -= var1
                        var1 -= var2
                        var2 = graphicsobj.rasterClipY[var2]

                        while(True):
                            var1 -= 1
                            if(var1 < 0):
                                while(True):
                                    var0 -= 1
                                    if(var0 < 0):
                                        return

                                    method2796(objectID, graphicsobj.annotationCanvas, graphicsobj.graphicsPixels, var19, var2, var5 >> 14,
                                               var4 >> 14, var8, var30, var32, var35, var38, var33, var36, var39,
                                               graphicsobj.rasterClipEnable, graphicsobj.rasterClipX, graphicsobj.lowMem, graphicsobj.centerX, graphicsobj.field1944)
                                    var4 += var26
                                    var5 += var28
                                    var8 += var31
                                    var2 += graphicsobj.graphicsPixelsWidth
                                    var32 += var34
                                    var35 += var37
                                    var38 += var40

                            method2796(objectID, graphicsobj.annotationCanvas, graphicsobj.graphicsPixels, var19, var2, var5 >> 14,
                                       var3 >> 14, var8, var30, var32, var35, var38, var33, var36, var39,
                                       graphicsobj.rasterClipEnable, graphicsobj.rasterClipX, graphicsobj.lowMem, graphicsobj.centerX, graphicsobj.field1944)
                            var3 += var27
                            var5 += var28
                            var8 += var31
                            var2 += graphicsobj.graphicsPixelsWidth
                            var32 += var34
                            var35 += var37
                            var38 += var40


@jit(nopython=True, cache=False)
def method2798(var0,  var1,  var2,  var3):
    return var0 * var2 + var3 * var1 >> 16


@jit(nopython=True, cache=False)
def method2799(var0,  var1,  var2,  var3):
    return var2 * var1 - var3 * var0 >> 16


@jit(nopython=True, cache=False)
def method2797(var0, var1):
    var1 = (var0 & 127) * var1 >> 7
    if(var1 < 2):
        var1 = 2
    elif(var1 > 126):
        var1 = 126

    return (var0 & 65408) + var1


@jit(nopython=True, cache=False)
def method2800(var0,  var1,  var2,  var3):
    return var0 * var2 - var3 * var1 >> 16


@jit(nopython=True, cache=False)
def method2812(var0,  var1,  var2,  var3):
    return var3 * var0 + var2 * var1 >> 16


@jit(nopython=True, cache=False)
def method2779(var0,  var1,  var2,  var3):
    return var0 * var2 + var3 * var1 >> 16


@jit(nopython=True, cache=False)
def method2803(var0,  var1,  var2,  var3):
    return var2 * var1 - var3 * var0 >> 16


@jit(nopython=True, cache=False)
def method2796(objectID, annotationCanvas, gameCanvas, var1, var4, var5, var6, var7, var8, var9, var10, var11, var12, var13, var14,
               rasterClipEnable, rasterClipX, lowMem, centerX, field1944):
    if(rasterClipEnable):
        if(var6 > rasterClipX):
            var6 = rasterClipX

        if(var5 < 0):
            var5 = 0

    if(var5 < var6):
        var4 += var5
        var7 += var5 * var8
        var17 = var6 - var5
        if(lowMem):

            raise Exception("Not Implemented")

            # var23 = var5 - self.centerX
            # var9 += var23 * (var12 >> 3)
            # var10 += (var13 >> 3) * var23
            # var11 += var23 * (var14 >> 3)
            # var22 = var11 >> 12
            # if(var22 != 0) :
            # var18 = var9 / var22
            # var19 = var10 / var22
            # if(var18 < 0) :
            # var18 = 0
            # elif(var18 > 4032) :
            # var18 = 4032

            # else :
            # var18 = 0
            # var19 = 0

            # var9 += var12
            # var10 += var13
            # var11 += var14
            # var22 = var11 >> 12
            # if(var22 != 0) :
            # var20 = var9 / var22
            # var21 = var10 / var22
            # if(var20 < 0) :
            # var20 = 0
            # elif(var20 > 4032) :
            # var20 = 4032

            # else :
            # var20 = 0
            # var21 = 0

            # var2 = (var18 << 20) + var19
            # var16 = (var21 - var19 >> 3) + (var20 - var18 >> 3 << 20)
            # var17 >>= 3
            # var8 <<= 3
            # var15 = var7 >> 8
            # if(field1944) :
            # if(var17 > 0) :
            # do :
            # var3 = var1[(var2 >>> 26) + (var2 & 4032)]
            # var0[var4++] = (var15 * (var3 & 65280) & 16711680) + ((var3 & 16711935) * var15 & -16711936) >> 8
            # var2 += var16
            # var3 = var1[(var2 >>> 26) + (var2 & 4032)]
            # var0[var4++] = (var15 * (var3 & 65280) & 16711680) + ((var3 & 16711935) * var15 & -16711936) >> 8
            # var2 += var16
            # var3 = var1[(var2 >>> 26) + (var2 & 4032)]
            # var0[var4++] = (var15 * (var3 & 65280) & 16711680) + ((var3 & 16711935) * var15 & -16711936) >> 8
            # var2 += var16
            # var3 = var1[(var2 >>> 26) + (var2 & 4032)]
            # var0[var4++] = (var15 * (var3 & 65280) & 16711680) + ((var3 & 16711935) * var15 & -16711936) >> 8
            # var2 += var16
            # var3 = var1[(var2 >>> 26) + (var2 & 4032)]
            # var0[var4++] = (var15 * (var3 & 65280) & 16711680) + ((var3 & 16711935) * var15 & -16711936) >> 8
            # var2 += var16
            # var3 = var1[(var2 >>> 26) + (var2 & 4032)]
            # var0[var4++] = (var15 * (var3 & 65280) & 16711680) + ((var3 & 16711935) * var15 & -16711936) >> 8
            # var2 += var16
            # var3 = var1[(var2 >>> 26) + (var2 & 4032)]
            # var0[var4++] = (var15 * (var3 & 65280) & 16711680) + ((var3 & 16711935) * var15 & -16711936) >> 8
            # var2 += var16
            # var3 = var1[(var2 >>> 26) + (var2 & 4032)]
            # var0[var4++] = (var15 * (var3 & 65280) & 16711680) + ((var3 & 16711935) * var15 & -16711936) >> 8
            # var18 = var20
            # var19 = var21
            # var9 += var12
            # var10 += var13
            # var11 += var14
            # var22 = var11 >> 12
            # if(var22 != 0) :
            # var20 = var9 / var22
            # var21 = var10 / var22
            # if(var20 < 0) :
            # var20 = 0
            # elif(var20 > 4032) :
            # var20 = 4032

            # else :
            # var20 = 0
            # var21 = 0

            # var2 = (var18 << 20) + var19
            # var16 = (var21 - var19 >> 3) + (var20 - var18 >> 3 << 20)
            # var7 += var8
            # var15 = var7 >> 8
            # --var17
            # while(var17 > 0)

            # var17 = var6 - var5 & 7
            # if(var17 > 0) :
            # do :
            # var3 = var1[(var2 >>> 26) + (var2 & 4032)]
            # var0[var4++] = (var15 * (var3 & 65280) & 16711680) + ((var3 & 16711935) * var15 & -16711936) >> 8
            # var2 += var16
            # --var17
            # while(var17 > 0)

            # else :
            # if(var17 > 0) :
            # do :
            # if((var3 = var1[(var2 >>> 26) + (var2 & 4032)]) != 0) :
            # var0[var4] = (var15 * (var3 & 65280) & 16711680) + ((var3 & 16711935) * var15 & -16711936) >> 8

            # ++var4
            # var2 += var16
            # if((var3 = var1[(var2 >>> 26) + (var2 & 4032)]) != 0) :
            # var0[var4] = (var15 * (var3 & 65280) & 16711680) + ((var3 & 16711935) * var15 & -16711936) >> 8

            # ++var4
            # var2 += var16
            # if((var3 = var1[(var2 >>> 26) + (var2 & 4032)]) != 0) :
            # var0[var4] = (var15 * (var3 & 65280) & 16711680) + ((var3 & 16711935) * var15 & -16711936) >> 8

            # ++var4
            # var2 += var16
            # if((var3 = var1[(var2 >>> 26) + (var2 & 4032)]) != 0) :
            # var0[var4] = (var15 * (var3 & 65280) & 16711680) + ((var3 & 16711935) * var15 & -16711936) >> 8

            # ++var4
            # var2 += var16
            # if((var3 = var1[(var2 >>> 26) + (var2 & 4032)]) != 0) :
            # var0[var4] = (var15 * (var3 & 65280) & 16711680) + ((var3 & 16711935) * var15 & -16711936) >> 8

            # ++var4
            # var2 += var16
            # if((var3 = var1[(var2 >>> 26) + (var2 & 4032)]) != 0) :
            # var0[var4] = (var15 * (var3 & 65280) & 16711680) + ((var3 & 16711935) * var15 & -16711936) >> 8

            # ++var4
            # var2 += var16
            # if((var3 = var1[(var2 >>> 26) + (var2 & 4032)]) != 0) :
            # var0[var4] = (var15 * (var3 & 65280) & 16711680) + ((var3 & 16711935) * var15 & -16711936) >> 8

            # ++var4
            # var2 += var16
            # if((var3 = var1[(var2 >>> 26) + (var2 & 4032)]) != 0) :
            # var0[var4] = (var15 * (var3 & 65280) & 16711680) + ((var3 & 16711935) * var15 & -16711936) >> 8

            # ++var4
            # var18 = var20
            # var19 = var21
            # var9 += var12
            # var10 += var13
            # var11 += var14
            # var22 = var11 >> 12
            # if(var22 != 0) :
            # var20 = var9 / var22
            # var21 = var10 / var22
            # if(var20 < 0) :
            # var20 = 0
            # elif(var20 > 4032) :
            # var20 = 4032

            # else :
            # var20 = 0
            # var21 = 0

            # var2 = (var18 << 20) + var19
            # var16 = (var21 - var19 >> 3) + (var20 - var18 >> 3 << 20)
            # var7 += var8
            # var15 = var7 >> 8
            # --var17
            # while(var17 > 0)

            # var17 = var6 - var5 & 7
            # if(var17 > 0) :
            # do :
            # if((var3 = var1[(var2 >>> 26) + (var2 & 4032)]) != 0) :
            # var0[var4] = (var15 * (var3 & 65280) & 16711680) + ((var3 & 16711935) * var15 & -16711936) >> 8

            # ++var4
            # var2 += var16
            # --var17
            # while(var17 > 0)

        else:
            var23 = var5 - centerX
            var9 += var23 * var12
            var10 += var13 * var23
            var11 += var23 * var14
            var22 = var11 >> 14
            if(var22 != 0):
                var18 = integerdivide(var9, var22)
                var19 = integerdivide(var10, var22)
            else:
                var18 = 0
                var19 = 0

            var9 += var17 * var12
            var10 += var13 * var17
            var11 += var17 * var14
            var22 = var11 >> 14
            if(var22 != 0):
                var20 = integerdivide(var9, var22)
                var21 = integerdivide(var10, var22)
            else:
                var20 = 0
                var21 = 0

            var2 = np.int32((var18 << 18) + var19)
            var16 = integerdivide(var21 - var19, var17) + \
                (integerdivide(var20 - var18, var17) << 18)
            var16 = np.int32(var16)
            var17 >>= 3
            var8 <<= 3
            var15 = var7 >> 8
            if(field1944):
                if(var17 > 0):

                    while (True):

                        #if var4 + 8 >= len(gameCanvas):
                        #    raise Exception("gon eror")

                        var3 = var1[(var2 & 16256) +
                                    MathUtills.unsignedrshift(var2, 25)]
                        gameCanvas[var4] = (
                            var15 * (var3 & 65280) & 16711680) + ((var3 & 16711935) * var15 & -16711936) >> 8
                        annotationCanvas[var4] = objectID
                        var4 += 1
                        var2 += var16
                        var3 = var1[(var2 & 16256) +
                                    MathUtills.unsignedrshift(var2, 25)]
                        gameCanvas[var4] = (
                            var15 * (var3 & 65280) & 16711680) + ((var3 & 16711935) * var15 & -16711936) >> 8
                        annotationCanvas[var4] = objectID
                        var4 += 1
                        var2 += var16
                        var3 = var1[(var2 & 16256) +
                                    MathUtills.unsignedrshift(var2, 25)]
                        gameCanvas[var4] = (
                            var15 * (var3 & 65280) & 16711680) + ((var3 & 16711935) * var15 & -16711936) >> 8
                        annotationCanvas[var4] = objectID
                        var4 += 1
                        var2 += var16
                        var3 = var1[(var2 & 16256) +
                                    MathUtills.unsignedrshift(var2, 25)]
                        gameCanvas[var4] = (
                            var15 * (var3 & 65280) & 16711680) + ((var3 & 16711935) * var15 & -16711936) >> 8
                        annotationCanvas[var4] = objectID
                        var4 += 1
                        var2 += var16
                        var3 = var1[(var2 & 16256) +
                                    MathUtills.unsignedrshift(var2, 25)]
                        gameCanvas[var4] = (
                            var15 * (var3 & 65280) & 16711680) + ((var3 & 16711935) * var15 & -16711936) >> 8
                        annotationCanvas[var4] = objectID
                        var4 += 1
                        var2 += var16
                        var3 = var1[(var2 & 16256) +
                                    MathUtills.unsignedrshift(var2, 25)]
                        gameCanvas[var4] = (
                            var15 * (var3 & 65280) & 16711680) + ((var3 & 16711935) * var15 & -16711936) >> 8
                        annotationCanvas[var4] = objectID
                        var4 += 1
                        var2 += var16
                        var3 = var1[(var2 & 16256) +
                                    MathUtills.unsignedrshift(var2, 25)]
                        gameCanvas[var4] = (
                            var15 * (var3 & 65280) & 16711680) + ((var3 & 16711935) * var15 & -16711936) >> 8
                        annotationCanvas[var4] = objectID
                        var4 += 1
                        var2 += var16
                        var3 = var1[(var2 & 16256) +
                                    MathUtills.unsignedrshift(var2, 25)]
                        gameCanvas[var4] = (
                            var15 * (var3 & 65280) & 16711680) + ((var3 & 16711935) * var15 & -16711936) >> 8
                        annotationCanvas[var4] = objectID
                        var4 += 1
                        var2 += var16
                        var7 += var8
                        var15 = var7 >> 8
                        var17 -= 1

                        if var17 <= 0:
                            break

                var17 = var6 - var5 & 7
                if(var17 > 0):
                    while (True):
                        var3 = var1[(var2 & 16256) +
                                    MathUtills.unsignedrshift(var2, 25)]
                        gameCanvas[var4] = (
                            var15 * (var3 & 65280) & 16711680) + ((var3 & 16711935) * var15 & -16711936) >> 8
                        annotationCanvas[var4] = objectID
                        var4 += 1
                        var2 += var16
                        var17 -= 1
                        if var17 <= 0:
                            break

            else:
                if(var17 > 0):
                    while True:  # do :

                        if var4 + 8 >= len(gameCanvas):
                            print("Gonna Error")

                        var3 = var1[(var2 & 16256) +
                                    MathUtills.unsignedrshift(var2, 25)]
                        if var3 != 0:
                            gameCanvas[var4] = (
                                var15 * (var3 & 65280) & 16711680) + ((var3 & 16711935) * var15 & -16711936) >> 8
                            annotationCanvas[var4] = objectID
                        var4 += 1
                        var2 += var16
                        var3 = var1[(var2 & 16256) +
                                    MathUtills.unsignedrshift(var2, 25)]
                        if var3 != 0:
                            gameCanvas[var4] = (
                                var15 * (var3 & 65280) & 16711680) + ((var3 & 16711935) * var15 & -16711936) >> 8
                            annotationCanvas[var4] = objectID
                        var4 += 1
                        var2 += var16
                        var3 = var1[(var2 & 16256) +
                                    MathUtills.unsignedrshift(var2, 25)]
                        if(var3 != 0):
                            gameCanvas[var4] = (
                                var15 * (var3 & 65280) & 16711680) + ((var3 & 16711935) * var15 & -16711936) >> 8
                            annotationCanvas[var4] = objectID
                        var4 += 1
                        var2 += var16
                        var3 = var1[(var2 & 16256) +
                                    MathUtills.unsignedrshift(var2, 25)]
                        if(var3 != 0):
                            gameCanvas[var4] = (
                                var15 * (var3 & 65280) & 16711680) + ((var3 & 16711935) * var15 & -16711936) >> 8
                            annotationCanvas[var4] = objectID
                        var4 += 1
                        var2 += var16
                        var3 = var1[(var2 & 16256) +
                                    MathUtills.unsignedrshift(var2, 25)]
                        if(var3 != 0):
                            gameCanvas[var4] = (
                                var15 * (var3 & 65280) & 16711680) + ((var3 & 16711935) * var15 & -16711936) >> 8
                            annotationCanvas[var4] = objectID
                        var4 += 1
                        var2 += var16
                        var3 = var1[(var2 & 16256) +
                                    MathUtills.unsignedrshift(var2, 25)]
                        if(var3 != 0):
                            gameCanvas[var4] = (
                                var15 * (var3 & 65280) & 16711680) + ((var3 & 16711935) * var15 & -16711936) >> 8
                            annotationCanvas[var4] = objectID
                        var4 += 1
                        var2 += var16
                        var3 = var1[(var2 & 16256) +
                                    MathUtills.unsignedrshift(var2, 25)]
                        if(var3 != 0):
                            gameCanvas[var4] = (
                                var15 * (var3 & 65280) & 16711680) + ((var3 & 16711935) * var15 & -16711936) >> 8
                            annotationCanvas[var4] = objectID
                        var4 += 1
                        var2 += var16
                        var3 = var1[(var2 & 16256) +
                                    MathUtills.unsignedrshift(var2, 25)]
                        if(var3 != 0):
                            gameCanvas[var4] = (
                                var15 * (var3 & 65280) & 16711680) + ((var3 & 16711935) * var15 & -16711936) >> 8
                            annotationCanvas[var4] = objectID
                        var4 += 1
                        var2 += var16
                        var7 += var8
                        var15 = var7 >> 8
                        var17 -= 1

                        if var17 <= 0:
                            break

                var17 = var6 - var5 & 7
                if(var17 > 0):
                    while (True):
                        var3 = var1[(var2 & 16256) +
                                    MathUtills.unsignedrshift(var2, 25)]
                        if(var3 != 0):
                            gameCanvas[var4] = (
                                var15 * (var3 & 65280) & 16711680) + ((var3 & 16711935) * var15 & -16711936) >> 8
                            annotationCanvas[var4] = objectID

                        var4 += 1
                        var2 += var16
                        var17 -= 1
                        if var17 <= 0:
                            break


@jit(nopython=True, cache=False)
def method2844(objectID, annotationCanvas, gameCanvas, var1, var4, var5, var6, var7, var8, var9, var10, var11, var12, var13, var14,
               rasterClipEnable, rasterClipX, lowMem, centerX, field1944):
    if(rasterClipEnable):
        if(var6 > rasterClipX):
            var6 = rasterClipX

        if(var5 < 0):
            var5 = 0

    if(var5 < var6):
        var4 += var5
        var7 += var5 * var8
        var17 = var6 - var5
        if(lowMem):

            raise Exception("Not Implemented")

            # var23 = var5 - self.centerX
            # var9 += var23 * (var12 >> 3)
            # var10 += (var13 >> 3) * var23
            # var11 += var23 * (var14 >> 3)
            # var22 = var11 >> 12
            # if(var22 != 0) :
            # var18 = var9 / var22
            # var19 = var10 / var22
            # if(var18 < 0) :
            # var18 = 0
            # elif(var18 > 4032) :
            # var18 = 4032

            # else :
            # var18 = 0
            # var19 = 0

            # var9 += var12
            # var10 += var13
            # var11 += var14
            # var22 = var11 >> 12
            # if(var22 != 0) :
            # var20 = var9 / var22
            # var21 = var10 / var22
            # if(var20 < 0) :
            # var20 = 0
            # elif(var20 > 4032) :
            # var20 = 4032

            # else :
            # var20 = 0
            # var21 = 0

            # var2 = (var18 << 20) + var19
            # var16 = (var21 - var19 >> 3) + (var20 - var18 >> 3 << 20)
            # var17 >>= 3
            # var8 <<= 3
            # var15 = var7 >> 8
            # if(field1944) :
            # if(var17 > 0) :
            # do :
            # var3 = var1[(var2 >>> 26) + (var2 & 4032)]
            # var0[var4++] = (var15 * (var3 & 65280) & 16711680) + ((var3 & 16711935) * var15 & -16711936) >> 8
            # var2 += var16
            # var3 = var1[(var2 >>> 26) + (var2 & 4032)]
            # var0[var4++] = (var15 * (var3 & 65280) & 16711680) + ((var3 & 16711935) * var15 & -16711936) >> 8
            # var2 += var16
            # var3 = var1[(var2 >>> 26) + (var2 & 4032)]
            # var0[var4++] = (var15 * (var3 & 65280) & 16711680) + ((var3 & 16711935) * var15 & -16711936) >> 8
            # var2 += var16
            # var3 = var1[(var2 >>> 26) + (var2 & 4032)]
            # var0[var4++] = (var15 * (var3 & 65280) & 16711680) + ((var3 & 16711935) * var15 & -16711936) >> 8
            # var2 += var16
            # var3 = var1[(var2 >>> 26) + (var2 & 4032)]
            # var0[var4++] = (var15 * (var3 & 65280) & 16711680) + ((var3 & 16711935) * var15 & -16711936) >> 8
            # var2 += var16
            # var3 = var1[(var2 >>> 26) + (var2 & 4032)]
            # var0[var4++] = (var15 * (var3 & 65280) & 16711680) + ((var3 & 16711935) * var15 & -16711936) >> 8
            # var2 += var16
            # var3 = var1[(var2 >>> 26) + (var2 & 4032)]
            # var0[var4++] = (var15 * (var3 & 65280) & 16711680) + ((var3 & 16711935) * var15 & -16711936) >> 8
            # var2 += var16
            # var3 = var1[(var2 >>> 26) + (var2 & 4032)]
            # var0[var4++] = (var15 * (var3 & 65280) & 16711680) + ((var3 & 16711935) * var15 & -16711936) >> 8
            # var18 = var20
            # var19 = var21
            # var9 += var12
            # var10 += var13
            # var11 += var14
            # var22 = var11 >> 12
            # if(var22 != 0) :
            # var20 = var9 / var22
            # var21 = var10 / var22
            # if(var20 < 0) :
            # var20 = 0
            # elif(var20 > 4032) :
            # var20 = 4032

            # else :
            # var20 = 0
            # var21 = 0

            # var2 = (var18 << 20) + var19
            # var16 = (var21 - var19 >> 3) + (var20 - var18 >> 3 << 20)
            # var7 += var8
            # var15 = var7 >> 8
            # --var17
            # while(var17 > 0)

            # var17 = var6 - var5 & 7
            # if(var17 > 0) :
            # do :
            # var3 = var1[(var2 >>> 26) + (var2 & 4032)]
            # var0[var4++] = (var15 * (var3 & 65280) & 16711680) + ((var3 & 16711935) * var15 & -16711936) >> 8
            # var2 += var16
            # --var17
            # while(var17 > 0)

            # else :
            # if(var17 > 0) :
            # do :
            # if((var3 = var1[(var2 >>> 26) + (var2 & 4032)]) != 0) :
            # var0[var4] = (var15 * (var3 & 65280) & 16711680) + ((var3 & 16711935) * var15 & -16711936) >> 8

            # ++var4
            # var2 += var16
            # if((var3 = var1[(var2 >>> 26) + (var2 & 4032)]) != 0) :
            # var0[var4] = (var15 * (var3 & 65280) & 16711680) + ((var3 & 16711935) * var15 & -16711936) >> 8

            # ++var4
            # var2 += var16
            # if((var3 = var1[(var2 >>> 26) + (var2 & 4032)]) != 0) :
            # var0[var4] = (var15 * (var3 & 65280) & 16711680) + ((var3 & 16711935) * var15 & -16711936) >> 8

            # ++var4
            # var2 += var16
            # if((var3 = var1[(var2 >>> 26) + (var2 & 4032)]) != 0) :
            # var0[var4] = (var15 * (var3 & 65280) & 16711680) + ((var3 & 16711935) * var15 & -16711936) >> 8

            # ++var4
            # var2 += var16
            # if((var3 = var1[(var2 >>> 26) + (var2 & 4032)]) != 0) :
            # var0[var4] = (var15 * (var3 & 65280) & 16711680) + ((var3 & 16711935) * var15 & -16711936) >> 8

            # ++var4
            # var2 += var16
            # if((var3 = var1[(var2 >>> 26) + (var2 & 4032)]) != 0) :
            # var0[var4] = (var15 * (var3 & 65280) & 16711680) + ((var3 & 16711935) * var15 & -16711936) >> 8

            # ++var4
            # var2 += var16
            # if((var3 = var1[(var2 >>> 26) + (var2 & 4032)]) != 0) :
            # var0[var4] = (var15 * (var3 & 65280) & 16711680) + ((var3 & 16711935) * var15 & -16711936) >> 8

            # ++var4
            # var2 += var16
            # if((var3 = var1[(var2 >>> 26) + (var2 & 4032)]) != 0) :
            # var0[var4] = (var15 * (var3 & 65280) & 16711680) + ((var3 & 16711935) * var15 & -16711936) >> 8

            # ++var4
            # var18 = var20
            # var19 = var21
            # var9 += var12
            # var10 += var13
            # var11 += var14
            # var22 = var11 >> 12
            # if(var22 != 0) :
            # var20 = var9 / var22
            # var21 = var10 / var22
            # if(var20 < 0) :
            # var20 = 0
            # elif(var20 > 4032) :
            # var20 = 4032

            # else :
            # var20 = 0
            # var21 = 0

            # var2 = (var18 << 20) + var19
            # var16 = (var21 - var19 >> 3) + (var20 - var18 >> 3 << 20)
            # var7 += var8
            # var15 = var7 >> 8
            # --var17
            # while(var17 > 0)

            # var17 = var6 - var5 & 7
            # if(var17 > 0) :
            # do :
            # if((var3 = var1[(var2 >>> 26) + (var2 & 4032)]) != 0) :
            # var0[var4] = (var15 * (var3 & 65280) & 16711680) + ((var3 & 16711935) * var15 & -16711936) >> 8

            # ++var4
            # var2 += var16
            # --var17
            # while(var17 > 0)

        else:
            var23 = var5 - centerX
            var9 += var23 * (var12 >> 3)
            var10 += (var13 >> 3) * var23
            var11 += var23 * (var14 >> 3)
            var22 = var11 >> 14
            if(var22 != 0):
                var18 = integerdivide(var9, var22)
                var19 = integerdivide(var10, var22)
                if(var18 < 0):
                    var18 = 0
                elif(var18 > 16256):
                    var18 = 16256

            else:
                var18 = 0
                var19 = 0

            var9 += var12
            var10 += var13
            var11 += var14
            var22 = var11 >> 14
            if(var22 != 0):
                var20 = integerdivide(var9, var22)
                var21 = integerdivide(var10, var22)
                if(var20 < 0):
                    var20 = 0
                elif(var20 > 16256):
                    var20 = 16256
            else:
                var20 = 0
                var21 = 0

            var2 = (var18 << 18) + var19
            var16 = (var21 - var19 >> 3) + (var20 - var18 >> 3 << 18)
            var17 >>= 3
            var8 <<= 3
            var15 = var7 >> 8
            if(field1944):
                if(var17 > 0):

                    while (True):

                        var3 = var1[(var2 & 16256) +
                                    MathUtills.unsignedrshift(var2, 25)]
                        gameCanvas[var4] = (
                            var15 * (var3 & 65280) & 16711680) + ((var3 & 16711935) * var15 & -16711936) >> 8
                        annotationCanvas[var4] = objectID
                        var4 += 1
                        var2 += var16
                        var3 = var1[(var2 & 16256) +
                                    MathUtills.unsignedrshift(var2, 25)]
                        gameCanvas[var4] = (
                            var15 * (var3 & 65280) & 16711680) + ((var3 & 16711935) * var15 & -16711936) >> 8
                        annotationCanvas[var4] = objectID
                        var4 += 1
                        var2 += var16
                        var3 = var1[(var2 & 16256) +
                                    MathUtills.unsignedrshift(var2, 25)]
                        gameCanvas[var4] = (
                            var15 * (var3 & 65280) & 16711680) + ((var3 & 16711935) * var15 & -16711936) >> 8
                        annotationCanvas[var4] = objectID
                        var4 += 1
                        var2 += var16
                        var3 = var1[(var2 & 16256) +
                                    MathUtills.unsignedrshift(var2, 25)]
                        gameCanvas[var4] = (
                            var15 * (var3 & 65280) & 16711680) + ((var3 & 16711935) * var15 & -16711936) >> 8
                        annotationCanvas[var4] = objectID
                        var4 += 1
                        var2 += var16
                        var3 = var1[(var2 & 16256) +
                                    MathUtills.unsignedrshift(var2, 25)]
                        gameCanvas[var4] = (
                            var15 * (var3 & 65280) & 16711680) + ((var3 & 16711935) * var15 & -16711936) >> 8
                        annotationCanvas[var4] = objectID
                        var4 += 1
                        var2 += var16
                        var3 = var1[(var2 & 16256) +
                                    MathUtills.unsignedrshift(var2, 25)]
                        gameCanvas[var4] = (
                            var15 * (var3 & 65280) & 16711680) + ((var3 & 16711935) * var15 & -16711936) >> 8
                        annotationCanvas[var4] = objectID
                        var4 += 1
                        var2 += var16
                        var3 = var1[(var2 & 16256) +
                                    MathUtills.unsignedrshift(var2, 25)]
                        gameCanvas[var4] = (
                            var15 * (var3 & 65280) & 16711680) + ((var3 & 16711935) * var15 & -16711936) >> 8
                        annotationCanvas[var4] = objectID
                        var4 += 1
                        var2 += var16
                        var3 = var1[(var2 & 16256) +
                                    MathUtills.unsignedrshift(var2, 25)]
                        gameCanvas[var4] = (
                            var15 * (var3 & 65280) & 16711680) + ((var3 & 16711935) * var15 & -16711936) >> 8
                        annotationCanvas[var4] = objectID
                        var4 += 1
                        var18 = var20
                        var19 = var21
                        var9 += var12
                        var10 += var13
                        var11 += var14
                        var22 = var11 >> 14
                        if(var22 != 0):
                            var20 = integerdivide(var9, var22)
                            var21 = integerdivide(var10, var22)
                            if(var20 < 0):
                                var20 = 0
                            elif(var20 > 16256):
                                var20 = 16256

                        else:
                            var20 = 0
                            var21 = 0

                        var2 = (var18 << 18) + var19
                        var16 = (var21 - var19 >> 3) + \
                            (var20 - var18 >> 3 << 18)
                        var7 += var8
                        var15 = var7 >> 8
                        var17 -= 1

                        if var17 <= 0:
                            break

                var17 = var6 - var5 & 7
                if(var17 > 0):
                    while (True):
                        var3 = var1[(var2 & 16256) +
                                    MathUtills.unsignedrshift(var2, 25)]
                        gameCanvas[var4] = (
                            var15 * (var3 & 65280) & 16711680) + ((var3 & 16711935) * var15 & -16711936) >> 8
                        annotationCanvas[var4] = objectID
                        var4 += 1
                        var2 += var16
                        var17 -= 1
                        if var17 <= 0:
                            break

            else:
                if(var17 > 0):
                    while True:  # do :
                        var3 = var1[(var2 & 16256) +
                                    MathUtills.unsignedrshift(var2, 25)]
                        if var3 != 0:
                            gameCanvas[var4] = (
                                var15 * (var3 & 65280) & 16711680) + ((var3 & 16711935) * var15 & -16711936) >> 8
                            annotationCanvas[var4] = objectID

                        var4 += 1
                        var2 += var16
                        var3 = var1[(var2 & 16256) +
                                    MathUtills.unsignedrshift(var2, 25)]
                        if var3 != 0:
                            gameCanvas[var4] = (
                                var15 * (var3 & 65280) & 16711680) + ((var3 & 16711935) * var15 & -16711936) >> 8
                            annotationCanvas[var4] = objectID

                        var4 += 1
                        var2 += var16
                        var3 = var1[(var2 & 16256) +
                                    MathUtills.unsignedrshift(var2, 25)]
                        if(var3 != 0):
                            gameCanvas[var4] = (
                                var15 * (var3 & 65280) & 16711680) + ((var3 & 16711935) * var15 & -16711936) >> 8
                            annotationCanvas[var4] = objectID

                        var4 += 1
                        var2 += var16
                        var3 = var1[(var2 & 16256) +
                                    MathUtills.unsignedrshift(var2, 25)]
                        if(var3 != 0):
                            gameCanvas[var4] = (
                                var15 * (var3 & 65280) & 16711680) + ((var3 & 16711935) * var15 & -16711936) >> 8
                            annotationCanvas[var4] = objectID

                        var4 += 1
                        var2 += var16
                        var3 = var1[(var2 & 16256) +
                                    MathUtills.unsignedrshift(var2, 25)]
                        if(var3 != 0):
                            gameCanvas[var4] = (
                                var15 * (var3 & 65280) & 16711680) + ((var3 & 16711935) * var15 & -16711936) >> 8
                            annotationCanvas[var4] = objectID

                        var4 += 1
                        var2 += var16
                        var3 = var1[(var2 & 16256) +
                                    MathUtills.unsignedrshift(var2, 25)]
                        if(var3 != 0):
                            gameCanvas[var4] = (
                                var15 * (var3 & 65280) & 16711680) + ((var3 & 16711935) * var15 & -16711936) >> 8
                            annotationCanvas[var4] = objectID

                        var4 += 1
                        var2 += var16
                        var3 = var1[(var2 & 16256) +
                                    MathUtills.unsignedrshift(var2, 25)]
                        if(var3 != 0):
                            gameCanvas[var4] = (
                                var15 * (var3 & 65280) & 16711680) + ((var3 & 16711935) * var15 & -16711936) >> 8
                            annotationCanvas[var4] = objectID

                        var4 += 1
                        var2 += var16
                        var3 = var1[(var2 & 16256) +
                                    MathUtills.unsignedrshift(var2, 25)]
                        if(var3 != 0):
                            gameCanvas[var4] = (
                                var15 * (var3 & 65280) & 16711680) + ((var3 & 16711935) * var15 & -16711936) >> 8
                            annotationCanvas[var4] = objectID

                        var4 += 1
                        var18 = var20
                        var19 = var21
                        var9 += var12
                        var10 += var13
                        var11 += var14
                        var22 = var11 >> 14
                        if(var22 != 0):
                            var20 = integerdivide(var9, var22)
                            var21 = integerdivide(var10, var22)
                            if(var20 < 0):
                                var20 = 0
                            elif(var20 > 16256):
                                var20 = 16256

                        else:
                            var20 = 0
                            var21 = 0

                        var2 = (var18 << 18) + var19
                        var16 = (var21 - var19 >> 3) + \
                            (var20 - var18 >> 3 << 18)
                        var7 += var8
                        var15 = var7 >> 8
                        var17 -= 1

                        if var17 <= 0:  # while(var17 > 0)
                            break

                var17 = var6 - var5 & 7
                if(var17 > 0):
                    while (True):
                        var3 = var1[(var2 & 16256) +
                                    MathUtills.unsignedrshift(var2, 25)]
                        if(var3 != 0):
                            gameCanvas[var4] = (
                                var15 * (var3 & 65280) & 16711680) + ((var3 & 16711935) * var15 & -16711936) >> 8
                            annotationCanvas[var4] = objectID

                        var4 += 1
                        var2 += var16
                        var17 -= 1
                        if var17 <= 0:
                            break


@jit(nopython=True, cache=False)
def method2826(objectID, annotationCanvas, gameCanvas, var1, var2, var4, var5, rasterClipEnable, rasterClipX, rasterAlpha):
    if(rasterClipEnable):
        if(var5 > rasterClipX):
            var5 = rasterClipX

        if(var4 < 0):
            var4 = 0

    if(var4 < var5):
        var1 += var4
        var3 = var5 - var4 >> 2
        if(rasterAlpha != 0):
            if(rasterAlpha == 254):
                while(True):
                    var3 -= 1
                    if(var3 < 0):
                        var3 = var5 - var4 & 3

                        while(True):
                            var3 -= 1
                            if(var3 < 0):
                                return

                            gameCanvas[var1] = gameCanvas[var1]
                            annotationCanvas[var1] = objectID
                            var1 += 1

                    gameCanvas[var1] = gameCanvas[var1]
                    annotationCanvas[var1] = objectID
                    var1 += 1
                    gameCanvas[var1] = gameCanvas[var1]
                    annotationCanvas[var1] = objectID
                    var1 += 1
                    gameCanvas[var1] = gameCanvas[var1]
                    annotationCanvas[var1] = objectID
                    var1 += 1
                    gameCanvas[var1] = gameCanvas[var1]
                    annotationCanvas[var1] = objectID
                    var1 += 1

            else:
                var6 = rasterAlpha
                var7 = 256 - rasterAlpha
                var2 = (var7 * (var2 & 65280) >> 8 & 65280) + \
                    (var7 * (var2 & 16711935) >> 8 & 16711935)

                while(True):
                    var3 -= 1
                    if(var3 < 0):
                        var3 = var5 - var4 & 3

                        while(True):
                            var3 -= 1
                            if(var3 < 0):
                                return

                            var8 = gameCanvas[var1]
                            gameCanvas[var1] = ((var8 & 16711935) * var6 >> 8 & 16711935) + \
                                var2 + (var6 * (var8 & 65280) >> 8 & 65280)
                            annotationCanvas[var1] = objectID
                            var1 += 1

                    var8 = gameCanvas[var1]
                    gameCanvas[var1] = ((var8 & 16711935) * var6 >> 8 & 16711935) + \
                        var2 + (var6 * (var8 & 65280) >> 8 & 65280)
                    annotationCanvas[var1] = objectID
                    var1 += 1

                    var8 = gameCanvas[var1]
                    gameCanvas[var1] = ((var8 & 16711935) * var6 >> 8 & 16711935) + \
                        var2 + (var6 * (var8 & 65280) >> 8 & 65280)
                    annotationCanvas[var1] = objectID
                    var1 += 1

                    var8 = gameCanvas[var1]
                    gameCanvas[var1] = ((var8 & 16711935) * var6 >> 8 & 16711935) + \
                        var2 + (var6 * (var8 & 65280) >> 8 & 65280)
                    annotationCanvas[var1] = objectID
                    var1 += 1

                    var8 = gameCanvas[var1]
                    gameCanvas[var1] = ((var8 & 16711935) * var6 >> 8 & 16711935) + \
                        var2 + (var6 * (var8 & 65280) >> 8 & 65280)
                    annotationCanvas[var1] = objectID
                    var1 += 1

        else:
            while(True):
                var3 -= 1
                if(var3 < 0):
                    var3 = var5 - var4 & 3

                    while(True):
                        var3 -= 1
                        if(var3 < 0):
                            return

                        gameCanvas[var1] = var2
                        annotationCanvas[var1] = objectID
                        var1 += 1

                gameCanvas[var1] = var2
                annotationCanvas[var1] = objectID
                var1 += 1

                gameCanvas[var1] = var2
                annotationCanvas[var1] = objectID
                var1 += 1

                gameCanvas[var1] = var2
                annotationCanvas[var1] = objectID
                var1 += 1

                gameCanvas[var1] = var2
                annotationCanvas[var1] = objectID
                var1 += 1


@jit(nopython=True, cache=False)
def method2790(objectID, annotationCanvas, gameCanvas, var1, var4, var5, var6, var7,
               rasterClipEnable, rasterClipX, rasterGouraudLowRes, rasterAlpha, colorPalette):

    if(rasterClipEnable):
        if(var5 > rasterClipX):
            var5 = rasterClipX

        if(var4 < 0):
            var4 = 0

    if(var4 < var5):
        var1 += var4
        var6 = np.int32(var6 + var4 * var7)
        if(rasterGouraudLowRes):
            var3 = var5 - var4 >> 2
            var7 <<= 2
            var7 = np.int32(var7)
            if(rasterAlpha == 0):
                if(var3 > 0):

                    while (True):

                        var2 = colorPalette[var6 >> 8]
                        var6 += var7

                        if var1 >= len(gameCanvas):
                            print("out of range Graphics3D 1")
                            break

                        gameCanvas[var1] = var2
                        annotationCanvas[var1] = objectID
                        var1 += 1
                        gameCanvas[var1] = var2
                        annotationCanvas[var1] = objectID
                        var1 += 1
                        gameCanvas[var1] = var2
                        annotationCanvas[var1] = objectID
                        var1 += 1
                        gameCanvas[var1] = var2
                        annotationCanvas[var1] = objectID
                        var1 += 1
                        var3 -= 1

                        if var3 < 1:
                            break

                var3 = var5 - var4 & 3
                if(var3 > 0):
                    var2 = colorPalette[var6 >> 8]

                    while (True):

                        if var1 >= len(gameCanvas):
                            print("out of range Graphics3D 2")
                            break

                        gameCanvas[var1] = var2
                        annotationCanvas[var1] = objectID
                        var1 += 1
                        var3 -= 1

                        if var3 < 1:
                            break

            else:
                var8 = rasterAlpha
                var9 = 256 - rasterAlpha
                if(var3 > 0):

                    while (True):

                        if var1 >= len(gameCanvas):
                            print("out of range Graphics3D 3")
                            break

                        var2 = colorPalette[var6 >> 8]
                        var6 += var7
                        var2 = (var9 * (var2 & 65280) >> 8 & 65280) + \
                            (var9 * (var2 & 16711935) >> 8 & 16711935)
                        var10 = gameCanvas[var1]
                        gameCanvas[var1] = ((var10 & 16711935) * var8 >> 8 & 16711935) + \
                            var2 + (var8 * (var10 & 65280) >> 8 & 65280)
                        annotationCanvas[var1] = objectID
                        var1 += 1

                        var10 = gameCanvas[var1]
                        gameCanvas[var1] = ((var10 & 16711935) * var8 >> 8 & 16711935) + \
                            var2 + (var8 * (var10 & 65280) >> 8 & 65280)
                        annotationCanvas[var1] = objectID
                        var1 += 1
                        var10 = gameCanvas[var1]

                        gameCanvas[var1] = ((var10 & 16711935) * var8 >> 8 & 16711935) + \
                            var2 + (var8 * (var10 & 65280) >> 8 & 65280)
                        annotationCanvas[var1] = objectID
                        var1 += 1

                        var10 = gameCanvas[var1]
                        gameCanvas[var1] = ((var10 & 16711935) * var8 >> 8 & 16711935) + \
                            var2 + (var8 * (var10 & 65280) >> 8 & 65280)
                        annotationCanvas[var1] = objectID
                        var1 += 1

                        var3 -= 1

                        if var3 < 1:
                            break

                var3 = var5 - var4 & 3
                if(var3 > 0):
                    var2 = colorPalette[var6 >> 8]
                    var2 = (var9 * (var2 & 65280) >> 8 & 65280) + \
                        (var9 * (var2 & 16711935) >> 8 & 16711935)

                    while (True):
                        if var1 >= len(gameCanvas):
                            print("out of range Graphics3D 4")
                            break

                        var10 = gameCanvas[var1]
                        gameCanvas[var1] = ((var10 & 16711935) * var8 >> 8 & 16711935) + \
                            var2 + (var8 * (var10 & 65280) >> 8 & 65280)
                        annotationCanvas[var1] = objectID
                        var1 += 1
                        var3 -= 1
                        if var3 < 1:
                            break

        else:
            var3 = var5 - var4
            if(rasterAlpha == 0):

                while (True):

                    if var1 >= len(gameCanvas):
                        print("out of range Graphics3D 5")
                        break

                    gameCanvas[var1] = colorPalette[var6 >> 8]
                    annotationCanvas[var1] = objectID
                    var1 += 1
                    var6 += var7
                    var3 -= 1

                    if var3 < 1:
                        break

            else:
                var8 = rasterAlpha
                var9 = 256 - rasterAlpha

                while (True):
                    if var1 >= len(gameCanvas):
                        print("out of range Graphics3D 6")
                        break

                    var2 = colorPalette[var6 >> 8]
                    var6 += var7
                    var2 = (var9 * (var2 & 65280) >> 8 & 65280) + \
                        (var9 * (var2 & 16711935) >> 8 & 16711935)
                    var10 = gameCanvas[var1]
                    gameCanvas[var1] = ((var10 & 16711935) * var8 >> 8 & 16711935) + \
                        var2 + (var8 * (var10 & 65280) >> 8 & 65280)
                    annotationCanvas[var1] = objectID
                    var1 += 1
                    var3 -= 1
                    if var3 < 1:
                        break


# @jit(nopython=True, cache=False)
# def resetGraphics(graphics3d):

#     # Fill pixels with value 0
#     graphics3d.graphicsPixels.fill(0)
#     graphics3d.annotationCanvas.fill(0)

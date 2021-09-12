#from Renderable import Renderable
import numpy as np
import math
from MathUtills import integerdivide
from MathUtills import Graphics3DCOSINE, Graphics3DSINE
from logging import debug
from numba import jit
from numba import int32, float32, int8
from Buffer import Buffer
from numba.experimental import jitclass
from numba import int32, float32, boolean, short, int64
#from FaceNormal import FaceNormal
import numpy as np
import math
from MathUtills import integerdivide
import numba
from Graphics3D import method2798, method2799
from Graphics3D import rasterGouraud, rasterFlat, rasterTextureAffine
numpyarrayint32_type = numba.typeof(np.empty(shape=(0), dtype=np.int32))

@jitclass()
class staticModel:

    #field1856
    field1911 : int8[:] # = np.zeros(shape = (1,), dtype = np.byte)
    #field1850
    field1904 : int8[:] # = np.zeros(shape = (1,), dtype = np.byte)
    field1887 : boolean[:] # = np.zeros(shape = (4700,), dtype = np.bool8)
    field1848 : boolean[:] # = np.zeros(shape = (4700,), dtype = np.bool8)
    modelViewportYs : int32[:] # = np.zeros(shape = (4700,), dtype = np.int32)
    modelViewportXs : int32[:] # = np.zeros(shape = (4700,), dtype = np.int32)
    field1891 : int32[:] # = np.zeros(shape = (4700,), dtype = np.int32)
    yViewportBuffer : int32[:] # = np.zeros(shape = (4700,), dtype = np.int32)
    field1893 : int32[:] # = np.zeros(shape = (4700,), dtype = np.int32)
    field1894 : int32[:] # = np.zeros(shape = (4700,), dtype = np.int32)
    field1896 : int32[:] # = np.zeros(shape = (1600,), dtype = np.int32)
    field1860 : int32[:,:] # = np.zeros(shape = (1600, 512), dtype = np.int32)
    field1898 : int32[:] # = np.zeros(shape = (12,), dtype = np.int32)
    field1899 : int32[:,:] # = np.zeros(shape = (12, 2000), dtype = np.int32)
    field1900 : int32[:] # = np.zeros(shape = (2000), dtype = np.int32)
    field1895 : int32[:] # = np.zeros(shape = (2000), dtype = np.int32)
    field1901 : int32[:] # = np.zeros(shape = (12,), dtype = np.int32)
    field1903 : int32[:] # = np.zeros(shape = (10,), dtype = np.int32)
    field1875 : int32[:] # = np.zeros(shape = (10,), dtype = np.int32)
    xViewportBuffer : int32[:] # = np.zeros(shape = (10,), dtype = np.int32)
    useBoundingBoxes3D : boolean
    #Model_sine = Graphics3D.SINE
    #Model_cosine = Graphics3D.COSINE
    #field1914 = Graphics3D.colorPalette
    #field1915 = Graphics3D.field1952

    def __init__(self):
        
        #field1856
        self.field1911 = np.empty(shape=(1,), dtype=np.byte)
        #field1850
        self.field1904 = np.empty(shape=(1,), dtype=np.byte)
        self.field1887 = np.empty(shape=(4700,), dtype=np.bool8)
        self.field1848 = np.empty(shape=(4700,), dtype=np.bool8)


        self.modelViewportYs = np.empty(shape=(4700,), dtype=np.int32)
        self.modelViewportXs = np.empty(shape=(4700,), dtype=np.int32)
        self.field1891 = np.empty(shape=(4700,), dtype=np.int32)
        self.yViewportBuffer = np.empty(shape=(4700,), dtype=np.int32)

        self.field1893 = np.empty(shape=(4700,), dtype=np.int32)
        self.field1894 = np.empty(shape=(4700,), dtype=np.int32)
        self.field1896 = np.empty(shape=(1600,), dtype=np.int32)
        self.field1860 = np.empty(shape=(1600, 512), dtype=np.int32)
        self.field1898 = np.empty(shape=(12,), dtype=np.int32)
        self.field1899 = np.empty(shape=(12, 2000), dtype=np.int32)
        self.field1900 = np.empty(shape=(2000), dtype=np.int32)
        self.field1895 = np.empty(shape=(2000), dtype=np.int32)


        self.field1901 = np.empty(shape=(12,), dtype=np.int32)
        self.field1903 = np.empty(shape=(10,), dtype=np.int32)
        self.field1875 = np.empty(shape=(10,), dtype=np.int32)
        self.xViewportBuffer = np.empty(shape=(10,), dtype=np.int32)
        self.useBoundingBoxes3D = True

        #self.reset()

    def reset(self):
        self.field1911.fill(0)
        #field1850
        self.field1904.fill(0)
        self.field1887.fill(0)
        self.field1848.fill(0)

        self.modelViewportYs.fill(0)
        self.modelViewportXs.fill(0)
        self.field1891.fill(0)
        self.yViewportBuffer.fill(0)

        self.field1893.fill(0)
        self.field1894.fill(0)
        self.field1896.fill(0)
        self.field1860.fill(0)
        self.field1898.fill(0)
        self.field1899.fill(0)
        self.field1900.fill(0)
        self.field1895.fill(0)


        self.field1901.fill(0)
        self.field1903.fill(0)
        self.field1875.fill(0)
        self.xViewportBuffer.fill(0)
        self.useBoundingBoxes3D = True


@jitclass()
class Model:

    id : int32
    objectID : int32

    verticesCount : int32
    verticesX : int32[:]
    verticesY : int32[:]
    verticesZ  : int32[:]
    indicesCount : int32
    indices1  : int32[:]
    indices2  : int32[:]
    indices3  : int32[:]
    field1852  : int32[:]
    field1861  : int32[:]
    field1862  : int32[:]
    faceRenderPriorities  : int8[:]
    faceAplhas  : int8[:]
    field1865  : int8[:]
    faceTextures  : short[:]
    priority : int8
    field1866 : int32
    field1869  : int32[:]
    field1868  : int32[:]
    field1871  : int32[:]
    #vertexGroups  : int32[:,:]
    #field1890  : int32[:,:]
    field1874 : boolean
    boundsType  : int32
    bottomY  : int32
    XYZMag  : int32
    diameter  : int32
    radius  : int32
    centerX  : int32
    centerY  : int32
    centerZ  : int32
    extremeX : int32
    extremeY : int32
    extremeZ : int32
    modelHeight : int32

    vertexGroups: numba.types.ListType(numpyarrayint32_type)  # int32[:]
    field1890: numba.types.ListType(numpyarrayint32_type)  # int32[:]

    
    
    # model_.model_sine  : int32 # = Graphics3D_.SINE
    # model_.Model_cosine  : int32 # = Graphics3D_.COSINE
    # model_.field1914  : int32 # = Graphics3D_.colorPalette
    # model_.field1915  : int32 # = Graphics3D_.field1952

    #model_.Graphics3D_ = Graphics3D_

    def __init__(self, id, objectID):

        self.id = id
        self.objectID = objectID

        self.vertexGroups = numba.typed.List.empty_list(numpyarrayint32_type)
        self.field1890 = numba.typed.List.empty_list(numpyarrayint32_type)




# public Model(final Model[] var1, var2) :
# modelself.verticesCount = 0
# modelself.indicesCount = 0
# modelself.priority = 0
# modelself.field1866 = 0
# modelself.field1874 = False
# modelself.extremeX = -1
# modelself.extremeY = -1
# modelself.extremeZ = -1
# boolean var3 = False
# boolean var4 = False
# boolean var5 = False
# boolean var6 = False
# modelself.verticesCount = 0
# modelself.indicesCount = 0
# modelself.field1866 = 0
# modelself.priority = -1

# var7
# Model var8
# for(var7 = 0 var7 < var2 ++var7) :
# var8 = var1[var7]
# if(var8 is not None) :
# modelself.verticesCount += var8.verticesCount
# modelself.indicesCount += var8.indicesCount
# modelself.field1866 += var8.field1866
# if(var8.faceRenderPriorities is not None) :
# var3 = True
# else :
# if(modelself.priority == -1) :
# modelself.priority = var8.priority


# if(modelself.priority != var8.priority) :
# var3 = True


# var4 |= var8.faceAplhas is not None
# var5 |= var8.faceTextures is not None
# var6 |= var8.field1865 is not None


# modelself.verticesX = new int[modelself.verticesCount]
# modelself.verticesY = new int[modelself.verticesCount]
# modelself.verticesZ = new int[modelself.verticesCount]
# modelself.indices1 = new int[modelself.indicesCount]
# modelself.indices2 = new int[modelself.indicesCount]
# modelself.indices3 = new int[modelself.indicesCount]
# modelself.field1852 = new int[modelself.indicesCount]
# modelself.field1861 = new int[modelself.indicesCount]
# modelself.field1862 = new int[modelself.indicesCount]
# if(var3) :
# modelself.faceRenderPriorities = new byte[modelself.indicesCount]


# if(var4) :
# modelself.faceAplhas = new byte[modelself.indicesCount]


# if(var5) :
# modelself.faceTextures = new short[modelself.indicesCount]


# if(var6) :
# modelself.field1865 = new byte[modelself.indicesCount]


# if(modelself.field1866 > 0) :
# modelself.field1869 = new int[modelself.field1866]
# modelself.field1868 = new int[modelself.field1866]
# modelself.field1871 = new int[modelself.field1866]


# modelself.verticesCount = 0
# modelself.indicesCount = 0
# modelself.field1866 = 0

# for(var7 = 0 var7 < var2 ++var7) :
# var8 = var1[var7]
# if(var8 is not None) :
# var9
# for(var9 = 0 var9 < var8.indicesCount ++var9) :
# modelself.indices1[modelself.indicesCount] = modelself.verticesCount + var8.indices1[var9]
# modelself.indices2[modelself.indicesCount] = modelself.verticesCount + var8.indices2[var9]
# modelself.indices3[modelself.indicesCount] = modelself.verticesCount + var8.indices3[var9]
# modelself.field1852[modelself.indicesCount] = var8.field1852[var9]
# modelself.field1861[modelself.indicesCount] = var8.field1861[var9]
# modelself.field1862[modelself.indicesCount] = var8.field1862[var9]
# if(var3) :
# if(var8.faceRenderPriorities is not None) :
# modelself.faceRenderPriorities[modelself.indicesCount] = var8.faceRenderPriorities[var9]
# else :
# modelself.faceRenderPriorities[modelself.indicesCount] = var8.priority


# if(var4 and var8.faceAplhas is not None) :
# modelself.faceAplhas[modelself.indicesCount] = var8.faceAplhas[var9]


# if(var5) :
# if(var8.faceTextures is not None) :
# modelself.faceTextures[modelself.indicesCount] = var8.faceTextures[var9]
# else :
# modelself.faceTextures[modelself.indicesCount] = -1


# if(var6) :
# if(var8.field1865 is not None and var8.field1865[var9] != -1) :
# modelself.field1865[modelself.indicesCount] = (byte)(modelself.field1866 + var8.field1865[var9])
# else :
# modelself.field1865[modelself.indicesCount] = -1


# ++modelself.indicesCount


# for(var9 = 0 var9 < var8.field1866 ++var9) :
# modelself.field1869[modelself.field1866] = modelself.verticesCount + var8.field1869[var9]
# modelself.field1868[modelself.field1866] = modelself.verticesCount + var8.field1868[var9]
# modelself.field1871[modelself.field1866] = modelself.verticesCount + var8.field1871[var9]
# ++modelself.field1866


# for(var9 = 0 var9 < var8.verticesCount ++var9) :
# modelself.verticesX[modelself.verticesCount] = var8.verticesX[var9]
# modelself.verticesY[modelself.verticesCount] = var8.verticesY[var9]
# modelself.verticesZ[modelself.verticesCount] = var8.verticesZ[var9]
# ++modelself.verticesCount


# public static boolean boundingBox3DContainsMouse(final Model model, var1, var2, var3) :
# if(!IndexStoreActionHandler.method4629()) :
# return False
# else :
# class33.method408()
# centerX = model.centerX + var1
# centerY = var2 + model.centerY
# centerZ = var3 + model.centerZ
# extremeX = model.extremeX
# extremeY = model.extremeY
# extremeZ = model.extremeZ
# var10 = modelself.class132_.field1919 - centerX
# var11 = modelself.class132_.field1923 - centerY
# var12 = modelself.class132_.field1924 - centerZ
# return Math.abs(var10) <= extremeX + class20.field336 and (Math.abs(var11) <= extremeY + modelself.class132_.field1926 and (Math.abs(var12) <= extremeZ + IndexStoreActionHandler.field3399 and (Math.abs(var12 * class37.field502 - var11 * Resampler.field1629) <= extremeY * IndexStoreActionHandler.field3399 + extremeZ * modelself.class132_.field1926 and (Math.abs(var10 * Resampler.field1629 - var12 * modelself.class132_.field1925) <= extremeX * IndexStoreActionHandler.field3399 + extremeZ * class20.field336 and Math.abs(var11 * modelself.class132_.field1925 - var10 * class37.field502) <= extremeX * modelself.class132_.field1926 + extremeY * class20.field336))))


# static getViewportMouseY() :
# return modelself.class132_.Viewport_mouseY

# werk

@jit(nopython=True, cache=False)
def method2686(modelself, var1, var2, var3, var4, var5, var6):
    calculateBoundsCylinder(modelself)
    var7 = var2 - modelself.XYZMag
    var8 = var2 + modelself.XYZMag
    var9 = var4 - modelself.XYZMag
    var10 = var4 + modelself.XYZMag
    if(var7 >= 0 and var8 + 128 >> 7 < len(var1) and var9 >= 0 and var10 + 128 >> 7 < len(var1[0])):
        var7 >>= 7
        var8 = var8 + 127 >> 7
        var9 >>= 7
        var10 = var10 + 127 >> 7
        if(var3 == var1[var7][var9] and var3 == var1[var8][var9] and var3 == var1[var7][var10] and var3 == var1[var8][var10]):
            return modelself
        else:
            if var5:
                var11 = Model(modelself.id, modelself.objectID)
                var11.verticesCount = modelself.verticesCount
                var11.indicesCount = modelself.indicesCount
                var11.field1866 = modelself.field1866
                var11.verticesX = modelself.verticesX
                var11.verticesZ = modelself.verticesZ
                var11.indices1 = modelself.indices1
                var11.indices2 = modelself.indices2
                var11.indices3 = modelself.indices3
                var11.field1852 = modelself.field1852
                var11.field1861 = modelself.field1861
                var11.field1862 = modelself.field1862
                var11.faceRenderPriorities = modelself.faceRenderPriorities
                var11.faceAplhas = modelself.faceAplhas
                var11.field1865 = modelself.field1865
                var11.faceTextures = modelself.faceTextures
                var11.priority = modelself.priority
                var11.field1869 = modelself.field1869
                var11.field1868 = modelself.field1868
                var11.field1871 = modelself.field1871
                var11.vertexGroups = modelself.vertexGroups
                var11.field1890 = modelself.field1890
                var11.field1874 = modelself.field1874
                # new int[var11.verticesCount]
                var11.verticesY = np.zeros(
                    shape=(var11.verticesCount), dtype=np.int32)
            else:
                var11 = modelself

            if(var6 == 0):
                for var12 in range(0, var11.verticesCount):
                    var13 = var2 + modelself.verticesX[var12]
                    var14 = var4 + modelself.verticesZ[var12]
                    var15 = var13 & 127
                    var16 = var14 & 127
                    var17 = var13 >> 7
                    var18 = var14 >> 7
                    var19 = var1[var17][var18] * \
                        (128 - var15) + var1[var17 + 1][var18] * var15 >> 7
                    var20 = var1[var17][var18 + 1] * \
                        (128 - var15) + var15 * \
                        var1[var17 + 1][var18 + 1] >> 7
                    var21 = var19 * (128 - var16) + var20 * var16 >> 7
                    var11.verticesY[var12] = var21 + \
                        modelself.verticesY[var12] - var3
            else:
                for var12 in range(0, var11.verticesCount):
                    var13 = integerdivide(
                        (-modelself.verticesY[var12] << 16), modelself.modelHeight)
                    if(var13 < var6):
                        var14 = var2 + modelself.verticesX[var12]
                        var15 = var4 + modelself.verticesZ[var12]
                        var16 = var14 & 127
                        var17 = var15 & 127
                        var18 = var14 >> 7
                        var19 = var15 >> 7
                        var20 = var1[var18][var19] * \
                            (128 - var16) + \
                            var1[var18 + 1][var19] * var16 >> 7
                        var21 = var1[var18][var19 + 1] * \
                            (128 - var16) + var16 * \
                            var1[var18 + 1][var19 + 1] >> 7
                        var22 = var20 * (128 - var17) + var21 * var17 >> 7
                        var11.verticesY[var12] = integerdivide(
                            (var6 - var13) * (var22 - var3), var6) + modelself.verticesY[var12]

            resetBounds(var11)
            return var11

    else:
        return modelself


# public Model toSharedModel(final boolean var1) :
# if(!var1 and field1911.length < modelself.indicesCount) :
# field1911 = new byte[modelself.indicesCount + 100]


# return modelself.method2689(var1, field1856, field1911)


# public Model toSharedSpotAnimModel(final boolean var1) :
# if(!var1 and field1904.length < modelself.indicesCount) :
# field1904 = new byte[modelself.indicesCount + 100]


# return modelself.method2689(var1, field1850, field1904)


# private Model method2689(final boolean var1, final Model var2, final byte[] var3) :
# var2.verticesCount = modelself.verticesCount
# var2.indicesCount = modelself.indicesCount
# var2.field1866 = modelself.field1866
# if(var2.verticesX is None or var2.verticesX.length < modelself.verticesCount) :
# var2.verticesX = new int[modelself.verticesCount + 100]
# var2.verticesY = new int[modelself.verticesCount + 100]
# var2.verticesZ = new int[modelself.verticesCount + 100]


# var4
# for(var4 = 0 var4 < modelself.verticesCount ++var4) :
# var2.verticesX[var4] = modelself.verticesX[var4]
# var2.verticesY[var4] = modelself.verticesY[var4]
# var2.verticesZ[var4] = modelself.verticesZ[var4]


# if(var1) :
# var2.faceAplhas = modelself.faceAplhas
# else :
# var2.faceAplhas = var3
# if(modelself.faceAplhas is None) :
# for(var4 = 0 var4 < modelself.indicesCount ++var4) :
# var2.faceAplhas[var4] = 0

# else :
# for(var4 = 0 var4 < modelself.indicesCount ++var4) :
# var2.faceAplhas[var4] = modelself.faceAplhas[var4]


# var2.indices1 = modelself.indices1
# var2.indices2 = modelself.indices2
# var2.indices3 = modelself.indices3
# var2.field1852 = modelself.field1852
# var2.field1861 = modelself.field1861
# var2.field1862 = modelself.field1862
# var2.faceRenderPriorities = modelself.faceRenderPriorities
# var2.field1865 = modelself.field1865
# var2.faceTextures = modelself.faceTextures
# var2.priority = modelself.priority
# var2.field1869 = modelself.field1869
# var2.field1868 = modelself.field1868
# var2.field1871 = modelself.field1871
# var2.vertexGroups = modelself.vertexGroups
# var2.field1890 = modelself.field1890
# var2.field1874 = modelself.field1874
# var2.resetBounds()
# return var2

@jit(nopython=True, cache=False)
def method2690(modelself, var1):
    if(modelself.extremeX == -1):
        var2 = 0
        var3 = 0
        var4 = 0
        var5 = 0
        var6 = 0
        var7 = 0
        var8 = Graphics3DCOSINE(var1)  # Graphics3D_.COSINE[var1]
        var9 = Graphics3DSINE(var1)  # Graphics3D_.SINE[var1]

        for var10 in range(0, modelself.verticesCount):
            var11 = method2798(
                modelself.verticesX[var10], modelself.verticesZ[var10], var8, var9)
            var12 = modelself.verticesY[var10]
            var13 = method2799(
                modelself.verticesX[var10], modelself.verticesZ[var10], var8, var9)
            if(var11 < var2):
                var2 = var11

            if(var11 > var5):
                var5 = var11

            if(var12 < var3):
                var3 = var12

            if(var12 > var6):
                var6 = var12

            if(var13 < var4):
                var4 = var13

            if(var13 > var7):
                var7 = var13

        modelself.centerX = integerdivide((var5 + var2), 2)
        modelself.centerY = integerdivide((var6 + var3), 2)
        modelself.centerZ = integerdivide((var7 + var4), 2)
        modelself.extremeX = integerdivide((var5 - var2 + 1), 2)
        modelself.extremeY = integerdivide((var6 - var3 + 1), 2)
        modelself.extremeZ = integerdivide((var7 - var4 + 1), 2)
        if(modelself.extremeX < 32):
            modelself.extremeX = 32

        if(modelself.extremeZ < 32):
            modelself.extremeZ = 32

        if(modelself.field1874):
            modelself.extremeX += 8
            modelself.extremeZ += 8

@jit(nopython=True, cache=False)
def calculateBoundsCylinder(modelself):
    if(modelself.boundsType != 1):

        modelself.boundsType = 1
        modelself.modelHeight = 0
        modelself.bottomY = 0
        modelself.XYZMag = 0

        for var1 in range(0, modelself.verticesCount):
            var2 = modelself.verticesX[var1]
            var3 = modelself.verticesY[var1]
            var4 = modelself.verticesZ[var1]
            if(-var3 > modelself.modelHeight):
                modelself.modelHeight = -var3

            if(var3 > modelself.bottomY):
                modelself.bottomY = var3

            var5 = var2 * var2 + var4 * var4
            if(var5 > modelself.XYZMag):
                modelself.XYZMag = var5

        modelself.XYZMag = np.int32(math.sqrt(modelself.XYZMag) + 0.99)
        modelself.radius = np.int32(math.sqrt(
            (modelself.XYZMag * modelself.XYZMag + modelself.modelHeight * modelself.modelHeight)) + 0.99)
        modelself.diameter = modelself.radius + \
            np.int32(math.sqrt((modelself.XYZMag * modelself.XYZMag +
                        modelself.bottomY * modelself.bottomY)) + 0.99)

@jit(nopython=True, cache=False)
def method2692(modelself):
    if(modelself.boundsType != 2):
        modelself.boundsType = 2
        modelself.XYZMag = 0

        for var1 in range(0, modelself.verticesCount):
            var2 = modelself.verticesX[var1]
            var3 = modelself.verticesY[var1]
            var4 = modelself.verticesZ[var1]
            var5 = var2 * var2 + var4 * var4 + var3 * var3
            if(var5 > modelself.XYZMag):
                modelself.XYZMag = var5

        modelself.XYZMag = np.int32(math.sqrt(modelself.XYZMag) + 0.99)
        modelself.radius = modelself.XYZMag
        modelself.diameter = modelself.XYZMag + modelself.XYZMag

@jit(nopython=True, cache=False)
def method2693(modelself):
    calculateBoundsCylinder(modelself)
    return modelself.XYZMag

@jit(nopython=True, cache=False)
def resetBounds(modelself):
    modelself.boundsType = 0
    modelself.extremeX = -1

def method2695(modelself, var1, var2):

    raise Exception("Not Implemented")

    if(len(modelself.vertexGroups) > 0): # is not None):
        if(var2 != -1):
            var3 = var1.skeletons[var2]
            var4 = var3.skin
            modelself.animOffsetX = 0
            modelself.animOffsetY = 0
            modelself.animOffsetZ = 0

            for var5 in range(0, var3.transformCount):
                var6 = var3.transformTypes[var5]
                modelself.animate(var4.types[var6], var4.list[var6], var3.translator_x[var5],
                                var3.translator_y[var5], var3.translator_z[var5])

            modelself.resetBounds()


# public void method2745(final Frames var1, var2, final Frames var3, var4, final int[] var5) :
# if(var2 != -1) :
# if(var5 is not None and var4 != -1) :
# final Frame var6 = var1.skeletons[var2]
# final Frame var7 = var3.skeletons[var4]
# final FrameMap var8 = var6.skin
# animOffsetX = 0
# animOffsetY = 0
# animOffsetZ = 0
# byte var9 = 0
# var13 = var9 + 1
# var10 = var5[var9]

# var11
# var12
# for(var11 = 0 var11 < var6.transformCount ++var11) :
# for(var12 = var6.transformTypes[var11] var12 > var10 var10 = var5[var13++]) :


# if(var12 != var10 or var8.types[var12] == 0) :
# modelself.animate(var8.types[var12], var8.list[var12], var6.translator_x[var11], var6.translator_y[var11], var6.translator_z[var11])


# animOffsetX = 0
# animOffsetY = 0
# animOffsetZ = 0
# var9 = 0
# var13 = var9 + 1
# var10 = var5[var9]

# for(var11 = 0 var11 < var7.transformCount ++var11) :
# for(var12 = var7.transformTypes[var11] var12 > var10 var10 = var5[var13++]) :


# if(var12 == var10 or var8.types[var12] == 0) :
# modelself.animate(var8.types[var12], var8.list[var12], var7.translator_x[var11], var7.translator_y[var11], var7.translator_z[var11])


# modelself.resetBounds()
# else :
# modelself.method2695(var1, var2)


# private void animate(var1, final int[] var2, var3, var4, var5) :
# var6 = var2.length
# var7
# var8
# var11
# var12
# if(var1 == 0) :
# var7 = 0
# animOffsetX = 0
# animOffsetY = 0
# animOffsetZ = 0

# for(var8 = 0 var8 < var6 ++var8) :
# var9 = var2[var8]
# if(var9 < modelself.vertexGroups.length) :
# final int[] var10 = modelself.vertexGroups[var9]

# for(var11 = 0 var11 < var10.length ++var11) :
# var12 = var10[var11]
# animOffsetX += modelself.verticesX[var12]
# animOffsetY += modelself.verticesY[var12]
# animOffsetZ += modelself.verticesZ[var12]
# ++var7


# if(var7 > 0) :
# animOffsetX = var3 + integerdivide(animOffsetX, var7)
# animOffsetY = var4 + integerdivide(animOffsetY, var7)
# animOffsetZ = var5 + integerdivide(animOffsetZ, var7)
# else :
# animOffsetX = var3
# animOffsetY = var4
# animOffsetZ = var5


# else :
# int[] var18
# var19
# if(var1 == 1) :
# for(var7 = 0 var7 < var6 ++var7) :
# var8 = var2[var7]
# if(var8 < modelself.vertexGroups.length) :
# var18 = modelself.vertexGroups[var8]

# for(var19 = 0 var19 < var18.length ++var19) :
# var11 = var18[var19]
# modelself.verticesX[var11] += var3
# modelself.verticesY[var11] += var4
# modelself.verticesZ[var11] += var5


# elif(var1 == 2) :
# for(var7 = 0 var7 < var6 ++var7) :
# var8 = var2[var7]
# if(var8 < modelself.vertexGroups.length) :
# var18 = modelself.vertexGroups[var8]

# for(var19 = 0 var19 < var18.length ++var19) :
# var11 = var18[var19]
# modelself.verticesX[var11] -= animOffsetX
# modelself.verticesY[var11] -= animOffsetY
# modelself.verticesZ[var11] -= animOffsetZ
# var12 = (var3 & 255) * 8
# var13 = (var4 & 255) * 8
# var14 = (var5 & 255) * 8
# var15
# var16
# var17
# if(var14 != 0) :
# var15 = Model_sine[var14]
# var16 = Model_cosine[var14]
# var17 = var15 * modelself.verticesY[var11] + var16 * modelself.verticesX[var11] >> 16
# modelself.verticesY[var11] = var16 * modelself.verticesY[var11] - var15 * modelself.verticesX[var11] >> 16
# modelself.verticesX[var11] = var17


# if(var12 != 0) :
# var15 = Model_sine[var12]
# var16 = Model_cosine[var12]
# var17 = var16 * modelself.verticesY[var11] - var15 * modelself.verticesZ[var11] >> 16
# modelself.verticesZ[var11] = var15 * modelself.verticesY[var11] + var16 * modelself.verticesZ[var11] >> 16
# modelself.verticesY[var11] = var17


# if(var13 != 0) :
# var15 = Model_sine[var13]
# var16 = Model_cosine[var13]
# var17 = var15 * modelself.verticesZ[var11] + var16 * modelself.verticesX[var11] >> 16
# modelself.verticesZ[var11] = var16 * modelself.verticesZ[var11] - var15 * modelself.verticesX[var11] >> 16
# modelself.verticesX[var11] = var17


# modelself.verticesX[var11] += animOffsetX
# modelself.verticesY[var11] += animOffsetY
# modelself.verticesZ[var11] += animOffsetZ


# elif(var1 == 3) :
# for(var7 = 0 var7 < var6 ++var7) :
# var8 = var2[var7]
# if(var8 < modelself.vertexGroups.length) :
# var18 = modelself.vertexGroups[var8]

# for(var19 = 0 var19 < var18.length ++var19) :
# var11 = var18[var19]
# modelself.verticesX[var11] -= animOffsetX
# modelself.verticesY[var11] -= animOffsetY
# modelself.verticesZ[var11] -= animOffsetZ
# modelself.verticesX[var11] = integerdivide(var3 * modelself.verticesX[var11], 128)
# modelself.verticesY[var11] = integerdivide(var4 * modelself.verticesY[var11], 128)
# modelself.verticesZ[var11] = integerdivide(var5 * modelself.verticesZ[var11], 128)
# modelself.verticesX[var11] += animOffsetX
# modelself.verticesY[var11] += animOffsetY
# modelself.verticesZ[var11] += animOffsetZ


# elif(var1 == 5) :
# if(modelself.field1890 is not None and modelself.faceAplhas is not None) :
# for(var7 = 0 var7 < var6 ++var7) :
# var8 = var2[var7]
# if(var8 < modelself.field1890.length) :
# var18 = modelself.field1890[var8]

# for(var19 = 0 var19 < var18.length ++var19) :
# var11 = var18[var19]
# var12 = (modelself.faceAplhas[var11] & 255) + var3 * 8
# if(var12 < 0) :
# var12 = 0
# elif(var12 > 255) :
# var12 = 255


# modelself.faceAplhas[var11] = (byte)var12


# public void rotateY90Ccw() :
# for(var1 = 0 var1 < modelself.verticesCount ++var1) :
# var2 = modelself.verticesX[var1]
# modelself.verticesX[var1] = modelself.verticesZ[var1]
# modelself.verticesZ[var1] = -var2


# modelself.resetBounds()


# public void rotateY180Ccw() :
# for(var1 = 0 var1 < modelself.verticesCount ++var1) :
# modelself.verticesX[var1] = -modelself.verticesX[var1]
# modelself.verticesZ[var1] = -modelself.verticesZ[var1]


# modelself.resetBounds()


# public void rotateY270Ccw() :
# for(var1 = 0 var1 < modelself.verticesCount ++var1) :
# var2 = modelself.verticesZ[var1]
# modelself.verticesZ[var1] = modelself.verticesX[var1]
# modelself.verticesX[var1] = -var2


# modelself.resetBounds()


# public void rotateZ(var1) :
# var2 = Model_sine[var1]
# var3 = Model_cosine[var1]

# for(var4 = 0 var4 < modelself.verticesCount ++var4) :
# var5 = var3 * modelself.verticesY[var4] - var2 * modelself.verticesZ[var4] >> 16
# modelself.verticesZ[var4] = var2 * modelself.verticesY[var4] + var3 * modelself.verticesZ[var4] >> 16
# modelself.verticesY[var4] = var5


# modelself.resetBounds()


# public void offsetBy(var1, var2, var3) :
# for(var4 = 0 var4 < modelself.verticesCount ++var4) :
# modelself.verticesX[var4] += var1
# modelself.verticesY[var4] += var2
# modelself.verticesZ[var4] += var3


# modelself.resetBounds()


# public void scale(var1, var2, var3) :
# for(var4 = 0 var4 < modelself.verticesCount ++var4) :
# modelself.verticesX[var4] = integerdivide(modelself.verticesX[var4] * var1, 128)
# modelself.verticesY[var4] = integerdivide(var2 * modelself.verticesY[var4], 128)
# modelself.verticesZ[var4] = integerdivide(var3 * modelself.verticesZ[var4], 128)


# modelself.resetBounds()

# def method2734(modelself, var1, var2, var3, var4, var5, var6, var7, Graphics3D_, textures) :
#     staticModel_.field1896[0] = -1
#     if(modelself.boundsType != 2 and modelself.boundsType != 1) :
#         modelself.method2692()

#     var8 = Graphics3D_.centerX
#     var9 = Graphics3D_.centerY
#     var10 = Graphics3DSINE(var1) #Graphics3D_.SINE[var1]
#     var11 = Graphics3DCOSINE(var1) #Graphics3D_.COSINE[var1]
#     var12 = Graphics3DSINE(var2) #Graphics3D_.SINE[var2]
#     var13 = Graphics3DCOSINE(var2) #Graphics3D_.COSINE[var2]
#     var14 = Graphics3DSINE(var3) #Graphics3D_.SINE[var3]
#     var15 = Graphics3DCOSINE(var3) #Graphics3D_.COSINE[var3]
#     var16 = Graphics3DSINE(var4) #Graphics3D_.SINE[var4]
#     var17 = Graphics3DCOSINE(var4) #Graphics3D_.COSINE[var4]
#     var18 = var16 * var6 + var17 * var7 >> 16

#     for var19 in range(0, modelself.verticesCount):
#         var20 = modelself.verticesX[var19]
#         var21 = modelself.verticesY[var19]
#         var22 = modelself.verticesZ[var19]
#         if(var3 != 0) :
#             var23 = var21 * var14 + var20 * var15 >> 16
#             var21 = var21 * var15 - var20 * var14 >> 16
#             var20 = var23

#         if(var1 != 0) :
#             var23 = var21 * var11 - var22 * var10 >> 16
#             var22 = var21 * var10 + var22 * var11 >> 16
#             var21 = var23

#         if(var2 != 0) :
#             var23 = var22 * var12 + var20 * var13 >> 16
#             var22 = var22 * var13 - var20 * var12 >> 16
#             var20 = var23

#         var20 += var5
#         var21 += var6
#         var22 += var7
#         var23 = var21 * var17 - var22 * var16 >> 16
#         var22 = var21 * var16 + var22 * var17 >> 16
#         staticModel_.field1891[var19] = var22 - var18
#         modelself.modelViewportYs[var19] = integerdivide(var20 * Graphics3D_.Rasterizer3D_zoom, var22) + var8
#         staticModel_.modelViewportXs[var19] = integerdivide(var23 * Graphics3D_.Rasterizer3D_zoom, var22) + var9
#         if(modelself.field1866 > 0) :
#             staticModel_.yViewportBuffer[var19] = var20
#             staticModel_.field1893[var19] = var23
#             staticModel_.field1894[var19] = var22

#     modelself.method2707(False, False, False, 0, Graphics3D_, textures)

# def method2748(modelself, var1, var2, var3, var4, var5, var6, var7, var8, Graphics3D_, textures) :
#     staticModel_.field1896[0] = -1
#     if(modelself.boundsType != 2 and modelself.boundsType != 1) :
#         modelself.method2692()

#     var9 = Graphics3D_.centerX
#     var10 = Graphics3D_.centerY
#     var11 = Graphics3DSINE(var1) #Graphics3D_.SINE[var1]
#     var12 = Graphics3DCOSINE(var1) #Graphics3D_.COSINE[var1]
#     var13 = Graphics3DSINE(var2) #Graphics3D_.SINE[var2]
#     var14 = Graphics3DCOSINE(var2) #Graphics3D_.COSINE[var2]
#     var15 = Graphics3DSINE(var3) #Graphics3D_.SINE[var3]
#     var16 = Graphics3DCOSINE(var3) #Graphics3D_.COSINE[var3]
#     var17 = Graphics3DSINE(var4) #Graphics3D_.SINE[var4]
#     var18 = Graphics3DCOSINE(var4) #Graphics3D_.COSINE[var4]
#     var19 = var17 * var6 + var18 * var7 >> 16

#     for var20 in range(0, modelself.verticesCount):
#         var21 = modelself.verticesX[var20]
#         var22 = modelself.verticesY[var20]
#         var23 = modelself.verticesZ[var20]
#         if(var3 != 0) :
#             var24 = var22 * var15 + var21 * var16 >> 16
#             var22 = var22 * var16 - var21 * var15 >> 16
#             var21 = var24

#         if(var1 != 0) :
#             var24 = var22 * var12 - var23 * var11 >> 16
#             var23 = var22 * var11 + var23 * var12 >> 16
#             var22 = var24

#         if(var2 != 0) :
#             var24 = var23 * var13 + var21 * var14 >> 16
#             var23 = var23 * var14 - var21 * var13 >> 16
#             var21 = var24

#         var21 += var5
#         var22 += var6
#         var23 += var7
#         var24 = var22 * var18 - var23 * var17 >> 16
#         var23 = var22 * var17 + var23 * var18 >> 16
#         staticModel_.field1891[var20] = var23 - var19
#         modelself.modelViewportYs[var20] = var9 + integerdivide(var21 * Graphics3D_.Rasterizer3D_zoom, var8)
#         staticModel_.modelViewportXs[var20] = var10 + integerdivide(var24 * Graphics3D_.Rasterizer3D_zoom, var8)
#         if(modelself.field1866 > 0) :
#             staticModel_.yViewportBuffer[var20] = var21
#             staticModel_.field1893[var20] = var24
#             staticModel_.field1894[var20] = var23

#     modelself.method2707(False, False, False, 0, Graphics3D_, textures)


@jit(nopython=True, cache=False)
def method2707(colorPalette, staticModel_, modelself, var1, var2, var3, var4, Graphics3D_, textures):

    #diameter == maxDepth
    if(modelself.diameter >= 1600):
        return

    for var5 in range(0, modelself.diameter):
        staticModel_.field1896[var5] = 0

    # var5 = var3?20:5
    if var3 is True:
        var5 = 20
    else:
        var5 = 5

    # if(modelself.class7_.drawObjectGeometry2D and var2) :
    #     print("Ignoring this Model.py")
    #     #WorldMapData.method398(modelself, var5)


    for var6 in range(0, modelself.indicesCount):
        if(modelself.field1862[var6] != -2):
            var7 = modelself.indices1[var6]
            var8 = modelself.indices2[var6]
            var9 = modelself.indices3[var6]
            var10 = staticModel_.modelViewportYs[var7]
            var11 = staticModel_.modelViewportYs[var8]
            var12 = staticModel_.modelViewportYs[var9]
            if(var1 and (var10 == -5000 or var11 == -5000 or var12 == -5000)):
                var31 = staticModel_.yViewportBuffer[var7]
                var14 = staticModel_.yViewportBuffer[var8]
                var15 = staticModel_.yViewportBuffer[var9]
                var16 = staticModel_.field1893[var7]
                var17 = staticModel_.field1893[var8]
                var18 = staticModel_.field1893[var9]
                var19 = staticModel_.field1894[var7]
                var20 = staticModel_.field1894[var8]
                var21 = staticModel_.field1894[var9]
                var31 -= var14
                var15 -= var14
                var16 -= var17
                var18 -= var17
                var19 -= var20
                var21 -= var20
                var22 = var16 * var21 - var19 * var18
                var23 = var19 * var15 - var31 * var21
                var24 = var31 * var18 - var16 * var15
                if(var14 * var22 + var17 * var23 + var20 * var24 > 0):
                    staticModel_.field1848[var6] = True
                    var25 = integerdivide(
                        staticModel_.field1891[var7] + staticModel_.field1891[var8] + staticModel_.field1891[var9], 3) + modelself.radius
                    staticModel_.field1860[var25][staticModel_.field1896[var25]] = var6
                    staticModel_.field1896[var25] += 1

            else:
                if(var2):
                    var14 = staticModel_.modelViewportXs[var7]
                    var15 = staticModel_.modelViewportXs[var8]
                    var16 = staticModel_.modelViewportXs[var9]
                    # var17 = var5 + modelself.class132_.Viewport_mouseY
                    # if(var17 < var14 and var17 < var15 and var17 < var16) :
                    #     var13 = False
                    # else :
                    #     var17 = modelself.class132_.Viewport_mouseY - var5
                    #     if(var17 > var14 and var17 > var15 and var17 > var16) :
                    #         var13 = False
                    #     else :
                    #         var17 = var5 + modelself.class132_.Viewport_mouseX
                    #         if(var17 < var10 and var17 < var11 and var17 < var12) :
                    #             var13 = False
                    #         else :
                    #             var17 = modelself.class132_.Viewport_mouseX - var5
                    #             var13 = var17 <= var10 or var17 <= var11 or var17 <= var12

                    # if(var13) :
                    #     print("pass projectile Model.py")
                    #     #Projectile.method1944(var4)
                    #     #var2 = False

                if((var10 - var11) * (staticModel_.modelViewportXs[var9] - staticModel_.modelViewportXs[var8]) - (var12 - var11) * (staticModel_.modelViewportXs[var7] - staticModel_.modelViewportXs[var8]) > 0):
                    staticModel_.field1848[var6] = False
                    staticModel_.field1887[var6] = var10 < 0 or var11 < 0 or var12 < 0 or var10 > Graphics3D_.rasterClipX or var11 > Graphics3D_.rasterClipX or var12 > Graphics3D_.rasterClipX

                    var31 = integerdivide(
                        staticModel_.field1891[var7] + staticModel_.field1891[var8] + staticModel_.field1891[var9], 3) + modelself.radius
                    staticModel_.field1860[var31][staticModel_.field1896[var31]] = var6
                    staticModel_.field1896[var31] += 1

    if(modelself.faceRenderPriorities.size == 0): # is None):

        var6 = modelself.diameter - 1
        while var6 >= 0:
            var7 = staticModel_.field1896[var6]
            if(var7 > 0):
                var26 = staticModel_.field1860[var6]

                for var9 in range(0, var7):
                    method2708(colorPalette, staticModel_, modelself, var26[var9], Graphics3D_, textures)

            var6 -= 1

    else:
        for var6 in range(0, 12):
            staticModel_.field1898[var6] = 0
            staticModel_.field1901[var6] = 0

        var6 = modelself.diameter - 1
        while var6 >= 0:
            var7 = staticModel_.field1896[var6]
            if(var7 > 0):
                var26 = staticModel_.field1860[var6]

                for var9 in range(0, var7):
                    var10 = var26[var9]
                    var30 = modelself.faceRenderPriorities[var10]
                    var12 = staticModel_.field1898[var30]
                    staticModel_.field1898[var30] += 1
                    staticModel_.field1899[var30][var12] = var10
                    if(var30 < 10):
                        staticModel_.field1901[var30] += var6
                    elif(var30 == 10):
                        staticModel_.field1900[var12] = var6
                    else:
                        staticModel_.field1895[var12] = var6

            var6 -= 1

        var6 = 0
        if(staticModel_.field1898[1] > 0 or staticModel_.field1898[2] > 0):
            var6 = integerdivide(
                (staticModel_.field1901[1] + staticModel_.field1901[2]), (staticModel_.field1898[1] + staticModel_.field1898[2]))

        var7 = 0
        if(staticModel_.field1898[3] > 0 or staticModel_.field1898[4] > 0):
            var7 = integerdivide(
                (staticModel_.field1901[3] + staticModel_.field1901[4]), (staticModel_.field1898[3] + staticModel_.field1898[4]))

        var8 = 0
        if(staticModel_.field1898[6] > 0 or staticModel_.field1898[8] > 0):
            var8 = integerdivide(
                (staticModel_.field1901[8] + staticModel_.field1901[6]), (staticModel_.field1898[8] + staticModel_.field1898[6]))

        var10 = 0
        var11 = staticModel_.field1898[10]
        var27 = staticModel_.field1899[10]
        var28 = staticModel_.field1900
        if(var10 == var11):
            var10 = 0
            var11 = staticModel_.field1898[11]
            var27 = staticModel_.field1899[11]
            var28 = staticModel_.field1895

        if(var10 < var11):
            var9 = var28[var10]
        else:
            var9 = -1000

        for var14 in range(0, 10):
            while(var14 == 0 and var9 > var6):
                method2708(colorPalette, staticModel_, modelself, var27[var10], Graphics3D_, textures)
                var10 += 1
                if(var10 == var11 and not np.all(var27 == staticModel_.field1899[11])):
                    var10 = 0
                    var11 = staticModel_.field1898[11]
                    var27 = staticModel_.field1899[11]
                    var28 = staticModel_.field1895

                if(var10 < var11):
                    var9 = var28[var10]
                else:
                    var9 = -1000

            while(var14 == 3 and var9 > var7):
                method2708(colorPalette, staticModel_, modelself, var27[var10], Graphics3D_, textures)
                var10 += 1
                if(var10 == var11 and not np.all(var27 == staticModel_.field1899[11])):
                    var10 = 0
                    var11 = staticModel_.field1898[11]
                    var27 = staticModel_.field1899[11]
                    var28 = staticModel_.field1895

                if(var10 < var11):
                    var9 = var28[var10]
                else:
                    var9 = -1000

            while(var14 == 5 and var9 > var8):
                method2708(colorPalette, staticModel_, modelself, var27[var10], Graphics3D_, textures)
                var10 += 1
                if(var10 == var11 and not np.all(var27 == staticModel_.field1899[11])):
                    var10 = 0
                    var11 = staticModel_.field1898[11]
                    var27 = staticModel_.field1899[11]
                    var28 = staticModel_.field1895

                if(var10 < var11):
                    var9 = var28[var10]
                else:
                    var9 = -1000

            var15 = staticModel_.field1898[var14]
            var29 = staticModel_.field1899[var14]

            for var17 in range(0, var15):
                method2708(colorPalette, staticModel_, modelself, var29[var17], Graphics3D_, textures)

        while(var9 != -1000):
            method2708(colorPalette, staticModel_, modelself, var27[var10], Graphics3D_, textures)
            var10 += 1
            if(var10 == var11 and not np.all(var27 == staticModel_.field1899[11])):
                var10 = 0
                var27 = staticModel_.field1899[11]
                var11 = staticModel_.field1898[11]
                var28 = staticModel_.field1895

            if(var10 < var11):
                var9 = var28[var10]
            else:
                var9 = -1000

@jit(nopython=True, cache=False)
def method2708(colorPalette, staticModel_, modelself, var1, Graphics3D_, textures):

    if(staticModel_.field1848[var1]):
        method2709(colorPalette, staticModel_, modelself, var1, Graphics3D_, textures)
    else:
        var2 = modelself.indices1[var1]
        var3 = modelself.indices2[var1]
        var4 = modelself.indices3[var1]
        Graphics3D_.rasterClipEnable = staticModel_.field1887[var1]
        if(modelself.faceAplhas.size == 0): # is None):
            Graphics3D_.rasterAlpha = 0
        else:
            Graphics3D_.rasterAlpha = modelself.faceAplhas[var1] & 255

        # is not None
        if(modelself.faceTextures.size > 0 and modelself.faceTextures[var1] != -1):

            # is not None
            if(modelself.field1865.size > 0 and modelself.field1865[var1] != -1):
                var8 = modelself.field1865[var1] & 255
                var5 = modelself.field1869[var8]
                var6 = modelself.field1868[var8]
                var7 = modelself.field1871[var8]
            else:
                var5 = var2
                var6 = var3
                var7 = var4

            if(modelself.field1862[var1] == -1):
                rasterTextureAffine(colorPalette, Graphics3D_, modelself.objectID, staticModel_.modelViewportXs[var2], staticModel_.modelViewportXs[var3], staticModel_.modelViewportXs[var4], staticModel_.modelViewportYs[var2], staticModel_.modelViewportYs[var3], staticModel_.modelViewportYs[var4], modelself.field1852[var1], modelself.field1852[var1], modelself.field1852[
                                                var1], staticModel_.yViewportBuffer[var5], staticModel_.yViewportBuffer[var6], staticModel_.yViewportBuffer[var7], staticModel_.field1893[var5], staticModel_.field1893[var6], staticModel_.field1893[var7], staticModel_.field1894[var5], staticModel_.field1894[var6], staticModel_.field1894[var7], modelself.faceTextures[var1], textures)
            else:
                rasterTextureAffine(colorPalette, Graphics3D_, modelself.objectID, staticModel_.modelViewportXs[var2], staticModel_.modelViewportXs[var3], staticModel_.modelViewportXs[var4], staticModel_.modelViewportYs[var2], staticModel_.modelViewportYs[var3], staticModel_.modelViewportYs[var4], modelself.field1852[var1], modelself.field1861[var1], modelself.field1862[
                                                var1], staticModel_.yViewportBuffer[var5], staticModel_.yViewportBuffer[var6], staticModel_.yViewportBuffer[var7], staticModel_.field1893[var5], staticModel_.field1893[var6], staticModel_.field1893[var7], staticModel_.field1894[var5], staticModel_.field1894[var6], staticModel_.field1894[var7], modelself.faceTextures[var1], textures)

        elif(modelself.field1862[var1] == -1):
            rasterFlat(Graphics3D_, modelself.objectID, staticModel_.modelViewportXs[var2], staticModel_.modelViewportXs[var3], staticModel_.modelViewportXs[var4], staticModel_.modelViewportYs[var2],
                                    staticModel_.modelViewportYs[var3], staticModel_.modelViewportYs[var4], colorPalette[modelself.field1852[var1]])
        else:
            rasterGouraud(colorPalette, Graphics3D_, modelself.objectID, staticModel_.modelViewportXs[var2], staticModel_.modelViewportXs[var3], staticModel_.modelViewportXs[var4], staticModel_.modelViewportYs[var2],
                                        staticModel_.modelViewportYs[var3], staticModel_.modelViewportYs[var4], modelself.field1852[var1], modelself.field1861[var1], modelself.field1862[var1])

@jit(nopython=True, cache=False)
def method2709(colorPalette, staticModel_, modelself, var1, Graphics3D_, textures):
    var2 = Graphics3D_.centerX
    var3 = Graphics3D_.centerY
    var4 = 0
    var5 = modelself.indices1[var1]
    var6 = modelself.indices2[var1]
    var7 = modelself.indices3[var1]
    var8 = staticModel_.field1894[var5]
    var9 = staticModel_.field1894[var6]
    var10 = staticModel_.field1894[var7]
    if(modelself.faceAplhas.size == 0): # is None):
        Graphics3D_.rasterAlpha = 0
    else:
        Graphics3D_.rasterAlpha = modelself.faceAplhas[var1] & 255

    if(var8 >= 50):
        staticModel_.field1903[var4] = staticModel_.modelViewportYs[var5]
        staticModel_.field1875[var4] = staticModel_.modelViewportXs[var5]
        staticModel_.xViewportBuffer[var4] = modelself.field1852[var1]
        var4 += 1
    else:
        var11 = staticModel_.yViewportBuffer[var5]
        var12 = staticModel_.field1893[var5]
        var13 = modelself.field1852[var1]
        if(var10 >= 50):
            var14 = Graphics3D_.field1952[var10 - var8] * (50 - var8)
            staticModel_.field1903[var4] = var2 + integerdivide(Graphics3D_.Rasterizer3D_zoom * (
                var11 + ((staticModel_.yViewportBuffer[var7] - var11) * var14 >> 16)), 50)
            staticModel_.field1875[var4] = var3 + integerdivide(Graphics3D_.Rasterizer3D_zoom * (
                var12 + ((staticModel_.field1893[var7] - var12) * var14 >> 16)), 50)
            staticModel_.xViewportBuffer[var4] = var13 + \
                ((modelself.field1862[var1] - var13) * var14 >> 16)
            var4 += 1

        if(var9 >= 50):
            var14 = Graphics3D_.field1952[var9 - var8] * (50 - var8)
            staticModel_.field1903[var4] = var2 + integerdivide(Graphics3D_.Rasterizer3D_zoom * (
                var11 + ((staticModel_.yViewportBuffer[var6] - var11) * var14 >> 16)), 50)
            staticModel_.field1875[var4] = var3 + integerdivide(Graphics3D_.Rasterizer3D_zoom * (
                var12 + ((staticModel_.field1893[var6] - var12) * var14 >> 16)), 50)
            staticModel_.xViewportBuffer[var4] = var13 + \
                ((modelself.field1861[var1] - var13) * var14 >> 16)
            var4 += 1

    if(var9 >= 50):
        staticModel_.field1903[var4] = staticModel_.modelViewportYs[var6]
        staticModel_.field1875[var4] = staticModel_.modelViewportXs[var6]
        staticModel_.xViewportBuffer[var4] = modelself.field1861[var1]
        var4 += 1
    else:
        var11 = staticModel_.yViewportBuffer[var6]
        var12 = staticModel_.field1893[var6]
        var13 = modelself.field1861[var1]
        if(var8 >= 50):
            var14 = Graphics3D_.field1952[var8 - var9] * (50 - var9)
            staticModel_.field1903[var4] = var2 + integerdivide(Graphics3D_.Rasterizer3D_zoom * (
                var11 + ((staticModel_.yViewportBuffer[var5] - var11) * var14 >> 16)), 50)
            staticModel_.field1875[var4] = var3 + integerdivide(Graphics3D_.Rasterizer3D_zoom * (
                var12 + ((staticModel_.field1893[var5] - var12) * var14 >> 16)), 50)
            staticModel_.xViewportBuffer[var4] = var13 + \
                ((modelself.field1852[var1] - var13) * var14 >> 16)
            var4 += 1

        if(var10 >= 50):
            var14 = Graphics3D_.field1952[var10 - var9] * (50 - var9)
            staticModel_.field1903[var4] = var2 + integerdivide(Graphics3D_.Rasterizer3D_zoom * (
                var11 + ((staticModel_.yViewportBuffer[var7] - var11) * var14 >> 16)), 50)
            staticModel_.field1875[var4] = var3 + integerdivide(Graphics3D_.Rasterizer3D_zoom * (
                var12 + ((staticModel_.field1893[var7] - var12) * var14 >> 16)), 50)
            staticModel_.xViewportBuffer[var4] = var13 + \
                ((modelself.field1862[var1] - var13) * var14 >> 16)
            var4 += 1

    if(var10 >= 50):
        staticModel_.field1903[var4] = staticModel_.modelViewportYs[var7]
        staticModel_.field1875[var4] = staticModel_.modelViewportXs[var7]
        staticModel_.xViewportBuffer[var4] = modelself.field1862[var1]
        var4 += 1
    else:
        var11 = staticModel_.yViewportBuffer[var7]
        var12 = staticModel_.field1893[var7]
        var13 = modelself.field1862[var1]
        if(var9 >= 50):
            var14 = Graphics3D_.field1952[var9 - var10] * (50 - var10)
            staticModel_.field1903[var4] = var2 + integerdivide(Graphics3D_.Rasterizer3D_zoom * (
                var11 + ((staticModel_.yViewportBuffer[var6] - var11) * var14 >> 16)), 50)
            staticModel_.field1875[var4] = var3 + integerdivide(Graphics3D_.Rasterizer3D_zoom * (
                var12 + ((staticModel_.field1893[var6] - var12) * var14 >> 16)), 50)
            staticModel_.xViewportBuffer[var4] = var13 + \
                ((modelself.field1861[var1] - var13) * var14 >> 16)
            var4 += 1

        if(var8 >= 50):
            var14 = Graphics3D_.field1952[var8 - var10] * (50 - var10)
            staticModel_.field1903[var4] = var2 + integerdivide(Graphics3D_.Rasterizer3D_zoom * (
                var11 + ((staticModel_.yViewportBuffer[var5] - var11) * var14 >> 16)), 50)
            staticModel_.field1875[var4] = var3 + integerdivide(Graphics3D_.Rasterizer3D_zoom * (
                var12 + ((staticModel_.field1893[var5] - var12) * var14 >> 16)), 50)
            staticModel_.xViewportBuffer[var4] = var13 + \
                ((modelself.field1852[var1] - var13) * var14 >> 16)
            var4 += 1

    var11 = staticModel_.field1903[0]
    var12 = staticModel_.field1903[1]
    var13 = staticModel_.field1903[2]
    var14 = staticModel_.field1875[0]
    var15 = staticModel_.field1875[1]
    var16 = staticModel_.field1875[2]
    Graphics3D_.rasterClipEnable = False

    if(var4 == 3):
        if(var11 < 0 or var12 < 0 or var13 < 0 or var11 > Graphics3D_.rasterClipX or var12 > Graphics3D_.rasterClipX or var13 > Graphics3D_.rasterClipX):
            Graphics3D_.rasterClipEnable = True

        # is not None 
        if(modelself.faceTextures.size != 0 and modelself.faceTextures[var1] != -1):
            # is not None 
            if(modelself.field1865.size != 0 and modelself.field1865[var1] != -1):
                var20 = modelself.field1865[var1] & 255
                var17 = modelself.field1869[var20]
                var18 = modelself.field1868[var20]
                var19 = modelself.field1871[var20]
            else:
                var17 = var5
                var18 = var6
                var19 = var7

            if(modelself.field1862[var1] == -1):
                rasterTextureAffine(colorPalette, Graphics3D_, modelself.objectID, var14, var15, var16, var11, var12, var13,
                                                modelself.field1852[var1], modelself.field1852[var1], modelself.field1852[
                                                    var1], staticModel_.yViewportBuffer[var17], staticModel_.yViewportBuffer[var18],
                                                staticModel_.yViewportBuffer[var19], staticModel_.field1893[
                                                    var17], staticModel_.field1893[var18], staticModel_.field1893[var19],
                                                staticModel_.field1894[var17], staticModel_.field1894[var18], staticModel_.field1894[var19], modelself.faceTextures[var1], textures)
            else:
                rasterTextureAffine(colorPalette, Graphics3D_, modelself.objectID, var14, var15, var16, var11, var12, var13,
                                                staticModel_.xViewportBuffer[0], staticModel_.xViewportBuffer[
                                                    1], staticModel_.xViewportBuffer[2], staticModel_.yViewportBuffer[var17],
                                                staticModel_.yViewportBuffer[var18], staticModel_.yViewportBuffer[
                                                    var19], staticModel_.field1893[var17], staticModel_.field1893[var18],
                                                staticModel_.field1893[var19], staticModel_.field1894[var17], staticModel_.field1894[var18], staticModel_.field1894[var19], modelself.faceTextures[var1], textures)

        elif(modelself.field1862[var1] == -1):
            rasterFlat(Graphics3D_, modelself.objectID, var14, var15, var16, var11, var12, var13,
                                    colorPalette[modelself.field1852[var1]])
        else:
            rasterGouraud(colorPalette, Graphics3D_, modelself.objectID, var14, var15, var16, var11, var12, var13,
                                        staticModel_.xViewportBuffer[0], staticModel_.xViewportBuffer[1], staticModel_.xViewportBuffer[2])

    if(var4 == 4):
        if(var11 < 0 or var12 < 0 or var13 < 0 or var11 > Graphics3D_.rasterClipX or var12 > Graphics3D_.rasterClipX or var13 > Graphics3D_.rasterClipX or staticModel_.field1903[3] < 0 or staticModel_.field1903[3] > Graphics3D_.rasterClipX):
            Graphics3D_.rasterClipEnable = True

        # is not None 
        if(modelself.faceTextures.size != 0 and modelself.faceTextures[var1] != -1):

            # is not None 
            if(modelself.field1865.size != 0  and modelself.field1865[var1] != -1):
                var20 = modelself.field1865[var1] & 255
                var17 = modelself.field1869[var20]
                var18 = modelself.field1868[var20]
                var19 = modelself.field1871[var20]
            else:
                var17 = var5
                var18 = var6
                var19 = var7

            var21 = modelself.faceTextures[var1]
            if(modelself.field1862[var1] == -1):
                rasterTextureAffine(colorPalette, Graphics3D_, modelself.objectID, var14, var15, var16, var11, var12, var13, modelself.field1852[var1], modelself.field1852[var1], modelself.field1852[var1], staticModel_.yViewportBuffer[var17], staticModel_.yViewportBuffer[
                                                var18], staticModel_.yViewportBuffer[var19], staticModel_.field1893[var17], staticModel_.field1893[var18], staticModel_.field1893[var19], staticModel_.field1894[var17], staticModel_.field1894[var18], staticModel_.field1894[var19], var21, textures)
                rasterTextureAffine(colorPalette, Graphics3D_, modelself.objectID, var14, var16, staticModel_.field1875[3], var11, var13, staticModel_.field1903[3], modelself.field1852[var1], modelself.field1852[var1], modelself.field1852[var1], staticModel_.yViewportBuffer[var17], staticModel_.yViewportBuffer[
                                                var18], staticModel_.yViewportBuffer[var19], staticModel_.field1893[var17], staticModel_.field1893[var18], staticModel_.field1893[var19], staticModel_.field1894[var17], staticModel_.field1894[var18], staticModel_.field1894[var19], var21, textures)
            else:
                rasterTextureAffine(colorPalette, Graphics3D_, modelself.objectID, var14, var15, var16, var11, var12, var13, staticModel_.xViewportBuffer[0], staticModel_.xViewportBuffer[1], staticModel_.xViewportBuffer[2], staticModel_.yViewportBuffer[var17], staticModel_.yViewportBuffer[
                                                var18], staticModel_.yViewportBuffer[var19], staticModel_.field1893[var17], staticModel_.field1893[var18], staticModel_.field1893[var19], staticModel_.field1894[var17], staticModel_.field1894[var18], staticModel_.field1894[var19], var21, textures)
                rasterTextureAffine(colorPalette, Graphics3D_, modelself.objectID, var14, var16, staticModel_.field1875[3], var11, var13, staticModel_.field1903[3], staticModel_.xViewportBuffer[0], staticModel_.xViewportBuffer[2], staticModel_.xViewportBuffer[3], staticModel_.yViewportBuffer[var17], staticModel_.yViewportBuffer[
                                                var18], staticModel_.yViewportBuffer[var19], staticModel_.field1893[var17], staticModel_.field1893[var18], staticModel_.field1893[var19], staticModel_.field1894[var17], staticModel_.field1894[var18], staticModel_.field1894[var19], var21, textures)

        elif(modelself.field1862[var1] == -1):
            var17 = colorPalette[modelself.field1852[var1]]
            rasterFlat(Graphics3D_, modelself.objectID, 
                var14, var15, var16, var11, var12, var13, var17)
            rasterFlat(Graphics3D_, modelself.objectID, 
                var14, var16, staticModel_.field1875[3], var11, var13, staticModel_.field1903[3], var17)
        else:
            rasterGouraud(colorPalette, Graphics3D_, modelself.objectID, var14, var15, var16, var11, var12, var13,
                                        staticModel_.xViewportBuffer[0], staticModel_.xViewportBuffer[1], staticModel_.xViewportBuffer[2])
            rasterGouraud(colorPalette, Graphics3D_, modelself.objectID, var14, var16, staticModel_.field1875[3], var11, var13, staticModel_.field1903[3],
                                        staticModel_.xViewportBuffer[0], staticModel_.xViewportBuffer[2], staticModel_.xViewportBuffer[3])

@jit(nopython=True, cache=False)
def drawModel(colorPalette, staticModel_, modelself, var1, var2, var3, var4, var5, var6, var7, var8, var9, Graphics3D_, tileHeights, textures, objectDefinitions):

    # if (modelself.verticesCount == 264):
    #System.out.println("yaw en shit " + var1 + " " + var2 + " " + var3 + " " + var4 + " " + var5 + " " + var6 + " " + var7 + " " + var8 + " " + var9)

    staticModel_.field1896[0] = -1
    if(modelself.boundsType != 1):
        calculateBoundsCylinder(modelself)

    method2690(modelself, var1)
    var10 = var5 * var8 - var4 * var6 >> 16
    var11 = var2 * var7 + var3 * var10 >> 16
    var12 = var3 * modelself.XYZMag >> 16
    var13 = var11 + var12
    if(var13 > 50 and var11 < 3500):
        var14 = var8 * var4 + var5 * var6 >> 16
        var15 = (var14 - modelself.XYZMag) * Graphics3D_.Rasterizer3D_zoom
        if(integerdivide(var15, var13) < Graphics3D_.Rasterizer3D_clipMidX2):
            var16 = (var14 + modelself.XYZMag) * Graphics3D_.Rasterizer3D_zoom
            if(integerdivide(var16, var13) > Graphics3D_.Rasterizer3D_clipNegativeMidX):
                var17 = var3 * var7 - var10 * var2 >> 16
                var18 = var2 * modelself.XYZMag >> 16
                var19 = (var17 + var18) * Graphics3D_.Rasterizer3D_zoom
                if(integerdivide(var19, var13) > Graphics3D_.Rasterizer3D_clipNegativeMidY):
                    var20 = (var3 * modelself.modelHeight >> 16) + var18
                    var21 = (var17 - var20) * Graphics3D_.Rasterizer3D_zoom
                    if(integerdivide(var21, var13) < Graphics3D_.Rasterizer3D_clipMidY2):
                        var22 = var12 + (var2 * modelself.modelHeight >> 16)
                        var23 = False
                        var24 = False
                        if(var11 - var22 <= 50):
                            var24 = True

                        var25 = var24 or modelself.field1866 > 0
                        # var26 = modelself.class132_.Viewport_mouseX
                        # var28 = modelself.class132_.Viewport_mouseY
                        # var29 = modelself.class132_.Viewport_containsMouse
                        # if(modelself.class7_.drawBoundingBoxes3D and var9 > 0) :
                        #     print("Passing this, model.py")
                        #     #World.method1723(modelself, var6, var7, var8)

                        # Draws BoundingBox???
                        # if(modelself.class7_.drawBoundingBoxes2D and var9 > 0) :
                        #     var30 = var11 - var12
                        #     if(var30 <= 50) :
                        #         var30 = 50

                        #     if(var14 > 0) :
                        #         var31 = integerdivide(var15, var13)
                        #         var32 = integerdivide(var16, var30)
                        #     else :
                        #         var32 = integerdivide(var16, var13)
                        #         var31 = integerdivide(var15, var30)

                        #     if(var17 > 0) :
                        #         var33 = integerdivide(var21, var13)
                        #         var34 = integerdivide(var19, var30)
                        #     else :
                        #         var34 = integerdivide(var19, var13)
                        #         var33 = integerdivide(var21, var30)

                        #     var35 = -8355840
                        #     var36 = var26 - Graphics3D_.centerX
                        #     var37 = var28 - Graphics3D_.centerY
                        #     if(var36 > var31 and var36 < var32 and var37 > var33 and var37 < var34) :
                        #         var35 = -256

                        #     class149.method3104(var31 + Graphics3D_.centerX, var33 + Graphics3D_.centerY, var32 + Graphics3D_.centerX, var34 + Graphics3D_.centerY, var35)

                        var42 = False

                        # Something with mouse?
                        # if(var9 > 0 and var29) :
                        #     var43 = False
                        #     if(staticModel_.useBoundingBoxes3D) :
                        #         pass
                        #         #var43 = boundingBox3DContainsMouse(modelself, var6, var7, var8)
                        #     else :
                        #         var32 = var11 - var12
                        #         if(var32 <= 50) :
                        #             var32 = 50

                        #         if(var14 > 0) :
                        #             var15 = integerdivide(var15, var13)
                        #             var16 = integerdivide(var16, var32)
                        #         else :
                        #             var16 = integerdivide(var16, var13)
                        #             var15 = integerdivide(var15, var32)

                        #         if(var17 > 0) :
                        #             var21 = integerdivide(var21, var13)
                        #             var19 = integerdivide(var19, var32)
                        #         else :
                        #             var19 = integerdivide(var19, var13)
                        #             var21 = integerdivide(var21, var32)

                        #         var33 = var26 - Graphics3D_.centerX
                        #         var34 = var28 - Graphics3D_.centerY
                        #         if(var33 > var15 and var33 < var16 and var34 > var21 and var34 < var19) :
                        #             var43 = True

                        #     if(var43) :
                        #         if(modelself.field1874) :
                        #             modelself.class132_.Viewport_entityCountAtMouse += 1
                        #             modelself.class132_.Viewport_entityIdsAtMouse[modelself.class132_.Viewport_entityCountAtMouse - 1] = var9
                        #         else :
                        #             var42 = True

                        var31 = Graphics3D_.centerX
                        var32 = Graphics3D_.centerY
                        var33 = 0
                        var34 = 0
                        if(var1 != 0):
                            # Graphics3D_.SINE[var1]
                            var33 = Graphics3DSINE(var1)
                            # Graphics3D_.COSINE[var1]
                            var34 = Graphics3DCOSINE(var1)

                        for var35 in range(0, modelself.verticesCount):
                            var36 = modelself.verticesX[var35]
                            var37 = modelself.verticesY[var35]
                            var38 = modelself.verticesZ[var35]
                            if(var1 != 0):
                                var39 = var38 * var33 + var36 * var34 >> 16
                                var38 = var38 * var34 - var36 * var33 >> 16
                                var36 = var39

                            var36 += var6
                            var37 += var7
                            var38 += var8
                            var39 = var38 * var4 + var5 * var36 >> 16
                            var38 = var5 * var38 - var36 * var4 >> 16
                            var36 = var39
                            var39 = var3 * var37 - var38 * var2 >> 16
                            var38 = var37 * var2 + var3 * var38 >> 16
                            staticModel_.field1891[var35] = var38 - var11
                            if(var38 >= 50):
                                staticModel_.modelViewportYs[var35] = integerdivide(
                                    var36 * Graphics3D_.Rasterizer3D_zoom, var38) + var31
                                staticModel_.modelViewportXs[var35] = integerdivide(
                                    var39 * Graphics3D_.Rasterizer3D_zoom, var38) + var32
                            else:
                                staticModel_.modelViewportYs[var35] = -5000
                                var23 = True

                            if(var25):
                                staticModel_.yViewportBuffer[var35] = var36
                                staticModel_.field1893[var35] = var39
                                staticModel_.field1894[var35] = var38

                        method2707(colorPalette, staticModel_, modelself, 
                            var23, var42, modelself.field1874, var9, Graphics3D_, textures)


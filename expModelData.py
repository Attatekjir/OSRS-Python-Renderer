from expModel import Model
from MathUtills import Graphics3DCOSINE, Graphics3DSINE
from logging import debug
from bitoperation import readUnsignedByte, readUnsignedShort, readShortSmart, readByte, readInt
from numba import jit
from numba import int32, float32
from Buffer import Buffer
from numba.experimental import jitclass
from numba import int32, float32, boolean, short, int64, int8
#from FaceNormal import FaceNormal
import numpy as np
import math
from MathUtills import integerdivide
import numba


@jitclass()
class expVertexNormal:

    field1931: int32
    x: int32
    y: int32
    z: int32
    magnitude: int32
    isNotNull: boolean

    def __init__(self):
        self.field1931 = 0
        self.x = 0
        self.y = 0
        self.z = 0
        self.magnitude = 0
        self.isNotNull = False

    def copyFrom(self, otherexpVertexNormal):
        self.x = otherexpVertexNormal.x
        self.y = otherexpVertexNormal.y
        self.z = otherexpVertexNormal.z
        self.magnitude = otherexpVertexNormal.magnitude
        self.isNotNull = otherexpVertexNormal.isNotNull


@jitclass()
class expFaceNormal:

    x: int32
    y: int32
    z: int32

    def __init__(self):
        pass


expVertexNormal_type = expVertexNormal.class_type.instance_type
expFaceNormal_type = expFaceNormal.class_type.instance_type
numpyarrayint32_type = numba.typeof(np.empty(shape=(0), dtype=np.int32))

@jitclass()
class staticModelData():

    field1765: int32[:]  # [0] * 10000
    field1753: int32[:]  # [0] * 10000
    field1724: int32

    def __init__(self):

        self.field1765 = np.empty(shape=(10000), dtype=np.int32)
        self.field1753 = np.empty(shape=(10000), dtype=np.int32)
        self.field1724 = 0

@jitclass()
class ModelData():

    id: int32
    objectID: int32

    modelHeight: int64

    #xd: numba.types.Array(numba.types.pyobject)

    #field1765: int32[:]  # [0] * 10000
    #field1753: int32[:]  # [0] * 10000
    #field1724: int32
    # field1768: int32[:]  # Graphics3D_.SINE
    # field1757: int32[:]  # Graphics3D_.COSINE

    vertexCount: int32
    vertexX: int32[:]
    vertexY: int32[:]
    vertexZ: int32[:]
    triangleFaceCount: int32
    trianglePointsX: int32[:]
    trianglePointsY: int32[:]
    trianglePointsZ: int32[:]
    faceRenderTypes: int8[:]
    faceRenderPriorities: int8[:]
    faceAlphas: int8[:]
    textureCoords: int8[:]
    faceColor: short[:]
    faceTextures: short[:]
    priority: int8
    field1738: int32
    textureRenderTypes: int8[:]
    texTriangleX: short[:]
    texTriangleY: short[:]
    texTriangleZ: short[:]
    field1743: short[:]
    field1745: short[:]
    field1740: short[:]
    field1746: short[:]
    field1747: short[:]
    texturePrimaryColor: short[:]
    field1749: int8[:]
    vertexSkins: int32[:]
    triangleSkinValues: int32[:]

    #vertexGroups : int32[:,:]
    #field1758 : int32[:,:]

    vertexGroups: numba.types.ListType(numpyarrayint32_type)  # int32[:]
    field1758: numba.types.ListType(numpyarrayint32_type)  # int32[:]

    #faceNormals : FaceNormal[:]
    faceNormals: numba.types.ListType(expFaceNormal_type)

    #normals : VertexNormal[:]
    normals: numba.types.ListType(expVertexNormal_type)

    #field1756 : VertexNormal[:]
    field1756: numba.types.ListType(expVertexNormal_type)

    field1731: short
    contrast: short[:]
    field1759: boolean  # Calculated model bounds
    field1760: int32
    field1761: int32
    field1762: int32
    field1763: int32
    field1764: int32

    # Errors if u enter a single argument, so just assign outside of class?

    def __init__(self):
        self.faceNormals = numba.typed.List.empty_list(expFaceNormal_type)
        self.normals = numba.typed.List.empty_list(expVertexNormal_type)
        self.field1756 = numba.typed.List.empty_list(expVertexNormal_type)

        self.vertexGroups = numba.typed.List.empty_list(numpyarrayint32_type)
        self.field1758 = numba.typed.List.empty_list(numpyarrayint32_type)

        # STATIC in the static class?
        #self.field1765 = np.empty(shape=(10000), dtype=np.int32)
        #self.field1753 = np.empty(shape=(10000), dtype=np.int32)
        #self.field1724 = 0

        self.vertexCount = 0
        self.triangleFaceCount = 0
        self.priority = 0
        self.field1759 = False

    def method2626(self, var1, var2):
        var3 = -1
        var4 = var1.vertexX[var2]
        var5 = var1.vertexY[var2]
        var6 = var1.vertexZ[var2]

        for var7 in range(0, self.vertexCount):
            if(var4 == self.vertexX[var7] and
               var5 == self.vertexY[var7] and
               var6 == self.vertexZ[var7]):
                var3 = var7
                break
        if(var3 == -1):
            self.vertexX[self.vertexCount] = var4
            self.vertexY[self.vertexCount] = var5
            self.vertexZ[self.vertexCount] = var6
            if(var1.vertexSkins.size != 0):  # is not None) :
                self.vertexSkins[self.vertexCount] = var1.vertexSkins[var2]

            var3 = self.vertexCount
            self.vertexCount += 1

        return var3

@jit(nopython=True, cache=False)
def ModelData2(selfModelData, listOfModelDatas, var2):
    selfModelData.vertexCount = 0
    selfModelData.triangleFaceCount = 0
    selfModelData.priority = 0
    selfModelData.field1759 = False
    var3 = False
    var4 = False
    var5 = False
    var6 = False
    var7 = False
    var8 = False
    selfModelData.vertexCount = 0
    selfModelData.triangleFaceCount = 0
    selfModelData.field1738 = 0
    selfModelData.priority = -1

    for var9 in range(0, var2):
        var10 = listOfModelDatas[var9]
        # if(len(var10) > 0): # is not None) :
        selfModelData.vertexCount += var10.vertexCount
        selfModelData.triangleFaceCount += var10.triangleFaceCount
        selfModelData.field1738 += var10.field1738
        if(var10.faceRenderPriorities.size > 0):  # is not None) :
            var4 = True
        else:
            if(selfModelData.priority == -1):
                selfModelData.priority = var10.priority

            if(selfModelData.priority != var10.priority):
                var4 = True

        var3 |= var10.faceRenderTypes.size != 0  # is not None
        var5 |= var10.faceAlphas.size != 0  # is not None
        var6 |= var10.triangleSkinValues.size != 0  # is not None
        var7 |= var10.faceTextures.size != 0  # is not None
        var8 |= var10.textureCoords.size != 0  # is not None

    selfModelData.vertexX = np.zeros(shape=(
        selfModelData.vertexCount), dtype=np.int32)  # [0] * selfModelData.vertexCount
    selfModelData.vertexY = np.zeros(shape=(
        selfModelData.vertexCount), dtype=np.int32)  # [0] * selfModelData.vertexCount
    selfModelData.vertexZ = np.zeros(shape=(
        selfModelData.vertexCount), dtype=np.int32)  # [0] * selfModelData.vertexCount
    selfModelData.vertexSkins = np.zeros(shape=(
        selfModelData.vertexCount), dtype=np.int32)  # [0] * selfModelData.vertexCount
    selfModelData.trianglePointsX = np.zeros(
        shape=(selfModelData.triangleFaceCount), dtype=np.int32)
    selfModelData.trianglePointsY = np.zeros(
        shape=(selfModelData.triangleFaceCount), dtype=np.int32)
    selfModelData.trianglePointsZ = np.zeros(
        shape=(selfModelData.triangleFaceCount), dtype=np.int32)
    if(var3):
        selfModelData.faceRenderTypes = np.zeros(shape=(
            selfModelData.triangleFaceCount), dtype=np.byte)  # [0] * selfModelData.triangleFaceCount

    if(var4):
        selfModelData.faceRenderPriorities = np.zeros(shape=(
            selfModelData.triangleFaceCount), dtype=np.byte)  # [0] * selfModelData.triangleFaceCount

    if(var5):
        # [0] * selfModelData.triangleFaceCount
        selfModelData.faceAlphas = np.zeros(
            shape=(selfModelData.triangleFaceCount), dtype=np.byte)

    if(var6):
        selfModelData.triangleSkinValues = np.zeros(shape=(
            selfModelData.triangleFaceCount), dtype=np.int32)  # [0] * selfModelData.triangleFaceCount

    if(var7):
        selfModelData.faceTextures = np.zeros(shape=(
            selfModelData.triangleFaceCount), dtype=np.short)  # [0] * selfModelData.triangleFaceCount

    if(var8):
        selfModelData.textureCoords = np.zeros(shape=(
            selfModelData.triangleFaceCount), dtype=np.byte)  # [0] * selfModelData.triangleFaceCount

    # [0] * selfModelData.triangleFaceCount
    selfModelData.faceColor = np.zeros(
        shape=(selfModelData.triangleFaceCount), dtype=np.short)
    if(selfModelData.field1738 > 0):
        selfModelData.textureRenderTypes = np.zeros(
            shape=(selfModelData.field1738), dtype=np.byte)  # [0] * selfModelData.field1738
        selfModelData.texTriangleX = np.zeros(shape=(
            selfModelData.field1738), dtype=np.short)  # [0] * selfModelData.field1738
        selfModelData.texTriangleY = np.zeros(shape=(
            selfModelData.field1738), dtype=np.short)  # [0] * selfModelData.field1738
        selfModelData.texTriangleZ = np.zeros(shape=(
            selfModelData.field1738), dtype=np.short)  # [0] * selfModelData.field1738
        selfModelData.field1743 = np.zeros(shape=(
            selfModelData.field1738), dtype=np.short)  # [0] * selfModelData.field1738
        selfModelData.field1745 = np.zeros(shape=(
            selfModelData.field1738), dtype=np.short)  # [0] * selfModelData.field1738
        selfModelData.field1740 = np.zeros(shape=(
            selfModelData.field1738), dtype=np.short)  # [0] * selfModelData.field1738
        selfModelData.field1746 = np.zeros(shape=(
            selfModelData.field1738), dtype=np.short)  # [0] * selfModelData.field1738
        selfModelData.field1749 = np.zeros(shape=(
            selfModelData.field1738), dtype=np.byte)  # [0] * selfModelData.field1738
        selfModelData.field1747 = np.zeros(shape=(
            selfModelData.field1738), dtype=np.short)  # [0] * selfModelData.field1738
        selfModelData.texturePrimaryColor = np.zeros(shape=(
            selfModelData.field1738), dtype=np.short)  # [0] * selfModelData.field1738

    selfModelData.vertexCount = 0
    selfModelData.triangleFaceCount = 0
    selfModelData.field1738 = 0

    for var9 in range(0, var2):
        var10 = listOfModelDatas[var9]
        # if(len(var10) > 0): # is not None) :
        for var11 in range(0, var10.triangleFaceCount):
            if(var3 and var10.faceRenderTypes.size != 0):  # is not None) :
                selfModelData.faceRenderTypes[selfModelData.triangleFaceCount] = var10.faceRenderTypes[var11]

            if(var4):
                if(var10.faceRenderPriorities.size != 0):  # is not None) :
                    selfModelData.faceRenderPriorities[selfModelData.triangleFaceCount] = var10.faceRenderPriorities[var11]
                else:
                    selfModelData.faceRenderPriorities[selfModelData.triangleFaceCount] = var10.priority

            if(var5 and var10.faceAlphas.size != 0):  # is not None) :
                selfModelData.faceAlphas[selfModelData.triangleFaceCount] = var10.faceAlphas[var11]

            if(var6 and var10.triangleSkinValues.size != 0):  # is not None) :
                selfModelData.triangleSkinValues[selfModelData.triangleFaceCount] = var10.triangleSkinValues[var11]

            if(var7):
                if(var10.faceTextures.size != 0):  # is not None) :
                    selfModelData.faceTextures[selfModelData.triangleFaceCount] = var10.faceTextures[var11]
                else:
                    selfModelData.faceTextures[selfModelData.triangleFaceCount] = -1

            if(var8):
                # is not None
                if(var10.textureCoords.size != 0 and var10.textureCoords[var11] != -1):
                    # Enter here in Lumbridge, probably the bridge
                    var9910 = np.byte(
                        (selfModelData.field1738 + var10.textureCoords[var11]))
                    selfModelData.textureCoords[selfModelData.triangleFaceCount] = var9910
                else:
                    selfModelData.textureCoords[selfModelData.triangleFaceCount] = -1

            selfModelData.faceColor[selfModelData.triangleFaceCount] = var10.faceColor[var11]
            selfModelData.trianglePointsX[selfModelData.triangleFaceCount] = selfModelData.method2626(
                var10, var10.trianglePointsX[var11])
            selfModelData.trianglePointsY[selfModelData.triangleFaceCount] = selfModelData.method2626(
                var10, var10.trianglePointsY[var11])
            selfModelData.trianglePointsZ[selfModelData.triangleFaceCount] = selfModelData.method2626(
                var10, var10.trianglePointsZ[var11])
            selfModelData.triangleFaceCount += 1

        for var11 in range(0, var10.field1738):
            var12 = selfModelData.textureRenderTypes[selfModelData.field1738] = var10.textureRenderTypes[var11]
            if(var12 == 0):

                selfModelData.texTriangleX[selfModelData.field1738] = selfModelData.method2626(
                    var10, var10.texTriangleX[var11])
                selfModelData.texTriangleY[selfModelData.field1738] = selfModelData.method2626(
                    var10, var10.texTriangleY[var11])
                selfModelData.texTriangleZ[selfModelData.field1738] = selfModelData.method2626(
                    var10, var10.texTriangleZ[var11])

            if(var12 >= 1 and var12 <= 3):
                selfModelData.texTriangleX[selfModelData.field1738] = var10.texTriangleX[var11]
                selfModelData.texTriangleY[selfModelData.field1738] = var10.texTriangleY[var11]
                selfModelData.texTriangleZ[selfModelData.field1738] = var10.texTriangleZ[var11]
                selfModelData.field1743[selfModelData.field1738] = var10.field1743[var11]
                selfModelData.field1745[selfModelData.field1738] = var10.field1745[var11]
                selfModelData.field1740[selfModelData.field1738] = var10.field1740[var11]
                selfModelData.field1746[selfModelData.field1738] = var10.field1746[var11]
                selfModelData.field1749[selfModelData.field1738] = var10.field1749[var11]
                selfModelData.field1747[selfModelData.field1738] = var10.field1747[var11]

            if(var12 == 2):
                selfModelData.texturePrimaryColor[selfModelData.field1738] = var10.texturePrimaryColor[var11]

            selfModelData.field1738 += 1

@jit(nopython=True, cache=False)
def ModelData4(selfModelData, otherModelData, var2, var3, var4):
    #selfModelData.vertexCount = 0
    #selfModelData.triangleFaceCount = 0
    #selfModelData.priority = 0
    selfModelData.field1759 = False
    selfModelData.vertexCount = otherModelData.vertexCount
    selfModelData.triangleFaceCount = otherModelData.triangleFaceCount
    selfModelData.field1738 = otherModelData.field1738

    if var2:
        selfModelData.vertexX = otherModelData.vertexX
        selfModelData.vertexY = otherModelData.vertexY
        selfModelData.vertexZ = otherModelData.vertexZ
    else:
        selfModelData.vertexX = np.zeros(shape=(
            selfModelData.vertexCount), dtype=np.int32)  # [0] * selfModelData.vertexCount
        selfModelData.vertexY = np.zeros(
            shape=(selfModelData.vertexCount), dtype=np.int32)
        selfModelData.vertexZ = np.zeros(
            shape=(selfModelData.vertexCount), dtype=np.int32)

        for var6 in range(0, selfModelData.vertexCount):
            selfModelData.vertexX[var6] = otherModelData.vertexX[var6]
            selfModelData.vertexY[var6] = otherModelData.vertexY[var6]
            selfModelData.vertexZ[var6] = otherModelData.vertexZ[var6]

    if(var3):
        selfModelData.faceColor = otherModelData.faceColor
    else:
        # [0] * selfModelData.triangleFaceCount
        selfModelData.faceColor = np.zeros(
            shape=(selfModelData.triangleFaceCount), dtype=np.short)

        for var6 in range(0, selfModelData.triangleFaceCount):
            selfModelData.faceColor[var6] = otherModelData.faceColor[var6]

    if(var4 is False and otherModelData.faceTextures.size != 0):  # is not None) :
        selfModelData.faceTextures = np.zeros(shape=(
            selfModelData.triangleFaceCount), dtype=np.short)  # [0] * selfModelData.triangleFaceCount

        for var6 in range(0, selfModelData.triangleFaceCount):
            selfModelData.faceTextures[var6] = otherModelData.faceTextures[var6]

    else:
        selfModelData.faceTextures = otherModelData.faceTextures

    selfModelData.faceAlphas = otherModelData.faceAlphas
    selfModelData.trianglePointsX = otherModelData.trianglePointsX
    selfModelData.trianglePointsY = otherModelData.trianglePointsY
    selfModelData.trianglePointsZ = otherModelData.trianglePointsZ
    selfModelData.faceRenderTypes = otherModelData.faceRenderTypes
    selfModelData.faceRenderPriorities = otherModelData.faceRenderPriorities
    selfModelData.textureCoords = otherModelData.textureCoords
    selfModelData.priority = otherModelData.priority
    selfModelData.textureRenderTypes = otherModelData.textureRenderTypes
    selfModelData.texTriangleX = otherModelData.texTriangleX
    selfModelData.texTriangleY = otherModelData.texTriangleY
    selfModelData.texTriangleZ = otherModelData.texTriangleZ
    selfModelData.field1743 = otherModelData.field1743
    selfModelData.field1745 = otherModelData.field1745
    selfModelData.field1740 = otherModelData.field1740
    selfModelData.field1746 = otherModelData.field1746
    selfModelData.field1749 = otherModelData.field1749
    selfModelData.field1747 = otherModelData.field1747
    selfModelData.texturePrimaryColor = otherModelData.texturePrimaryColor
    selfModelData.vertexSkins = otherModelData.vertexSkins
    selfModelData.triangleSkinValues = otherModelData.triangleSkinValues
    selfModelData.vertexGroups = otherModelData.vertexGroups
    selfModelData.field1758 = otherModelData.field1758
    selfModelData.normals = otherModelData.normals
    selfModelData.faceNormals = otherModelData.faceNormals
    selfModelData.field1756 = otherModelData.field1756
    selfModelData.field1731 = otherModelData.field1731
    selfModelData.contrast = otherModelData.contrast


@jit(nopython=True, cache=False)
def computeAnimationTables(modelData):

    # is not None
    if(modelData.vertexSkins.size > 0):

        var1 = np.zeros(shape=(256), dtype=np.int32)
        var2 = 0

        for var3 in range(0, modelData.vertexCount):
            var4 = modelData.vertexSkins[var3]
            var1[var4] += 1
            if(var4 > var2):
                var2 = var4


        #var1[:var2 + 1] = 0

        for var3 in range(0, var2 + 1):
            var9999 = np.empty(shape=(var1[var3]), dtype=np.int32)
            # modelData.vertexGroups[var3] = np.empty(shape = (var1[var3]), dtype = np.int32)
            modelData.vertexGroups.append(var9999)
            var1[var3] = 0

        # for(var3 = 0 var3 < modelData.vertexCount modelData.vertexGroups[var4][var1[var4]++] = var3++) :

        for var3 in range(0, modelData.vertexCount):

            var4 = modelData.vertexSkins[var3]
            #modelData.vertexGroups[var4, var1[var4]] = var3
            modelData.vertexGroups[var4][var1[var4]] = var3

            var1[var4] += 1

        modelData.vertexSkins = np.empty(shape=(0), dtype=np.int32)  # None

    #  is not None
    if(modelData.triangleSkinValues.size > 0):
        var1 = np.zeros(shape=(256), dtype=np.int32)
        var2 = 0

        for var3 in range(0, modelData.triangleFaceCount):
            var4 = modelData.triangleSkinValues[var3]
            var1[var4] += 1
            if(var4 > var2):
                var2 = var4

        # Leave it at 0, else cant broadcast to array
        #modelData.field1758 = [0] * (var2 + 1)

        for var3 in range(0, var2 + 1):
            var9999 = np.empty(shape=(var1[var3]), dtype=np.int32)
            # modelData.field1758[var3] = np.empty(shape = (var1[var3]), dtype = np.int32)
            modelData.field1758.append(var9999)
            var1[var3] = 0

        for var3 in range(0, modelData.triangleFaceCount):
            var4 = modelData.triangleSkinValues[var3]
            #modelData.field1758[var4, var1[var4]] = var3

            modelData.field1758[var4][var1[var4]] = var3
            var1[var4] += 1

        modelData.triangleSkinValues = np.empty(
            shape=(0), dtype=np.int32)  # None


@jit(nopython=True, cache=False)
def method2607(modelData):
    for var1 in range(0, modelData.vertexCount):
        var2 = modelData.vertexX[var1]
        modelData.vertexX[var1] = modelData.vertexZ[var1]
        modelData.vertexZ[var1] = -var2

    method2617(modelData)


@jit(nopython=True, cache=False)
def method2625(modelData):
    for var1 in range(0, modelData.vertexCount):
        modelData.vertexX[var1] = -modelData.vertexX[var1]
        modelData.vertexZ[var1] = -modelData.vertexZ[var1]

    method2617(modelData)


@jit(nopython=True, cache=False)
def method2610(modelData):
    for var1 in range(0, modelData.vertexCount):
        var2 = modelData.vertexZ[var1]
        modelData.vertexZ[var1] = modelData.vertexX[var1]
        modelData.vertexX[var1] = -var2

    method2617(modelData)


@jit(nopython=True, cache=False)
def method2606(modelData, var1):
    var2 = Graphics3DSINE(var1)  # modelData.field1768[var1]
    var3 = Graphics3DCOSINE(var1)  # modelData.field1757[var1]
    for var4 in range(0, modelData.vertexCount):
        var5 = var2 * modelData.vertexZ[var4] + \
            var3 * modelData.vertexX[var4] >> 16
        modelData.vertexZ[var4] = var3 * modelData.vertexZ[var4] - \
            var2 * modelData.vertexX[var4] >> 16
        modelData.vertexX[var4] = var5

    method2617(modelData)


@jit(nopython=True, cache=False)
def method2611(modelData, var1, var2, var3):
    for var4 in range(0, modelData.vertexCount):
        modelData.vertexX[var4] += var1
        modelData.vertexY[var4] += var2
        modelData.vertexZ[var4] += var3

    method2617(modelData)


@jit(nopython=True, cache=False)
def recolor(modelData, var1, var2):
    for var3 in range(0, modelData.triangleFaceCount):
        if(modelData.faceColor[var3] == var1):
            modelData.faceColor[var3] = var2


@jit(nopython=True, cache=False)
def method2613(modelData, var1, var2):
    # is not None
    if(modelData.faceTextures.size > 0):
        for var3 in range(0, modelData.triangleFaceCount):
            if(modelData.faceTextures[var3] == var1):
                modelData.faceTextures[var3] = var2


@jit(nopython=True, cache=False)
def method2614(modelData):

    for var1 in range(0, modelData.vertexCount):
        modelData.vertexZ[var1] = -modelData.vertexZ[var1]

    for var1 in range(0, modelData.triangleFaceCount):
        var2 = modelData.trianglePointsX[var1]
        modelData.trianglePointsX[var1] = modelData.trianglePointsZ[var1]
        modelData.trianglePointsZ[var1] = var2

    method2617(modelData)


@jit(nopython=True, cache=False)
def method2615(modelData, var1, var2, var3):
    for var4 in range(0, modelData.vertexCount):
        modelData.vertexX[var4] = integerdivide(
            var1 * modelData.vertexX[var4], 128)
        modelData.vertexY[var4] = integerdivide(
            var2 * modelData.vertexY[var4], 128)
        modelData.vertexZ[var4] = integerdivide(
            var3 * modelData.vertexZ[var4], 128)

    method2617(modelData)


@jit(nopython=True, cache=False)
def method2617(modelData):
    modelData.normals = numba.typed.List.empty_list(expVertexNormal_type)
    modelData.field1756 = numba.typed.List.empty_list(expVertexNormal_type)
    modelData.faceNormals = numba.typed.List.empty_list(expFaceNormal_type)
    modelData.field1759 = False


# Calculate bounds of model
@jit(nopython=True, cache=False)
def method2641(modelData):
    if(not modelData.field1759):
        modelData.modelHeight = 0
        modelData.field1760 = 0
        modelData.field1761 = 999999
        modelData.field1762 = -999999
        modelData.field1763 = -99999
        modelData.field1764 = 99999

        for vertexIdx in range(0, modelData.vertexCount):
            var2 = modelData.vertexX[vertexIdx]
            var3 = modelData.vertexY[vertexIdx]
            var4 = modelData.vertexZ[vertexIdx]

            # if(var2 < modelData.field1761):
            #    modelData.field1761 = var2
            modelData.field1761 = min(var2, modelData.field1761)

            # if(var2 > modelData.field1762):
            #     modelData.field1762 = var2
            modelData.field1762 = max(var2, modelData.field1762)

            # if(var4 < modelData.field1764):
            #     modelData.field1764 = var4
            modelData.field1764 = min(var4, modelData.field1764)

            # if(var4 > modelData.field1763):
            #     modelData.field1763 = var4
            modelData.field1763 = max(var4, modelData.field1763)

            # if(-var3 > modelData.modelHeight):
            #     modelData.modelHeight = -var3
            modelData.modelHeight = max(-var3, modelData.modelHeight)

            # if(var3 > modelData.field1760):
            #     modelData.field1760 = var3
            modelData.field1760 = max(var3, modelData.field1760)

        modelData.field1759 = True


@jit(nopython=True, cache=False)
def light(modelData, var1, var2, var3, var4, var5):
    computeNormals(modelData)
    var6 = np.int32(math.sqrt(var5 * var5 + var3 * var3 + var4 * var4))
    var7 = var6 * var2 >> 8
    model = Model(modelData.id, modelData.objectID)
    model.field1852 = np.zeros(
        shape=(modelData.triangleFaceCount), dtype=np.int32)
    model.field1861 = np.zeros(
        shape=(modelData.triangleFaceCount), dtype=np.int32)
    model.field1862 = np.zeros(
        shape=(modelData.triangleFaceCount), dtype=np.int32)

    # is not None):
    if(modelData.field1738 > 0 and modelData.textureCoords.size != 0):
        var9 = np.zeros(shape=(modelData.field1738), dtype=np.int32)

        for var10 in range(0, modelData.triangleFaceCount):
            if(modelData.textureCoords[var10] != -1):
                var9[modelData.textureCoords[var10] & 255] += 1

        model.field1866 = 0

        for var10 in range(modelData.field1738):
            if(var9[var10] > 0 and modelData.textureRenderTypes[var10] == 0):
                model.field1866 += 1

        model.field1869 = np.zeros(shape=(model.field1866), dtype=np.int32)
        model.field1868 = np.zeros(shape=(model.field1866), dtype=np.int32)
        model.field1871 = np.zeros(shape=(model.field1866), dtype=np.int32)
        var10 = 0

        for var11 in range(0, modelData.field1738):
            if(var9[var11] > 0 and modelData.textureRenderTypes[var11] == 0):
                model.field1869[var10] = modelData.texTriangleX[var11] & 0xffff
                model.field1868[var10] = modelData.texTriangleY[var11] & 0xffff
                model.field1871[var10] = modelData.texTriangleZ[var11] & 0xffff
                var9[var11] = var10
                var10 += 1
            else:
                var9[var11] = -1

        model.field1865 = np.zeros(
            shape=(modelData.triangleFaceCount), dtype=np.byte)

        for var11 in range(0, modelData.triangleFaceCount):
            if(modelData.textureCoords[var11] != -1):
                model.field1865[var11] = np.byte(
                    var9[modelData.textureCoords[var11] & 255])
            else:
                model.field1865[var11] = -1

    for faceIdx in range(0, modelData.triangleFaceCount):

        # is None
        if(modelData.faceRenderTypes.size == 0):
            faceRenderType = 0
        else:
            faceRenderType = modelData.faceRenderTypes[faceIdx]

        # is None
        if(modelData.faceAlphas.size == 0):
            faceAlpha = 0
        else:
            faceAlpha = modelData.faceAlphas[faceIdx]

        if(modelData.faceTextures.size == 0):  # is None):
            faceTexture = -1
        else:
            faceTexture = modelData.faceTextures[faceIdx]

        if(faceAlpha == -2):
            faceRenderType = 3

        if(faceAlpha == -1):
            faceRenderType = 2

        if(faceTexture == -1):
            if(faceRenderType != 0):
                if(faceRenderType == 1):
                    faceNormal = modelData.faceNormals[faceIdx]
                    var14 = integerdivide((var4 * faceNormal.y + var5 * faceNormal.z +
                                          var3 * faceNormal.x), (integerdivide(var7, 2) + var7)) + var1
                    model.field1852[faceIdx] = method2630(
                        modelData.faceColor[faceIdx] & 0xffff, var14)
                    model.field1862[faceIdx] = -1
                elif(faceRenderType == 3):
                    model.field1852[faceIdx] = 128
                    model.field1862[faceIdx] = -1
                else:
                    model.field1862[faceIdx] = -2

            else:

                var15 = modelData.faceColor[faceIdx] & 0xffff

                # is not None
                # is not None
                if(len(modelData.field1756) > 0 and modelData.field1756[modelData.trianglePointsX[faceIdx]].isNotNull):
                    vertexNormal = modelData.field1756[modelData.trianglePointsX[faceIdx]]
                else:
                    vertexNormal = modelData.normals[modelData.trianglePointsX[faceIdx]]

                var14 = integerdivide((var4 * vertexNormal.y + var5 * vertexNormal.z +
                                      var3 * vertexNormal.x),  (var7 * vertexNormal.magnitude)) + var1

                model.field1852[faceIdx] = method2630(var15, var14)

                # is not None
                # is not None):
                if(len(modelData.field1756) > 0 and modelData.field1756[modelData.trianglePointsY[faceIdx]].isNotNull):
                    vertexNormal = modelData.field1756[modelData.trianglePointsY[faceIdx]]
                else:
                    vertexNormal = modelData.normals[modelData.trianglePointsY[faceIdx]]

                var14 = integerdivide((var4 * vertexNormal.y + var5 * vertexNormal.z +
                                      var3 * vertexNormal.x), (var7 * vertexNormal.magnitude)) + var1
                model.field1861[faceIdx] = method2630(var15, var14)

                # is not None
                # is not None):
                if(len(modelData.field1756) > 0 and modelData.field1756[modelData.trianglePointsZ[faceIdx]].isNotNull):
                    vertexNormal = modelData.field1756[modelData.trianglePointsZ[faceIdx]]
                else:
                    vertexNormal = modelData.normals[modelData.trianglePointsZ[faceIdx]]

                var14 = integerdivide((var4 * vertexNormal.y + var5 * vertexNormal.z +
                                      var3 * vertexNormal.x), (var7 * vertexNormal.magnitude)) + var1
                model.field1862[faceIdx] = method2630(var15, var14)

        elif(faceRenderType != 0):
            if(faceRenderType == 1):
                faceNormal = modelData.faceNormals[faceIdx]
                var14 = integerdivide((var4 * faceNormal.y + var5 * faceNormal.z +
                                      var3 * faceNormal.x), (integerdivide(var7, 2) + var7)) + var1
                model.field1852[faceIdx] = method2622(var14)
                model.field1862[faceIdx] = -1
            else:
                model.field1862[faceIdx] = -2

        else:
            # is not None):
            if(len(modelData.field1756) > 0 and modelData.field1756[modelData.trianglePointsX[faceIdx]].isNotNull):
                vertexNormal = modelData.field1756[modelData.trianglePointsX[faceIdx]]
            else:
                vertexNormal = modelData.normals[modelData.trianglePointsX[faceIdx]]

            var14 = integerdivide((var4 * vertexNormal.y + var5 * vertexNormal.z +
                                  var3 * vertexNormal.x), (var7 * vertexNormal.magnitude)) + var1
            model.field1852[faceIdx] = method2622(var14)
            # is not None):
            if(len(modelData.field1756) > 0 and modelData.field1756[modelData.trianglePointsY[faceIdx]].isNotNull):
                vertexNormal = modelData.field1756[modelData.trianglePointsY[faceIdx]]
            else:
                vertexNormal = modelData.normals[modelData.trianglePointsY[faceIdx]]

            var14 = integerdivide((var4 * vertexNormal.y + var5 * vertexNormal.z +
                                  var3 * vertexNormal.x), (var7 * vertexNormal.magnitude)) + var1
            model.field1861[faceIdx] = method2622(var14)
            # is not None):
            if(len(modelData.field1756) > 0 and modelData.field1756[modelData.trianglePointsZ[faceIdx]].isNotNull):
                vertexNormal = modelData.field1756[modelData.trianglePointsZ[faceIdx]]
            else:
                vertexNormal = modelData.normals[modelData.trianglePointsZ[faceIdx]]

            var14 = integerdivide((var4 * vertexNormal.y + var5 * vertexNormal.z +
                                  var3 * vertexNormal.x), (var7 * vertexNormal.magnitude)) + var1
            model.field1862[faceIdx] = method2622(var14)

    computeAnimationTables(modelData)
    model.verticesCount = modelData.vertexCount
    model.verticesX = modelData.vertexX
    model.verticesY = modelData.vertexY
    model.verticesZ = modelData.vertexZ
    model.indicesCount = modelData.triangleFaceCount
    model.indices1 = modelData.trianglePointsX
    model.indices2 = modelData.trianglePointsY
    model.indices3 = modelData.trianglePointsZ
    model.faceRenderPriorities = modelData.faceRenderPriorities
    model.faceAplhas = modelData.faceAlphas
    model.priority = modelData.priority

    model.vertexGroups = modelData.vertexGroups
    model.field1890 = modelData.field1758
    model.faceTextures = modelData.faceTextures
    return model

@jit(nopython=True, cache=False)
def method2608(staticModelData, var0, var1, var2, var3, var4, var5):
    method2641(var0)
    computeNormals(var0)
    method2641(var1)
    computeNormals(var1)
    staticModelData.field1724 += 1
    var6 = 0
    var7 = var1.vertexX
    var8 = var1.vertexCount

    for var9 in range(0, var0.vertexCount):
        var10 = var0.normals[var9]
        if(var10.magnitude != 0):
            var11 = var0.vertexY[var9] - var3
            if(var11 <= var1.field1760):
                var12 = var0.vertexX[var9] - var2
                if(var12 >= var1.field1761 and var12 <= var1.field1762):
                    var13 = var0.vertexZ[var9] - var4
                    if(var13 >= var1.field1764 and var13 <= var1.field1763):
                        for var14 in range(0, var8):
                            var15 = var1.normals[var14]
                            if(var12 == var7[var14] and var13 == var1.vertexZ[var14] and var11 == var1.vertexY[var14] and var15.magnitude != 0):
                                if(len(var0.field1756) == 0):  # is None) :
                                    for i in range(0, var0.vertexCount):
                                        var0.field1756.append(
                                            expVertexNormal())
                                    #var0.field1756 = [None] * var0.vertexCount

                                if(len(var1.field1756) == 0):  # is None) :
                                    for i in range(0, var8):
                                        var1.field1756.append(
                                            expVertexNormal())
                                    #var1.field1756 = [None] * var8

                                var16 = var0.field1756[var9]
                                var16.copyFrom(var10)
                                # if(var16 is None) :
                                #    var16 = expVertexNormal(var10)
                                #    var0.field1756[var9] = var16

                                var17 = var1.field1756[var14]
                                var17.copyFrom(var15)
                                # if(var17 is None) :
                                #    var17 = expVertexNormal(var15)
                                #    var1.field1756[var14] = var17

                                var16.x += var15.x
                                var16.y += var15.y
                                var16.z += var15.z
                                var16.magnitude += var15.magnitude
                                var16.isNotNull = var15.isNotNull

                                var17.x += var10.x
                                var17.y += var10.y
                                var17.z += var10.z
                                var17.magnitude += var10.magnitude
                                var17.isNotNull = var10.isNotNull

                                var6 += 1
                                staticModelData.field1765[var9] = staticModelData.field1724
                                staticModelData.field1753[var14] = staticModelData.field1724

    if(var6 >= 3 and var5):
        for var9 in range(0, var0.triangleFaceCount):
            if(staticModelData.field1765[var0.trianglePointsX[var9]] == staticModelData.field1724 and staticModelData.field1765[var0.trianglePointsY[var9]] == staticModelData.field1724 and staticModelData.field1765[var0.trianglePointsZ[var9]] == staticModelData.field1724):
                if(var0.faceRenderTypes.size == 0):  # is None) :
                    # new byte[var0.triangleFaceCount]
                    var0.faceRenderTypes = np.zeros(
                        shape=(var0.triangleFaceCount), dtype=np.byte)

                var0.faceRenderTypes[var9] = 2

    for var9 in range(0, var1.triangleFaceCount):
        if(staticModelData.field1724 == staticModelData.field1753[var1.trianglePointsX[var9]] and staticModelData.field1724 == staticModelData.field1753[var1.trianglePointsY[var9]] and staticModelData.field1724 == staticModelData.field1753[var1.trianglePointsZ[var9]]):
            if(var1.faceRenderTypes.size == 0):  # is None) :
                # new byte[var1.triangleFaceCount]
                var1.faceRenderTypes = np.zeros(
                    shape=(var1.triangleFaceCount), dtype=np.byte)

            var1.faceRenderTypes[var9] = 2


@jit(nopython=True, cache=False)
def method2630(var0, var1):
    var1 = (var0 & 127) * var1 >> 7
    if(var1 < 2):
        var1 = 2
    elif(var1 > 126):
        var1 = 126

    return (var0 & 65408) + var1


@jit(nopython=True, cache=False)
def method2622(var0):
    if(var0 < 2):
        var0 = 2
    elif(var0 > 126):
        var0 = 126

    return var0


@jit(nopython=True, cache=False)
def computeNormals(modelData):

    #  is None
    if(len(modelData.normals) == 0):

        #modelData.normals = [None] * modelData.vertexCount
        for vertexIdx in range(0, modelData.vertexCount):
            #modelData.normals[vertexIdx] = expVertexNormal()
            modelData.normals.append(expVertexNormal())

        for faceIdx in range(0, modelData.triangleFaceCount):
            pointX = modelData.trianglePointsX[faceIdx]
            pointY = modelData.trianglePointsY[faceIdx]
            pointZ = modelData.trianglePointsZ[faceIdx]
            var5 = modelData.vertexX[pointY] - modelData.vertexX[pointX]
            var6 = modelData.vertexY[pointY] - modelData.vertexY[pointX]
            var7 = modelData.vertexZ[pointY] - modelData.vertexZ[pointX]
            var8 = modelData.vertexX[pointZ] - modelData.vertexX[pointX]
            var9 = modelData.vertexY[pointZ] - modelData.vertexY[pointX]
            var10 = modelData.vertexZ[pointZ] - modelData.vertexZ[pointX]
            x = var6 * var10 - var9 * var7
            y = var7 * var8 - var10 * var5

            z = np.int32(var5 * var9 - var8 * var6)
            while x > 8192 or y > 8192 or z > 8192 or x < -8192 or y < -8192 or z < -8192:
                x >>= 1
                y >>= 1
                z >>= 1

            var14 = np.int32(math.sqrt(x * x + y * y + z * z))
            if(var14 <= 0):
                var14 = 1

            x = integerdivide(x * 256, var14)
            y = integerdivide(y * 256, var14)
            z = integerdivide(z * 256, var14)

            # is None
            if(modelData.faceRenderTypes.size == 0):
                faceRenderType = 0
            else:
                faceRenderType = modelData.faceRenderTypes[faceIdx]

            if(faceRenderType == 0):
                vertexNormal = modelData.normals[pointX]
                vertexNormal.x += x
                vertexNormal.y += y
                vertexNormal.z += z
                vertexNormal.magnitude += 1
                vertexNormal.isNotNull = True
                vertexNormal = modelData.normals[pointY]
                vertexNormal.x += x
                vertexNormal.y += y
                vertexNormal.z += z
                vertexNormal.magnitude += 1
                vertexNormal.isNotNull = True
                vertexNormal = modelData.normals[pointZ]
                vertexNormal.x += x
                vertexNormal.y += y
                vertexNormal.z += z
                vertexNormal.magnitude += 1
                vertexNormal.isNotNull = True
            elif(faceRenderType == 1):

                # is None
                if(len(modelData.faceNormals) == 0):
                    for faceIdx in range(0, modelData.triangleFaceCount):
                        modelData.faceNormals.append(expFaceNormal())

                #modelData.faceNormals[faceIdx] = expFaceNormal()
                faceNormal = modelData.faceNormals[faceIdx]
                faceNormal.x = x
                faceNormal.y = y
                faceNormal.z = z


# @jit(nopython=True, cache=False)
# def decodeOldModelFormat(id, var1):

#     model = ModelData()
#     model.id = id

#     var2 = False
#     var43 = False
#     var5 = Buffer(var1)
#     var39 = Buffer(var1)
#     var26 = Buffer(var1)
#     var9 = Buffer(var1)
#     var3 = Buffer(var1)
#     var5.offset = len(var1) - 18

#     var10 = var5.readUnsignedShort()
#     var11 = var5.readUnsignedShort()
#     var12 = var5.readUnsignedByte()

#     var13 = var5.readUnsignedByte()
#     var14 = var5.readUnsignedByte()
#     var30 = var5.readUnsignedByte()
#     var15 = var5.readUnsignedByte()
#     var28 = var5.readUnsignedByte()
#     var27 = var5.readUnsignedShort()
#     var20 = var5.readUnsignedShort()
#     var36 = var5.readUnsignedShort()
#     var23 = var5.readUnsignedShort()

#     var16 = 0
#     var46 = var16 + var10
#     var24 = var46
#     var46 += var11
#     var25 = var46
#     if (var14 == 255):
#         var46 += var11

#     var4 = var46
#     if (var15 == 1):
#         var46 += var11

#     var42 = var46
#     if (var13 == 1):
#         var46 += var11

#     var37 = var46
#     if (var28 == 1):
#         var46 += var10

#     var29 = var46
#     if (var30 == 1):
#         var46 += var11

#     var44 = var46
#     var46 += var23
#     var17 = var46
#     var46 += var11 * 2
#     var32 = var46
#     var46 += var12 * 6
#     var34 = var46
#     var46 += var27
#     var35 = var46
#     var46 += var20
#     var10000 = var46 + var36
#     model.vertexCount = var10
#     model.triangleFaceCount = var11
#     model.field1738 = var12

#     model.vertexX = np.zeros(shape=(var10), dtype=np.int32)
#     model.vertexY = np.zeros(shape=(var10), dtype=np.int32)
#     model.vertexZ = np.zeros(shape=(var10), dtype=np.int32)
#     model.trianglePointsX = np.zeros(shape=(var11), dtype=np.int32)
#     model.trianglePointsY = np.zeros(shape=(var11), dtype=np.int32)
#     model.trianglePointsZ = np.zeros(shape=(var11), dtype=np.int32)
#     if (var12 > 0):
#         model.textureRenderTypes = np.zeros(shape=(var12), dtype=np.byte)
#         model.texTriangleX = np.zeros(shape=(var12), dtype=np.short)
#         model.texTriangleY = np.zeros(shape=(var12), dtype=np.short)
#         model.texTriangleZ = np.zeros(shape=(var12), dtype=np.short)

#     if (var28 == 1):
#         model.vertexSkins = np.zeros(shape=(var10), dtype=np.int32)

#     if (var13 == 1):
#         model.faceRenderTypes = np.zeros(shape=(var11), dtype=np.byte)
#         model.textureCoords = np.zeros(shape=(var11), dtype=np.byte)
#         model.faceTextures = np.zeros(shape=(var11), dtype=np.short)

#     if (var14 == 255):
#         model.faceRenderPriorities = np.zeros(shape=(var11), dtype=np.byte)
#     else:
#         model.priority = np.byte(var14)

#     if (var30 == 1):
#         model.faceAlphas = np.zeros(shape=(var11), dtype=np.byte)

#     if (var15 == 1):
#         model.triangleSkinValues = np.zeros(shape=(var11), dtype=np.int32)

#     model.faceColor = np.zeros(shape=(var11), dtype=np.short)
#     var5.setOffset(var16)
#     var39.setOffset(var34)
#     var26.setOffset(var35)
#     var9.setOffset(var46)
#     var3.setOffset(var37)
#     var41 = 0
#     var33 = 0
#     var19 = 0

#     for var18 in range(0, var10):
#         var8 = var5.readUnsignedByte()
#         var31 = 0
#         if ((var8 & 1) != 0):
#             var31 = var39.readShortSmart()

#         var6 = 0
#         if ((var8 & 2) != 0):
#             var6 = var26.readShortSmart()

#         var7 = 0
#         if ((var8 & 4) != 0):
#             var7 = var9.readShortSmart()

#         model.vertexX[var18] = var41 + var31
#         model.vertexY[var18] = var33 + var6
#         model.vertexZ[var18] = var19 + var7
#         var41 = model.vertexX[var18]
#         var33 = model.vertexY[var18]
#         var19 = model.vertexZ[var18]
#         if (var28 == 1):
#             model.vertexSkins[var18] = var3.readUnsignedByte()

#     var5.setOffset(var17)
#     var39.setOffset(var42)
#     var26.setOffset(var25)
#     var9.setOffset(var29)
#     var3.setOffset(var4)

#     for var18 in range(var11):
#         model.faceColor[var18] = var5.readUnsignedShort()
#         if (var13 == 1):
#             var8 = var39.readUnsignedByte()
#             if ((var8 & 1) == 1):
#                 model.faceRenderTypes[var18] = 1
#                 var2 = True

#             else:
#                 model.faceRenderTypes[var18] = 0

#             if ((var8 & 2) == 2):
#                 model.textureCoords[var18] = np.byte(var8 >> 2)
#                 model.faceTextures[var18] = model.faceColor[var18]
#                 model.faceColor[var18] = 127
#                 if (model.faceTextures[var18] != -1):
#                     var43 = True

#             else:
#                 model.textureCoords[var18] = -1
#                 model.faceTextures[var18] = -1

#         if (var14 == 255):
#             model.faceRenderPriorities[var18] = var26.readByte()

#         if (var30 == 1):
#             model.faceAlphas[var18] = var9.readByte()

#         if (var15 == 1):
#             model.triangleSkinValues[var18] = var3.readUnsignedByte()

#     var5.setOffset(var44)
#     var39.setOffset(var24)
#     var18 = 0
#     var8 = 0
#     var31 = 0
#     var6 = 0

#     for var7 in range(var11):
#         var43_ = var39.readUnsignedByte()
#         if (var43_ == 1):
#             var18 = var5.readShortSmart() + var6
#             var8 = var5.readShortSmart() + var18
#             var31 = var5.readShortSmart() + var8
#             var6 = var31
#             model.trianglePointsX[var7] = var18
#             model.trianglePointsY[var7] = var8
#             model.trianglePointsZ[var7] = var31

#         elif (var43_ == 2):
#             var8 = var31
#             var31 = var5.readShortSmart() + var6
#             var6 = var31
#             model.trianglePointsX[var7] = var18
#             model.trianglePointsY[var7] = var8
#             model.trianglePointsZ[var7] = var31

#         elif (var43_ == 3):
#             var18 = var31
#             var31 = var5.readShortSmart() + var6
#             var6 = var31
#             model.trianglePointsX[var7] = var18
#             model.trianglePointsY[var7] = var8
#             model.trianglePointsZ[var7] = var31

#         elif (var43_ == 4):
#             var44_ = var18
#             var18 = var8
#             var8 = var44_
#             var31 = var5.readShortSmart() + var6
#             var6 = var31
#             model.trianglePointsX[var7] = var18
#             model.trianglePointsY[var7] = var44_
#             model.trianglePointsZ[var7] = var31

#     var5.setOffset(var32)

#     for var7 in range(var12):
#         model.textureRenderTypes[var7] = 0
#         model.texTriangleX[var7] = np.short(var5.readUnsignedShort())
#         model.texTriangleY[var7] = np.short(var5.readUnsignedShort())
#         model.texTriangleZ[var7] = np.short(var5.readUnsignedShort())

#     if (model.textureCoords.size > 0):  # is not None

#         var45 = False
#         for var43_ in range(0, var11):
#             var44_ = model.textureCoords[var43_] & 255
#             if (var44_ != 255):
#                 if ((model.trianglePointsX[var43_]) == model.texTriangleX[var44_] & 0xffff
#                     and (model.trianglePointsY[var43_]) == model.texTriangleY[var44_] & 0xffff
#                         and (model.trianglePointsZ[var43_]) == model.texTriangleZ[var44_] & 0xffff):
#                     model.textureCoords[var43_] = -1

#                 else:
#                     var45 = True

#         if (not var45):
#             model.textureCoords = np.empty(shape=(0), dtype=np.byte)  # None

#     if (not var43):
#         model.faceTextures = np.empty(shape=(0), dtype=np.short)  # None

#     if (not var2):
#         model.faceRenderTypes = np.empty(shape=(0), dtype=np.byte)  # None

#     return model


# @jit(nopython=True, cache=False)
# def decodeOldModelFormatEfficient(id, var1):

#     model = ModelData()
#     model.id = id

#     var2 = False
#     var43 = False
#     #var5 = Buffer(var1)
#     #var39 = Buffer(var1)
#     #var26 = Buffer(var1)
#     #var9 = Buffer(var1)
#     #var3 = Buffer(var1)

#     var5index = len(var1) - 18  # var5.offset = len(var1) - 18

#     var10, var5index = readUnsignedShort(var1, var5index)
#     var11, var5index = readUnsignedShort(var1, var5index)
#     var12, var5index = readUnsignedByte(var1, var5index)

#     var13, var5index = readUnsignedByte(var1, var5index)
#     var14, var5index = readUnsignedByte(var1, var5index)
#     var30, var5index = readUnsignedByte(var1, var5index)
#     var15, var5index = readUnsignedByte(var1, var5index)
#     var28, var5index = readUnsignedByte(var1, var5index)
#     var27, var5index = readUnsignedShort(var1, var5index)
#     var20, var5index = readUnsignedShort(var1, var5index)
#     var36, var5index = readUnsignedShort(var1, var5index)
#     var23, var5index = readUnsignedShort(var1, var5index)

#     var16 = 0
#     var46 = var16 + var10
#     var24 = var46
#     var46 += var11
#     var25 = var46
#     if (var14 == 255):
#         var46 += var11

#     var4 = var46
#     if (var15 == 1):
#         var46 += var11

#     var42 = var46
#     if (var13 == 1):
#         var46 += var11

#     var37 = var46
#     if (var28 == 1):
#         var46 += var10

#     var29 = var46
#     if (var30 == 1):
#         var46 += var11

#     var44 = var46
#     var46 += var23
#     var17 = var46
#     var46 += var11 * 2
#     var32 = var46
#     var46 += var12 * 6
#     var34 = var46
#     var46 += var27
#     var35 = var46
#     var46 += var20
#     var10000 = var46 + var36
#     model.vertexCount = var10
#     model.triangleFaceCount = var11
#     model.field1738 = var12

#     model.vertexX = np.zeros(shape=(var10), dtype=np.int32)
#     model.vertexY = np.zeros(shape=(var10), dtype=np.int32)
#     model.vertexZ = np.zeros(shape=(var10), dtype=np.int32)
#     model.trianglePointsX = np.zeros(shape=(var11), dtype=np.int32)
#     model.trianglePointsY = np.zeros(shape=(var11), dtype=np.int32)
#     model.trianglePointsZ = np.zeros(shape=(var11), dtype=np.int32)
#     if (var12 > 0):
#         model.textureRenderTypes = np.zeros(shape=(var12), dtype=np.byte)
#         model.texTriangleX = np.zeros(shape=(var12), dtype=np.short)
#         model.texTriangleY = np.zeros(shape=(var12), dtype=np.short)
#         model.texTriangleZ = np.zeros(shape=(var12), dtype=np.short)

#     if (var28 == 1):
#         model.vertexSkins = np.zeros(shape=(var10), dtype=np.int32)

#     if (var13 == 1):
#         model.faceRenderTypes = np.zeros(shape=(var11), dtype=np.byte)
#         model.textureCoords = np.zeros(shape=(var11), dtype=np.byte)
#         model.faceTextures = np.zeros(shape=(var11), dtype=np.short)

#     if (var14 == 255):
#         model.faceRenderPriorities = np.zeros(shape=(var11), dtype=np.byte)
#     else:
#         model.priority = np.byte(var14)

#     if (var30 == 1):
#         model.faceAlphas = np.zeros(shape=(var11), dtype=np.byte)

#     if (var15 == 1):
#         model.triangleSkinValues = np.zeros(shape=(var11), dtype=np.int32)

#     model.faceColor = np.zeros(shape=(var11), dtype=np.short)
#     var5index = var16  # var5.setOffset(var16)

#     var39index = var34  # var39.setOffset(var34)
#     var26index = var35  # var26.setOffset(var35)
#     var9index = var46  # var9.setOffset(var46)
#     var3index = var37  # var3.setOffset(var37)
#     var41 = 0
#     var33 = 0
#     var19 = 0

#     for var18 in range(0, var10):
#         var8, var5index = readUnsignedByte(var1, var5index)
#         var31 = 0
#         if ((var8 & 1) != 0):
#             var31, var39index = readShortSmart(var1, var39index)

#         var6 = 0
#         if ((var8 & 2) != 0):
#             var6, var26index = readShortSmart(var1, var26index)

#         var7 = 0
#         if ((var8 & 4) != 0):
#             var7, var9index = readShortSmart(var1, var9index)

#         model.vertexX[var18] = var41 + var31
#         model.vertexY[var18] = var33 + var6
#         model.vertexZ[var18] = var19 + var7
#         var41 = model.vertexX[var18]
#         var33 = model.vertexY[var18]
#         var19 = model.vertexZ[var18]
#         if (var28 == 1):
#             model.vertexSkins[var18], var3index = readUnsignedByte(
#                 var1, var3index)

#     var5index = var17  # var5.setOffset(var17)
#     var39index = var42  # var39.setOffset(var42)
#     var26index = var25  # var26.setOffset(var25)
#     var9index = var29  # var9.setOffset(var29)
#     var3index = var4  # var3.setOffset(var4)

#     for var18 in range(var11):
#         var9999, var5index = readUnsignedShort(var1, var5index)
#         model.faceColor[var18] = np.short(var9999)
#         if (var13 == 1):
#             var8, var39index = readUnsignedByte(var1, var39index)
#             if ((var8 & 1) == 1):
#                 model.faceRenderTypes[var18] = 1
#                 var2 = True

#             else:
#                 model.faceRenderTypes[var18] = 0

#             if ((var8 & 2) == 2):
#                 model.textureCoords[var18] = np.byte(var8 >> 2)
#                 model.faceTextures[var18] = model.faceColor[var18]
#                 model.faceColor[var18] = 127
#                 if (model.faceTextures[var18] != -1):
#                     var43 = True

#             else:
#                 model.textureCoords[var18] = -1
#                 model.faceTextures[var18] = -1

#         if (var14 == 255):
#             model.faceRenderPriorities[var18], var26index = readByte(
#                 var1, var26index)

#         if (var30 == 1):
#             model.faceAlphas[var18], var9index = readByte(var1, var9index)

#         if (var15 == 1):
#             model.triangleSkinValues[var18], var3index = readUnsignedByte(
#                 var1, var3index)

#     var5index = var44  # var5.setOffset(var44)
#     var39index = var24  # var39.setOffset(var24)
#     var18 = 0
#     var8 = 0
#     var31 = 0
#     var6 = 0

#     for var7 in range(var11):
#         var43_, var39index = readUnsignedByte(var1, var39index)
#         if (var43_ == 1):
#             var18, var5index = readShortSmart(var1, var5index)  # + var6
#             var18 += var6
#             var8, var5index = readShortSmart(var1, var5index)  # + var18
#             var8 += var18
#             var31, var5index = readShortSmart(var1, var5index)  # + var8
#             var31 += var8
#             var6 = var31
#             model.trianglePointsX[var7] = var18
#             model.trianglePointsY[var7] = var8
#             model.trianglePointsZ[var7] = var31

#         elif (var43_ == 2):
#             var8 = var31
#             var31, var5index = readShortSmart(var1, var5index)  # + var6
#             var31 += var6
#             var6 = var31
#             model.trianglePointsX[var7] = var18
#             model.trianglePointsY[var7] = var8
#             model.trianglePointsZ[var7] = var31

#         elif (var43_ == 3):
#             var18 = var31
#             var31, var5index = readShortSmart(var1, var5index)  # + var6
#             var31 += var6
#             var6 = var31
#             model.trianglePointsX[var7] = var18
#             model.trianglePointsY[var7] = var8
#             model.trianglePointsZ[var7] = var31

#         elif (var43_ == 4):
#             var44_ = var18
#             var18 = var8
#             var8 = var44_
#             var31, var5index = readShortSmart(var1, var5index)  # + var6
#             var31 += var6
#             var6 = var31
#             model.trianglePointsX[var7] = var18
#             model.trianglePointsY[var7] = var44_
#             model.trianglePointsZ[var7] = var31

#     var5index = var32  # var5.setOffset(var32)

#     for var7 in range(var12):
#         model.textureRenderTypes[var7] = 0
#         model.texTriangleX[var7], var5index = readUnsignedShort(
#             var1, var5index)  # np.short
#         model.texTriangleY[var7], var5index = readUnsignedShort(
#             var1, var5index)  # np.short
#         model.texTriangleZ[var7], var5index = readUnsignedShort(
#             var1, var5index)  # np.short

#     if (model.textureCoords.size != 0):  # is not None

#         var45 = False
#         for var43_ in range(0, var11):
#             var44_ = model.textureCoords[var43_] & 255
#             if (var44_ != 255):
#                 if (model.trianglePointsX[var43_] == (model.texTriangleX[var44_] & 0xffff)
#                     and model.trianglePointsY[var43_] == (model.texTriangleY[var44_] & 0xffff)
#                         and model.trianglePointsZ[var43_] == (model.texTriangleZ[var44_] & 0xffff)):
#                     model.textureCoords[var43_] = -1

#                 else:
#                     var45 = True

#         if (not var45):
#             model.textureCoords = np.empty(shape=(0), dtype=np.byte)  # None

#     if (not var43):
#         model.faceTextures = np.empty(shape=(0), dtype=np.short)  # None

#     if (not var2):
#         model.faceRenderTypes = np.empty(shape=(0), dtype=np.byte)  # None

#     return model


# @jit(nopython=True, cache=False)
# def decodeNewModelFormatEfficient(id, var1):

#     model = ModelData()
#     model.id = id

#     #var2 = Buffer(var1)
#     #var3 = Buffer(var1)
#     #var4 = Buffer(var1)
#     #var5 = Buffer(var1)
#     #var6 = Buffer(var1)
#     #var7 = Buffer(var1)
#     #var8 = Buffer(var1)

#     var2index = len(var1) - 23  # var2.offset = len(var1) - 23
#     var9, var2index = readUnsignedShort(var1, var2index)
#     var10, var2index = readUnsignedShort(var1, var2index)
#     var11, var2index = readUnsignedByte(var1, var2index)
#     var12, var2index = readUnsignedByte(var1, var2index)
#     var13, var2index = readUnsignedByte(var1, var2index)
#     var14, var2index = readUnsignedByte(var1, var2index)
#     var15, var2index = readUnsignedByte(var1, var2index)
#     var16, var2index = readUnsignedByte(var1, var2index)
#     var17, var2index = readUnsignedByte(var1, var2index)
#     var18, var2index = readUnsignedShort(var1, var2index)
#     var19, var2index = readUnsignedShort(var1, var2index)
#     var20, var2index = readUnsignedShort(var1, var2index)
#     var21, var2index = readUnsignedShort(var1, var2index)
#     var22, var2index = readUnsignedShort(var1, var2index)
#     var23 = 0
#     var24 = 0
#     var25 = 0
#     if(var11 > 0):
#         model.textureRenderTypes = np.empty(shape=(var11), dtype=np.byte)
#         var2index = 0  # var2.offset = 0

#         for var26 in range(0, var11):
#             var27, var2index = readByte(var1, var2index)
#             model.textureRenderTypes[var26] = var27
#             if(var27 == 0):
#                 var23 += 1

#             if(var27 >= 1 and var27 <= 3):
#                 var24 += 1

#             if(var27 == 2):
#                 var25 += 1

#     var26 = var11 + var9
#     var28 = var26
#     if(var12 == 1):
#         var26 += var10

#     var29 = var26
#     var26 += var10
#     var30 = var26
#     if(var13 == 255):
#         var26 += var10

#     var31 = var26
#     if(var15 == 1):
#         var26 += var10

#     var32 = var26
#     if(var17 == 1):
#         var26 += var9

#     var33 = var26
#     if(var14 == 1):
#         var26 += var10

#     var34 = var26
#     var26 += var21
#     var35 = var26
#     if(var16 == 1):
#         var26 += var10 * 2

#     var36 = var26
#     var26 += var22
#     var37 = var26
#     var26 += var10 * 2
#     var38 = var26
#     var26 += var18
#     var39 = var26
#     var26 += var19
#     var40 = var26
#     var26 += var20
#     var41 = var26
#     var26 += var23 * 6
#     var42 = var26
#     var26 += var24 * 6
#     var43 = var26
#     var26 += var24 * 6
#     var44 = var26
#     var26 += var24 * 2
#     var45 = var26
#     var26 += var24
#     var46 = var26
#     var26 += var24 * 2 + var25 * 2
#     model.vertexCount = var9
#     model.triangleFaceCount = var10
#     model.field1738 = var11
#     model.vertexX = np.empty(shape=(var9), dtype=np.int32)
#     model.vertexY = np.empty(shape=(var9), dtype=np.int32)
#     model.vertexZ = np.empty(shape=(var9), dtype=np.int32)
#     model.trianglePointsX = np.zeros(shape=(var10), dtype=np.int32)
#     model.trianglePointsY = np.zeros(shape=(var10), dtype=np.int32)
#     model.trianglePointsZ = np.zeros(shape=(var10), dtype=np.int32)
#     if(var17 == 1):
#         model.vertexSkins = np.zeros(shape=(var9), dtype=np.int32)

#     if(var12 == 1):
#         model.faceRenderTypes = np.zeros(shape=(var10), dtype=np.byte)

#     if(var13 == 255):
#         model.faceRenderPriorities = np.zeros(shape=(var10), dtype=np.byte)
#     else:
#         model.priority = np.byte(var13)

#     if(var14 == 1):
#         model.faceAlphas = np.zeros(shape=(var10), dtype=np.byte)

#     if(var15 == 1):
#         model.triangleSkinValues = np.zeros(shape=(var10), dtype=np.int32)

#     if(var16 == 1):
#         model.faceTextures = np.zeros(shape=(var10), dtype=np.short)

#     if(var16 == 1 and var11 > 0):
#         model.textureCoords = np.zeros(shape=(var10), dtype=np.byte)

#     model.faceColor = np.zeros(shape=(var10), dtype=np.short)
#     if(var11 > 0):
#         model.texTriangleX = np.zeros(shape=(var11), dtype=np.short)
#         model.texTriangleY = np.zeros(shape=(var11), dtype=np.short)
#         model.texTriangleZ = np.zeros(shape=(var11), dtype=np.short)
#         if(var24 > 0):
#             model.field1743 = np.zeros(shape=(var24), dtype=np.short)
#             model.field1745 = np.zeros(shape=(var24), dtype=np.short)
#             model.field1740 = np.zeros(shape=(var24), dtype=np.short)
#             model.field1746 = np.zeros(shape=(var24), dtype=np.short)
#             model.field1749 = np.zeros(shape=(var24), dtype=np.byte)
#             model.field1747 = np.zeros(shape=(var24), dtype=np.short)

#         if(var25 > 0):
#             model.texturePrimaryColor = np.zeros(shape=(var25), dtype=np.short)

#     var2index = var11  # var2.offset = var11

#     var3index = var38
#     var4index = var39
#     var5index = var40
#     var6index = var32

#     #var3.offset = var38
#     #var4.offset = var39
#     #var5.offset = var40
#     #var6.offset = var32
#     var48 = 0
#     var49 = 0
#     var50 = 0

#     for var51 in range(0, var9):
#         var52, var2index = readUnsignedByte(var1, var2index)
#         var53 = 0
#         if((var52 & 1) != 0):
#             var53, var3index = readShortSmart(var1, var3index)

#         var54 = 0
#         if((var52 & 2) != 0):
#             var54, var4index = readShortSmart(var1, var4index)

#         var55 = 0
#         if((var52 & 4) != 0):
#             var55, var5index = readShortSmart(var1, var5index)

#         model.vertexX[var51] = var48 + var53
#         model.vertexY[var51] = var49 + var54
#         model.vertexZ[var51] = var50 + var55
#         var48 = model.vertexX[var51]
#         var49 = model.vertexY[var51]
#         var50 = model.vertexZ[var51]
#         if(var17 == 1):
#             model.vertexSkins[var51], var6index = readUnsignedByte(
#                 var1, var6index)

#     var2index = var37  # var2.offset = var37
#     # var3.offset = var28
#     # var4.offset = var30
#     # var5.offset = var33
#     # var6.offset = var31
#     # var7.offset = var35
#     # var8.offset = var36
#     var3index = var28
#     var4index = var30
#     var5index = var33
#     var6index = var31
#     var7index = var35
#     var8index = var36

#     for var51 in range(0, var10):
#         model.faceColor[var51], var2index = readUnsignedShort(var1, var2index)
#         if(var12 == 1):
#             model.faceRenderTypes[var51], var3index = readByte(var1, var3index)

#         if(var13 == 255):
#             model.faceRenderPriorities[var51], var4index = readByte(
#                 var1, var4index)

#         if(var14 == 1):
#             model.faceAlphas[var51], var5index = readByte(var1, var5index)

#         if(var15 == 1):
#             model.triangleSkinValues[var51], var6index = readUnsignedByte(
#                 var1, var6index)

#         if(var16 == 1):
#             var9999, var7index = readUnsignedShort(var1, var7index)
#             model.faceTextures[var51] = np.short(var9999 - 1)

#         # is not None
#         if(model.textureCoords.size > 0 and model.faceTextures[var51] != -1):
#             var9999, var8index = readUnsignedByte(var1, var8index)
#             model.textureCoords[var51] = np.byte(var9999 - 1)

#     var2index = var34  # var2.offset = var34
#     var3index = var29  # var3.offset = var29
#     var51 = 0
#     var52 = 0
#     var53 = 0
#     var54 = 0

#     for var55 in range(0, var10):
#         var56, var3index = readUnsignedByte(var1, var3index)
#         if(var56 == 1):
#             var51, var2index = readShortSmart(var1, var2index)  # + var54
#             var51 += var54
#             var52, var2index = readShortSmart(var1, var2index)  # + var51
#             var52 += var51
#             var53, var2index = readShortSmart(var1, var2index)  # + var52
#             var53 += var52
#             var54 = var53
#             model.trianglePointsX[var55] = var51
#             model.trianglePointsY[var55] = var52
#             model.trianglePointsZ[var55] = var53

#         elif(var56 == 2):
#             var52 = var53
#             var53, var2index = readShortSmart(var1, var2index)  # + var54
#             var53 += var54
#             var54 = var53
#             model.trianglePointsX[var55] = var51
#             model.trianglePointsY[var55] = var52
#             model.trianglePointsZ[var55] = var53

#         elif(var56 == 3):
#             var51 = var53
#             var53, var2index = readShortSmart(var1, var2index)  # + var54
#             var53 += var54
#             var54 = var53
#             model.trianglePointsX[var55] = var51
#             model.trianglePointsY[var55] = var52
#             model.trianglePointsZ[var55] = var53

#         elif(var56 == 4):
#             var57 = var51
#             var51 = var52
#             var52 = var57
#             var53, var2index = readShortSmart(var1, var2index)  # + var54
#             var53 += var54
#             var54 = var53
#             model.trianglePointsX[var55] = var51
#             model.trianglePointsY[var55] = var57
#             model.trianglePointsZ[var55] = var53

#         else:
#             raise Exception("huh?")

#     var2index = var41  # var2.offset = var41
#     # var3.offset = var42
#     # var4.offset = var43
#     # var5.offset = var44
#     # var6.offset = var45
#     # var7.offset = var46
#     var3index = var42
#     var4index = var43
#     var5index = var44
#     var6index = var45
#     var7index = var46

#     for var55 in range(0, var11):
#         var56 = model.textureRenderTypes[var55] & 255
#         if(var56 == 0):
#             model.texTriangleX[var55], var2index = readUnsignedShort(
#                 var1, var2index)
#             model.texTriangleY[var55], var2index = readUnsignedShort(
#                 var1, var2index)
#             model.texTriangleZ[var55], var2index = readUnsignedShort(
#                 var1, var2index)

#         elif(var56 == 1):
#             model.texTriangleX[var55], var3index = readUnsignedShort(
#                 var1, var3index)
#             model.texTriangleY[var55], var3index = readUnsignedShort(
#                 var1, var3index)
#             model.texTriangleZ[var55], var3index = readUnsignedShort(
#                 var1, var3index)
#             model.field1743[var55], var4index = readUnsignedShort(
#                 var1, var4index)
#             model.field1745[var55], var4index = readUnsignedShort(
#                 var1, var4index)
#             model.field1740[var55], var4index = readUnsignedShort(
#                 var1, var4index)
#             model.field1746[var55], var5index = readUnsignedShort(
#                 var1, var5index)
#             model.field1749[var55], var6index = readByte(var1, var6index)
#             model.field1747[var55], var7index = readUnsignedShort(
#                 var1, var7index)

#         elif(var56 == 2):
#             model.texTriangleX[var55], var3index = readUnsignedShort(
#                 var1, var3index)
#             model.texTriangleY[var55], var3index = readUnsignedShort(
#                 var1, var3index)
#             model.texTriangleZ[var55], var3index = readUnsignedShort(
#                 var1, var3index)
#             model.field1743[var55], var4index = readUnsignedShort(
#                 var1, var4index)
#             model.field1745[var55], var4index = readUnsignedShort(
#                 var1, var4index)
#             model.field1740[var55], var4index = readUnsignedShort(
#                 var1, var4index)
#             model.field1746[var55], var5index = readUnsignedShort(
#                 var1, var5index)
#             model.field1749[var55], var6index = readByte(var1, var6index)
#             model.field1747[var55], var7index = readUnsignedShort(
#                 var1, var7index)
#             model.texturePrimaryColor[var55], var7index = readUnsignedShort(
#                 var1, var7index)

#         elif(var56 == 3):
#             model.texTriangleX[var55], var3index = readUnsignedShort(
#                 var1, var3index)
#             model.texTriangleY[var55], var3index = readUnsignedShort(
#                 var1, var3index)
#             model.texTriangleZ[var55], var3index = readUnsignedShort(
#                 var1, var3index)
#             model.field1743[var55], var4index = readUnsignedShort(
#                 var1, var4index)
#             model.field1745[var55], var4index = readUnsignedShort(
#                 var1, var4index)
#             model.field1740[var55], var4index = readUnsignedShort(
#                 var1, var4index)
#             model.field1746[var55], var5index = readUnsignedShort(
#                 var1, var5index)
#             model.field1749[var55], var6index = readByte(var1, var6index)
#             model.field1747[var55], var7index = readUnsignedShort(
#                 var1, var7index)

#     var2index = var26  # var2.offset = var26
#     var55, var2index = readUnsignedByte(var1, var2index)
#     if(var55 != 0):
#         # new class138(var1) Literally why
#         l, _ = readUnsignedShort(var1, var2index)
#         l, _ = readUnsignedShort(var1, var2index)
#         l, _ = readUnsignedShort(var1, var2index)
#         l, _ = readInt(var1, var2index)

#     return model


# @jit(nopython=True, cache=False)
# def exploadModel(modelId, bffr):

#     if (bffr[len(bffr) - 1] == -1 and bffr[len(bffr) - 2] == -1):
#         model = decodeNewModelFormatEfficient(modelId, bffr)
#     else:
#         model = decodeOldModelFormatEfficient(modelId, bffr)

#     return model


# @jit(nopython=True, cache=False)
# def decodeNewModelFormat(id, var1):

#     model = ModelData()
#     model.id = id

#     var2 = Buffer(var1)
#     var3 = Buffer(var1)
#     var4 = Buffer(var1)
#     var5 = Buffer(var1)
#     var6 = Buffer(var1)
#     var7 = Buffer(var1)
#     var8 = Buffer(var1)
#     var2.offset = len(var1) - 23
#     var9 = var2.readUnsignedShort()
#     var10 = var2.readUnsignedShort()
#     var11 = var2.readUnsignedByte()
#     var12 = var2.readUnsignedByte()
#     var13 = var2.readUnsignedByte()
#     var14 = var2.readUnsignedByte()
#     var15 = var2.readUnsignedByte()
#     var16 = var2.readUnsignedByte()
#     var17 = var2.readUnsignedByte()
#     var18 = var2.readUnsignedShort()
#     var19 = var2.readUnsignedShort()
#     var20 = var2.readUnsignedShort()
#     var21 = var2.readUnsignedShort()
#     var22 = var2.readUnsignedShort()
#     var23 = 0
#     var24 = 0
#     var25 = 0
#     if(var11 > 0):
#         model.textureRenderTypes = np.empty(shape=(var11), dtype=np.byte)
#         var2.offset = 0

#         for var26 in range(0, var11):
#             var27 = var2.readByte()
#             model.textureRenderTypes[var26] = var27
#             if(var27 == 0):
#                 var23 += 1

#             if(var27 >= 1 and var27 <= 3):
#                 var24 += 1

#             if(var27 == 2):
#                 var25 += 1

#     var26 = var11 + var9
#     var28 = var26
#     if(var12 == 1):
#         var26 += var10

#     var29 = var26
#     var26 += var10
#     var30 = var26
#     if(var13 == 255):
#         var26 += var10

#     var31 = var26
#     if(var15 == 1):
#         var26 += var10

#     var32 = var26
#     if(var17 == 1):
#         var26 += var9

#     var33 = var26
#     if(var14 == 1):
#         var26 += var10

#     var34 = var26
#     var26 += var21
#     var35 = var26
#     if(var16 == 1):
#         var26 += var10 * 2

#     var36 = var26
#     var26 += var22
#     var37 = var26
#     var26 += var10 * 2
#     var38 = var26
#     var26 += var18
#     var39 = var26
#     var26 += var19
#     var40 = var26
#     var26 += var20
#     var41 = var26
#     var26 += var23 * 6
#     var42 = var26
#     var26 += var24 * 6
#     var43 = var26
#     var26 += var24 * 6
#     var44 = var26
#     var26 += var24 * 2
#     var45 = var26
#     var26 += var24
#     var46 = var26
#     var26 += var24 * 2 + var25 * 2
#     model.vertexCount = var9
#     model.triangleFaceCount = var10
#     model.field1738 = var11
#     model.vertexX = np.empty(shape=(var9), dtype=np.int32)
#     model.vertexY = np.empty(shape=(var9), dtype=np.int32)
#     model.vertexZ = np.empty(shape=(var9), dtype=np.int32)
#     model.trianglePointsX = np.zeros(shape=(var10), dtype=np.int32)
#     model.trianglePointsY = np.zeros(shape=(var10), dtype=np.int32)
#     model.trianglePointsZ = np.zeros(shape=(var10), dtype=np.int32)
#     if(var17 == 1):
#         model.vertexSkins = np.zeros(shape=(var9), dtype=np.int32)

#     if(var12 == 1):
#         model.faceRenderTypes = np.zeros(shape=(var10), dtype=np.byte)

#     if(var13 == 255):
#         model.faceRenderPriorities = np.zeros(shape=(var10), dtype=np.byte)
#     else:
#         model.priority = np.byte(var13)

#     if(var14 == 1):
#         model.faceAlphas = np.zeros(shape=(var10), dtype=np.byte)

#     if(var15 == 1):
#         model.triangleSkinValues = np.zeros(shape=(var10), dtype=np.int32)

#     if(var16 == 1):
#         model.faceTextures = np.zeros(shape=(var10), dtype=np.short)

#     if(var16 == 1 and var11 > 0):
#         model.textureCoords = np.zeros(shape=(var10), dtype=np.byte)

#     model.faceColor = np.zeros(shape=(var10), dtype=np.short)
#     if(var11 > 0):
#         model.texTriangleX = np.zeros(shape=(var11), dtype=np.short)
#         model.texTriangleY = np.zeros(shape=(var11), dtype=np.short)
#         model.texTriangleZ = np.zeros(shape=(var11), dtype=np.short)
#         if(var24 > 0):
#             model.field1743 = np.zeros(shape=(var24), dtype=np.short)
#             model.field1745 = np.zeros(shape=(var24), dtype=np.short)
#             model.field1740 = np.zeros(shape=(var24), dtype=np.short)
#             model.field1746 = np.zeros(shape=(var24), dtype=np.short)
#             model.field1749 = np.zeros(shape=(var24), dtype=np.byte)
#             model.field1747 = np.zeros(shape=(var24), dtype=np.short)

#         if(var25 > 0):
#             model.texturePrimaryColor = np.zeros(shape=(var25), dtype=np.short)

#     var2.offset = var11
#     var3.offset = var38
#     var4.offset = var39
#     var5.offset = var40
#     var6.offset = var32
#     var48 = 0
#     var49 = 0
#     var50 = 0

#     for var51 in range(0, var9):
#         var52 = var2.readUnsignedByte()
#         var53 = 0
#         if((var52 & 1) != 0):
#             var53 = var3.readShortSmart()

#         var54 = 0
#         if((var52 & 2) != 0):
#             var54 = var4.readShortSmart()

#         var55 = 0
#         if((var52 & 4) != 0):
#             var55 = var5.readShortSmart()

#         model.vertexX[var51] = var48 + var53
#         model.vertexY[var51] = var49 + var54
#         model.vertexZ[var51] = var50 + var55
#         var48 = model.vertexX[var51]
#         var49 = model.vertexY[var51]
#         var50 = model.vertexZ[var51]
#         if(var17 == 1):
#             model.vertexSkins[var51] = var6.readUnsignedByte()

#     var2.offset = var37
#     var3.offset = var28
#     var4.offset = var30
#     var5.offset = var33
#     var6.offset = var31
#     var7.offset = var35
#     var8.offset = var36

#     for var51 in range(0, var10):
#         model.faceColor[var51] = var2.readUnsignedShort()
#         if(var12 == 1):
#             model.faceRenderTypes[var51] = var3.readByte()

#         if(var13 == 255):
#             model.faceRenderPriorities[var51] = var4.readByte()

#         if(var14 == 1):
#             model.faceAlphas[var51] = var5.readByte()

#         if(var15 == 1):
#             model.triangleSkinValues[var51] = var6.readUnsignedByte()

#         if(var16 == 1):
#             model.faceTextures[var51] = np.short(var7.readUnsignedShort() - 1)

#         # is not None
#         if(model.textureCoords.size > 0 and model.faceTextures[var51] != -1):
#             model.textureCoords[var51] = np.byte(var8.readUnsignedByte() - 1)

#     var2.offset = var34
#     var3.offset = var29
#     var51 = 0
#     var52 = 0
#     var53 = 0
#     var54 = 0

#     for var55 in range(0, var10):
#         var56 = var3.readUnsignedByte()
#         if(var56 == 1):
#             var51 = var2.readShortSmart() + var54
#             var52 = var2.readShortSmart() + var51
#             var53 = var2.readShortSmart() + var52
#             var54 = var53
#             model.trianglePointsX[var55] = var51
#             model.trianglePointsY[var55] = var52
#             model.trianglePointsZ[var55] = var53

#         elif(var56 == 2):
#             var52 = var53
#             var53 = var2.readShortSmart() + var54
#             var54 = var53
#             model.trianglePointsX[var55] = var51
#             model.trianglePointsY[var55] = var52
#             model.trianglePointsZ[var55] = var53

#         elif(var56 == 3):
#             var51 = var53
#             var53 = var2.readShortSmart() + var54
#             var54 = var53
#             model.trianglePointsX[var55] = var51
#             model.trianglePointsY[var55] = var52
#             model.trianglePointsZ[var55] = var53

#         elif(var56 == 4):
#             var57 = var51
#             var51 = var52
#             var52 = var57
#             var53 = var2.readShortSmart() + var54
#             var54 = var53
#             model.trianglePointsX[var55] = var51
#             model.trianglePointsY[var55] = var57
#             model.trianglePointsZ[var55] = var53

#         else:
#             raise Exception("huh?")

#     var2.offset = var41
#     var3.offset = var42
#     var4.offset = var43
#     var5.offset = var44
#     var6.offset = var45
#     var7.offset = var46

#     for var55 in range(0, var11):
#         var56 = model.textureRenderTypes[var55] & 255
#         if(var56 == 0):
#             model.texTriangleX[var55] = np.short(var2.readUnsignedShort())
#             model.texTriangleY[var55] = np.short(var2.readUnsignedShort())
#             model.texTriangleZ[var55] = np.short(var2.readUnsignedShort())

#         elif(var56 == 1):
#             model.texTriangleX[var55] = np.short(var3.readUnsignedShort())
#             model.texTriangleY[var55] = np.short(var3.readUnsignedShort())
#             model.texTriangleZ[var55] = np.short(var3.readUnsignedShort())
#             model.field1743[var55] = np.short(var4.readUnsignedShort())
#             model.field1745[var55] = np.short(var4.readUnsignedShort())
#             model.field1740[var55] = np.short(var4.readUnsignedShort())
#             model.field1746[var55] = np.short(var5.readUnsignedShort())
#             model.field1749[var55] = var6.readByte()
#             model.field1747[var55] = np.short(var7.readUnsignedShort())

#         elif(var56 == 2):
#             model.texTriangleX[var55] = np.short(var3.readUnsignedShort())
#             model.texTriangleY[var55] = np.short(var3.readUnsignedShort())
#             model.texTriangleZ[var55] = np.short(var3.readUnsignedShort())
#             model.field1743[var55] = np.short(var4.readUnsignedShort())
#             model.field1745[var55] = np.short(var4.readUnsignedShort())
#             model.field1740[var55] = np.short(var4.readUnsignedShort())
#             model.field1746[var55] = np.short(var5.readUnsignedShort())
#             model.field1749[var55] = var6.readByte()
#             model.field1747[var55] = np.short(var7.readUnsignedShort())
#             model.texturePrimaryColor[var55] = np.short(
#                 var7.readUnsignedShort())

#         elif(var56 == 3):
#             model.texTriangleX[var55] = np.short(var3.readUnsignedShort())
#             model.texTriangleY[var55] = np.short(var3.readUnsignedShort())
#             model.texTriangleZ[var55] = np.short(var3.readUnsignedShort())
#             model.field1743[var55] = np.short(var4.readUnsignedShort())
#             model.field1745[var55] = np.short(var4.readUnsignedShort())
#             model.field1740[var55] = np.short(var4.readUnsignedShort())
#             model.field1746[var55] = np.short(var5.readUnsignedShort())
#             model.field1749[var55] = var6.readByte()
#             model.field1747[var55] = np.short(var7.readUnsignedShort())

#     var2.offset = var26
#     var55 = var2.readUnsignedByte()
#     if(var55 != 0):
#         # new class138() Literally why
#         var2.readUnsignedShort()
#         var2.readUnsignedShort()
#         var2.readUnsignedShort()
#         var2.readInt()

#     return model

from MathUtills import integerdivide

from numba import int32, boolean
import numpy as np
from MathUtills import integerdivide
import numba
from numba.experimental import jitclass
from expModel import Model

Model_type = Model.class_type.instance_type

@jitclass()
class SceneTileModel:

    vertexX : int32[:]
    vertexY : int32[:]
    vertexZ : int32[:]
    triangleColorA : int32[:]
    triangleColorB : int32[:]
    triangleColorC : int32[:]
    field1772 : int32[:]
    field1774 : int32[:]
    field1778 : int32[:]
    triangleTextureId : numba.optional(int32[:])
    flatShade : boolean
    shape : int32
    rotation : int32
    underlay : int32
    overlay : int32

    def __init__(self, field1790, field1791, var1,  var2,  var3,  var4,  var5,  var6,  var7,  var8,  var9,  var10,  var11,  var12,  var13,  var14,  var15,  var16,  var17,  var18,  var19) -> None:

        self.triangleTextureId = None

        self.flatShade = var7 == var6 and var8 == var6 and var9 == var6

        self.shape = var1
        self.rotation = var2
        self.underlay = var18
        self.overlay = var19
        var20 = 128
        var21 = integerdivide(var20, 2)
        var22 = integerdivide(var20, 4)
        var23 = integerdivide(var20 * 3, 4)
        var24 = field1790[var1]
        var25 = len(var24)
        self.vertexX = np.empty(shape = (var25), dtype = np.int32) # [0] * var25
        self.vertexY = np.empty(shape = (var25), dtype = np.int32) #[0] * var25
        self.vertexZ = np.empty(shape = (var25), dtype = np.int32) #[0] * var25
        var26 = np.empty(shape = (var25), dtype = np.int32) # [0] * var25
        var27 = np.empty(shape = (var25), dtype = np.int32)  #[0] * var25
        var28 = var20 * var4
        var29 = var5 * var20

        for var30 in range(0, var25):
            var31 = var24[var30]
            if((var31 & 1) == 0 and var31 <= 8):
                var31 = (var31 - var2 - var2 - 1 & 7) + 1

            if(var31 > 8 and var31 <= 12):
                var31 = (var31 - 9 - var2 & 3) + 9

            if(var31 > 12 and var31 <= 16):
                var31 = (var31 - 13 - var2 & 3) + 13

            if(var31 == 1):
                var32 = var28
                var33 = var29
                var34 = var6
                var35 = var10
                var36 = var14
            elif(var31 == 2):
                var32 = var28 + var21
                var33 = var29
                var34 = var7 + var6 >> 1
                var35 = var11 + var10 >> 1
                var36 = var15 + var14 >> 1
            elif(var31 == 3):
                var32 = var28 + var20
                var33 = var29
                var34 = var7
                var35 = var11
                var36 = var15
            elif(var31 == 4):
                var32 = var28 + var20
                var33 = var29 + var21
                var34 = var8 + var7 >> 1
                var35 = var11 + var12 >> 1
                var36 = var15 + var16 >> 1
            elif(var31 == 5):
                var32 = var28 + var20
                var33 = var29 + var20
                var34 = var8
                var35 = var12
                var36 = var16
            elif(var31 == 6):
                var32 = var28 + var21
                var33 = var29 + var20
                var34 = var8 + var9 >> 1
                var35 = var13 + var12 >> 1
                var36 = var17 + var16 >> 1
            elif(var31 == 7):
                var32 = var28
                var33 = var29 + var20
                var34 = var9
                var35 = var13
                var36 = var17
            elif(var31 == 8):
                var32 = var28
                var33 = var29 + var21
                var34 = var9 + var6 >> 1
                var35 = var13 + var10 >> 1
                var36 = var17 + var14 >> 1
            elif(var31 == 9):
                var32 = var28 + var21
                var33 = var29 + var22
                var34 = var7 + var6 >> 1
                var35 = var11 + var10 >> 1
                var36 = var15 + var14 >> 1
            elif(var31 == 10):
                var32 = var28 + var23
                var33 = var29 + var21
                var34 = var8 + var7 >> 1
                var35 = var11 + var12 >> 1
                var36 = var15 + var16 >> 1
            elif(var31 == 11):
                var32 = var28 + var21
                var33 = var29 + var23
                var34 = var8 + var9 >> 1
                var35 = var13 + var12 >> 1
                var36 = var17 + var16 >> 1
            elif(var31 == 12):
                var32 = var28 + var22
                var33 = var29 + var21
                var34 = var9 + var6 >> 1
                var35 = var13 + var10 >> 1
                var36 = var17 + var14 >> 1
            elif(var31 == 13):
                var32 = var28 + var22
                var33 = var29 + var22
                var34 = var6
                var35 = var10
                var36 = var14
            elif(var31 == 14):
                var32 = var28 + var23
                var33 = var29 + var22
                var34 = var7
                var35 = var11
                var36 = var15
            elif(var31 == 15):
                var32 = var28 + var23
                var33 = var29 + var23
                var34 = var8
                var35 = var12
                var36 = var16
            else:
                var32 = var28 + var22
                var33 = var29 + var23
                var34 = var9
                var35 = var13
                var36 = var17

            self.vertexX[var30] = var32
            self.vertexY[var30] = var34
            self.vertexZ[var30] = var33
            var26[var30] = var35
            var27[var30] = var36

        var38 = field1791[var1]
        var31 = integerdivide(len(var38), 4)
        self.field1772 = np.empty(shape = (var31), dtype = np.int32) #[0] * var31
        self.field1774 = np.empty(shape = (var31), dtype = np.int32) #[0] * var31
        self.field1778 = np.empty(shape = (var31), dtype = np.int32) #[0] * var31
        self.triangleColorA = np.empty(shape = (var31), dtype = np.int32) #[0] * var31
        self.triangleColorB = np.empty(shape = (var31), dtype = np.int32) #[0] * var31
        self.triangleColorC = np.empty(shape = (var31), dtype = np.int32) #[0] * var31
        if(var3 != -1):
            self.triangleTextureId = np.empty(shape = (var31), dtype = np.int32) # [0] * var31

        var32 = 0

        for var33 in range(0, var31):
            var34 = var38[var32]
            var35 = var38[var32 + 1]
            var36 = var38[var32 + 2]
            var37 = var38[var32 + 3]
            var32 += 4
            if(var35 < 4):
                var35 = var35 - var2 & 3

            if(var36 < 4):
                var36 = var36 - var2 & 3

            if(var37 < 4):
                var37 = var37 - var2 & 3

            self.field1772[var33] = var35
            self.field1774[var33] = var36
            self.field1778[var33] = var37
            if(var34 == 0):
                self.triangleColorA[var33] = var26[var35]
                self.triangleColorB[var33] = var26[var36]
                self.triangleColorC[var33] = var26[var37]
                if(self.triangleTextureId is not None):
                    self.triangleTextureId[var33] = -1

            else:
                self.triangleColorA[var33] = var27[var35]
                self.triangleColorB[var33] = var27[var36]
                self.triangleColorC[var33] = var27[var37]
                if(self.triangleTextureId is not None):
                    self.triangleTextureId[var33] = var3

        var33 = var6
        var34 = var7
        if(var7 < var6):
            var33 = var7

        if(var7 > var7):
            var34 = var7

        if(var8 < var33):
            var33 = var8

        if(var8 > var34):
            var34 = var8

        if(var9 < var33):
            var33 = var9

        if(var9 > var34):
            var34 = var9

        var34 = integerdivide(var34, 14)

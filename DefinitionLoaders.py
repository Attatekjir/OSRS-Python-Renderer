import numba
from cacheUtills import loadContents
from fileCounts import FILECOUNTS195
from OverlayLoader import calculateHsl
from OverlayLoader import OverlayDefinition
from NpcDefinition import NpcDefinition
from Buffer import Buffer
from expModelData import ModelData
import numpy as np
from numba import int32, float32
from numba import jit
from UnderlayLoader import UnderlayDefinition
from bitoperation import readUnsignedByte, read24BitInt, readString, readInt, readByte, readUnsignedShort, readShortSmart
from TextureDefinition import TextureDefinition


@jit(nopython=True, cache=False)
def loadUnderlayDefinition(id, b):

    index = 0
    _, index = readUnsignedByte(b, index)
    color, index = read24BitInt(b, index)

    var2 = (color >> 16 & 255) / 256.0
    var4 = (color >> 8 & 255) / 256.0
    var6 = (color & 255) / 256.0
    var8 = var2
    if (var4 < var2):
        var8 = var4
    if (var6 < var8):
        var8 = var6

    var10 = var2
    if (var4 > var2):
        var10 = var4
    if (var6 > var10):
        var10 = var6

    var12 = 0.0
    var14 = 0.0
    var16 = (var10 + var8) / 2.0
    if (var8 != var10):

        if (var16 < 0.5):
            var14 = (var10 - var8) / (var8 + var10)
        if (var16 >= 0.5):
            var14 = (var10 - var8) / (2.0 - var10 - var8)

        if (var2 == var10):
            var12 = (var4 - var6) / (var10 - var8)
        elif (var10 == var4):
            var12 = 2.0 + (var6 - var2) / (var10 - var8)
        elif (var10 == var6):
            var12 = 4.0 + (var2 - var4) / (var10 - var8)

    var12 /= 6.0
    saturation = np.int32(var14 * 256.0)
    lightness = np.int32(var16 * 256.0)
    if (saturation < 0):
        saturation = np.int32(0)

    elif (saturation > 255):
        saturation = np.int32(255)

    if (lightness < 0):
        lightness = np.int32(0)
    elif (lightness > 255):
        lightness = np.int32(255)

    if (var16 > 0.5):
        hueMultiplier = np.int32(var14 * (1.0 - var16) * 512.0)

    else:
        hueMultiplier = np.int32(var14 * var16 * 512.0)

    if (hueMultiplier < 1):
        hueMultiplier = np.int32(1)

    hue = np.int32(hueMultiplier * var12)

    underlayDef = UnderlayDefinition(
        id, color, hue, saturation, lightness, hueMultiplier)

    return underlayDef


@jit(nopython=True, cache=False)
def loadOverlayDefinition(id, data):

    overlaydef = OverlayDefinition(id)

    index = 0

    while True:

        opcode, index = readUnsignedByte(data, index)
        if (opcode == 0):
            break

        elif (opcode == 1):
            color, index = read24BitInt(data, index)
            overlaydef.color = color

        elif (opcode == 2):
            texture, index = readUnsignedByte(data, index)
            overlaydef.texture = texture

        elif (opcode == 5):
            overlaydef.isHidden = False

        elif (opcode == 7):
            secondaryColor, index = read24BitInt(data, index)
            overlaydef.otherRgbColor = secondaryColor

    calculateHsl(overlaydef)

    return overlaydef


@jit(nopython=True, cache=False)
def loadNpcDefinition(id, data):

    npcdef = NpcDefinition(id)
    index = 0

    while True:

        opcode, index = readUnsignedByte(data, index)
        if (opcode == 0):
            break

        elif (opcode == 1):

            length, index = readUnsignedByte(data, index)
            npcdef.models = np.empty(shape=(length), dtype=np.int32)

            for i in range(0, length):
                npcdef.models[i], index = readUnsignedShort(data, index)

        elif (opcode == 2):
            npcdef.name, index = readString(data, index)

        elif (opcode == 12):
            npcdef.size, index = readUnsignedByte(data, index)

        elif (opcode == 13):
            npcdef.standingAnimation, index = readUnsignedShort(data, index)

        elif (opcode == 14):
            npcdef.walkingAnimation, index = readUnsignedShort(data, index)

        elif (opcode == 15):
            npcdef.rotateLeftAnimation, index = readUnsignedShort(data, index)

        elif (opcode == 16):
            npcdef.rotateRightAnimation, index = readUnsignedShort(data, index)

        elif (opcode == 17):
            npcdef.walkingAnimation, index = readUnsignedShort(data, index)
            npcdef.rotate180Animation, index = readUnsignedShort(data, index)
            npcdef.rotate90RightAnimation, index = readUnsignedShort(
                data, index)
            npcdef.rotate90LeftAnimation, index = readUnsignedShort(
                data, index)

        elif (opcode == 18):
            npcdef.category, index = readUnsignedShort(data, index)

        elif (opcode >= 30 and opcode < 35):

            var9999, index = readString(data, index)
            #npcdef.actions[opcode - 30] = readString()
            # if (npcdef.actions[opcode - 30] == "Hidden"):
            #    npcdef.actions[opcode - 30] = None

        elif (opcode == 40):

            length, index = readUnsignedByte(data, index)
            npcdef.recolorToFind = np.empty(shape=(length), dtype=np.short)
            npcdef.recolorToReplace = np.empty(shape=(length), dtype=np.short)

            for i in range(0, length):

                var8888, index = readUnsignedShort(data, index)
                npcdef.recolorToFind[i] = var8888

                var9999, index = readUnsignedShort(data, index)
                npcdef.recolorToReplace[i] = var9999

        elif (opcode == 41):

            length, index = readUnsignedByte(data, index)
            npcdef.retextureToFind = np.empty(shape=(length), dtype=np.short)
            npcdef.retextureToReplace = np.empty(
                shape=(length), dtype=np.short)

            for i in range(0, length):
                npcdef.retextureToFind[i], index = readUnsignedShort(
                    data, index)
                npcdef.retextureToReplace[i], index = readUnsignedShort(
                    data, index)

        elif (opcode == 60):

            length, index = readUnsignedByte(data, index)
            npcdef.chatheadModels = np.empty(shape=(length), dtype=np.int32)

            for i in range(0, length):
                npcdef.chatheadModels[i], index = readUnsignedShort(
                    data, index)

        elif (opcode == 93):

            npcdef.isMinimapVisible = False

        elif (opcode == 95):

            npcdef.combatLevel, index = readUnsignedShort(data, index)

        elif (opcode == 97):

            npcdef.widthScale, index = readUnsignedShort(data, index)

        elif (opcode == 98):

            npcdef.heightScale, index = readUnsignedShort(data, index)

        elif (opcode == 99):

            npcdef.hasRenderPriority = True

        elif (opcode == 100):

            npcdef.ambient, index = readByte(data, index)

        elif (opcode == 101):

            npcdef.contrast, index = readByte(data, index)

        elif (opcode == 102):

            npcdef.headIcon, index = readUnsignedShort(data, index)

        elif (opcode == 103):

            npcdef.rotationSpeed, index = readUnsignedShort(data, index)

        elif (opcode == 106):

            npcdef.varbitId, index = readUnsignedShort(data, index)
            if (npcdef.varbitId == 65535):
                npcdef.varbitId = -1

            npcdef.varpIndex, index = readUnsignedShort(data, index)
            if (npcdef.varpIndex == 65535):
                npcdef.varpIndex = -1

            length, index = readUnsignedByte(data, index)
            npcdef.configs = np.empty(shape=(length + 2), dtype=np.int32)

            for i in range(0, length + 1):

                npcdef.configs[i], index = readUnsignedShort(data, index)
                if (npcdef.configs[i] == '\uffff'):
                    npcdef.configs[i] = -1

            npcdef.configs[length + 1] = -1

        elif (opcode == 107):

            npcdef.isInteractable = False

        elif (opcode == 109):

            npcdef.rotationFlag = False

        elif (opcode == 111):

            npcdef.isPet = True

        elif (opcode == 118):

            npcdef.varbitId, index = readUnsignedShort(data, index)
            if (npcdef.varbitId == 65535):

                npcdef.varbitId = -1

            npcdef.varpIndex, index = readUnsignedShort(data, index)
            if (npcdef.varpIndex == 65535):

                npcdef.varpIndex = -1

            var, index = readUnsignedShort(data, index)
            if (var == 0xFFFF):

                var = -1

            length, index = readUnsignedByte(data, index)
            npcdef.configs = np.empty(shape=(length + 2), dtype=np.int32)

            for i in range(0, length + 1):

                npcdef.configs[i], index = readUnsignedShort(data, index)
                if (npcdef.configs[i] == '\uffff'):

                    npcdef.configs[i] = -1

            npcdef.configs[length + 1] = var

        elif (opcode == 249):

            length, index = readUnsignedByte(data, index)

            #npcdef.params = {}

            for i in range(0, length):
                var7777, index = readUnsignedByte(data, index)
                isString = var7777 == 1
                key, index = read24BitInt(data, index)

                if isString:
                    value, index = readString(data, index)
                else:
                    value, index = readInt(data, index)

                #npcdef.params[key] = value

        else:
            #logger.warn("Unrecognized opcode :", opcode)
            raise Exception("Unrecognized opcode")

    return npcdef


@jit(nopython=True, cache=False)
def loadNpcDefinitionOLD(id, b):

    npcdef = NpcDefinition(id)
    stream = Buffer(b)

    while True:
        opcode = stream.readUnsignedByte()
        if (opcode == 0):
            break

        elif (opcode == 1):

            length = stream.readUnsignedByte()
            npcdef.models = np.empty(shape=(length), dtype=np.int32)

            for index in range(0, length):
                npcdef.models[index] = stream.readUnsignedShort()

        elif (opcode == 2):
            npcdef.name = stream.readString()

        elif (opcode == 12):
            npcdef.size = stream.readUnsignedByte()

        elif (opcode == 13):
            npcdef.standingAnimation = stream.readUnsignedShort()

        elif (opcode == 14):
            npcdef.walkingAnimation = stream.readUnsignedShort()

        elif (opcode == 15):
            npcdef.rotateLeftAnimation = stream.readUnsignedShort()

        elif (opcode == 16):
            npcdef.rotateRightAnimation = stream.readUnsignedShort()

        elif (opcode == 17):
            npcdef.walkingAnimation = stream.readUnsignedShort()
            npcdef.rotate180Animation = stream.readUnsignedShort()
            npcdef.rotate90RightAnimation = stream.readUnsignedShort()
            npcdef.rotate90LeftAnimation = stream.readUnsignedShort()

        elif (opcode == 18):
            npcdef.category = stream.readUnsignedShort()

        elif (opcode >= 30 and opcode < 35):

            var9999 = stream.readString()
            #npcdef.actions[opcode - 30] = stream.readString()
            # if (npcdef.actions[opcode - 30] == "Hidden"):
            #    npcdef.actions[opcode - 30] = None

        elif (opcode == 40):

            length = stream.readUnsignedByte()
            npcdef.recolorToFind = np.empty(shape=(length), dtype=np.short)
            npcdef.recolorToReplace = np.empty(shape=(length), dtype=np.short)

            for index in range(0, length):
                npcdef.recolorToFind[index] = np.ushort(
                    stream.readUnsignedShort())
                npcdef.recolorToReplace[index] = np.ushort(
                    stream.readUnsignedShort())

        elif (opcode == 41):

            length = stream.readUnsignedByte()
            npcdef.retextureToFind = np.empty(shape=(length), dtype=np.short)
            npcdef.retextureToReplace = np.empty(
                shape=(length), dtype=np.short)

            for index in range(0, length):
                npcdef.retextureToFind[index] = np.ushort(
                    stream.readUnsignedShort())
                npcdef.retextureToReplace[index] = np.ushort(
                    stream.readUnsignedShort())

        elif (opcode == 60):

            length = stream.readUnsignedByte()
            npcdef.chatheadModels = np.empty(shape=(length), dtype=np.int32)

            for index in range(0, length):
                npcdef.chatheadModels[index] = stream.readUnsignedShort()

        elif (opcode == 93):

            npcdef.isMinimapVisible = False

        elif (opcode == 95):

            npcdef.combatLevel = stream.readUnsignedShort()

        elif (opcode == 97):

            npcdef.widthScale = stream.readUnsignedShort()

        elif (opcode == 98):

            npcdef.heightScale = stream.readUnsignedShort()

        elif (opcode == 99):

            npcdef.hasRenderPriority = True

        elif (opcode == 100):

            npcdef.ambient = stream.readByte()

        elif (opcode == 101):

            npcdef.contrast = stream.readByte()

        elif (opcode == 102):

            npcdef.headIcon = stream.readUnsignedShort()

        elif (opcode == 103):

            npcdef.rotationSpeed = stream.readUnsignedShort()

        elif (opcode == 106):

            npcdef.varbitId = stream.readUnsignedShort()
            if (npcdef.varbitId == 65535):
                npcdef.varbitId = -1

            npcdef.varpIndex = stream.readUnsignedShort()
            if (npcdef.varpIndex == 65535):
                npcdef.varpIndex = -1

            length = stream.readUnsignedByte()
            npcdef.configs = np.empty(shape=(length + 2), dtype=np.int32)

            for index in range(0, length + 1):

                npcdef.configs[index] = stream.readUnsignedShort()
                if (npcdef.configs[index] == '\uffff'):
                    npcdef.configs[index] = -1

            npcdef.configs[length + 1] = -1

        elif (opcode == 107):

            npcdef.isInteractable = False

        elif (opcode == 109):

            npcdef.rotationFlag = False

        elif (opcode == 111):

            npcdef.isPet = True

        elif (opcode == 118):

            npcdef.varbitId = stream.readUnsignedShort()
            if (npcdef.varbitId == 65535):

                npcdef.varbitId = -1

            npcdef.varpIndex = stream.readUnsignedShort()
            if (npcdef.varpIndex == 65535):

                npcdef.varpIndex = -1

            var = stream.readUnsignedShort()
            if (var == 0xFFFF):

                var = -1

            length = stream.readUnsignedByte()
            npcdef.configs = np.empty(shape=(length + 2), dtype=np.int32)

            for index in range(0, length + 1):

                npcdef.configs[index] = stream.readUnsignedShort()
                if (npcdef.configs[index] == '\uffff'):

                    npcdef.configs[index] = -1

            npcdef.configs[length + 1] = var

        elif (opcode == 249):

            length = stream.readUnsignedByte()

            #npcdef.params = {}

            for i in range(0, length):

                isString = stream.readUnsignedByte() == 1
                key = stream.read24BitInt()

                if isString:
                    value = stream.readString()
                else:
                    value = stream.readInt()

                #npcdef.params[key] = value

        else:
            #logger.warn("Unrecognized opcode :", opcode)
            raise Exception("Unrecognized opcode")

    return npcdef


@jit(nopython=True, cache=False)
def loadModelData(modelId, bffr):

    if (bffr[len(bffr) - 1] == -1 and bffr[len(bffr) - 2] == -1):
        model = decodeNewModelFormat(modelId, bffr)
    else:
        model = decodeOldModelFormat(modelId, bffr)

    return model


@jit(nopython=True, cache=False)
def decodeOldModelFormat(id, var1):

    model = ModelData()
    model.id = id

    var2 = False
    var43 = False
    #var5 = Buffer(var1)
    #var39 = Buffer(var1)
    #var26 = Buffer(var1)
    #var9 = Buffer(var1)
    #var3 = Buffer(var1)

    var5index = len(var1) - 18  # var5.offset = len(var1) - 18

    var10, var5index = readUnsignedShort(var1, var5index)
    var11, var5index = readUnsignedShort(var1, var5index)
    var12, var5index = readUnsignedByte(var1, var5index)

    var13, var5index = readUnsignedByte(var1, var5index)
    var14, var5index = readUnsignedByte(var1, var5index)
    var30, var5index = readUnsignedByte(var1, var5index)
    var15, var5index = readUnsignedByte(var1, var5index)
    var28, var5index = readUnsignedByte(var1, var5index)
    var27, var5index = readUnsignedShort(var1, var5index)
    var20, var5index = readUnsignedShort(var1, var5index)
    var36, var5index = readUnsignedShort(var1, var5index)
    var23, var5index = readUnsignedShort(var1, var5index)

    var16 = 0
    var46 = var16 + var10
    var24 = var46
    var46 += var11
    var25 = var46
    if (var14 == 255):
        var46 += var11

    var4 = var46
    if (var15 == 1):
        var46 += var11

    var42 = var46
    if (var13 == 1):
        var46 += var11

    var37 = var46
    if (var28 == 1):
        var46 += var10

    var29 = var46
    if (var30 == 1):
        var46 += var11

    var44 = var46
    var46 += var23
    var17 = var46
    var46 += var11 * 2
    var32 = var46
    var46 += var12 * 6
    var34 = var46
    var46 += var27
    var35 = var46
    var46 += var20
    var10000 = var46 + var36
    model.vertexCount = var10
    model.triangleFaceCount = var11
    model.field1738 = var12

    model.vertexX = np.zeros(shape=(var10), dtype=np.int32)
    model.vertexY = np.zeros(shape=(var10), dtype=np.int32)
    model.vertexZ = np.zeros(shape=(var10), dtype=np.int32)
    model.trianglePointsX = np.zeros(shape=(var11), dtype=np.int32)
    model.trianglePointsY = np.zeros(shape=(var11), dtype=np.int32)
    model.trianglePointsZ = np.zeros(shape=(var11), dtype=np.int32)
    if (var12 > 0):
        model.textureRenderTypes = np.zeros(shape=(var12), dtype=np.byte)
        model.texTriangleX = np.zeros(shape=(var12), dtype=np.short)
        model.texTriangleY = np.zeros(shape=(var12), dtype=np.short)
        model.texTriangleZ = np.zeros(shape=(var12), dtype=np.short)

    if (var28 == 1):
        model.vertexSkins = np.zeros(shape=(var10), dtype=np.int32)

    if (var13 == 1):
        model.faceRenderTypes = np.zeros(shape=(var11), dtype=np.byte)
        model.textureCoords = np.zeros(shape=(var11), dtype=np.byte)
        model.faceTextures = np.zeros(shape=(var11), dtype=np.short)

    if (var14 == 255):
        model.faceRenderPriorities = np.zeros(shape=(var11), dtype=np.byte)
    else:
        model.priority = np.byte(var14)

    if (var30 == 1):
        model.faceAlphas = np.zeros(shape=(var11), dtype=np.byte)

    if (var15 == 1):
        model.triangleSkinValues = np.zeros(shape=(var11), dtype=np.int32)

    model.faceColor = np.zeros(shape=(var11), dtype=np.short)
    var5index = var16  # var5.setOffset(var16)

    var39index = var34  # var39.setOffset(var34)
    var26index = var35  # var26.setOffset(var35)
    var9index = var46  # var9.setOffset(var46)
    var3index = var37  # var3.setOffset(var37)
    var41 = 0
    var33 = 0
    var19 = 0

    for var18 in range(0, var10):
        var8, var5index = readUnsignedByte(var1, var5index)
        var31 = 0
        if ((var8 & 1) != 0):
            var31, var39index = readShortSmart(var1, var39index)

        var6 = 0
        if ((var8 & 2) != 0):
            var6, var26index = readShortSmart(var1, var26index)

        var7 = 0
        if ((var8 & 4) != 0):
            var7, var9index = readShortSmart(var1, var9index)

        model.vertexX[var18] = var41 + var31
        model.vertexY[var18] = var33 + var6
        model.vertexZ[var18] = var19 + var7
        var41 = model.vertexX[var18]
        var33 = model.vertexY[var18]
        var19 = model.vertexZ[var18]
        if (var28 == 1):
            model.vertexSkins[var18], var3index = readUnsignedByte(
                var1, var3index)

    var5index = var17  # var5.setOffset(var17)
    var39index = var42  # var39.setOffset(var42)
    var26index = var25  # var26.setOffset(var25)
    var9index = var29  # var9.setOffset(var29)
    var3index = var4  # var3.setOffset(var4)

    for var18 in range(var11):
        var9999, var5index = readUnsignedShort(var1, var5index)
        model.faceColor[var18] = np.short(var9999)
        if (var13 == 1):
            var8, var39index = readUnsignedByte(var1, var39index)
            if ((var8 & 1) == 1):
                model.faceRenderTypes[var18] = 1
                var2 = True

            else:
                model.faceRenderTypes[var18] = 0

            if ((var8 & 2) == 2):
                model.textureCoords[var18] = np.byte(var8 >> 2)
                model.faceTextures[var18] = model.faceColor[var18]
                model.faceColor[var18] = 127
                if (model.faceTextures[var18] != -1):
                    var43 = True

            else:
                model.textureCoords[var18] = -1
                model.faceTextures[var18] = -1

        if (var14 == 255):
            model.faceRenderPriorities[var18], var26index = readByte(
                var1, var26index)

        if (var30 == 1):
            model.faceAlphas[var18], var9index = readByte(var1, var9index)

        if (var15 == 1):
            model.triangleSkinValues[var18], var3index = readUnsignedByte(
                var1, var3index)

    var5index = var44  # var5.setOffset(var44)
    var39index = var24  # var39.setOffset(var24)
    var18 = 0
    var8 = 0
    var31 = 0
    var6 = 0

    for var7 in range(var11):
        var43_, var39index = readUnsignedByte(var1, var39index)
        if (var43_ == 1):
            var18, var5index = readShortSmart(var1, var5index)  # + var6
            var18 += var6
            var8, var5index = readShortSmart(var1, var5index)  # + var18
            var8 += var18
            var31, var5index = readShortSmart(var1, var5index)  # + var8
            var31 += var8
            var6 = var31
            model.trianglePointsX[var7] = var18
            model.trianglePointsY[var7] = var8
            model.trianglePointsZ[var7] = var31

        elif (var43_ == 2):
            var8 = var31
            var31, var5index = readShortSmart(var1, var5index)  # + var6
            var31 += var6
            var6 = var31
            model.trianglePointsX[var7] = var18
            model.trianglePointsY[var7] = var8
            model.trianglePointsZ[var7] = var31

        elif (var43_ == 3):
            var18 = var31
            var31, var5index = readShortSmart(var1, var5index)  # + var6
            var31 += var6
            var6 = var31
            model.trianglePointsX[var7] = var18
            model.trianglePointsY[var7] = var8
            model.trianglePointsZ[var7] = var31

        elif (var43_ == 4):
            var44_ = var18
            var18 = var8
            var8 = var44_
            var31, var5index = readShortSmart(var1, var5index)  # + var6
            var31 += var6
            var6 = var31
            model.trianglePointsX[var7] = var18
            model.trianglePointsY[var7] = var44_
            model.trianglePointsZ[var7] = var31

    var5index = var32  # var5.setOffset(var32)

    for var7 in range(var12):
        model.textureRenderTypes[var7] = 0
        model.texTriangleX[var7], var5index = readUnsignedShort(
            var1, var5index)  # np.short
        model.texTriangleY[var7], var5index = readUnsignedShort(
            var1, var5index)  # np.short
        model.texTriangleZ[var7], var5index = readUnsignedShort(
            var1, var5index)  # np.short

    if (model.textureCoords.size != 0):  # is not None

        var45 = False
        for var43_ in range(0, var11):
            var44_ = model.textureCoords[var43_] & 255
            if (var44_ != 255):
                if (model.trianglePointsX[var43_] == (model.texTriangleX[var44_] & 0xffff)
                    and model.trianglePointsY[var43_] == (model.texTriangleY[var44_] & 0xffff)
                        and model.trianglePointsZ[var43_] == (model.texTriangleZ[var44_] & 0xffff)):
                    model.textureCoords[var43_] = -1

                else:
                    var45 = True

        if (not var45):
            model.textureCoords = np.empty(shape=(0), dtype=np.byte)  # None

    if (not var43):
        model.faceTextures = np.empty(shape=(0), dtype=np.short)  # None

    if (not var2):
        model.faceRenderTypes = np.empty(shape=(0), dtype=np.byte)  # None

    return model


@jit(nopython=True, cache=False)
def decodeNewModelFormat(id, var1):

    model = ModelData()
    model.id = id

    #var2 = Buffer(var1)
    #var3 = Buffer(var1)
    #var4 = Buffer(var1)
    #var5 = Buffer(var1)
    #var6 = Buffer(var1)
    #var7 = Buffer(var1)
    #var8 = Buffer(var1)

    var2index = len(var1) - 23  # var2.offset = len(var1) - 23
    var9, var2index = readUnsignedShort(var1, var2index)
    var10, var2index = readUnsignedShort(var1, var2index)
    var11, var2index = readUnsignedByte(var1, var2index)
    var12, var2index = readUnsignedByte(var1, var2index)
    var13, var2index = readUnsignedByte(var1, var2index)
    var14, var2index = readUnsignedByte(var1, var2index)
    var15, var2index = readUnsignedByte(var1, var2index)
    var16, var2index = readUnsignedByte(var1, var2index)
    var17, var2index = readUnsignedByte(var1, var2index)
    var18, var2index = readUnsignedShort(var1, var2index)
    var19, var2index = readUnsignedShort(var1, var2index)
    var20, var2index = readUnsignedShort(var1, var2index)
    var21, var2index = readUnsignedShort(var1, var2index)
    var22, var2index = readUnsignedShort(var1, var2index)
    var23 = 0
    var24 = 0
    var25 = 0
    if(var11 > 0):
        model.textureRenderTypes = np.empty(shape=(var11), dtype=np.byte)
        var2index = 0  # var2.offset = 0

        for var26 in range(0, var11):
            var27, var2index = readByte(var1, var2index)
            model.textureRenderTypes[var26] = var27
            if(var27 == 0):
                var23 += 1

            if(var27 >= 1 and var27 <= 3):
                var24 += 1

            if(var27 == 2):
                var25 += 1

    var26 = var11 + var9
    var28 = var26
    if(var12 == 1):
        var26 += var10

    var29 = var26
    var26 += var10
    var30 = var26
    if(var13 == 255):
        var26 += var10

    var31 = var26
    if(var15 == 1):
        var26 += var10

    var32 = var26
    if(var17 == 1):
        var26 += var9

    var33 = var26
    if(var14 == 1):
        var26 += var10

    var34 = var26
    var26 += var21
    var35 = var26
    if(var16 == 1):
        var26 += var10 * 2

    var36 = var26
    var26 += var22
    var37 = var26
    var26 += var10 * 2
    var38 = var26
    var26 += var18
    var39 = var26
    var26 += var19
    var40 = var26
    var26 += var20
    var41 = var26
    var26 += var23 * 6
    var42 = var26
    var26 += var24 * 6
    var43 = var26
    var26 += var24 * 6
    var44 = var26
    var26 += var24 * 2
    var45 = var26
    var26 += var24
    var46 = var26
    var26 += var24 * 2 + var25 * 2
    model.vertexCount = var9
    model.triangleFaceCount = var10
    model.field1738 = var11
    model.vertexX = np.empty(shape=(var9), dtype=np.int32)
    model.vertexY = np.empty(shape=(var9), dtype=np.int32)
    model.vertexZ = np.empty(shape=(var9), dtype=np.int32)
    model.trianglePointsX = np.zeros(shape=(var10), dtype=np.int32)
    model.trianglePointsY = np.zeros(shape=(var10), dtype=np.int32)
    model.trianglePointsZ = np.zeros(shape=(var10), dtype=np.int32)
    if(var17 == 1):
        model.vertexSkins = np.zeros(shape=(var9), dtype=np.int32)

    if(var12 == 1):
        model.faceRenderTypes = np.zeros(shape=(var10), dtype=np.byte)

    if(var13 == 255):
        model.faceRenderPriorities = np.zeros(shape=(var10), dtype=np.byte)
    else:
        model.priority = np.byte(var13)

    if(var14 == 1):
        model.faceAlphas = np.zeros(shape=(var10), dtype=np.byte)

    if(var15 == 1):
        model.triangleSkinValues = np.zeros(shape=(var10), dtype=np.int32)

    if(var16 == 1):
        model.faceTextures = np.zeros(shape=(var10), dtype=np.short)

    if(var16 == 1 and var11 > 0):
        model.textureCoords = np.zeros(shape=(var10), dtype=np.byte)

    model.faceColor = np.zeros(shape=(var10), dtype=np.short)
    if(var11 > 0):
        model.texTriangleX = np.zeros(shape=(var11), dtype=np.short)
        model.texTriangleY = np.zeros(shape=(var11), dtype=np.short)
        model.texTriangleZ = np.zeros(shape=(var11), dtype=np.short)
        if(var24 > 0):
            model.field1743 = np.zeros(shape=(var24), dtype=np.short)
            model.field1745 = np.zeros(shape=(var24), dtype=np.short)
            model.field1740 = np.zeros(shape=(var24), dtype=np.short)
            model.field1746 = np.zeros(shape=(var24), dtype=np.short)
            model.field1749 = np.zeros(shape=(var24), dtype=np.byte)
            model.field1747 = np.zeros(shape=(var24), dtype=np.short)

        if(var25 > 0):
            model.texturePrimaryColor = np.zeros(shape=(var25), dtype=np.short)

    var2index = var11  # var2.offset = var11

    var3index = var38
    var4index = var39
    var5index = var40
    var6index = var32

    #var3.offset = var38
    #var4.offset = var39
    #var5.offset = var40
    #var6.offset = var32
    var48 = 0
    var49 = 0
    var50 = 0

    for var51 in range(0, var9):
        var52, var2index = readUnsignedByte(var1, var2index)
        var53 = 0
        if((var52 & 1) != 0):
            var53, var3index = readShortSmart(var1, var3index)

        var54 = 0
        if((var52 & 2) != 0):
            var54, var4index = readShortSmart(var1, var4index)

        var55 = 0
        if((var52 & 4) != 0):
            var55, var5index = readShortSmart(var1, var5index)

        model.vertexX[var51] = var48 + var53
        model.vertexY[var51] = var49 + var54
        model.vertexZ[var51] = var50 + var55
        var48 = model.vertexX[var51]
        var49 = model.vertexY[var51]
        var50 = model.vertexZ[var51]
        if(var17 == 1):
            model.vertexSkins[var51], var6index = readUnsignedByte(
                var1, var6index)

    var2index = var37  # var2.offset = var37
    # var3.offset = var28
    # var4.offset = var30
    # var5.offset = var33
    # var6.offset = var31
    # var7.offset = var35
    # var8.offset = var36
    var3index = var28
    var4index = var30
    var5index = var33
    var6index = var31
    var7index = var35
    var8index = var36

    for var51 in range(0, var10):
        model.faceColor[var51], var2index = readUnsignedShort(var1, var2index)
        if(var12 == 1):
            model.faceRenderTypes[var51], var3index = readByte(var1, var3index)

        if(var13 == 255):
            model.faceRenderPriorities[var51], var4index = readByte(
                var1, var4index)

        if(var14 == 1):
            model.faceAlphas[var51], var5index = readByte(var1, var5index)

        if(var15 == 1):
            model.triangleSkinValues[var51], var6index = readUnsignedByte(
                var1, var6index)

        if(var16 == 1):
            var9999, var7index = readUnsignedShort(var1, var7index)
            model.faceTextures[var51] = np.short(var9999 - 1)

        # is not None
        if(model.textureCoords.size > 0 and model.faceTextures[var51] != -1):
            var9999, var8index = readUnsignedByte(var1, var8index)
            model.textureCoords[var51] = np.byte(var9999 - 1)

    var2index = var34  # var2.offset = var34
    var3index = var29  # var3.offset = var29
    var51 = 0
    var52 = 0
    var53 = 0
    var54 = 0

    for var55 in range(0, var10):
        var56, var3index = readUnsignedByte(var1, var3index)
        if(var56 == 1):
            var51, var2index = readShortSmart(var1, var2index)  # + var54
            var51 += var54
            var52, var2index = readShortSmart(var1, var2index)  # + var51
            var52 += var51
            var53, var2index = readShortSmart(var1, var2index)  # + var52
            var53 += var52
            var54 = var53
            model.trianglePointsX[var55] = var51
            model.trianglePointsY[var55] = var52
            model.trianglePointsZ[var55] = var53

        elif(var56 == 2):
            var52 = var53
            var53, var2index = readShortSmart(var1, var2index)  # + var54
            var53 += var54
            var54 = var53
            model.trianglePointsX[var55] = var51
            model.trianglePointsY[var55] = var52
            model.trianglePointsZ[var55] = var53

        elif(var56 == 3):
            var51 = var53
            var53, var2index = readShortSmart(var1, var2index)  # + var54
            var53 += var54
            var54 = var53
            model.trianglePointsX[var55] = var51
            model.trianglePointsY[var55] = var52
            model.trianglePointsZ[var55] = var53

        elif(var56 == 4):
            var57 = var51
            var51 = var52
            var52 = var57
            var53, var2index = readShortSmart(var1, var2index)  # + var54
            var53 += var54
            var54 = var53
            model.trianglePointsX[var55] = var51
            model.trianglePointsY[var55] = var57
            model.trianglePointsZ[var55] = var53

        else:
            raise Exception("huh?")

    var2index = var41  # var2.offset = var41
    # var3.offset = var42
    # var4.offset = var43
    # var5.offset = var44
    # var6.offset = var45
    # var7.offset = var46
    var3index = var42
    var4index = var43
    var5index = var44
    var6index = var45
    var7index = var46

    for var55 in range(0, var11):
        var56 = model.textureRenderTypes[var55] & 255
        if(var56 == 0):
            model.texTriangleX[var55], var2index = readUnsignedShort(
                var1, var2index)
            model.texTriangleY[var55], var2index = readUnsignedShort(
                var1, var2index)
            model.texTriangleZ[var55], var2index = readUnsignedShort(
                var1, var2index)

        elif(var56 == 1):
            model.texTriangleX[var55], var3index = readUnsignedShort(
                var1, var3index)
            model.texTriangleY[var55], var3index = readUnsignedShort(
                var1, var3index)
            model.texTriangleZ[var55], var3index = readUnsignedShort(
                var1, var3index)
            model.field1743[var55], var4index = readUnsignedShort(
                var1, var4index)
            model.field1745[var55], var4index = readUnsignedShort(
                var1, var4index)
            model.field1740[var55], var4index = readUnsignedShort(
                var1, var4index)
            model.field1746[var55], var5index = readUnsignedShort(
                var1, var5index)
            model.field1749[var55], var6index = readByte(var1, var6index)
            model.field1747[var55], var7index = readUnsignedShort(
                var1, var7index)

        elif(var56 == 2):
            model.texTriangleX[var55], var3index = readUnsignedShort(
                var1, var3index)
            model.texTriangleY[var55], var3index = readUnsignedShort(
                var1, var3index)
            model.texTriangleZ[var55], var3index = readUnsignedShort(
                var1, var3index)
            model.field1743[var55], var4index = readUnsignedShort(
                var1, var4index)
            model.field1745[var55], var4index = readUnsignedShort(
                var1, var4index)
            model.field1740[var55], var4index = readUnsignedShort(
                var1, var4index)
            model.field1746[var55], var5index = readUnsignedShort(
                var1, var5index)
            model.field1749[var55], var6index = readByte(var1, var6index)
            model.field1747[var55], var7index = readUnsignedShort(
                var1, var7index)
            model.texturePrimaryColor[var55], var7index = readUnsignedShort(
                var1, var7index)

        elif(var56 == 3):
            model.texTriangleX[var55], var3index = readUnsignedShort(
                var1, var3index)
            model.texTriangleY[var55], var3index = readUnsignedShort(
                var1, var3index)
            model.texTriangleZ[var55], var3index = readUnsignedShort(
                var1, var3index)
            model.field1743[var55], var4index = readUnsignedShort(
                var1, var4index)
            model.field1745[var55], var4index = readUnsignedShort(
                var1, var4index)
            model.field1740[var55], var4index = readUnsignedShort(
                var1, var4index)
            model.field1746[var55], var5index = readUnsignedShort(
                var1, var5index)
            model.field1749[var55], var6index = readByte(var1, var6index)
            model.field1747[var55], var7index = readUnsignedShort(
                var1, var7index)

    var2index = var26  # var2.offset = var26
    var55, var2index = readUnsignedByte(var1, var2index)
    if(var55 != 0):
        # new class138(var1) Literally why
        l, _ = readUnsignedShort(var1, var2index)
        l, _ = readUnsignedShort(var1, var2index)
        l, _ = readUnsignedShort(var1, var2index)
        l, _ = readInt(var1, var2index)

    return model


@jit(nopython=True, cache=False)
def loadTextureDefinitions(data, ci):

    # According to runelite way
    fileContents = loadContents(data, FILECOUNTS195.TEXTURE.value)

    textureDefinitions = numba.typed.Dict.empty(
        key_type=numba.int64,
        value_type=ci,  # TextureDefinition.class_type.instance_type,
    )

    for i, fileContent in enumerate(fileContents):

        # Cache195 has texture54 placed as texture 55 etc
        index = i
        if index > 53:
            index += 1

        textureDefinition_ = loadTextureDefinition(i, fileContent)
        textureDefinitions[index] = textureDefinition_

    return textureDefinitions


@jit(nopython=True, cache=False)
def loadTextureDefinition(id, data):

    stream = Buffer(data)

    field1803 = stream.readUnsignedShort()
    field1806 = stream.readByte() != 0

    count = stream.readUnsignedByte()

    fileIds = np.empty(shape=(count), dtype=np.int32)
    for i in range(0, count):
        fileIds[i] = stream.readUnsignedShort()

    if (count > 1):
        field1801 = np.empty(shape=(count - 1), dtype=np.int32)
        for var3 in range(0, count - 1):
            field1801[var3] = stream.readUnsignedByte()
    else:
        field1801 = np.zeros(shape=(1), dtype=np.int32)

    if (count > 1):
        field1807 = np.empty(shape=(count - 1), dtype=np.int32)
        for var3 in range(0, count - 1):
            field1807[var3] = stream.readUnsignedByte()
    else:
        field1807 = np.zeros(shape=(1), dtype=np.int32)

    field1808 = np.empty(shape=(count), dtype=np.int32)
    for var3 in range(0, count):
        field1808[var3] = stream.readInt()

    field1810 = stream.readUnsignedByte()
    field1809 = stream.readUnsignedByte()

    textureDefinition = TextureDefinition(id, field1801, field1803, field1806, field1807,
                                          field1808, field1809, field1810, fileIds)

    return textureDefinition

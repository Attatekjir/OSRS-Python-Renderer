import numpy as np
from math import sqrt
from MathUtills import integerdivide
from MathUtills import method4490
from Region import addTile
from Region import setPhysicalLevel
from numba import jit
from TextureProvider import TextureLoaderGetAverageTextureRGB
from Region import addOcclude
from Region import setBridge


@jit(nopython=True, cache=True)
def method3058(var0, var1) :
    if(var0 == -1) :
        return 12345678
    #else :
    var1 = integerdivide((var0 & 127) * var1, 128)
    if(var1 < 2) :
        var1 = 2
    elif(var1 > 126) :
        var1 = 126

    return (var0 & 65408) + var1

@jit(nopython=True, cache=True)
def adjustHSLListness0(var0, var1):
    if(var0 == -2):
        # This does happen
        #raise Exception ('WHAT?')
        return 12345678
    elif(var0 == -1):
        if(var1 < 2):
            var1 = 2
        elif(var1 > 126):
            var1 = 126
        return var1
    else:
        var1 = integerdivide((var0 & 127) * var1, 128)
        if(var1 < 2):
            var1 = 2
        elif(var1 > 126):
            var1 = 126
        return (var0 & 65408) + var1


@jit(nopython=True, cache=False)
def tst(floorSaturations, floorHues, floorMultiplier, field3314, field1356, field1354, colorPalette, field2520, field3831, tileHeights, tileUnderlayIds, underlayDefinitions, tileSettings,
        tiles, tileOverlayIds, levelOccluders, levelOccluderCount, field751, tileOverlayPath,
        overlayDefinitions, field745, field1790, field1791, textures, overlayRotations):

    field1354.fill(0)

    for var5 in range(0, 4):

        # Zero'd for every level
        floorSaturations.fill(0)
        floorHues.fill(0)
        floorMultiplier.fill(0)
        field3314.fill(0)
        field1356.fill(0)

        var81 = field3831[var5]
        var12 = np.int32(sqrt(5100.0))
        var75 = var12 * 768 >> 8

        for var14 in range(1, 103):
            for var15 in range(1, 103):
                var16 = tileHeights[var5][var15 + 1][var14] - \
                    tileHeights[var5][var15 - 1][var14]
                var17 = tileHeights[var5][var15][var14 + 1] - \
                    tileHeights[var5][var15][var14 - 1]
                var18 = np.int32(sqrt((var16 * var16 + var17 * var17 + 65536)))
                var19 = integerdivide((var16 << 8), var18)
                var59 = integerdivide(65536, var18)
                var21 = integerdivide((var17 << 8), var18)
                var22 = integerdivide(
                    (var21 * -50 + var19 * -50 + var59 * -10), var75) + 96
                var23 = (var81[var15 - 1][var14] >> 2) + (var81[var15][var14 - 1] >> 2) + (
                    var81[var15 + 1][var14] >> 3) + (var81[var15][var14 + 1] >> 3) + (var81[var15][var14] >> 1)
                field1354[var15][var14] = var22 - var23

        

        for var14 in range(-5, 109):
            for var15 in range(0, 104):
                var16 = var14 + 5
                if(var16 >= 0 and var16 < 104):
                    var17 = tileUnderlayIds[var5][var16][var15] & 255
                    if(var17 > 0):
                        var85 = underlayDefinitions[var17 - 1]
                        floorHues[var15] += var85.hue
                        floorSaturations[var15] += var85.saturation
                        field3314[var15] += var85.lightness
                        floorMultiplier[var15] += var85.hueMultiplier
                        field1356[var15] += 1

                var17 = var14 - 5
                if(var17 >= 0 and var17 < 104):
                    var18 = tileUnderlayIds[var5][var17][var15] & 255
                    if(var18 > 0):
                        var84 = underlayDefinitions[var18 - 1]
                        floorHues[var15] -= var84.hue
                        floorSaturations[var15] -= var84.saturation
                        field3314[var15] -= var84.lightness
                        floorMultiplier[var15] -= var84.hueMultiplier
                        field1356[var15] -= 1

            if(var14 >= 1 and var14 < 103):

                var15 = 0
                var16 = 0
                var17 = 0
                var18 = 0
                var19 = 0

                for var59 in range(-5, 109):
                    var21 = var59 + 5
                    if(var21 >= 0 and var21 < 104):
                        var15 += floorHues[var21]
                        var16 += floorSaturations[var21]
                        var17 += field3314[var21]
                        var18 += floorMultiplier[var21]
                        var19 += field1356[var21]

                    var22 = var59 - 5
                    if(var22 >= 0 and var22 < 104):
                        var15 -= floorHues[var22]
                        var16 -= floorSaturations[var22]
                        var17 -= field3314[var22]
                        var18 -= floorMultiplier[var22]
                        var19 -= field1356[var22]

                    # not lowMemory or 
                    if(var59 >= 1 and var59 < 103 and
                            ((tileSettings[0][var14][var59] & 2) != 0 or (tileSettings[var5][var14][var59] & 16) == 0)):

                        # if(var5 < field747):
                        #    field747 = var5

                        var23 = tileUnderlayIds[var5][var14][var59] & 255
                        var62 = tileOverlayIds[var5][var14][var59] & 255
                        if(var23 > 0 or var62 > 0):
                            var25 = tileHeights[var5][var14][var59]
                            var26 = tileHeights[var5][var14 + 1][var59]
                            var27 = tileHeights[var5][var14 + 1][var59 + 1]
                            var28 = tileHeights[var5][var14][var59 + 1]
                            var29 = field1354[var14][var59]
                            var30 = field1354[var14 + 1][var59]
                            var63 = field1354[var14 + 1][var59 + 1]
                            var32 = field1354[var14][var59 + 1]
                            var33 = -1
                            var34 = -1
                            if(var23 > 0):
                                var35 = integerdivide(var15 * 256, var18)
                                var36 = integerdivide(var16, var19)
                                var37 = integerdivide(var17, var19)
                                var33 = method4490(var35, var36, var37)
                                var35 = var35 + field751 & 255
                                var37 += field745
                                if(var37 < 0):
                                    var37 = 0
                                elif(var37 > 255):
                                    var37 = 255

                                var34 = method4490(var35, var36, var37)

                            if(var5 > 0):
                                var78 = True
                                if(var23 == 0 and tileOverlayPath[var5][var14][var59] != 0):
                                    var78 = False

                                if var62 > 0 and not overlayDefinitions[var62 - 1].isHidden:
                                    var78 = False

                                if(var78 and var26 == var25 and var27 == var25 and var28 == var25):
                                    field2520[var5][var14][var59] |= 2340

                            var35 = 0
                            if(var34 != -1):
                                var35 = colorPalette[method3058(
                                    var34, 96)]

                            if(var62 == 0):

                                addTile(field1790, field1791, var5, var14, var59, 0, 0, -1, var25, var26, var27, var28, method3058(var33, var29),
                                        method3058(var33, var30), method3058(var33, var63), method3058(var33, var32), 0, 0, 0, 0, var35, 0, tiles)

                            else:

                                var36 = tileOverlayPath[var5][var14][var59] + 1
                                var79 = overlayRotations[var5][var14][var59]
                                var64 = overlayDefinitions[var62 - 1]
                                var39 = var64.texture
                                if(var39 >= 0):
                                    var41 = TextureLoaderGetAverageTextureRGB(
                                        textures, var39)
                                    var40 = -1
                                elif(var64.color == 16711935):
                                    var40 = -2
                                    var39 = -1
                                    var41 = -2
                                else:
                                    var40 = method4490(
                                        var64.hue, var64.saturation, var64.lightness)
                                    var42 = var64.hue + field751 & 255
                                    var43 = var64.lightness + field745
                                    if(var43 < 0):
                                        var43 = 0
                                    elif(var43 > 255):
                                        var43 = 255

                                    var41 = method4490(
                                        var42, var64.saturation, var43)

                                var42 = 0
                                if(var41 != -2):
                                    var42 = colorPalette[adjustHSLListness0(
                                        var41, 96)]

                                if(var64.otherRgbColor != -1):
                                    var43 = var64.otherHue + field751 & 255
                                    var44 = var64.otherLightness + field745
                                    if(var44 < 0):
                                        var44 = 0
                                    elif(var44 > 255):
                                        var44 = 255

                                    var41 = method4490(
                                        var43, var64.otherSaturation, var44)
                                    var42 = colorPalette[adjustHSLListness0(
                                        var41, 96)]

                                addTile(field1790, field1791, var5, var14, var59, var36, var79, var39, var25, var26, var27, var28, method3058(var33, var29), method3058(var33, var30), method3058(
                                    var33, var63), method3058(var33, var32), adjustHSLListness0(var40, var29), adjustHSLListness0(var40, var30), adjustHSLListness0(var40, var63), adjustHSLListness0(var40, var32), var35, var42, tiles)

        for var14 in range(1, 103):
            for var15 in range(1, 103):
                if((tileSettings[var5][var15][var14] & 8) != 0):
                    var59 = 0
                elif(var5 > 0 and (tileSettings[1][var15][var14] & 2) != 0):
                    var59 = var5 - 1
                else:
                    var59 = var5

                setPhysicalLevel(var5, var15, var14, var59, tiles)

    # Line 1823
    #class255region.applyLighting(-50, -10, -50, tileHeights, tiles)

    for var5 in range(0, 104):
        for var6 in range(0, 104):
            if((tileSettings[1][var5][var6] & 2) == 2):
                setBridge(var5, var6, tiles)

    var5 = 1
    var6 = 2
    var7 = 4

    for var73 in range(0, 4):
        if(var73 > 0):
            var5 <<= 3
            var6 <<= 3
            var7 <<= 3

        for var56 in range(0, var73 + 1):
            for var10 in range(0, 104 + 1):
                for var11 in range(0, 104 + 1):

                    if (field2520[var56][var11][var10] & var5) != 0:
                        var12 = var10
                        var75 = var10
                        var14 = var56

                        var15 = var56
                        while var12 > 0 and (field2520[var56][var11][var12 - 1] & var5) != 0:
                            var12 -= 1

                        while (var75 < 104 and (field2520[var56][var11][var75 + 1] & var5) != 0):
                            var75 += 1

                        breaklabel1011 = False
                        while (var14 > 0):
                            for var16 in range(var12, var75 + 1):
                                if ((field2520[var14 - 1][var11][var16] & var5) == 0):
                                    breaklabel1011 = True
                                    break

                            if breaklabel1011:
                                break

                            var14 -= 1

                        breaklabel1000 = False
                        while(var15 < var73):
                            for var16 in range(var12, var75 + 1):
                                if((field2520[var15 + 1][var11][var16] & var5) == 0):
                                    breaklabel1000 = True
                                    break

                            if breaklabel1000:
                                break

                            var15 += 1

                        var16 = (var15 + 1 - var14) * (var75 - var12 + 1)
                        if(var16 >= 8):
                            var77 = 240
                            var18 = tileHeights[var15][var11][var12] - var77
                            var19 = tileHeights[var14][var11][var12]
                            addOcclude(levelOccluders, levelOccluderCount,
                                       var73, 1, var11 * 128, var11 * 128, var12 * 128, var75 * 128 + 128, var18, var19)

                            for var59 in range(var14, var15 + 1):
                                for var21 in range(var12, var75 + 1):
                                    field2520[var59][var11][var21] &= ~var5

                    if((field2520[var56][var11][var10] & var6) != 0):
                        var12 = var11
                        var75 = var11
                        var14 = var56

                        var15 = var56
                        while var12 > 0 and (field2520[var56][var12 - 1][var10] & var6) != 0:
                            var12 -= 1

                        while(var75 < 104 and (field2520[var56][var75 + 1][var10] & var6) != 0):
                            var75 += 1

                        breaklabel1064 = False
                        while(var14 > 0):
                            for var16 in range(var12, var75 + 1):
                                if((field2520[var14 - 1][var16][var10] & var6) == 0):
                                    breaklabel1064 = True
                                    break

                            if breaklabel1064:
                                break

                            var14 -= 1

                        breaklabel1053 = False
                        while(var15 < var73):
                            for var16 in range(var12, var75 + 1):
                                if((field2520[var15 + 1][var16][var10] & var6) == 0):
                                    breaklabel1053 = True
                                    break

                            if breaklabel1053:
                                break

                            var15 += 1

                        var16 = (var75 - var12 + 1) * (var15 + 1 - var14)
                        if(var16 >= 8):
                            var77 = 240
                            var18 = tileHeights[var15][var12][var10] - var77
                            var19 = tileHeights[var14][var12][var10]
                            addOcclude(levelOccluders, levelOccluderCount,
                                       var73, 2, var12 * 128, var75 * 128 + 128, var10 * 128, var10 * 128, var18, var19)

                            for var59 in range(var14, var15 + 1):
                                for var21 in range(var12, var75 + 1):
                                    field2520[var59][var21][var10] &= ~var6

                    if((field2520[var56][var11][var10] & var7) != 0):
                        var12 = var11
                        var75 = var11
                        var14 = var10

                        # for(var15 = var10 var14 > 0 and (GZipDecompressor.field2520[var56][var11][var14 - 1] & var7) != 0 --var14) :
                        var15 = var10
                        while var14 > 0 and (field2520[var56][var11][var14 - 1] & var7) != 0:
                            var14 -= 1

                        while(var15 < 104 and (field2520[var56][var11][var15 + 1] & var7) != 0):
                            var15 += 1

                        breaklabel1117 = False
                        while(var12 > 0):
                            for var16 in range(var14, var15 + 1):
                                if((field2520[var56][var12 - 1][var16] & var7) == 0):
                                    breaklabel1117 = True
                                    break

                            if breaklabel1117:
                                break

                            var12 -= 1

                        breaklabel1106 = False
                        while(var75 < 104):
                            for var16 in range(var14, var15 + 1):
                                if((field2520[var56][var75 + 1][var16] & var7) == 0):
                                    breaklabel1106 = True
                                    break

                            if breaklabel1106:
                                break

                            var75 += 1

                        if((var75 - var12 + 1) * (var15 - var14 + 1) >= 4):
                            var16 = tileHeights[var56][var12][var14]
                            addOcclude(levelOccluders, levelOccluderCount,
                                       var73, 4, var12 * 128, var75 * 128 + 128, var14 * 128, var15 * 128 + 128, var16, var16)

                            for var17 in range(var12, var75 + 1):
                                for var18 in range(var14, var15 + 1):
                                    field2520[var56][var17][var18] &= ~var7

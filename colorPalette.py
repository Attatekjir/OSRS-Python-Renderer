from utills import adjustRGB
import numpy as np
from numba import jit

# method2786
@jit(nopython=True, cache=False)
def initiateColorPalette(colorPalette, brightness):

    colorid = 0
    for var5 in range(0, 512):
        var6 = (var5 >> 3) / 64.0 + 0.0078125
        var8 = (var5 & 7) / 8.0 + 0.0625

        for var10 in range(0, 128):
            var11 = var10 / 128.0
            var13 = var11
            var15 = var11
            var17 = var11
            if(var8 != 0.0):
                if(var11 < 0.5):
                    var19 = var11 * (1.0 + var8)
                else:
                    var19 = var11 + var8 - var11 * var8

                var21 = 2.0 * var11 - var19
                var23 = var6 + 0.3333333333333333
                if(var23 > 1.0):
                    var23 -= 1

                var27 = var6 - 0.3333333333333333
                if(var27 < 0.0):
                    var27 += 1

                if(6.0 * var23 < 1.0):
                    var13 = var21 + (var19 - var21) * 6.0 * var23
                elif(2.0 * var23 < 1.0):
                    var13 = var19
                elif(3.0 * var23 < 2.0):
                    var13 = var21 + (var19 - var21) * \
                        (0.6666666666666666 - var23) * 6.0
                else:
                    var13 = var21

                if(6.0 * var6 < 1.0):
                    var15 = var21 + (var19 - var21) * 6.0 * var6
                elif(2.0 * var6 < 1.0):
                    var15 = var19
                elif(3.0 * var6 < 2.0):
                    var15 = var21 + (var19 - var21) * \
                        (0.6666666666666666 - var6) * 6.0
                else:
                    var15 = var21

                if(6.0 * var27 < 1.0):
                    var17 = var21 + (var19 - var21) * 6.0 * var27
                elif(2.0 * var27 < 1.0):
                    var17 = var19
                elif(3.0 * var27 < 2.0):
                    var17 = var21 + (var19 - var21) * \
                        (0.6666666666666666 - var27) * 6.0
                else:
                    var17 = var21

            var29 = np.int32(var13 * 256.0)
            var20 = np.int32(var15 * 256.0)
            var30 = np.int32(var17 * 256.0)
            var22 = var30 + (var20 << 8) + (var29 << 16)
            var22 = adjustRGB(var22, brightness)
            if(var22 == 0):
                var22 = 1

            colorPalette[colorid] = var22
            colorid += 1

    return colorPalette
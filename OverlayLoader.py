from Buffer import Buffer
import numpy as np
from numba.experimental import jitclass
from numba import int32, float32, boolean
from numba import int64, types, typed
from numba.experimental import jitclass
import typing as pt

from numba import jit

@jitclass()
class OverlayDefinition:

    id: int32
    color: int32
    texture: int32
    otherRgbColor: int32
    isHidden: boolean

    hue: int32
    saturation: int32
    lightness: int32

    otherHue: int32
    otherSaturation: int32
    otherLightness: int32

    def __init__(self, id):

        self.id = id
        self.color = 0
        self.texture = -1
        self.otherRgbColor = -1
        self.isHidden = True

        self.hue = 0
        self.saturation = 0
        self.lightness = 0

        self.otherHue = 0
        self.otherSaturation = 0
        self.otherLightness = 0

@jit(nopython=True, cache=False)
def calculateHsl2(overlay, var1):

    var2 =  (var1 >> 16 & 255) / 256.0
    var4 =  (var1 >> 8 & 255) / 256.0
    var6 =  (var1 & 255) / 256.0
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
    var16 = (var8 + var10) / 2.0
    if (var10 != var8):

        if (var16 < 0.5):
            var14 = (var10 - var8) / (var10 + var8)

        if (var16 >= 0.5):
            var14 = (var10 - var8) / (2.0 - var10 - var8)

        if (var2 == var10):
            var12 = (var4 - var6) / (var10 - var8)

        elif (var4 == var10):
            var12 = 2.0 + (var6 - var2) / (var10 - var8)

        elif (var10 == var6):
            var12 = 4.0 + (var2 - var4) / (var10 - var8)

    var12 /= 6.0
    overlay.hue = np.int32(256.0 * var12)
    overlay.saturation = np.int32(var14 * 256.0)
    overlay.lightness = np.int32(var16 * 256.0)
    if (overlay.saturation < 0):
        overlay.saturation = 0

    elif (overlay.saturation > 255):
        overlay.saturation = 255

    if (overlay.lightness < 0):
        overlay.lightness = 0

    elif (overlay.lightness > 255):
        overlay.lightness = 255

@jit(nopython=True, cache=False)
def calculateHsl(overlay):

    if (overlay.otherRgbColor != -1):

        calculateHsl2(overlay, overlay.otherRgbColor)
        overlay.otherHue = overlay.hue
        overlay.otherSaturation = overlay.saturation
        overlay.otherLightness = overlay.lightness

    calculateHsl2(overlay, overlay.color)
	





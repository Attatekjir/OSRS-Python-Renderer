from Buffer import Buffer
import numpy as np
from numba.experimental import jitclass
from numba import int32, float32

spec1 = [
    ('id', int32),           
    ('color', int32), 
    ('hue', int32),
    ('saturation', int32),
    ('lightness', int32),
    ('hueMultiplier', int32),
]

@jitclass(spec1)
class UnderlayDefinition:

    def __init__(self, id, color, hue, saturation, lightness, hueMultiplier):

        self.id = id #None
        self.color = color #None

        self.hue = hue #None
        self.saturation = saturation #None
        self.lightness = lightness #None
        self.hueMultiplier = hueMultiplier #None

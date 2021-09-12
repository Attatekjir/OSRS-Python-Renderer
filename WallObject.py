from numba.experimental import jitclass
from expModel import Model
from numba import int32
import numba


Model_type = Model.class_type.instance_type

@jitclass()
class WallObject:

    floor : int32
    x : int32
    y : int32
    orientationA : int32
    orientationB : int32

    renderable1 : numba.optional(Model_type)
    renderable2 : numba.optional(Model_type)
    hash : int32
    config : int32

    def __init__(self, a, b):

        self.floor = 0
        self.x = 0
        self.y = 0
        self.orientationA = 0
        self.orientationB = 0

        self.renderable1 = a
        self.renderable2 = b

        self.hash = 0
        self.config = 0


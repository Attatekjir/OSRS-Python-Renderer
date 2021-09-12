from MathUtills import integerdivide
from numba import int32, float32, boolean, short, int64
#from FaceNormal import FaceNormal
import numpy as np
import math
from MathUtills import integerdivide
import numba
from Graphics3D import method2798, method2799
from numba.experimental import jitclass
from expModel import Model

Model_type = Model.class_type.instance_type
#Model_type = numba.deferred_type()

# spec = [
#     ('renderable1', numba.optional(Model_type)),
#     ('renderable2', numba.optional(Model_type))
# ]

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

        self.hash = 0
        self.config = 0
        self.renderable1 = a
        self.renderable2 = b

        # self.floor = None
        # self.x = None
        # self.y = None
        # self.orientationA = None
        # self.orientationB = None
        # self.renderable1 = None
        # self.renderable2 = None

#Model_type.define(Model.class_type.instance_type)
        


#    public static String method3061(final Buffer var0) :
#       String var1
#       try :
#          int var2 = var0.getUSmart()
#          if(var2 > 32767) :
#             var2 = 32767


#          final byte[] var3 = new byte[var2]
#          var0.offset += class313.huffman.decompress(var0.payload, var0.offset, var3, 0, var2)
#           var1 = ChatPlayer.getString(var3, 0, var2)
#        catch (final Exception var6) :
#          var1 = "Cabbage"


#       return var1


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

@jitclass()
class SceneTilePaint:

    flatShade : int32
    swColor : int32
    seColor : int32
    neColor : int32
    nwColor : int32
    texture : int32
    rgb : int32
    flatShade : boolean

    #varcs : int32
    #field1965 : int32
    #fonts : int32

    def __init__(self, var1,  var2,  var3,  var4,  var5,  var6, var7):
        #self.flatShade = True
        
        self.swColor = var1
        self.seColor = var2
        self.neColor = var3
        self.nwColor = var4
        self.texture = var5
        self.rgb = var6
        self.flatShade = var7

        #self.varcs = None
        #self.field1965 = None
        #self.fonts = None

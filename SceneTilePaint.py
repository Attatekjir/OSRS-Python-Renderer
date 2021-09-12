from numba.experimental import jitclass
from numba import int32, boolean
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

    def __init__(self, var1,  var2,  var3,  var4,  var5,  var6, var7):

        self.swColor = var1
        self.seColor = var2
        self.neColor = var3
        self.nwColor = var4
        self.texture = var5
        self.rgb = var6
        self.flatShade = var7

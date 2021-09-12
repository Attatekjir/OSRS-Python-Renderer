from Buffer import Buffer
import numpy as np
from MathUtills import integerdivide
from MathUtills import Graphics3DCOSINE, Graphics3DSINE
from logging import debug
from bitoperation import readUnsignedByte, readUnsignedShort, readShortSmart, readByte, readInt
from numba import jit
from numba import int32, float32
from Buffer import Buffer
from numba.experimental import jitclass
from numba import int32, float32, boolean, short, int64
#from FaceNormal import FaceNormal
import numpy as np
import math
from MathUtills import integerdivide
import numba

@jitclass()
class NpcDefinition:

    id : int32
    name : numba.types.unicode_type
    size : int32
    models : int32[:]
    chatheadModels : int32[:]
    standingAnimation : int32
    rotateLeftAnimation : int32
    rotateRightAnimation : int32
    walkingAnimation : int32
    rotate180Animation : int32
    rotate90RightAnimation : int32
    rotate90LeftAnimation : int32
    recolorToFind : short[:]
    recolorToReplace : short[:]
    retextureToFind : short[:]
    retextureToReplace : short[:]
    #actions : [''] * 5
    isMinimapVisible : boolean
    combatLevel : int32
    widthScale : int32
    heightScale : int32
    hasRenderPriority : boolean
    ambient : int32
    contrast : int32
    headIcon : int32
    rotationSpeed : int32
    configs : int32[:]
    varbitId : int32
    varpIndex : int32
    isInteractable : boolean
    rotationFlag : boolean
    isPet : boolean
    #params : int32
    category : int32


    def __init__(self, id):

        self.id = id

        pass

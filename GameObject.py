from numba.experimental import jitclass
from expModel import Model
from numba import int32
import numba

Model_type = Model.class_type.instance_type

@jitclass()
class GameObject :

    hash : int32
    flags : int32

    cycle : int32
    cameraZ : int32
    plane : int32
    height : int32
    x : int32
    y : int32
    renderable : numba.optional(Model_type)

    orientation : int32
    relativeX : int32
    relativeY : int32
    offsetX : int32
    offsetY : int32
    drawPriority : int32

    def __init__(self):

        self.hash = 0
        self.flags = 0

        self.cycle = 0
        self.cameraZ = 0
        self.plane = 0
        self.height = 0
        self.x = 0
        self.y = 0
        self.renderable = None

        self.orientation = 0
        self.relativeX = 0
        self.relativeY = 0
        self.offsetX = 0
        self.offsetY = 0
        self.drawPriority = 0
   

   


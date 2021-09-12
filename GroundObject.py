from numba.experimental import jitclass
from expModel import Model
from numba import int32

Model_type = Model.class_type.instance_type

@jitclass()
class GroundObject :

    #mapscene : int32
    floor : int32
    x : int32
    y : int32
    renderable : Model_type #int32
    hash : int32
    renderInfoBitPacked : int32

    def __init__(self, floor, x, y, renderable, hash, renderInfoBitPacked):

        #self.mapscene = None
        self.floor = floor
        self.x = x
        self.y = y
        self.renderable = renderable
        self.hash = hash
        self.renderInfoBitPacked = renderInfoBitPacked



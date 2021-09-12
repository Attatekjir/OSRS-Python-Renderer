import numpy as np
import numba
from GroundObject import GroundObject
from DecorativeObject import DecorativeObject
from WallObject import WallObject
from SceneTileModel import SceneTileModel
from SceneTilePaint import SceneTilePaint
from GameObject import GameObject
from numba import int32, float32, boolean, short, int64
from numba.experimental import jitclass

atype = SceneTilePaint.class_type.instance_type
btype = SceneTileModel.class_type.instance_type
ctype = WallObject.class_type.instance_type
dtype = DecorativeObject.class_type.instance_type
etype = GroundObject.class_type.instance_type
#ftype = ItemLayer.class_type.instance_type
gtype = GameObject.class_type.instance_type
tile_type = numba.deferred_type()


@jitclass()
class Tile():

    paint: numba.optional(atype)
    overlay: numba.optional(btype)
    wallObject: numba.optional(ctype)
    decorativeObject: numba.optional(dtype)
    groundObject: numba.optional(etype)
    # itemLayer : int32
    entityCount: int32
    # numba.optional(numba.types.ListType(gtype))
    objects: numba.types.ListType(gtype)

    physicalLevel: int32
    draw: boolean
    visible: boolean
    drawEntities: boolean
    wallCullDirection: int32
    wallUncullDirection: int32
    wallCullOppositeDirection: int32
    wallDrawFlags: int32
    bridge: numba.optional(tile_type)

    entityFlags: numba.optional(int32[:])
    flags: int32

    plane: int32
    renderLevel: int32
    x: int32
    y: int32

    def __init__(self, plane, x, y):

        self.paint = None
        self.overlay = None
        self.wallObject = None
        self.decorativeObject = None
        self.groundObject = None
        # self.itemLayer = None
        # self.entityCount = 0
        self.objects = numba.typed.List.empty_list(gtype)  # self.objects = [None] * 5
        for i in range(0, 5):
            self.objects.append(GameObject())

        # self.physicalLevel = 10
        # self.draw = False
        # self.visible = False
        # self.drawEntities = False
        # self.wallCullDirection = 0
        # self.wallUncullDirection = 0
        # self.wallCullOppositeDirection = 0
        # self.wallDrawFlags = 0
        self.bridge = None

        self.entityFlags = np.zeros(shape=(5), dtype=np.int32)  # [0] * 5
        #self.flags = 0

        self.plane = plane
        self.renderLevel = plane
        self.x = x
        self.y = y

    def reset(self):

        self.paint = None
        self.overlay = None
        self.wallObject = None
        self.decorativeObject = None
        self.groundObject = None
        # self.itemLayer = None
        self.entityCount = 0
        # self.objects = numba.typed.List.empty_list(gtype)  # self.objects = [None] * 5
        # for i in range(0, 5):
        #     self.objects.append(GameObject())

        self.physicalLevel = 0 # As long as it is more than 10
        self.draw = False
        self.visible = False
        self.drawEntities = False
        self.wallCullDirection = 0
        self.wallUncullDirection = 0
        self.wallCullOppositeDirection = 0
        self.wallDrawFlags = 0
        self.bridge = None

        # = np.zeros(shape=(5), dtype=np.int32)  # [0] * 5
        self.entityFlags.fill(0)
        self.flags = 0



tile_type.define(Tile.class_type.instance_type)

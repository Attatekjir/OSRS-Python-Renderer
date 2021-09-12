from Buffer import Buffer
from expModel import method2686
import expModelData
from expModelData import ModelData2, ModelData4
from expModelData import light
from expModelData import ModelData
import numpy as np
from numba import int32, float32
from numba.experimental import jitclass
from numba import int32, float32, boolean, short, int64
from DefinitionLoaders import loadModelData
import numpy as np
import numba

modeldata_type = ModelData.class_type.instance_type


@numba.jit(nopython=True, cache=False)
def getModelFromCache(uncryptedModelContents, modelID):

    data = uncryptedModelContents[modelID]
    modelData = loadModelData(modelID, data)

    return modelData


@jitclass()
class ObjectDefinition:

    objectCompositionLowDetail: boolean
    # objects_ref : int32
    # models_ref : int32
    # objects : int32 #NodeCache(4096)
    # field3593 : int32 #NodeCache(500)
    # cachedModels : int32 #NodeCache(30)
    # field3595 : int32 #NodeCache(30)

    field3596: numba.types.ListType(modeldata_type)  # int32 ModelData

    field3640: int32
    id: int32
    objectModels: numba.optional(int32[:])
    objectTypes: int32[:]
    name: numba.types.unicode_type
    recolorToFind: short[:]
    recolorToReplace: short[:]
    textureToFind: short[:]
    textureToReplace: short[:]
    width: int32
    length: int32
    field3614: int32[:]
    params: boolean  # hmm, DUMMY
    clipType: int32
    blocksProjectile: boolean
    int1: int32
    contouredGround: int32
    nonFlatShading: boolean
    modelClipped: boolean
    animationId: int32
    decorDisplacement: int32
    ambient: int32
    contrast: int32
    #actions  : numba.types.unicode_type
    mapIconId: int32
    mapSceneId: int32
    isRotated: boolean
    clipped: boolean
    modelSizeX: int32
    modelSizeHeight: int32
    modelSizeY: int32
    offsetX: int32
    offsetHeight: int32
    offsetY: int32
    obstructsGround: boolean
    isHollow: boolean
    supportItems: int32
    varpId: int32
    configId: int32
    ambientSoundId: int32
    int4: int32
    int5: int32
    int6: int32
    impostorIds: int32[:]

    def __init__(self, id):
        self.id = id

        self.field3596 = numba.typed.List.empty_list(modeldata_type)
        for i in range(0, 4):
            self.field3596.append(ModelData())

        self.objectCompositionLowDetail = False

        self.name = "null"
        self.width = 1
        self.length = 1
        self.clipType = 2
        self.blocksProjectile = True
        self.int1 = -1
        self.contouredGround = -1
        self.nonFlatShading = False
        self.modelClipped = False
        self.animationId = -1
        self.decorDisplacement = 16
        self.ambient = 0
        self.contrast = 0
        # self.actions = new String[5]
        self.mapIconId = -1
        self.mapSceneId = -1
        self.isRotated = False
        self.clipped = True
        self.modelSizeX = 128
        self.modelSizeHeight = 128
        self.modelSizeY = 128
        self.offsetX = 0
        self.offsetHeight = 0
        self.offsetY = 0
        self.obstructsGround = False
        self.isHollow = False
        self.supportItems = -1
        self.varpId = -1
        self.configId = -1
        self.ambientSoundId = -1
        self.int4 = 0
        self.int5 = 0
        self.int6 = 0


@numba.jit(nopython=True, cache=False)
def getModel(uncryptedModelContents, objectDef, objectType, orientation, tileHeight, var4, var5, var6):

    modelData = getModel2(uncryptedModelContents, objectDef,
                          objectType, orientation)
    #model = modelData.light(objectDef.ambient + 64, objectDef.contrast + 768, -50, -10, -50)

    #if objectDef.width > 1 or objectDef.length > 1:
    #    print("<>", objectDef.name, objectDef.width, objectDef.length)

    

    #print("flatshade?", objectDef.nonFlatShading)
    model = light(modelData, objectDef.ambient + 64,
                  objectDef.contrast + 768, -50, -10, -50)

    if(objectDef.contouredGround >= 0):
        model = method2686(model, tileHeight, var4, var5,
                           var6, True, objectDef.contouredGround)

    return model


@numba.jit(nopython=True, cache=False)
def getModel2(uncryptedModelContents, objectDef, objectType, orientation):
    var3 = None

    if(objectDef.objectTypes.size == 0):

        if(objectType != 10):
            raise Exception("how?")
            return None

        if(objectDef.objectModels is None):
            raise Exception("how2?")
            return None

        var4 = objectDef.isRotated
        if(objectType == 2 and orientation > 3):
            var4 = not var4

        #var5 = len(objectDef.objectModels)
        var5 = objectDef.objectModels.size

        for var6 in range(0, var5):
            #var7 = np.int32(objectDef.objectModels[var6])
            var7 = objectDef.objectModels[var6]
            # if var4:
            #var7 += np.int32(65536)

            var3 = getModelFromCache(uncryptedModelContents, var7)
            if var4:
                expModelData.method2614(var3)

            if(var5 > 1):
                objectDef.field3596[var6] = var3

        if(var5 > 1):
            #var3 = ModelData(objectDef.field3596, var5)
            var3 = ModelData()
            ModelData2(var3, objectDef.field3596, var5)

    else:

        var9 = -1
        # for var5 in range(0, len(objectDef.objectTypes)):
        for var5 in range(0, objectDef.objectTypes.size):
            if(objectDef.objectTypes[var5] == objectType):
                var9 = var5
                break
        if(var9 == -1):
            raise Exception("When ever?")

        # np.int32(objectDef.objectModels[var9])
        var5 = objectDef.objectModels[var9]
        var10 = objectDef.isRotated ^ orientation > 3
        #if var10:
        #    pass
        #    var5 += np.int32(65536)

        #var5 == ModelID
        var3 = getModelFromCache(uncryptedModelContents, var5)
        if var10:
            expModelData.method2614(var3)

    var4 = objectDef.modelSizeX != 128 or objectDef.modelSizeHeight != 128 or objectDef.modelSizeY != 128

    var11 = objectDef.offsetX != 0 or objectDef.offsetHeight != 0 or objectDef.offsetY != 0

    arg9991 = orientation == 0 and not var4 and not var11
    arg9992 = objectDef.recolorToFind.size == 0  # is None
    arg9993 = objectDef.textureToFind.size == 0  # is None
    var8 = ModelData()
    ModelData4(var8, var3, arg9991, arg9992, arg9993)
    #var8 = ModelData(var3, arg9991, arg9992, arg9993)

    if(objectType == 4 and orientation > 3):
        expModelData.method2606(var8, 256)
        expModelData.method2611(var8, 45, 0, -45)

    # Rotate the model if needed
    orientation &= 3
    if(orientation == 1):
        expModelData.method2607(var8)
    elif(orientation == 2):
        expModelData.method2625(var8)
    elif(orientation == 3):
        expModelData.method2610(var8)

    if(objectDef.recolorToFind.size > 0):  # is not None):
        for var7 in range(0, objectDef.recolorToFind.size):
            expModelData.recolor(var8,
                                 objectDef.recolorToFind[var7], objectDef.recolorToReplace[var7])

    if(objectDef.textureToFind.size > 0):  # is not None):
        for var7 in range(0, objectDef.textureToFind.size):
            expModelData.method2613(var8,
                                    objectDef.textureToFind[var7], objectDef.textureToReplace[var7])

    if var4:
        expModelData.method2615(var8, objectDef.modelSizeX,
                                objectDef.modelSizeHeight, objectDef.modelSizeY)

    if var11:
        expModelData.method2611(var8, objectDef.offsetX,
                                objectDef.offsetHeight, objectDef.offsetY)

    var8.objectID = objectDef.id

    return var8


@numba.jit(nopython=True, cache=False)
def loadObjectDefinition(id, b):

    objdef = ObjectDefinition(id)
    stream = Buffer(b)

    while True:
        opcode = stream.readUnsignedByte()
        if (opcode == 0):
            break

        elif(opcode == 1):
            var3 = stream.readUnsignedByte()
            if(var3 > 0):
                if(objdef.objectModels is not None and not objdef.objectCompositionLowDetail):
                    stream.offset += 3 * var3
                else:
                    objdef.objectTypes = np.empty(
                        shape=(var3), dtype=np.int32)  # [0] * var3
                    objdef.objectModels = np.empty(
                        shape=(var3), dtype=np.int32)  # [0] * var3
                    for var4 in range(0, var3):
                        objdef.objectModels[var4] = stream.readUnsignedShort()
                        objdef.objectTypes[var4] = stream.readUnsignedByte()
        elif(opcode == 2):
            objdef.name = stream.readString()
        elif(opcode == 5):
            var3 = stream.readUnsignedByte()
            if(var3 > 0):
                if(objdef.objectModels is not None and not objdef.objectCompositionLowDetail):
                    stream.offset += var3 * 2
                else:
                    objdef.objectTypes = np.empty(
                        shape=(0), dtype=np.int32)  # None
                    objdef.objectModels = np.empty(
                        shape=(var3), dtype=np.int32)  # [0] * var3
                    for var4 in range(0, var3):
                        objdef.objectModels[var4] = stream.readUnsignedShort()
        elif(opcode == 14):
            objdef.width = stream.readUnsignedByte()
        elif(opcode == 15):
            objdef.length = stream.readUnsignedByte()
        elif(opcode == 17):
            objdef.clipType = 0
            objdef.blocksProjectile = False
        elif(opcode == 18):
            objdef.blocksProjectile = False
        elif(opcode == 19):
            objdef.int1 = stream.readUnsignedByte()
        elif(opcode == 21):
            objdef.contouredGround = 0
        elif(opcode == 22):
            objdef.nonFlatShading = True
        elif(opcode == 23):
            objdef.modelClipped = True
        elif(opcode == 24):
            objdef.animationId = stream.readUnsignedShort()
            if(objdef.animationId == 65535):
                objdef.animationId = -1
        elif(opcode == 27):
            objdef.clipType = 1
        elif(opcode == 28):
            objdef.decorDisplacement = stream.readUnsignedByte()
        elif(opcode == 29):
            objdef.ambient = stream.readByte()
        elif(opcode == 39):
            objdef.contrast = stream.readByte() * 25
        elif(opcode >= 30 and opcode < 35):
            var9999 = stream.readString()
            #objdef.actions[opcode - 30] = stream.readString()
            # if objdef.actions[opcode - 30] == "Hidden":
            #    objdef.actions[opcode - 30] = None
        elif(opcode == 40):
            var3 = stream.readUnsignedByte()
            objdef.recolorToFind = np.empty(
                shape=(var3,), dtype=np.short)  # new short[var3]
            objdef.recolorToReplace = np.empty(
                shape=(var3,), dtype=np.short)  # new short[var3]
            for var4 in range(0, var3):
                objdef.recolorToFind[var4] = stream.readUnsignedShort()
                objdef.recolorToReplace[var4] = stream.readUnsignedShort()
        elif(opcode == 41):
            var3 = stream.readUnsignedByte()
            objdef.textureToFind = np.empty(
                shape=(var3,), dtype=np.short)  # new short[var3]
            objdef.textureToReplace = np.empty(
                shape=(var3,), dtype=np.short)  # new short[var3]
            for var4 in range(0, var3):
                objdef.textureToFind[var4] = stream.readUnsignedShort()
                objdef.textureToReplace[var4] = stream.readUnsignedShort()
        elif(opcode == 62):
            objdef.isRotated = True
        elif(opcode == 64):
            objdef.clipped = False
        elif(opcode == 65):
            objdef.modelSizeX = stream.readUnsignedShort()
        elif(opcode == 66):
            objdef.modelSizeHeight = stream.readUnsignedShort()
        elif(opcode == 67):
            objdef.modelSizeY = stream.readUnsignedShort()
        elif(opcode == 68):
            objdef.mapSceneId = stream.readUnsignedShort()
        elif(opcode == 69):
            stream.readUnsignedByte()
        elif(opcode == 70):
            objdef.offsetX = stream.readShort()
        elif(opcode == 71):
            objdef.offsetHeight = stream.readShort()
        elif(opcode == 72):
            objdef.offsetY = stream.readShort()
        elif(opcode == 73):
            objdef.obstructsGround = True
        elif(opcode == 74):
            objdef.isHollow = True
        elif(opcode == 75):
            objdef.supportItems = stream.readUnsignedByte()
        elif(opcode != 77 and opcode != 92):
            if(opcode == 78):
                objdef.ambientSoundId = stream.readUnsignedShort()
                objdef.int4 = stream.readUnsignedByte()
            elif(opcode == 79):
                objdef.int5 = stream.readUnsignedShort()
                objdef.int6 = stream.readUnsignedShort()
                objdef.int4 = stream.readUnsignedByte()
                var3 = stream.readUnsignedByte()
                objdef.field3614 = np.empty(
                    shape=(var3), dtype=np.int32)  # [0] * var3
                for var4 in range(0, var3):
                    objdef.field3614[var4] = stream.readUnsignedShort()
            elif(opcode == 81):
                objdef.contouredGround = stream.readUnsignedByte() * 256
            elif(opcode == 82):
                objdef.mapIconId = stream.readUnsignedShort()
            elif(opcode == 249):
                var9999 = stream.readStringIntParametersSpoofed(objdef.params)
                #objdef.params = stream.readStringIntParameters(objdef.params)
        else:
            objdef.varpId = stream.readUnsignedShort()
            if(objdef.varpId == 65535):
                objdef.varpId = -1
            objdef.configId = stream.readUnsignedShort()
            if(objdef.configId == 65535):
                objdef.configId = -1
            var3 = -1
            if(opcode == 92):
                var3 = stream.readUnsignedShort()
                if(var3 == 65535):
                    var3 = -1
            var4 = stream.readUnsignedByte()
            objdef.impostorIds = np.zeros(
                shape=(var4 + 2), dtype=np.int32)  # [0] * (var4 + 2)
            for var5 in range(0, var4 + 1):
                objdef.impostorIds[var5] = stream.readUnsignedShort()
                if(objdef.impostorIds[var5] == 65535):
                    objdef.impostorIds[var5] = -1
            objdef.impostorIds[var4 + 1] = var3

    return objdef

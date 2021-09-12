
from OverlayLoader import OverlayDefinition
from TextureDefinition import method2680
from NpcDefinition import NpcDefinition
from expObjectDefinition import ObjectDefinition
from cacheUtills import loadContents
from SpriteDefinition import SpriteDefinition
import numba
from fileCounts import FILECOUNTS195
from UnderlayLoader import UnderlayDefinition
from numba import int64, typed
from SpriteDefinition import loadSprite
from DefinitionLoaders import loadUnderlayDefinition, loadNpcDefinition, loadOverlayDefinition, loadModelData, loadTextureDefinitions
from TextureDefinition import TextureDefinition
from expObjectDefinition import loadObjectDefinition

class cacheStore:

    def __init__(self, FileStore_):

        self.textureWidth = 128
        self.FileStore_ = FileStore_

    def getAllUnderlayDefinitions(self):

        def gte():
            print("ATTENTION THIS ONLY WORKS FOR SPECIFIC J")
            return [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60,
                    61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 77, 91, 92, 93, 94, 95, 96, 97, 98, 99, 102, 110, 111, 112, 113, 114, 115, 117, 120, 121, 123, 124, 125, 128, 137, 138, 139, 140, 141, 142, 143, 144, 145, 146, 147, 148, 149]

        data = self.FileStore_.FileStoreRead(2, 1)

        contents = loadContents(data, FILECOUNTS195.UNDERLAY.value)

        idToIndex = gte()

        ci = UnderlayDefinition.class_type.instance_type
        underlayDefinitions = numba.typed.Dict.empty(
            key_type=int64, value_type=ci)

        for i, content in enumerate(contents):

            id = idToIndex[i]

            underlayDefinition = loadUnderlayDefinition(id, content)
            underlayDefinitions[id] = underlayDefinition

        return underlayDefinitions

    def getAllOverlayDefinitions(self):

        data = self.FileStore_.FileStoreRead(2, 4)
        contents = loadContents(data, FILECOUNTS195.OVERLAY.value)

        ci = OverlayDefinition.class_type.instance_type
        overlayDefinitions = typed.List.empty_list(ci)

        #overlayDefinitions = [None] * len(contents)
        for i, content in enumerate(contents):
            overlayDefinition = loadOverlayDefinition(i, content)
            #overlayDefinitions[i] = overlayDefinition
            overlayDefinitions.append(overlayDefinition)

        return overlayDefinitions

    def getAllSprites(self):

        ci = SpriteDefinition.class_type.instance_type
        lci = numba.typeof(typed.List.empty_list(ci))

        sprites = numba.typed.Dict.empty(key_type=int64, value_type=lci)
        for id in range(0, self.FileStore_.GetIDCount(8)):

            data = self.FileStore_.FileStoreRead(8, id)
            spriteDefinitionList = loadSprite(id, data, ci)
            sprites[id] = spriteDefinitionList

        return sprites

    def getAllTextures(self):

        sprites = self.getAllSprites()

        data = self.FileStore_.FileStoreRead(9, 0)

        # Need to be inferred within CPython
        ci = TextureDefinition.class_type.instance_type

        # A NumbaDict of textures
        textures = loadTextureDefinitions(data, ci)

        brightness = 0.6
        for texid in textures:
            texture = textures[texid]
            method2680(texture, brightness, self.textureWidth, sprites)

        return textures

    def getAllNpcDefinitions(self):

        data = self.FileStore_.FileStoreRead(2, 9)
        contents = loadContents(data, FILECOUNTS195.NPC.value)

        ci = NpcDefinition.class_type.instance_type
        npcDefinitions = numba.typed.Dict.empty(key_type=int64, value_type=ci)

        for i, content in enumerate(contents):
            npcDefinition = loadNpcDefinition(i, content)
            npcDefinitions[i] = npcDefinition

        return npcDefinitions



    def getAllObjectDefinitions(self):

        data = self.FileStore_.FileStoreRead(2, 6)
        contents = loadContents(data, FILECOUNTS195.OBJECT.value)

        ci = ObjectDefinition.class_type.instance_type
        objectDefinitions = typed.List.empty_list(ci)

        for i, content in enumerate(contents):
            objectDefinition = loadObjectDefinition(i, content)
            objectDefinitions.append(objectDefinition)

        return objectDefinitions



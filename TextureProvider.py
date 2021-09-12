from numba import jit

@jit(nopython=True, cache=False)
def TextureLoaderGetAverageTextureRGB(textures, textureId) :

    #texture = self.cacheStore_.getTexture(textureId)
    texture = textures[textureId]

    return texture.field1803

    #if texture is not None:
    #    return texture.field1803
    #else:
    #    return 0

@jit(nopython=True, cache=False)
def TextureLoaderLoad(textures, textureId) :
    #texture = self.cacheStore_.getTexture(var1) #self.textures[var1]

    texture = textures[textureId]

    #if texture is None:
    #    raise Exception("Texture does not exist?")

    return texture.pixels

@jit(nopython=True, cache=False)
def TextureLoaderVmethod3069(textures, textureId) :
    # self.textures[textureId].field1806
    #return self.cacheStore_.getTexture(textureId).field1806 
    return textures[textureId].field1806

@jit(nopython=True, cache=False)
def TextureLoaderIsLowMem(textures, var1) :
    return False #self.textures[var1].width == 64 #False #self.width == 64

from numba import int32, float32, boolean, short, int64
from numba.experimental import jitclass
from expModel import Model

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

    # def method2669(var0) :
    #     return (var0 >> 21 & 1) != 0


    # def method2670() :
    #     if(Client.localPlayer.x >> 7 == Client.destinationX and Client.localPlayer.y >> 7 == Client.destinationY) :
    #         Client.destinationX = 0


    # def method2671() :
    #     var0 = WorldMapRectangle.method280(ClientPacket.field2398, Client.field957.field1484)
    #     var0.packetBuffer.putByte(0)
    #     Client.field957.method2052(var0)


    # def getWidgetClickMask(var0) :
    # final IntegerNode var1 = (IntegerNode)Client.widgetFlags.get(((long)var0.id << 32) + var0.index)
    # return var1 != null?var1.value:var0.clickMask
   


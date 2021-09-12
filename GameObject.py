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

    def __init__(self): #, renderable_):
        self.hash = 0
        self.flags = 0

        #self.renderable = renderable_

        # self.cycle = None
        # self.cameraZ = None
        # self.plane = None
        # self.height = None
        # self.x = None
        # self.y = None
        # self.renderable = None
        # self.orientation = None
        # self.relativeX = None
        # self.relativeY = None
        # self.offsetX = None
        # self.offsetY = None
        # self.drawPriority = None
   

    # def method3083(var0, var1, var2) :
    #     if(var0.animation == var1 and var1 != -1) :
    #         var3 = CombatInfo1.getAnimation(var1).replyMode
    #         if(var3 == 1) :
    #             var0.actionFrame = 0
    #             var0.actionFrameCycle = 0
    #             var0.actionAnimationDisable = var2
    #             var0.field1193 = 0

    #         if(var3 == 2) :
    #             var0.field1193 = 0

    #     elif(var1 == -1 or var0.animation == -1 or CombatInfo1.getAnimation(var1).forcedPriority >= CombatInfo1.getAnimation(var0.animation).forcedPriority) :
    #         var0.animation = var1
    #         var0.actionFrame = 0
    #         var0.actionFrameCycle = 0
    #         var0.actionAnimationDisable = var2
    #         var0.field1193 = 0
    #         var0.field1216 = var0.queueSize
      

   


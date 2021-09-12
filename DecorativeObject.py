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
class DecorativeObject:

    hash : int32
    renderInfoBitPacked : int32

    floor : int32
    x : int32
    y : int32
    renderFlag : int32
    rotation : int32
    offsetX : int32
    offsetY : int32
    renderable1 : Model_type # Must always be a valid Model according to region.py
    renderable2 : numba.optional(Model_type)

    def __init__(self, a, b):
        self.hash = 0
        self.renderInfoBitPacked = 0

        # self.floor = None
        # self.x = None
        # self.y = None
        # self.renderFlag = None
        # self.rotation = None
        # self.offsetX = None
        # self.offsetY = None
        self.renderable1 = a
        self.renderable2 = b



    # def method3082(var0) :
    #     try :
    #     Thread.sleep(var0)
    #     catch (final InterruptedException ignored) :




    # def method3081() :
    #     synchronized(KeyFocusListener.keyboard) :
    #     ++KeyFocusListener.keyboardIdleTicks
    #     KeyFocusListener.field620 = KeyFocusListener.field623
    #     KeyFocusListener.field638 = 0
    #     int var1
    #     if(KeyFocusListener.field627 < 0) :
    #     for(var1 = 0 var1 < 112 ++var1) :
    #     KeyFocusListener.keyPressed[var1] = false


    #     KeyFocusListener.field627 = KeyFocusListener.field626
    #     else :
    #     while(KeyFocusListener.field627 != KeyFocusListener.field626) :
    #     var1 = KeyFocusListener.field625[KeyFocusListener.field626]
    #     KeyFocusListener.field626 = KeyFocusListener.field626 + 1 & 127
    #     if(var1 < 0) :
    #     KeyFocusListener.keyPressed[~var1] = false
    #     else :
    #     if(!KeyFocusListener.keyPressed[var1] && KeyFocusListener.field638 < KeyFocusListener.field630.length - 1) :
    #     KeyFocusListener.field630[++KeyFocusListener.field638 - 1] = var1


    #     KeyFocusListener.keyPressed[var1] = true




    #     if(KeyFocusListener.field638 > 0) :
    #     KeyFocusListener.keyboardIdleTicks = 0


    #     KeyFocusListener.field623 = KeyFocusListener.field631




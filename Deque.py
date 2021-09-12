from numba.experimental import jitclass
import numpy as np
import numba

npint32type = numba.typeof(np.empty(shape=(1, 1), dtype=np.int32))

@jitclass()
class Deque:

    slots : npint32type
    #head : tile_typecurr # Else can not set self.head.next = X
    #current : numba.optional(DequeComponent_typecurr)

    def __init__(self):

        # Really cheecky +1, so 'head' is on position [-1] of array
        slots = np.zeros(shape = (4 * 104 * 104 + 1, 4), dtype = np.int32)
        slots[:, 0] = -1
        slots[-1, 1] = 1 #-1 #In use
        slots[:, 2] = -1
        slots[:-1, 3] = np.arange(4 * 104 * 104, dtype = np.int32)

        self.slots = slots

    def unlink(self, tileID):

        slot = self.slots[tileID]
            
        prevID = slot[0]
        nextID = slot[2]

        #if prevID != -1:
        prevslot = self.slots[prevID]
        prevslot[2] = nextID

        #if nextID != -1:
        nextslot = self.slots[nextID]
        nextslot[0] = prevID

        slot[0] = -1
        slot[1] = 0 # Mark as not in use
        slot[2] = -1

        return slot

        #self.slots[tileID] = slot

    def addFront(self, tileID):

        slot = self.slots[tileID]

        # if var1.previous is not None:
        #     var1.unlink()

        # Is it in use?
        if slot[1] == 1:

            slot = self.unlink(tileID)

        slot[0] = self.slots[-1][0] # var1.previous = self.head.previous
        slot[1] = 1 #mark as in use
        slot[2] = -1 # var1.next = self.head
        
        prevID = slot[0]
        nextID = slot[2]        

        prevslot = self.slots[prevID]
        prevslot[2] = tileID # var1.previous.setNext(var1) # = var1

        nextslot = self.slots[nextID]
        nextslot[0] = tileID # var1.next.setPrevious(var1) #previous = var1   

        #self.slots[tileID] = slot
        

    def popFront(self):
        nextslotID = self.slots[-1][2] #self.head.next

        #if(var1 == self.head):
        if(nextslotID == -1):
            return -1
        else:
            _ = self.unlink(nextslotID)
            self.slots[nextslotID] = _
            return nextslotID


# Deque_ = Deque()

# Deque_.addFront(1)
# Deque_.addFront(3456)
# Deque_.addFront(3)
# Deque_.addFront(4)
# Deque_.addFront(8)
# Deque_.addFront(1)
# print(Deque_.popFront())
# print(Deque_.popFront())
# print(Deque_.popFront())
# print(Deque_.popFront())
# print(Deque_.popFront())
# print(Deque_.popFront())
# print(Deque_.popFront())
# print(Deque_.popFront())


# # class Deque:

# #     def __init__(self):
# #         self.head = Node()
# #         self.head.hash = -1
# #         self.head.next = self.head
# #         self.head.previous = self.head

# #     #def Deque(self):
# #     #    self.head = Node()
# #     #    self.head.next = self.head
# #     #    self.head.previous = self.head

# #     def clear(self):

# #         while(True):
# #             var1 = self.head.next
# #             # if var1 == self.head:
# #             if var1.hash == -1:
# #                 self.current = None
# #                 return

# #             var1.unlink()

# #     def addFront(self, var1):
# #         if var1.previous is not None:
# #             var1.unlink()

# #         var1.previous = self.head.previous
# #         var1.next = self.head
# #         var1.previous.next = var1
# #         var1.next.previous = var1


# #     def addTail(self, var1):
# #         if var1.previous is not None:
# #             var1.unlink()

# #         var1.previous = self.head
# #         var1.next = self.head.next
# #         var1.previous.next = var1
# #         var1.next.previous = var1

# #     def popFront(self):
# #         var1 = self.head.next

# #         #if(var1 == self.head):
# #         if(var1.hash == -1):
# #             return None
# #         else:
# #             var1.unlink()
# #             return var1

# #     def popTail(self):
# #         var1 = self.head.previous
# #         #if(var1 == self.head):
# #         if(var1.hash == -1):
# #             return None
# #         else:
# #             var1.unlink()
# #             return var1

# #     def getFront(self):
# #         var1 = self.head.next
# #         #if(var1 == self.head):
# #         if(var1.hash == -1):
# #             self.current = None
# #             return None
# #         else:
# #             self.current = var1.next
# #             return var1

# #     def getTail(self):
# #         var1 = self.head.previous
# #         #if(var1 == self.head):
# #         if(var1.hash == -1):
# #             self.current = None
# #             return None
# #         else:
# #             self.current = var1.previous
# #             return var1

# #     def getNext(self):
# #         var1 = self.current
# #         #if(var1 == self.head):
# #         if(var1.hash == -1):
# #             self.current = None
# #             return None
# #         else:
# #             self.current = var1.next
# #             return var1

# #     def getPrevious(self):
# #         var1 = self.current
# #         #if(var1 == self.head):
# #         if(var1.hash == -1):
# #             self.current = None
# #             return None
# #         else:
# #             self.current = var1.previous
# #             return var1

# #     def method4011(self,  var0,  var1):
# #         if(var0.previous is not None):
# #             var0.unlink()

# #         var0.previous = var1.previous
# #         var0.next = var1
# #         var0.previous.next = var0
# #         var0.next.previous = var0
# from Tile import Tile

# from numba.experimental import jitclass
# from expModel import Model

# tile_typecurr = Tile.class_type.instance_type
# import numba

# @jitclass()
# class Deque:

#     head : tile_typecurr # Else can not set self.head.next = X
#     current : numba.optional(tile_typecurr)

#     def __init__(self):
#         newNode = Tile(0, 1, 2)
#         newNode.hash = -1 # So we can identify the head
#         self.head = newNode

#         self.head.next = None # Test whether they can be set to None
#         self.head.next = newNode

#         self.head.previous = None # Test whether they can be set to None
#         self.head.previous = newNode

#         self.current = newNode # Test whether they can be set to a Node
#         self.current = None 


#     def clear(self):

#         while(True):
#             var1 = self.head.next
#             # if var1 == self.head:
#             if var1.hash == -1:            
#                 self.current = None
#                 return

#             var1.unlink()

#     def addFront(self, var1):
#         if var1.previous is not None:
#             var1.unlink()

#         var1.previous = self.head.previous
#         var1.next = self.head
#         var1.previous.setNext(var1) # = var1
#         var1.next.setPrevious(var1) #previous = var1


#     def addTail(self, var1):
#         if var1.previous is not None:
#             var1.unlink()

#         var1.previous = self.head
#         var1.next = self.head.next
#         var1.previous.setNext(var1) #.next = var1
#         var1.next.setPrevious(var1) #previous = var1

#     def popFront(self):
#         var1 = self.head.next

#         #if(var1 == self.head):
#         if(var1.hash == -1):
#             return None
#         else:
#             var1.unlink()
#             return var1

#     def popTail(self):
#         var1 = self.head.previous
#         #if(var1 == self.head):
#         if(var1.hash == -1):
#             return None
#         else:
#             var1.unlink()
#             return var1

#     def getFront(self):
#         var1 = self.head.next
#         #if(var1 == self.head):
#         if(var1.hash == -1):
#             self.current = None
#             return None
#         else:
#             self.current = var1.next
#             return var1

#     def getTail(self):
#         var1 = self.head.previous
#         #if(var1 == self.head):
#         if(var1.hash == -1):
#             self.current = None
#             return None
#         else:
#             self.current = var1.previous
#             return var1

#     def getNext(self):
#         var1 = self.current
#         #if(var1 == self.head):
#         if(var1.hash == -1):
#             self.current = None
#             return None
#         else:
#             self.current = var1.next
#             return var1

#     def getPrevious(self):
#         var1 = self.current
#         #if(var1 == self.head):
#         if(var1.hash == -1):
#             self.current = None
#             return None
#         else:
#             self.current = var1.previous
#             return var1

#     def method4011(self,  var0,  var1):
#         if(var0.previous is not None):
#             var0.unlink()

#         var0.previous = var1.previous
#         var0.next = var1
#         var0.previous.setNext(var0) #next = var0
#         var0.next.setPrevious(var0) #previous = var0
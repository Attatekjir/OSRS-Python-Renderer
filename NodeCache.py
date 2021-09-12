# from HashTable import HashTable
# from CacheableNode import CacheableNode
# from Node2LinkedList import Node2LinkedList


# class NodeCache:

#     def __init__(self, var1):

#         self.field2638 = CacheableNode()
#         self.list = Node2LinkedList()
#         self.capacity = var1
#         self.remainingCapacity = var1

#         var2 = 1
#         while var2 + var2 < var1:
#             var2 += var2

#         self.table = HashTable(var2)

#     def get(self, var1):
#         var3 = self.table.get(var1)
#         if(var3 is not None):
#             var3 = CacheableNode(var3)
#             self.list.push(var3)

#         return var3

#     def remove(self, var1):
#         var3 = CacheableNode(self.table.get(var1))
#         if(var3 is not None):
#             var3.unlink()
#             var3.unlinkDual()
#             self.remainingCapacity += 1

#     def put(self, var1, var2):
#         if(self.remainingCapacity == 0):
#             var4 = self.list.pop()
#             var4.unlink()
#             var4.unlinkDual()
#             if(var4 == self.field2638):
#                 var4 = self.list.pop()
#                 var4.unlink()
#                 var4.unlinkDual()

#         else:
#             self.remainingCapacity -= 1

#         self.table.put(var1, var2)
#         self.list.push(var1)

#     def reset(self):
#         self.list.clear()
#         self.table.clear()
#         self.field2638 = CacheableNode()
#         self.remainingCapacity = self.capacity

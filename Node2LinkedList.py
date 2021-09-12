from CacheableNode import CacheableNode


class Node2LinkedList :

    def __init__(self):
        self.sentinel = CacheableNode()
        self.sentinel.previous = self.sentinel
        self.sentinel.next = self.sentinel
   

    def push(self, var1) :
        if(var1.next is not None) :
            var1.unlinkDual()


        var1.next = self.sentinel.next
        var1.previous = self.sentinel
        var1.next.previous = var1
        var1.previous.next = var1


    def setHead(self, var1) :
        if(var1.next is not None) :
            var1.unlinkDual()


        var1.next = self.sentinel
        var1.previous = self.sentinel.previous
        var1.next.previous = var1
        var1.previous.next = var1


    def pop(self, ) :
        var1 = self.sentinel.previous
        if(var1 == self.sentinel) :
            return None
        else :
            var1.unlinkDual()
        return var1



    def peek(self) :
        var1 = self.sentinel.previous

        if var1 == self.sentinel:
            return None
        else:
            return var1

        #return #var1 == self.sentinel?None:var1


    def clear(self, ) :
        while(True) :
            var1 = self.sentinel.previous
            if(var1 == self.sentinel) :
                return


            var1.unlinkDual()



    def method3860(self, var0, var1) :
        if(var0.next is not None) :
            var0.unlinkDual()


        var0.next = var1
        var0.previous = var1.previous
        var0.next.previous = var0
        var0.previous.next = var0



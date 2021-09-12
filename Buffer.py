import MathUtills
import numpy as np
from MathUtills import integerdivide
from numba.experimental import jitclass
from numba import int32, float32, int8

spec = [
    ('offset', int32),            # a simple scalar field
    ('payload', int8[:]),         # a numpy array of type np.byte
]

@jitclass(spec)
class Buffer:

    def __init__(self, bter):

        self.payload = bter #byte[]
        self.offset = 0

    def readUnsignedByte(self) :
        out = self.payload[self.offset] & 255
        self.offset += 1
        return out

    def readByte(self):
        out = self.payload[self.offset]
        self.offset += 1
        return out

    def setOffset(self, val):
        self.offset = val
        
    def remaining(self):
        return len(self.payload) - self.offset
    
    # def Buffer(self, var1) :
    #     self.payload = GrandExchangeOffer.method127(var1)
    #     self.offset = 0

    # def method3500() :
    #     if(self.payload is not None) :
    #         class150.method3110(self.payload)
        
    #     self.payload = None
    

    # def putByte(self, var1) :
    #     self.payload[self.offset++] = (byte)var1
    

    # def putShort(self, int var1) :
    #     self.payload[self.offset++] = (byte)(var1 >> 8)
    #     self.payload[self.offset++] = (byte)var1
    

    # def put24bitInt(self, int var1) :
    #     self.payload[self.offset++] = (byte)(var1 >> 16)
    #     self.payload[self.offset++] = (byte)(var1 >> 8)
    #     self.payload[self.offset++] = (byte)var1

    def readStringIntParameters(self, hashTable) :
        var2 = self.readUnsignedByte()
        if(hashTable == None) :
            var3 = MathUtills.nextPowerOfTwo(var2)
            hashTable = "SpoofReadStringIntParametersSpoof" #new IterableHashTable(var3)

        for var3 in range(0, var2):
            var4 = self.readUnsignedByte() == 1
            var5 = self.read24BitInt()
            if(var4) :
                var6 = self.readString() # new ObjectNode(buffer.readString())
            else :
                var6 = self.readInt() # new IntegerNode(buffer.readInt())

            #hashTable.put((Node)var6, var5)

        return hashTable

    def readStringIntParametersSpoofed(self, hashTable) :
        var2 = self.readUnsignedByte()
        for var3 in range(0, var2):
            var4 = self.readUnsignedByte() == 1
            var5 = self.read24BitInt()
            if(var4) :
                var6 = self.readString() # new ObjectNode(buffer.readString())
            else :
                var6 = self.readInt() # new IntegerNode(buffer.readInt())
        return hashTable
    

    def putInt(self, var1) :
        self.payload[self.offset] = np.byte(var1 >> 24)
        self.offset += 1
        self.payload[self.offset] = np.byte(var1 >> 16)
        self.offset += 1
        self.payload[self.offset] = np.byte(var1 >> 8)
        self.offset += 1
        self.payload[self.offset] = np.byte(var1)
        self.offset += 1
    

    # def method3671(self, long var1) :
    #     self.payload[self.offset++] = (byte)((int)(var1 >> 40))
    #     self.payload[self.offset++] = (byte)((int)(var1 >> 32))
    #     self.payload[self.offset++] = (byte)((int)(var1 >> 24))
    #     self.payload[self.offset++] = (byte)((int)(var1 >> 16))
    #     self.payload[self.offset++] = (byte)((int)(var1 >> 8))
    #     self.payload[self.offset++] = (byte)((int)var1)
    

    # def putLong(self, long var1) :
    #     self.payload[self.offset++] = (byte)((int)(var1 >> 56))
    #     self.payload[self.offset++] = (byte)((int)(var1 >> 48))
    #     self.payload[self.offset++] = (byte)((int)(var1 >> 40))
    #     self.payload[self.offset++] = (byte)((int)(var1 >> 32))
    #     self.payload[self.offset++] = (byte)((int)(var1 >> 24))
    #     self.payload[self.offset++] = (byte)((int)(var1 >> 16))
    #     self.payload[self.offset++] = (byte)((int)(var1 >> 8))
    #     self.payload[self.offset++] = (byte)((int)var1)
    

    # def writeBooleanAsByte(self, boolean var1) :
    #     self.putByte(var1?1:0)
    

    # def putString(self, String var1) :
    #     final int var2 = var1.indexOf(0)
    #     if(var2 >= 0) :
    #         throw new IllegalArgumentException("")
    #      else :
    #         self.offset += WorldMapDecorationInfo.encodeStringCp1252(var1, 0, var1.length(), self.payload, self.offset)
    #         self.payload[self.offset++] = 0
        
    

    # def putJagString(self, String var1) :
    #     final int var2 = var1.indexOf(0)
    #     if(var2 >= 0) :
    #         throw new IllegalArgumentException("")
    #      else :
    #         self.payload[self.offset++] = 0
    #         self.offset += WorldMapDecorationInfo.encodeStringCp1252(var1, 0, var1.length(), self.payload, self.offset)
    #         self.payload[self.offset++] = 0
        
    

    # def putCESU8(self, CharSequence var1) :
    #     final int var3 = var1.length()
    #     int var4 = 0

    #     int var5
    #     for(var5 = 0 var5 < var3 ++var5) :
    #         final char var6 = var1.charAt(var5)
    #         if(var6 <= 127) :
    #             ++var4
    #          else if(var6 <= 2047) :
    #             var4 += 2
    #          else :
    #             var4 += 3
            
        

    #     self.payload[self.offset++] = 0
    #     self.putVarInt(var4)
    #     var4 = self.offset
    #     final byte[] var12 = self.payload
    #     final int var7 = self.offset
    #     final int var8 = var1.length()
    #     int var9 = var7

    #     for(int var10 = 0 var10 < var8 ++var10) :
    #         final char var11 = var1.charAt(var10)
    #         if(var11 <= 127) :
    #             var12[var9++] = (byte)var11
    #          else if(var11 <= 2047) :
    #             var12[var9++] = (byte)(192 | var11 >> 6)
    #             var12[var9++] = (byte)(128 | var11 & '?')
    #          else :
    #             var12[var9++] = (byte)(224 | var11 >> '\f')
    #             var12[var9++] = (byte)(128 | var11 >> 6 & 63)
    #             var12[var9++] = (byte)(128 | var11 & '?')
            
        

    #     var5 = var9 - var7
    #     self.offset = var5 + var4
    

    # def putBytes(self, byte[] var1, final int var2, final int var3) :
    #     for(int var4 = var2 var4 < var3 + var2 ++var4) :
    #         self.payload[self.offset++] = var1[var4]
        

    

    # def putLengthInt(self, int var1) :
    #     self.payload[self.offset - var1 - 4] = (byte)(var1 >> 24)
    #     self.payload[self.offset - var1 - 3] = (byte)(var1 >> 16)
    #     self.payload[self.offset - var1 - 2] = (byte)(var1 >> 8)
    #     self.payload[self.offset - var1 - 1] = (byte)var1
    

    # def method3513(self, int var1) :
    #     self.payload[self.offset - var1 - 2] = (byte)(var1 >> 8)
    #     self.payload[self.offset - var1 - 1] = (byte)var1
    

    # def method3514(self, int var1) :
    #     self.payload[self.offset - var1 - 1] = (byte)var1
    

    # def putShortSmart(self, int var1) :
    #     if(var1 >= 0 && var1 < 128) :
    #         self.putByte(var1)
    #      else if(var1 >= 0 && var1 < 32768) :
    #         self.putShort(var1 + 32768)
    #      else :
    #         throw new IllegalArgumentException()
        
    

    # def putVarInt(self, int var1) :
    #     if((var1 & -128) != 0) :
    #         if((var1 & -16384) != 0) :
    #             if((var1 & -2097152) != 0) :
    #                 if((var1 & -268435456) != 0) :
    #                     self.putByte(unsignedrshift(var1, 28) | 128)
                    

    #                 self.putByte(unsignedrshift(var1, 21) | 128)
                

    #             self.putByte(unsignedrshift(var1, 14) | 128)
            

    #         self.putByte(unsignedrshift(var1, 7) | 128)
        

    #     self.putByte(var1 & 127)
    

    
    

    
    

    def readUnsignedShort(self) :
        self.offset += 2
        return  ((self.payload[self.offset - 2] & 255) << 8) + (self.payload[self.offset - 1] & 255)
    

    def readShort(self):
        self.offset += 2
        var1 = (self.payload[self.offset - 1] & 255) + ((self.payload[self.offset - 2] & 255) << 8)
        if(var1 > 32767) :
            var1 -= 65536
        
        return var1
    

    def read24BitInt(self) :
        self.offset += 3
        return ((self.payload[self.offset - 3] & 255) << 16) + (self.payload[self.offset - 1] & 255) + ((self.payload[self.offset - 2] & 255) << 8)
    

    def readInt(self) :
        self.offset += 4
        return np.int32(((self.payload[self.offset - 3] & 255) << 16) + (self.payload[self.offset - 1] & 255) + ((self.payload[self.offset - 2] & 255) << 8) + ((self.payload[self.offset - 4] & 255) << 24))
    

    # public long readLong() :
    #     final long var1 = self.readInt() & 4294967295L
    #     final long var3 = self.readInt() & 4294967295L
    #     return var3 + (var1 << 32)
    

    def readUnsignedByteAsBool(self) :
         return (self.readUnsignedByte() & 1) == 1
    

    # public String getNullString() :
    #     if(self.payload[self.offset] == 0) :
    #         ++self.offset
    #         return None
    #      else :
    #         return self.readString()
        
    

    # def readString(self) :

    #     var1 = self.offset

    #     while(self.payload[self.offset] != 0):
    #         self.offset += 1

    #     var2 = self.offset - var1 - 1
    #     if var2 == 0:
    #         return ""
    #     else:

            

    #         return "Buffer.py fuck it implementing this"
    #         #ChatPlayer.getString(self.payload, var1, var2)


    #     #return var2 == 0?"":

    def readString(self) :
        result = ""

        while (True):

            ch = self.readUnsignedByte()
            if ch == 0:
                break

            if (ch >= 128 and ch < 160):
                #var7 = CHARACTERS[ch - 128]
                #if (var7 == 0):
                #ch = '?'
                result += chr(ch) 
            else:
                result += chr(ch)
			
        return result
   
    

    # public String getJagString() :
    #     final byte var1 = self.payload[self.offset++]
    #     if(var1 != 0) :
    #         throw new IllegalStateException("")
    #      else :
    #         final int var2 = self.offset

    #         while(self.payload[self.offset++] != 0) :
            

    #         final int var3 = self.offset - var2 - 1
    #         return var3 == 0?"":ChatPlayer.getString(self.payload, var2, var3)
        
    

    # public String getCESU8() :
    #     final byte var1 = self.payload[self.offset++]
    #     if(var1 != 0) :
    #         throw new IllegalStateException("")
    #      else :
    #         final int var2 = self.readVarInt()
    #         if(var2 + self.offset > self.payload.length) :
    #             throw new IllegalStateException("")
    #          else :
    #             final byte[] var4 = self.payload
    #             final int var5 = self.offset
    #             final char[] var6 = new char[var2]
    #             int var7 = 0
    #             int var8 = var5

    #             int var11
    #             for(final int var9 = var2 + var5 var8 < var9 var6[var7++] = (char)var11) :
    #                 final int var10 = var4[var8++] & 255
    #                 if(var10 < 128) :
    #                     if(var10 == 0) :
    #                         var11 = 65533
    #                      else :
    #                         var11 = var10
                        
    #                  else if(var10 < 192) :
    #                     var11 = 65533
    #                  else if(var10 < 224) :
    #                     if(var8 < var9 && (var4[var8] & 192) == 128) :
    #                         var11 = (var10 & 31) << 6 | var4[var8++] & 63
    #                         if(var11 < 128) :
    #                             var11 = 65533
                            
    #                      else :
    #                         var11 = 65533
                        
    #                  else if(var10 < 240) :
    #                     if(var8 + 1 < var9 && (var4[var8] & 192) == 128 && (var4[var8 + 1] & 192) == 128) :
    #                         var11 = (var10 & 15) << 12 | (var4[var8++] & 63) << 6 | var4[var8++] & 63
    #                         if(var11 < 2048) :
    #                             var11 = 65533
                            
    #                      else :
    #                         var11 = 65533
                        
    #                  else if(var10 < 248) :
    #                     if(var8 + 2 < var9 && (var4[var8] & 192) == 128 && (var4[var8 + 1] & 192) == 128 && (var4[var8 + 2] & 192) == 128) :
    #                         var11 = (var10 & 7) << 18 | (var4[var8++] & 63) << 12 | (var4[var8++] & 63) << 6 | var4[var8++] & 63
    #                         var11 = 65533
    #                      else :
    #                         var11 = 65533
                        
    #                  else :
    #                     var11 = 65533
                    
                

    #             final String var3 = new String(var6, 0, var7)
    #             self.offset += var2
    #             return var3
            
        
    

    def readBytes(self, var1, var2, var3) :
        for var4 in range(var2, var3 + var2):
            var1[var4] = self.payload[self.offset]
            self.offset += 1
        
    def getLength(self):
        return len(self.payload)
    

    def readShortSmart(self) :

        # Peak first...
        var1 = np.int32(self.payload[self.offset] & 0xFF)

        if var1 < 128:
            result = self.readUnsignedByte() - 64
        else:
            result = self.readUnsignedShort() - 0xc000

        return result
    

    def getUSmart(self) :
        var1 = self.payload[self.offset] & 255

        if var1 < 128:
            return self.readUnsignedByte()
        else:
            return self.readUnsignedShort() - 32768

        #return var1 < 128?self.readUnsignedByte():self.readUnsignedShort() - 32768
    

    # public int getLargeSmart() :
    #     return self.payload[self.offset] < 0?self.readInt() & Integer.MAX_VALUE:self.readUnsignedShort()
    

    # public int method3576() :
    #     if(self.payload[self.offset] < 0) :
    #         return self.readInt() & Integer.MAX_VALUE
    #      else :
    #         final int var1 = self.readUnsignedShort()
    #         return var1 == 32767?-1:var1
        
    

    # public int readVarInt() :
    #     byte var1 = self.payload[self.offset++]

    #     int var2
    #     for(var2 = 0 var1 < 0 var1 = self.payload[self.offset++]) :
    #         var2 = (var2 | var1 & 127) << 7
        

    #     return var2 | var1
    

    # def encryptXtea2(final int[] var1) :
    #     final int var2 = integerdivide(self.offset, 8)
    #     self.offset = 0

    #     for(int var3 = 0 var3 < var2 ++var3) :
    #         int var4 = self.readInt()
    #         int var5 = self.readInt()
    #         int var6 = 0
    #         final int var7 = -1640531527

    #         for(int var8 = 32 var8-- > 0 var5 += var4 + (var4 << 4 ^ unsignedrshift(var4 , 5)) ^ var1[unsignedrshift(var6 , 11) & 3] + var6) :
    #             var4 += var5 + (var5 << 4 ^ unsignedrshift(var5 , 5)) ^ var6 + var1[var6 & 3]
    #             var6 += var7
            

    #         self.offset -= 8
    #         self.putInt(var4)
    #         self.putInt(var5)
        

    

    def decryptXtea(self, var1) :
        var2 = integerdivide(self.offset, 8)
        self.offset = 0

        for var3 in range(0, var2):
            var4 = self.readInt()
            var5 = self.readInt()
            var6 = -957401312
            var7 = -1640531527

            var8 = 32
            while (var8 > 0):

                var8 -= 1
            
            #for(int var8 = 32 var8-- > 0 var4 -= var5 + (var5 << 4 ^ unsignedrshift(var5, 5)) ^ var6 + var1[var6 & 3]) :
                var5 -= var4 + (var4 << 4 ^ MathUtills.unsignedrshift(var4, 5)) ^ var1[MathUtills.unsignedrshift(var6, 11) & 3] + var6
                var6 -= var7

                var4 -= var5 + (var5 << 4 ^ MathUtills.unsignedrshift(var5, 5)) ^ var6 + var1[var6 & 3]
            

            self.offset -= 8
            self.putInt(var4)
            self.putInt(var5)
        

    

    # def encryptXtea(final int[] var1, final int var2, final int var3) :
    #     final int var4 = self.offset
    #     self.offset = var2
    #     final int var5 = integerdivide((var3 - var2), 8)

    #     for(int var6 = 0 var6 < var5 ++var6) :
    #         int var7 = self.readInt()
    #         int var8 = self.readInt()
    #         int var9 = 0
    #         final int var10 = -1640531527

    #         for(int var11 = 32 var11-- > 0 var8 += var7 + (var7 << 4 ^ unsignedrshift(var7, 5)) ^ var1[unsignedrshift(var9, 11) & 3] + var9) :
    #             var7 += var8 + (var8 << 4 ^ unsignedrshift(var8 , 5)) ^ var9 + var1[var9 & 3]
    #             var9 += var10
            

    #         self.offset -= 8
    #         self.putInt(var7)
    #         self.putInt(var8)
        

    #     self.offset = var4
    

    # def decryptXtea(final int[] var1, final int var2, final int var3) :
    #     final int var4 = self.offset
    #     self.offset = var2
    #     final int var5 = integerdivide((var3 - var2), 8)

    #     for(int var6 = 0 var6 < var5 ++var6) :
    #         int var7 = self.readInt()
    #         int var8 = self.readInt()
    #         int var9 = -957401312
    #         final int var10 = -1640531527

    #         for(int var11 = 32 var11-- > 0 var7 -= var8 + (var8 << 4 ^ unsignedrshift(var8, 5)) ^ var9 + var1[var9 & 3]) :
    #             var8 -= var7 + (var7 << 4 ^ unsignedrshift(var7, 5)) ^ var1[unsignedrshift(var9, 11) & 3] + var9
    #             var9 -= var10
            

    #         self.offset -= 8
    #         self.putInt(var7)
    #         self.putInt(var8)
        

    #     self.offset = var4
    

    # def encryptRsa(final BigInteger var1, final BigInteger var2) :
    #     final int var3 = self.offset
    #     self.offset = 0
    #     final byte[] var4 = new byte[var3]
    #     self.readBytes(var4, 0, var3)
    #     final BigInteger var5 = new BigInteger(var4)
    #     final BigInteger var6 = var5.modPow(var1, var2)
    #     final byte[] var7 = var6.toByteArray()
    #     self.offset = 0
    #     self.putShort(var7.length)
    #     self.putBytes(var7, 0, var7.length)
    

    # public int putCrc(final int var1) :
    #     final int var2 = ClanMember.method5252(self.payload, var1, self.offset)
    #     self.putInt(var2)
    #     return var2
    

    # public boolean checkCrc() :
    #     self.offset -= 4
    #     final int var1 = ClanMember.method5252(self.payload, 0, self.offset)
    #     final int var2 = self.readInt()
    #     return var1 == var2
    

    # def method3541(final int var1) :
    #     self.payload[self.offset++] = (byte)(var1 + 128)
    

    # def method3542(final int var1) :
    #     self.payload[self.offset++] = (byte)(0 - var1)
    

    # def method3543(final int var1) :
    #     self.payload[self.offset++] = (byte)(128 - var1)
    

    # public int method3636() :
    #     return self.payload[self.offset++] - 128 & 255
    

    # public int method3538() :
    #     return 0 - self.payload[self.offset++] & 255
    

    # public int readUnsignedShortOb1() :
    #     return 128 - self.payload[self.offset++] & 255
    

    # public byte method3725() :
    #     return (byte)(self.payload[self.offset++] - 128)
    

    # public byte method3548() :
    #     return (byte)(0 - self.payload[self.offset++])
    

    # public byte method3634() :
    #     return (byte)(128 - self.payload[self.offset++])
    

    # def method3550(final int var1) :
    #     self.payload[self.offset++] = (byte)var1
    #     self.payload[self.offset++] = (byte)(var1 >> 8)
    

    # def method3551(final int var1) :
    #     self.payload[self.offset++] = (byte)(var1 >> 8)
    #     self.payload[self.offset++] = (byte)(var1 + 128)
    

    # def method3528(final int var1) :
    #     self.payload[self.offset++] = (byte)(var1 + 128)
    #     self.payload[self.offset++] = (byte)(var1 >> 8)
    

    # public int method3553() :
    #     self.offset += 2
    #     return ((self.payload[self.offset - 1] & 255) << 8) + (self.payload[self.offset - 2] & 255)
    

    # public int method3554() :
    #     self.offset += 2
    #     return (self.payload[self.offset - 1] - 128 & 255) + ((self.payload[self.offset - 2] & 255) << 8)
    

    # public int method3555() :
    #     self.offset += 2
    #     return ((self.payload[self.offset - 1] & 255) << 8) + (self.payload[self.offset - 2] - 128 & 255)
    

    # public int method3595() :
    #     self.offset += 2
    #     int var1 = ((self.payload[self.offset - 1] & 255) << 8) + (self.payload[self.offset - 2] & 255)
    #     if(var1 > 32767) :
    #         var1 -= 65536
        

    #     return var1
    

    # public int method3556() :
    #     self.offset += 2
    #     int var1 = ((self.payload[self.offset - 1] & 255) << 8) + (self.payload[self.offset - 2] - 128 & 255)
    #     if(var1 > 32767) :
    #         var1 -= 65536
        

    #     return var1
    

    # def method3722(final int var1) :
    #     self.payload[self.offset++] = (byte)(var1 >> 8)
    #     self.payload[self.offset++] = (byte)(var1 >> 16)
    #     self.payload[self.offset++] = (byte)var1
    

    # public int method3558() :
    #     self.offset += 3
    #     return (self.payload[self.offset - 1] & 255) + ((self.payload[self.offset - 3] & 255) << 8) + ((self.payload[self.offset - 2] & 255) << 16)
    

    # def method3559(final int var1) :
    #     self.payload[self.offset++] = (byte)var1
    #     self.payload[self.offset++] = (byte)(var1 >> 8)
    #     self.payload[self.offset++] = (byte)(var1 >> 16)
    #     self.payload[self.offset++] = (byte)(var1 >> 24)
    

    # def method3552(final int var1) :
    #     self.payload[self.offset++] = (byte)(var1 >> 8)
    #     self.payload[self.offset++] = (byte)var1
    #     self.payload[self.offset++] = (byte)(var1 >> 24)
    #     self.payload[self.offset++] = (byte)(var1 >> 16)
    

    # void method3561(final int var1) :
    #     self.payload[self.offset++] = (byte)(var1 >> 16)
    #     self.payload[self.offset++] = (byte)(var1 >> 24)
    #     self.payload[self.offset++] = (byte)var1
    #     self.payload[self.offset++] = (byte)(var1 >> 8)
    

    # public int method3562() :
    #     self.offset += 4
    #     return (self.payload[self.offset - 4] & 255) + ((self.payload[self.offset - 3] & 255) << 8) + ((self.payload[self.offset - 2] & 255) << 16) + ((self.payload[self.offset - 1] & 255) << 24)
    

    # public int method3563() :
    #     self.offset += 4
    #     return ((self.payload[self.offset - 2] & 255) << 24) + ((self.payload[self.offset - 4] & 255) << 8) + (self.payload[self.offset - 3] & 255) + ((self.payload[self.offset - 1] & 255) << 16)
    

    # public int method3564() :
    #     self.offset += 4
    #     return ((self.payload[self.offset - 1] & 255) << 8) + ((self.payload[self.offset - 4] & 255) << 16) + (self.payload[self.offset - 2] & 255) + ((self.payload[self.offset - 3] & 255) << 24)
    

    # def method3565(final byte[] var1, final int var2, final int var3) :
    #     for(int var4 = var3 + var2 - 1 var4 >= var2 --var4) :
    #         var1[var4] = self.payload[self.offset++]
        

    

    # def method3661(final byte[] var1, final int var2, final int var3) :
    #     for(int var4 = var2 var4 < var3 + var2 ++var4) :
    #         var1[var4] = (byte)(self.payload[self.offset++] - 128)
        

    

    # public static boolean method3727(final String var0, final int var1) :
    #     return CombatInfoListHolder.method1865(var0, var1, "openjs")
    


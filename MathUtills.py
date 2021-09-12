from numba import jit
import math
import numpy as np

# Divide two integers in Java style, which differs from python integer division
@jit(nopython=True, cache=True)
def integerdivide(a, b):
    out = a // b
    if out < 0 and a % b != 0:
        out += 1
    return out

@jit(nopython=True, cache=True)
def Graphics3DSINE(var0):
    return np.int32(65536.0 * math.sin(var0 * 0.0030679615))


@jit(nopython=True, cache=True)
def Graphics3DCOSINE(var0):
    return np.int32(65536.0 * math.cos(var0 * 0.0030679615))


@jit(nopython=True, cache=True)
def unsignedrshift(val, n):
    return (val % 0x100000000) >> n


@jit(nopython=True, cache=True)
def nextPowerOfTwo(var0):

    var0 -= 1

    var0 |= unsignedrshift(var0, 1)
    var0 |= unsignedrshift(var0, 2)
    var0 |= unsignedrshift(var0, 4)
    var0 |= unsignedrshift(var0, 8)
    var0 |= unsignedrshift(var0, 16)
    return var0 + 1


@jit(nopython=True, cache=True)
def method4490(var0, var1, var2):
    if(var2 > 179):
        var1 = integerdivide(var1, 2)
    if(var2 > 192):
        var1 = integerdivide(var1, 2)
    if(var2 > 217):
        var1 = integerdivide(var1, 2)
    if(var2 > 243):
        var1 = integerdivide(var1, 2)

    return (integerdivide(var1, 32) << 7) + (integerdivide(var0, 4) << 10) + integerdivide(var2, 2)


# def unsignedrshiftLONG(n, shiftr, bits = 64):

#     def bindigits(n, bits):
#         s = bin(n & int("1"*bits, 2))[2:]
#         return ("{0:0>%s}" % (bits)).format(s)

#     bitstring = bindigits(n, bits)

#     #The unsigned right shift operator ">>>" shifts a zero into the leftmost position
#     result = ("0" * shiftr)  + bitstring[0: -shiftr]
#     result = int(result, 2)

#     return result

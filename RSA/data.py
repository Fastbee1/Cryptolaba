import random
from MillerRabin import miller_rabin
import math
import hashlib


def interval(bits):
    a = 2 ** (bits - 1)
    b = (2 ** bits) - 1
    return a, b


def prime_generation(bgn, end):
    a = random.randint(bgn, end)
    b = False

    while not b:
        b = miller_rabin(a)
        if a + 1 > end and not b:
            a = random.randint(bgn, end)
        else:
            a += 1

    return a - 1


def rand_bin_str(p):
    r = ""
    for i in range(p):
        temp = str(random.randint(0, 1))

        r += temp
    return r


def xor(a, b):
    assert len(a) == len(b)
    return bytearray([aa ^ bb for aa, bb in zip(a, b)])


def hash_func(message, bits):
    if bits == 256:
        m = hashlib.sha256()
        m.update(message)
        return m.digest()
    elif bits == 384:
        m = hashlib.sha384()
        m.update(message)
        return m.digest()
    elif bits == 512:
        m = hashlib.sha512()
        m.update(message)
        return m.digest()

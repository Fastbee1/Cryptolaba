import random
import math


def miller_rabin(n):
    s = 0
    divisor = n - 1
    m = 0
    while m == 0:
        divisor, m = divmod(divisor, 2)
        s += 1

    s -= 1
    m = divisor * 2 + m
    k = int(math.log(n)/2)
    for j in range(k):
        a = random.randint(2, n - 2)
        b = pow(a, m, n)

        if b != 1 and b != n - 1:
            i = 1
            while i < s and b != n - 1:
                b = pow(b, 2, n)

                if b == 1:
                    return False

                i += 1

            if b != n - 1:
                return False

    return True


if __name__ == '__main__':
    while True:
        num = int(input())
        x = miller_rabin(num)
        if x:
            print("Prime")
        else:
            print("Comp")

from data import *


def rsa_encrypt(N, e, m, bits):
    m_int = int.from_bytes(m, 'big')
    return pow(m_int, e, N).to_bytes(bits // 4, 'big')


def rsa_decrypt(d, ciph, p, q):
    c = int.from_bytes(ciph, 'big')
    m1 = pow(c % p, d % (p - 1), p)
    m2 = pow(c % q, d % (q - 1), q)

    z = (m2 - (m1 % q))
    while z / (p % q) != int(z / (p % q)):
        print(z)
        z += q
    z = int(z / (p % q))

    m = p * z + m1
    return m.to_bytes(len(ciph), 'big')


if __name__ == '__main__':
    x, y = interval(512)
    message = bytearray(input(), "ascii")

    p = prime_generation(x, y)

    q = p
    while p == q:
        q = prime_generation(x, y)

    N = p * q
    f = (p - 1) * (q - 1)

    e = prime_generation(3, f - 1)
    while math.gcd(f, e) != 1:
        e = prime_generation(3, f - 1)

    d = pow(e, -1, f)
    if d == e:
        d += f

    cipher = rsa_encrypt(N, e, message, 512)

    m = rsa_decrypt(d, cipher, p, q)
    print(m.decode())

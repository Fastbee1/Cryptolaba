from data import *


def oaep_pad(message, g, h):
    r = bytearray(rand_bin_str(h), "ascii")

    m0 = message
    for j in range((g // 8) - len(message)):
        m0.append(0x00)

    G = xor(m0, hash_func(int(r, 2).to_bytes(h // 8, 'big'), g))
    H = xor(int(r, 2).to_bytes(h // 8, 'big'), hash_func(G, h))

    return G + H


def rsa_oaep_encrypt(N, e, message, g, h):
    oaep = oaep_pad(message, g, h)
    m = int.from_bytes(oaep, 'big')
    return pow(m, e, N).to_bytes((g + h) // 4, 'big')


def rsa_oaep_decrypt(d, ciph, p, q, g, h):
    c = int.from_bytes(ciph, 'big')
    m1 = pow(c % p, d % (p - 1), p)
    m2 = pow(c % q, d % (q - 1), q)

    z = (m2 - (m1 % q))
    while z / (p % q) != int(z / (p % q)):
        z += q
    z = int(z / (p % q))

    m = p * z + m1

    mess = m.to_bytes((g + h) // 8, 'big')
    G = mess[:g // 8]
    H = mess[g // 8:]

    r = xor(H, hash_func(G, h))
    m0 = xor(hash_func(r, g), G)

    return m0


if __name__ == '__main__':
    x, y = interval(896)
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

    cipher = rsa_oaep_encrypt(N, e, message, 384, 512)

    m = rsa_oaep_decrypt(d, cipher, p, q, 384, 512)
    print(m.decode())

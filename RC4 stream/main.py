def xor_bytes(a, b):
    return bytes(i ^ j for i, j in zip(a, b))


class RC4:
    def __init__(self, master_key):
        self.S = self.key_scheduling(master_key)
        self.K = self.keystream_generator(self.S)

    def key_scheduling(self, key):
        keylength = len(key)
        S = [i for i in range(256)]
        j = 0

        for i in range(256):
            j = (j + S[i] + key[i % keylength]) % 256
            S[i], S[j] = S[j], S[i]
        return S

    def keystream_generator(self, S):
        i = 0
        j = 0

        while True:
            i = (i + 1) % 256
            j = (j + S[i]) % 256
            S[i], S[j] = S[j], S[i]
            t = (S[i] + S[j]) % 256
            K = S[t]
            yield K

    def encrypt(self, plaintext):
        return xor_bytes(plaintext, self.K)

    def decrypt(self, ciphertext):
        return xor_bytes(ciphertext, self.K)


if __name__ == '__main__':
    import time

    master_k = b'k'*40
    L = 256
    plaintext = b'M'*L*1024

    start = time.time()
    rc4_obj = RC4(master_k)
    ciphertext = rc4_obj.encrypt(plaintext)
    stop1 = time.time()
    rc4_obj = RC4(master_k)
    decrypted = rc4_obj.decrypt(ciphertext)
    stop2 = time.time()
    if plaintext == decrypted:
        print('RC4 - {} KB: Encryption time:{}s; Decryption time:{}s'.format(L, stop1 - start, stop2 - stop1))
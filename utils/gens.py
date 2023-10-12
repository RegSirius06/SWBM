import random
import string

ALFABETS = {
    'RUSSIAN': f"{''.join([chr(ord('а') + x) for x in range(32)])}ё" +
               f"{''.join([chr(ord('а') + x) for x in range(32)])}ё".upper() +
               string.digits + string.punctuation + ' ',
    'ENGLAND': string.ascii_letters + string.digits + string.punctuation + ' ',
    'BOTH': f"{''.join([chr(ord('а') + x) for x in range(32)])}ё" +
            f"{''.join([chr(ord('а') + x) for x in range(32)])}ё".upper() +
            string.digits + string.ascii_letters + string.punctuation + ' ',
    'EXCLUDE': string.digits + string.punctuation + ' ',
}

def xor(x: int, y: int) -> int:
    xb = bin(x)[2:]
    s_d = '0' * (8 - len(xb))
    xb = s_d + xb
    yb = bin(y)[2:]
    s_d = '0' * (8 - len(yb))
    yb = s_d + yb
    rs = []
    for i, j in zip(xb, yb): rs.append('0' if i == j else '1')
    return int(''.join(rs), 2)

def encrypting_key(key: str, alf: str) -> str:
    # list_ = [ord(i) for i in key]
    # list_xor = [ord(i) for i in ALFABETS[alf]]
    # rs = [chr(xor(i, j)) for i, j in zip(list_, list_xor)]
    # return ''.join(rs)
    return key

def key_gen(alf: str) -> str:
    key = list(ALFABETS[alf])
    for i in range(1000):
        x = random.randint(0, len(key) - 1)
        y = random.randint(0, len(key) - 1)
        y = y if y != x else (y + y // 2) % len(key)
        key[x], key[y] = key[y], key[x]
    return encrypting_key(''.join(key), alf)

def three_n_plus_one(i: int):
    return i // 2 if i & 1 == 0 else 3 * i + 1

def gen_shift(length: int, seed: int) -> list:
    rs = []
    x = seed
    for i in range(length):
        rs.append(x)
        x = three_n_plus_one(x)
        if x == 4:
            x = seed + 1
            seed += 1
    return rs

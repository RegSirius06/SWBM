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

def key_gen(alf: str) -> str:
    key = list(ALFABETS[alf])
    for i in range(1000):
        x = random.randint(0, len(key) - 1)
        y = random.randint(0, len(key) - 1)
        y = y if y != x else (y + y // 2) % len(key)
        key[x], key[y] = key[y], key[x]
    return ''.join(key)

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

import random
from utils.gens import ALFABETS, gen_shift, encrypting_key

def get_best_alf(message: str) -> str:
    f = False
    b = False
    for i in message:
        if i.isalpha():
            f = f or i in ALFABETS["RUSSIAN"]
            b = b or i in ALFABETS["ENGLAND"]
        if f and b: return "BOTH"
    return "BOTH" if f and b else "RUSSIAN" if f else "ENGLAND" if b else "EXCLUDE"

def replace_digits(x: int, key: str, alf: str) -> str:
    key = encrypting_key(key, alf)
    list_ = [key[(i + 1) * 10 % len(key)] for i in range(16)]
    return ''.join([list_[int(s, 16)] for s in f'{hex(x)[2:]}'])

def replace_alphas(x: str, key: str, alf: str) -> int:
    key = encrypting_key(key, alf)
    dict_ = {f"{key[(i + 1) * 10 % len(key)]}": hex(i)[2:] for i in range(16)}
    return int(''.join([dict_[s] for s in x]), 16)

def encode(key: str, alf: str, message: str) -> (str, str):
    """
    "alf" может принимать только значения словаря ALFABETS.
    """

    alfabet = ALFABETS[alf]
    key = encrypting_key(key, alf)
    print(key)

    messagelist = [x for x in message]
    message_dublicate = []

    digit = random.randint(int('1000', 16), int('FFFF', 16))
    shift = gen_shift(len(messagelist), digit)

    for i in range(len(messagelist)):
        if messagelist[i] in key: messagelist[i] = key[(alfabet.find(messagelist[i]) + shift[i]) % len(key)]
        else:
            message_dublicate.append(messagelist[i])
            messagelist[i] = "\0"

    str_digit = replace_digits(digit, key, alf)
    code_message = str_digit[:2] + ''.join(messagelist) + str_digit[2:]

    return code_message, ''.join(message_dublicate)

def decode(key: str, alf: str, message: str, message_dublicate: str) -> str:
    """
    "alf" может принимать только значения словаря ALFABETS.
    """

    alfabet = ALFABETS[alf]
    key = encrypting_key(key, alf)

    messagelist = [x for x in message]

    digit = replace_alphas(''.join(messagelist[:2]) + ''.join(messagelist[-2:]), key, alf)
    messagelist = messagelist[2:-2]
    shift = gen_shift(len(messagelist), digit)

    index_d = 0
    for i in range(len(messagelist)):
        if messagelist[i] != "\0":
            messagelist[i] = alfabet[(key.find(messagelist[i]) - shift[i]) % len(alfabet)]
        else:
            try:
                messagelist[i] = message_dublicate[index_d]
                index_d += 1
            except IndexError:
                return "Данное сообщение непригодно для расшифровки."

    return "".join(messagelist)

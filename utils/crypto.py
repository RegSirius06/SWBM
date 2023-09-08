import random
from utils.gens import ALFABETS, gen_shift

def get_best_alf(message: str) -> str:
    f = False
    b = False
    for i in message:
        if i.isalpha():
            f = f or i in ALFABETS["RUSSIAN"]
            b = b or i in ALFABETS["ENGLAND"]
        if f and b: return "BOTH"
    return "BOTH" if f and b else "RUSSIAN" if f else "ENGLAND" if b else "EXCLUDE"

def encode(key: str, alf: str, message: str) -> (str, str):
    """
    "alf" может принимать только значения словаря ALFABETS.
    """

    alfabet = ALFABETS[alf]

    messagelist = [x for x in message]
    message_dublicate = []

    digit = random.randint(1000, 9999)
    shift = gen_shift(len(messagelist), digit)

    for i in range(len(messagelist)):
        if messagelist[i] in key: messagelist[i] = key[(alfabet.find(messagelist[i]) + shift[i]) % len(key)]
        else:
            message_dublicate.append(messagelist[i])
            messagelist[i] = "\0"

    code_message = str(digit)[:2] + ''.join(messagelist) + str(digit)[2:]

    return code_message, ''.join(message_dublicate)

def decode(key: str, alf: str, message: str, message_dublicate: str) -> str:
    """
    "alf" может принимать только значения словаря ALFABETS.
    """

    alfabet = ALFABETS[alf]

    messagelist = [x for x in message]

    digit = int(''.join(messagelist[:2]) + ''.join(messagelist[-2:]))
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
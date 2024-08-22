from ngrok import ngrok
import json

def start(*, host="localhost:8000"):
    try:
        with open("./server/ngrok.json") as f:
            token = json.load(f)['authtoken']
    except FileNotFoundError:
        raise Exception("File with token does not found.")
    except KeyError:
        raise Exception("Token is not defined.")

    listener = ngrok.forward(host, authtoken=token)

    return listener

def set_link4bot(link):
    with open('./tele_bot/link.txt', mode='w') as f:
        f.write(link)

def get_link4bot():
    with open('./tele_bot/link.txt') as f:
        s = f.readline().split()[0]
    return s

import json
import requests

url = f"http://localhost:8080/reply"

def chat():
    token = input("name: ").replace(' ', '_')
    print('Chat started.. Say something.')
    while True:
        text = input(">>")
        if text == '/stop':
            break
        reply = requests.post(url, )
        text = await websocket.recv()
        print(f"{text}")

chat()

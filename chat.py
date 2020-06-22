import json
import asyncio
import websockets
import requests

auth = f"http://localhost:{json.load(open('urls.json'))['meta']}/auth"
uri = f"ws://localhost:{json.load(open('urls.json'))['meta']}/"

async def chat():
    async with websockets.connect(uri) as websocket:
        token = requests.post(auth, json={"name": input("name: ")}).json()['token']
        await websocket.send(f'token {token}')
        print('Chat started.. Say something.')
        while True:
            text = input(">>")
            if text == '/stop':
                break
            await websocket.send(text)
            text = await websocket.recv()
            print(f"{text}")

asyncio.get_event_loop().run_until_complete(chat())

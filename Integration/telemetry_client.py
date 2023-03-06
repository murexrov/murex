import asyncio
import websockets
import ast

async def main():
    async with websockets.connect("ws://localhost:5678") as websocket:
        while True:
            data = await websocket.recv()
            print(data)

if __name__ == "__main__":
    asyncio.run(main())
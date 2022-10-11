#!/usr/bin/env python

import asyncio
from email import message
import json

import websockets


async def handler(websocket):
    await runningApplication(websocket)


async def runningApplication(websocket):
    for i in range(100):
        temp = input('N P L or Q :').capitalize()
        if temp == 'Q':
            break
        elif temp == 'N' or temp == 'P' or temp == 'L':
            await websocket.send(json.dumps(temp))
        else:
            print('Enter p, q, l or n ')


async def main():
    async with websockets.serve(handler, "", 8002):
        await asyncio.Future()  # run forever


if __name__ == "__main__":
    asyncio.run(main())

import websockets
import asyncio

async def file_receive():
    async with websockets.connect('ws://localhost:8765') as websocket:
        # Receive the file size from the server
        file_size = int(await websocket.recv())
        received_size = 0
        
        # Open a new file to save the received data
        with open('received_file.db', 'wb') as file:
            while received_size < file_size:
                chunk = await websocket.recv()
                received_size += len(chunk)
                file.write(chunk)

async def main():
    await file_receive()

asyncio.run(main())


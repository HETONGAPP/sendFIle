import websockets
import asyncio
import os
import glob
import setproctitle
import zipfile
import argparse
import shutil
def compress(folder_name):
    directory = "/home/khadas/rtabmap_data/"
    folder_path = os.path.join(directory, folder_name)
    zip_filename = f"{folder_path}.zip"

    with zipfile.ZipFile(zip_filename, "w") as zipf:
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                file_path = os.path.join(root, file)
                zipf.write(file_path, os.path.relpath(file_path, folder_path))

    print(f"The folder '{folder_path}' has been zipped to '{zip_filename}'.")
    shutil.rmtree(folder_path)
    print(f"The folder '{folder_path}' has been removed.")

async def file_transfer(websocket, path):

    
    # Get a list of all database files in the directory
    #files = glob.glob('/home/tong/Downloads/test/*.zip')

    # Sort the files based on their timestamps in descending order
    #sorted_files = sorted(files, key=os.path.getmtime, reverse=True)

    # Get the latest file
    #latest_file = sorted_files[0] if sorted_files else None
    folder_name = args.folder_name
    zipfile = "/home/khadas/rtabmap_data/" + folder_name + ".zip"

    if zipfile:
        file_size = os.path.getsize(zipfile)
        file_name = os.path.basename(zipfile)
        # Send the file size to the client
        #await websocket.send(str(file_size))
        await websocket.send(f"{file_name}:{file_size}")
        # Open the file and send its contents in chunks
        with open(zipfile, 'rb') as file:
            while True:
                chunk = file.read(1024*1024*10)  # Read 1KB at a time
                if not chunk:
                    break
                await websocket.send(chunk)

    await websocket.close()


async def run_server():
    server = await start_server
    print('Server started')

    # Wait for the file transfer to complete
    await server.wait_closed()
    print('File transfer completed. Exiting.')

    # Stop the event loop after file transfer is complete
    asyncio.get_event_loop().stop()

# Run the server until the file transfer is complete

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Compress a specific folder.")
    parser.add_argument("folder_name", type=str, help="Name of the folder to compress")
    args = parser.parse_args()
    compress(args.folder_name)
    start_server = websockets.serve(file_transfer, 'localhost', 8765)
    setproctitle.setproctitle("FileSender")
    asyncio.get_event_loop().run_until_complete(run_server())


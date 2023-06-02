const WebSocket = require('ws');
const fs = require('fs');

async function fileReceive() {
  const websocket = new WebSocket('ws://localhost:8765');

  await new Promise(resolve => {
    websocket.on('open', resolve);
  });

  // Receive the file size from the server
  const fileSize = parseInt(await new Promise(resolve => {
    websocket.on('message', data => resolve(data));
  }));

  let receivedSize = 0;

  // Open a new file to save the received data
  const fileStream = fs.createWriteStream('received_file.db');

  // Receive file data as chunks
  while (receivedSize < fileSize) {
    const chunk = await new Promise(resolve => {
      websocket.on('message', data => resolve(data));
    });

    receivedSize += chunk.length;
    fileStream.write(chunk);
  }

  fileStream.end();
}

async function main() {
  try {
    await fileReceive();
    console.log('File received successfully.');
  } catch (error) {
    console.error('Error receiving file:', error);
  }
}

main();

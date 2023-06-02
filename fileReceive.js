const WebSocket = require('ws');
const fs = require('fs');

async function fileReceive() {
  const websocket = new WebSocket('ws://localhost:8765');

  await new Promise(resolve => {
    websocket.on('open', resolve);
  });


  // Receive the file name and size from the server
  const fileInfo = await new Promise(resolve => {
    websocket.on('message', data => resolve(String(data)));
  });
  const parts = fileInfo.split(':');
  const fileSize = parts[1];
  const fileName = parts[0];

  let receivedSize = 0;

  // Open a new file to save the received data
  const fileStream = fs.createWriteStream(fileName);

  // Receive file data as chunks
  while (receivedSize < fileSize) {
    const chunk = await new Promise(resolve => {
      websocket.on('message', data => resolve(data));
    });

    receivedSize += chunk.length;
    fileStream.write(chunk);
  }

  fileStream.end();

  // Send confirmation message to the server
  websocket.send('File received');
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

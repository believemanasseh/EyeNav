const WSS_URL = "wss://eyenav.daimones.xyz/ws";
const RECONNECT_DELAY = 3000;
const MAX_RECONNECT_TIME = 5;
let inSession = false;
let clearTimeoutInterval = null;
let socket = null;
let myPort = null;

chrome.runtime.onConnect.addListener((port) => {
  if (port.name === "content") {
    myPort = port;
    myPort.onMessage.addListener((message) => {
      if (message.state === true) {
        startWebSocketConnection();
        inSession = true;
      }

      if (socket && inSession && message.state === false) {
        socket.close();
        inSession = false;
      }

      if (
        message.action === "sendData" &&
        socket &&
        socket.readyState === WebSocket.OPEN
      ) {
        socket.send(JSON.stringify({ image: message.image }));
      }
    });

    myPort.onDisconnect.addListener(() => {
      myPort = null;
    });
  }
});

function startWebSocketConnection() {
  socket = new WebSocket(WSS_URL);

  socket.onopen = () => {
    console.log("WebSocket connection opened");
  };

  socket.onmessage = (event) => {
    try {
      const data = JSON.parse(event.data);
      if (contentPort)
        contentPort.postMessage({ action: "moveCursor", data: data });
    } catch (err) {
      console.error("Error processing websocket message: ", err);
    }
  };

  socket.onerror = (error) => {
    console.error("WebSocket Error: ", error);
    reconnectWebSocket();
  };

  socket.onclose = () => {
    console.log("WebSocket connection closed");
    clearTimeout(clearTimeoutInterval);
  };
}

function reconnectWebSocket() {
  if (inSession) {
    clearTimeoutInterval = setTimeout(() => {
      if (MAX_RECONNECT_TIME > 0) {
        console.log("Attempting to reconnect WebSocket...");
        startWebSocketConnection();
        MAX_RECONNECT_TIME--;
      }
    }, RECONNECT_DELAY);
  }
}

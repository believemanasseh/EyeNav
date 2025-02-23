if (stream == undefined) {
  var FRAME_RATE = 30;
  var stream = null;
  var videoElement = null;
  var processImageFramesInterval = null;

  var port = chrome.runtime.connect({ name: "content" });
}

chrome.runtime.onMessage.addListener(async (message, sender, sendResponse) => {
  if (message.state === true) {
    await startTracking();
    port.postMessage({ state: true });
  } else if (message.state === false) {
    await stopTracking();
  } else if (message.action === "moveCursor") {
    moveCursor(message.data.coordinates.x, message.data.coordinates.y);
  }
});

async function startTracking() {
  try {
    videoElement = document.createElement("video");

    stream = await navigator.mediaDevices.getUserMedia({
      video: {
        facingMode: "user",
        width: { ideal: 1280 },
        height: { ideal: 720 },
        frameRate: { ideal: 30 },
      },
      audio: false,
    });

    // Attach stream to video element
    videoElement.srcObject = stream;
    videoElement.onloadedmetadata = () => {
      videoElement.play();
      startProcessingImageFrames();
    };
  } catch (err) {
    console.error("Error accessing webcam:", err);
    port.postMessage({ state: false });
  }
}

async function stopTracking() {
  if (stream) {
    stream.getTracks().forEach((track) => track.stop());
    stream = null;
  }

  clearInterval(processImageFramesInterval);
}

function processImageFrames() {
  const canvas = document.createElement("canvas");
  const ctx = canvas.getContext("2d");
  ctx.drawImage(videoElement, 0, 0, canvas.width, canvas.height);
  const _imageData = ctx.getImageData(0, 0, canvas.width, canvas.height);

  // Convert imageData to base64 for sending
  const base64Image = canvas.toDataURL("image/jpeg");
  port.postMessage({ action: "sendData", image: base64Image });
}

function startProcessingImageFrames() {
  processImageFramesInterval = setInterval(
    processImageFrames,
    1000 / FRAME_RATE
  );
}

function moveCursor(x, y) {
  // Convert relative coordinates (0-1) to screen coordinates
  const screenX = window.screen.width * x;
  const screenY = window.screen.height * y;

  chrome.input.mouse.move(screenX, screenY, {
    type: "move",
  });
}

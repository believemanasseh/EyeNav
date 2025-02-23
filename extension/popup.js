const START_TEXT = "Start eye tracking";
const STOP_TEXT = "Stop eye tracking";
const START_BTN_COLOR = "#000000";
const STOP_BTN_COLOR = "red";

let btn = document.getElementById("btn");

chrome.action.onClicked.addListener((tab) => {
  chrome.action.setTitle({
    tabId: tab.id,
    title: `You are on tab: ${tab.id}`,
  });
});

document.addEventListener("DOMContentLoaded", () => {
  checkExtensionState();
  btn.addEventListener("click", () => {
    const inSession = localStorage.getItem("inSession") === "true";
    chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
      const activeTab = tabs[0];
      chrome.scripting.executeScript(
        {
          target: { tabId: activeTab.id },
          files: ["content.js"],
        },
        () => {
          if (!inSession) {
            btn.textContent = START_TEXT;
            btn.style.backgroundColor = START_BTN_COLOR;
            chrome.tabs.sendMessage(activeTab.id, {
              state: inSession,
              target: "content",
            });
          } else {
            btn.textContent = STOP_TEXT;
            btn.style.backgroundColor = STOP_BTN_COLOR;
            chrome.tabs.sendMessage(activeTab.id, {
              state: inSession,
              target: "content",
            });
          }

          localStorage.setItem("inSession", !inSession);
        }
      );
    });
  });
});

function checkExtensionState() {
  btn = document.getElementById("btn");
  const inSession = localStorage.getItem("inSession") === "true";
  if (!inSession) {
    btn.textContent = STOP_TEXT;
    btn.style.backgroundColor = STOP_BTN_COLOR;
  } else {
    btn.textContent = START_TEXT;
    btn.style.backgroundColor = START_BTN_COLOR;
  }
}

chrome.tabs.query({ active: true, currentWindow: true }, function (tabs) {
  // Add retry logic
  function sendMessageWithRetry(attempt = 1) {
    chrome.tabs.sendMessage(
      tabs[0].id,
      { type: "startTracking" },
      (response) => {
        if (chrome.runtime.lastError) {
          if (attempt < 3) {
            setTimeout(() => sendMessageWithRetry(attempt + 1), 100);
          }
          console.log("Error sending message:", chrome.runtime.lastError);
        } else {
          console.log("Message sent successfully");
        }
      }
    );
  }
  sendMessageWithRetry();
});

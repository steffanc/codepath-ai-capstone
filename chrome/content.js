console.log("content.js loaded");

// Function to get the current timestamp of the video
function getCurrentVideoTimestamp() {
  const video = document.querySelector('video.video-stream');
  if (video) {
    return video.currentTime; // Current timestamp in seconds
  }
  return null;
}

// Listener for messages from the popup
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  if (request.action === "getTimestamp") {
    const timestamp = getCurrentVideoTimestamp();
    sendResponse({ timestamp: timestamp });
  }
  return true; // Keeps the message channel open for async responses
});
// Get video ID from URL
function getVideoId() {
  const urlParams = new URLSearchParams(window.location.search);
  return urlParams.get('v');
}

const videoId = getVideoId();

if (videoId) {
  chrome.runtime.sendMessage({ action: "getTranscript", videoId: videoId });
}

chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  if (request.action === "displayInsights") {
    // Create a container for the insights
    const insightsContainer = document.createElement('div');
    insightsContainer.style.position = 'fixed';
    insightsContainer.style.bottom = '10px';
    insightsContainer.style.right = '10px';
    insightsContainer.style.backgroundColor = 'rgba(0, 0, 0, 0.8)';
    insightsContainer.style.color = 'white';
    insightsContainer.style.padding = '10px';
    insightsContainer.style.borderRadius = '5px';
    insightsContainer.style.zIndex = '1000';
    insightsContainer.innerHTML = `<h4>Fun Facts & Insights</h4><ul>${request.insights.map(insight => `<li>${insight}</li>`).join('')}</ul>`;

    document.body.appendChild(insightsContainer);
  }
});
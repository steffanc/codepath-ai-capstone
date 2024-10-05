function getYouTubeVideoIdFromUrl(url) {
  const urlObj = new URL(url);
  const videoId = urlObj.searchParams.get('v');  // 'v' is the parameter for video ID in YouTube URLs
  return videoId;
}

// Get the active tab URL
chrome.tabs.query({ active: true, currentWindow: true }, function (tabs) {
  const activeTab = tabs[0];
  const url = activeTab.url;

  if (url && url.includes("youtube.com/watch")) {
    const videoId = getYouTubeVideoIdFromUrl(url);
    console.log("YouTube Video ID:", videoId);

    // Listen for changes in chrome.storage
    chrome.storage.onChanged.addListener(function (changes, namespace) {
      if (changes.chainlitSessionId && namespace === 'local') {
        const sessionId = changes.chainlitSessionId.newValue;
        console.log("Making requests with sessionId:", sessionId, "and videoId:", videoId);

        setTimeout(() => {
          fetchYouTubeTranscript(sessionId, videoId);  // Make the GET request after the delay
        }, 1000);
      }
    });

  } else {
    console.log("Not a YouTube video page.");
  }
});


// Function to make a GET request to the endpoint with session_id and video_id
function fetchYouTubeTranscript(sessionId, videoId) {
  const url = `http://localhost:8000/youtube-transcript/${sessionId}/${videoId}`;

  fetch(url, {
    method: "GET",
    headers: {
      "Content-Type": "application/json"
    }
  })
  .then(response => {
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    return response.json();  // Assuming the response is in JSON format
  })
  .then(data => {
    console.log("Backend response:", data);
  })
  .catch(error => {
    console.error("Error fetching transcript:", error);
  });
}

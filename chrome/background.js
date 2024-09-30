chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  if (request.action === "getTranscript") {
    fetch(`https://yourserver.com/getTranscript?videoId=${request.videoId}`)
      .then(response => response.json())
      .then(transcript => {
        // Once the transcript is available, send it to the LLM API for insights
        fetch(`https://yourllmserver.com/generateInsights`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({ transcript: transcript })
        })
        .then(response => response.json())
        .then(insights => {
          // Send insights back to content script to display on the page
          chrome.tabs.sendMessage(sender.tab.id, { action: "displayInsights", insights: insights });
        });
      });
  }
});
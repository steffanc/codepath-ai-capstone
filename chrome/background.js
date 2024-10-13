chrome.webRequest.onBeforeSendHeaders.addListener(
  function(details) {
    // Loop through request headers to find x-chainlit-session-id
    for (let header of details.requestHeaders) {
      if (header.name.toLowerCase() === 'x-chainlit-session-id') {
        const sessionId = header.value;
        console.log('Session ID found in request headers:', sessionId);

        // Store the session ID in chrome.storage or use it as needed
        chrome.storage.local.set({ chainlitSessionId: sessionId }, function() {
          console.log('Session ID saved to storage:', sessionId);
        });

        break;  // No need to keep looping once we find it
      }
    }
  },
  {
    urls: ["http://localhost:8000/chainlit/*"], // Only listen for requests to Chainlit app
    types: ["main_frame", "sub_frame", "xmlhttprequest"]  // Consider XMLHttpRequests as well
  },
  ["requestHeaders"]  // Intercept request headers
);
console.log("Content script loaded");

// Define the regular expression to match the session ID (assuming it's a UUID format)
const sessionIdRegex = /[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}/;

// Use MutationObserver to detect changes in the DOM
const observer = new MutationObserver((mutationsList, observer) => {
  for (let mutation of mutationsList) {
    if (mutation.type === "childList") {
      // Check the entire page or a specific element for the session ID
      const pageText = document.body.innerText;  // This will search the entire body, can be refined
      const sessionIdMatch = pageText.match(sessionIdRegex);

      if (sessionIdMatch) {
        const sessionId = sessionIdMatch[0];  // The first match should be the session ID
        console.log("Session ID found using regex:", sessionId);

        // Once you have the session ID, stop observing and make backend calls
        observer.disconnect();
        break;  // No need to keep checking other mutations
      } else {
        console.log("Session ID not found");
      }
    }
  }
});

// Start observing the body or a specific parent element for changes
observer.observe(document.body, { childList: true, subtree: true });
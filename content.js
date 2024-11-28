chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
  if (message.action === "extractContent") {
    // Clone the body element to avoid altering the original DOM
    const bodyClone = document.body.cloneNode(true);

    // Remove all <script> tags from the cloned body
    const scripts = bodyClone.querySelectorAll("script");
    scripts.forEach(script => script.remove());

    // Get the inner HTML of the cleaned body content
    const cleanedContent = bodyClone.innerHTML;

    // Send the cleaned content back
    sendResponse({ status: "success", content: cleanedContent });
  }
});

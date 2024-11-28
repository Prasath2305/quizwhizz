document.getElementById("extractButton").addEventListener("click", () => {
  chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
    chrome.tabs.sendMessage(tabs[0].id, { action: "extractContent" }, (response) => {
      if (response && response.status === "success") {
        const content = response.content;

        // Open a dialog box to ask for a name
        const contentName = prompt("Enter a name to save the content:");

        if (contentName) {
          // Send the content and name to the background script for saving
          chrome.runtime.sendMessage({ content, contentName }, (response) => {
            const statusElement = document.getElementById("status");
            if (response && response.status === "success") {
              statusElement.textContent = "Content saved successfully!";
              statusElement.style.color = "green";
            } else {
              statusElement.textContent = "Error saving content. Please try again.";
              statusElement.style.color = "red";
            }
          });
        } else {
          alert("Content name is required to save.");
        }
      } else {
        alert("Failed to extract content. Please try again.");
      }
    });
  });
});
document.getElementById("extractButton").addEventListener("click", () => {
  chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
    const tab = tabs[0];

    if (tab.url.includes("youtube.com/watch")) {
      // Extract the YouTube video link
      const videoLink = tab.url;

      // Open a dialog box to ask for a name
      const videoName = prompt("Enter a name to save the YouTube link:");

      if (videoName) {
        // Send the video link and name to the background script for saving
        chrome.runtime.sendMessage({ videoLink, videoName, type: "youtube" }, (response) => {
          const statusElement = document.getElementById("status");
          if (response && response.status === "success") {
            statusElement.textContent = "YouTube link saved successfully!";
          } else {
            statusElement.textContent = "Error saving YouTube link.";
          }
        });
      } else {
        alert("Name is required to save the YouTube link.");
      }
    } else {
      // Extract page content
      chrome.tabs.sendMessage(tab.id, { action: "extractContent" }, (response) => {
        if (response && response.status === "success") {
          let content = response.content;

          // Remove all HTML tags and CSS content
          const div = document.createElement("div");
          div.innerHTML = content; // Assuming the content is raw HTML

          // Remove all <style> tags and their content
          const styleElements = div.querySelectorAll("style");
          styleElements.forEach((style) => style.remove());

          // Extract only the plain text
          content = div.textContent || div.innerText || "";

          // Open a dialog box to ask for a name
          const contentName = prompt("Enter a name to save the page content:");

          if (contentName) {
            // Send the content and name to the background script for saving
            chrome.runtime.sendMessage({ content, contentName, type: "page" }, (response) => {
              const statusElement = document.getElementById("status");
              if (response && response.status === "success") {
                statusElement.textContent = "Page content saved successfully!";
              } else {
                statusElement.textContent = "Error saving page content.";
              }
            });
          } else {
            alert("Name is required to save the content.");
          }
        } else {
          alert("Failed to extract content.");
        }
      });
    }
  });
});

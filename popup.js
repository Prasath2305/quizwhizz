document.getElementById("extractButton").addEventListener("click", () => {
    chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
      chrome.tabs.sendMessage(tabs[0].id, { action: "extractContent" }, (response) => {
        const statusElement = document.getElementById("status");
        if (response && response.status === "success") {
          statusElement.textContent = "Content extracted and saved successfully!";
          statusElement.style.color = "green";
        } else {
          statusElement.textContent = "Failed to extract content. Please try again.";
          statusElement.style.color = "red";
        }
      });
    });
  });
  
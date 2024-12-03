import { initializeApp } from "https://www.gstatic.com/firebasejs/9.17.2/firebase-app.js";
import { getDatabase, ref, set } from "https://www.gstatic.com/firebasejs/9.17.2/firebase-database.js";

const firebaseConfig = {
  apiKey: "AIzaSyCePtnM6dfL9_S6q_6ZY_SOPT43rCTJTp8",
  authDomain: "web-extension-73948.firebaseapp.com",
  databaseURL: "https://web-extension-73948-default-rtdb.asia-southeast1.firebasedatabase.app",
  projectId: "web-extension-73948",
  storageBucket: "web-extension-73948.appspot.com",
  messagingSenderId: "1037719927941",
  appId: "1:1037719927941:web:580c67ead9d44c22363dec",
};

const app = initializeApp(firebaseConfig);
const database = getDatabase(app);

chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
  if (message.type === "page" && message.content && message.contentName) {
    const contentRef = ref(database, `pageContents/${message.contentName}`);
    set(contentRef, { content: message.content })
      .then(() => sendResponse({ status: "success" }))
      .catch((error) => {
        console.error("Error saving content:", error);
        sendResponse({ status: "error" });
      });
  } else if (message.type === "youtube" && message.videoLink && message.videoName) {
    const videoRef = ref(database, `youtubeLinks/${message.videoName}`);
    set(videoRef, { link: message.videoLink })
      .then(() => sendResponse({ status: "success" }))
      .catch((error) => {
        console.error("Error saving video link:", error);
        sendResponse({ status: "error" });
      });
  }

  // Indicate asynchronous response
  return true;
});

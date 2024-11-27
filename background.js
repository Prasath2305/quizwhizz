import { initializeApp } from "https://www.gstatic.com/firebasejs/9.17.2/firebase-app.js";
import { getDatabase, ref, set } from "https://www.gstatic.com/firebasejs/9.17.2/firebase-database.js";

// Firebase configuration
const firebaseConfig = {
  apiKey: "AIzaSyCePtnM6dfL9_S6q_6ZY_SOPT43rCTJTp8",
  authDomain: "web-extension-73948.firebaseapp.com",
  databaseURL: "https://web-extension-73948-default-rtdb.asia-southeast1.firebasedatabase.app",
  projectId: "web-extension-73948",
  storageBucket: "web-extension-73948.firebasestorage.app",
  messagingSenderId: "1037719927941",
  appId: "1:1037719927941:web:580c67ead9d44c22363dec",
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);
const database = getDatabase(app);

// Listen for messages from the content script
chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
  if (message && message.content) {
    const timestamp = Date.now();
    const contentRef = ref(database, `pageContents/${timestamp}`);
    set(contentRef, { content: message.content, timestamp })
      .then(() => {
        console.log('Content saved successfully');
        sendResponse({ status: 'success' });
      })
      .catch((error) => {
        console.error('Error saving content:', error);
        sendResponse({ status: 'error', error: error.message });
      });

    // Inform Chrome this is an asynchronous response
    return true;
  }
});

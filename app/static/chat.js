/**
 * Chat client using Socket.IO for real-time communication with the server.
 */
var socket = io();

/**
 * Sends the user's message to the server and displays it in the chat.
 */
function sendMessage() {
  var input = document.getElementById("message-input");
  var text = input.value.trim();

  if (!text) {
    return;
  }

  // Display the user's own message immediately
  appendMessage(text, "user-message");

  // Clear the input field
  input.value = "";

  // Send to server via Socket.IO
  socket.emit("message", { text: text });

  // Show loading indicator while waiting for response
  showLoadingIndicator();
}

/**
 * Listen for responses from the server and display them.
 */
socket.on("response", function (data) {
  appendMessage(data.text, "bot-message");
  hideLoadingIndicator();
});

/**
 * Append a message to the chat messages container.
 * @param {string} text - The message text
 * @param {string} className - CSS class to apply (user-message or bot-message)
 */
function appendMessage(text, className) {
  var messages = document.getElementById("messages");
  var newMessage = document.createElement("li");
  newMessage.textContent = text;
  newMessage.className = className;
  messages.appendChild(newMessage);

  // Auto-scroll to the latest message
  messages.scrollTop = messages.scrollHeight;
}

/**
 * Clear conversation history on the server and in the UI.
 */
function clearHistory() {
  fetch("/clear-history", { method: "POST" }).then(function () {
    var messages = document.getElementById("messages");
    while (messages.firstChild) {
      messages.removeChild(messages.firstChild);
    }
  });
}

function showLoadingIndicator() {
  document.getElementById("loading").style.display = "block";
}

function hideLoadingIndicator() {
  document.getElementById("loading").style.display = "none";
}

// Allow sending messages with the Enter key
document.getElementById("message-input").addEventListener("keypress", function (e) {
  if (e.key === "Enter") {
    sendMessage();
  }
});

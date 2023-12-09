/**
 * Establishes a connection to the server.
 * @type {Socket}
 */
var socket = io();

/**
 * Sends a message to the server and shows the loading indicator.
 */
function sendMessage() {
  var text = document.getElementById("message-input").value;

  // Validate the input
  if (!text) {
    alert("Please enter a message.");
    return;
  }

  socket.emit("message", { text: text });

  // Show the loading indicator
  showLoadingIndicator();
}

// Listening for responses from the server
socket.on("response", function (data) {
  updateMessages(data.text);

  // Hide the loading indicator
  hideLoadingIndicator();
});

/**
 * Shows the loading indicator by changing its display style to 'block'.
 */
function showLoadingIndicator() {
  document.getElementById("loading").style.display = "block";
}

/**
 * Hides the loading indicator by changing its display style to 'none'.
 */
function hideLoadingIndicator() {
  document.getElementById("loading").style.display = "none";
}

/**
 * Updates the messages displayed in the chat window.
 */
function updateMessages(message) {
  var messages = document.getElementById("messages");
  var newMessage = document.createElement("li");
  newMessage.textContent = message;
  messages.appendChild(newMessage);
}

// Add an event listener to the send button
document.getElementById("send-button").addEventListener("click", sendMessage);
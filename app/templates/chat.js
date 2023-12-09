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
 * Updates the messages displayed on the page by appending a new message.
 * @param {string} text - The text of the message to append.
 */
function updateMessages(text) {
  var messages = document.getElementById("messages");
  messages.innerHTML += "<div>" + text + "</div>";
}

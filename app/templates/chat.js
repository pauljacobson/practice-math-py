var socket = io();

function sendMessage() {
  var text = document.getElementById("message-input").value;
  socket.emit("message", { text: text });

  // Show the loading indicator
  document.getElementById("loading").style.display = "block";
}

// Listening for responses from the server
socket.on("response", function (data) {
  var messages = document.getElementById("messages");
  messages.innerHTML += "<div>" + data.text + "</div>";

  // Hide the loading indicator
  document.getElementById("loading").style.display = "none";
});

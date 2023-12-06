from app import app, socketio
from flask import render_template, request, redirect, url_for
from .openai_integration import ask_openai
from werkzeug.utils import secure_filename
import os

# Impose checks on file uploads
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg"}
MAX_FILE_SIZE = 1024 * 1024 * 5  # 5MB limit


def allowed_file(filename):
    """Check if a file is allowed to be uploaded"""
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


# Add route for the chat interface
@app.route("/chat")
def chat():
    return render_template("chat.html")


# SocketIO event for receiving a message
@socketio.on("message")
def handle_message(data):
    """Handle a message sent from the client"""
    question = data["text"]
    # Call OpenAI API
    response = ask_openai(question)
    # Emit the response back to the client
    socketio.emit("response", {"text": response})


# Handle image uploads
@app.route("/upload", methods=["POST"])
def upload_file():
    """Handle image uploads"""
    if "file" not in request.files:
        return "No file part", 400
    file = request.files["file"]
    if file.filename == "":
        return "No selected file", 400
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        # Check file size
        file.seek(0, os.SEEK_END)
        file_length = file.tell()
        if file_length > MAX_FILE_SIZE:
            return "File too large", 400
        file.seek(0)
        filepath = os.path.join(app.root_path, "static/uploads", filename)
        file.save(filepath)
        # Process the image with OpenAI API
        # ...
        return redirect(url_for("chat"))
    else:
        return "Invalid file type", 400

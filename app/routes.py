import os

from flask import Blueprint, render_template, request, redirect, url_for, session, current_app
from flask_login import login_required
from flask_socketio import emit
from werkzeug.utils import secure_filename

from app import socketio
from app.claude_integration import ask_claude

# Create a blueprint for the main routes
bp = Blueprint("main", __name__)

# File upload constraints
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg"}
MAX_FILE_SIZE = 1024 * 1024 * 5  # 5 MB


def allowed_file(filename):
    """Check if a file has an allowed extension."""
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@bp.route("/")
def index():
    """Landing page — public, no login required."""
    return render_template("index.html")


@bp.route("/chat")
@login_required
def chat():
    """Chat interface — requires authentication."""
    return render_template("chat.html")


@bp.route("/clear-history", methods=["POST"])
@login_required
def clear_history():
    """Reset the conversation history stored in the session."""
    session.pop("conversation_history", None)
    return "", 204


@bp.route("/upload", methods=["POST"])
@login_required
def upload_file():
    """Handle image uploads with validation."""
    if "file" not in request.files:
        return "No file part", 400

    file = request.files["file"]
    if file.filename == "":
        return "No selected file", 400

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)

        # Check file size without consuming the stream
        file.seek(0, os.SEEK_END)
        file_length = file.tell()
        if file_length > MAX_FILE_SIZE:
            return "File too large", 400
        file.seek(0)

        filepath = os.path.join(current_app.root_path, "static", "uploads", filename)
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        file.save(filepath)

        return redirect(url_for("main.chat"))
    else:
        return "Invalid file type", 400


# ---- Socket.IO event handlers ----

@socketio.on("message")
def handle_message(data):
    """Receive a chat message, send it to Claude, and emit the response."""
    question = data.get("text", "").strip()
    if not question:
        emit("response", {"text": "Please enter a question."})
        return

    response = ask_claude(question)
    emit("response", {"text": response})

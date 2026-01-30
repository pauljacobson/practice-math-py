from dotenv import load_dotenv

# Load .env before anything imports os.getenv
load_dotenv()

from app import create_app, socketio

app = create_app()

if __name__ == "__main__":
    # Use socketio.run() instead of app.run() so that
    # the Socket.IO WebSocket transport works correctly
    socketio.run(app, debug=True, allow_unsafe_werkzeug=True)

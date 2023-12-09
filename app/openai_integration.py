# Import necessary modules
from flask import Flask, jsonify, request
import logging
import openai
from dotenv import load_dotenv
import os
from auth import auth, get_auth_token

# Create a new Flask application
app = Flask(__name__)

# Set up logging with a level of INFO
logging.basicConfig(level=logging.INFO)


# Function to set up the OpenAI API
def setup_openai_api():
    # Load environment variables from .env file
    load_dotenv()
    # Set the OpenAI API key from the OPENAI_API_KEY environment variable
    openai.api_key = os.getenv("OPENAI_API_KEY")


# Function to send a question to the OpenAI API and get a response
def ask_openai(question):
    # Set up the OpenAI API
    setup_openai_api()
    try:
        # Send a series of messages to the OpenAI API and get a response
        response = openai.ChatCompletion.create(
            model="gpt-4-1106-preview",
            messages=[
                {
                    "role": "system",
                    "content": "You are a personal math tutor. Write and run code to answer math questions.",
                },
                {"role": "user", "content": question},
            ],
        )
        # Validate the response
        if response and response.get("choices") and len(response["choices"]) > 0:
            # Return the content of the first choice in the response
            return response["choices"][0]["message"]["content"]
        else:
            # Log an error and return None if the response is invalid
            logging.error("Invalid response from OpenAI API")
            return None
    except openai.error.AuthenticationError:
        logging.error("Authentication with OpenAI failed. Check your API key.")
        return None
    except openai.error.RateLimitError:
        logging.error("Rate limit exceeded. Please wait a moment and try again.")
        return None
    except openai.error.InvalidRequestError as e:
        logging.error(f"Invalid request: {e}")
        return None
    except Exception as e:
        # Log an error and return None if an exception occurs
        logging.error(f"Error querying OpenAI API: {e}")
        return None


# Define a Flask route for asking questions
@app.route("/ask", methods=["POST"])
def token_route():
    """Route to generate token"""
    return get_auth_token()


# Add the auth.login_required decorator to the /ask route
@app.route("/ask", methods=["POST"])
@auth.login_required
def ask_route():
    # Get the question from the request JSON
    question = request.json.get("question")
    # Return an error if no question is provided
    if not question:
        return jsonify({"error": "No question provided"}), 400
    # Get the answer from the OpenAI API
    answer = ask_openai(question)
    # Return an error if no answer is received
    if not answer:
        return jsonify({"error": "Could not get an answer"}), 500
    # Return the answer in a JSON response
    return jsonify({"answer": answer})

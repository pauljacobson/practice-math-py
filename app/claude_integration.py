"""Anthropic Claude integration for the math tutor chatbot.

Uses the Anthropic Python SDK to send questions to Claude and maintain
per-session conversation history via Flask's session object.
"""

import logging
import os

import anthropic
from flask import session

logger = logging.getLogger(__name__)

# Initialize the Anthropic client once at module level.
# The SDK reads ANTHROPIC_API_KEY from the environment automatically.
client = anthropic.Anthropic()

# The model to use for all requests
MODEL = "claude-haiku-3-5-20241022"

# System prompt that establishes Claude's role as a math tutor
SYSTEM_PROMPT = (
    "You are a friendly and patient personal math tutor for kids. "
    "Explain concepts step by step in simple language. "
    "Use examples and encourage the student. "
    "If the student makes a mistake, gently guide them to the correct answer "
    "rather than just giving it away."
)

# Maximum number of messages to keep in conversation history
MAX_HISTORY = 50


def ask_claude(question):
    """Send a question to Claude and return the response text.

    Maintains conversation history in Flask's session so that Claude
    has context from earlier messages in the same session.

    Args:
        question: The user's math question as a string.

    Returns:
        The assistant's response text, or an error message string.
    """
    # Retrieve or initialize conversation history from the session
    history = session.get("conversation_history", [])

    # Append the new user message
    history.append({"role": "user", "content": question})

    # Trim history to prevent the context from growing unbounded
    if len(history) > MAX_HISTORY:
        history = history[-MAX_HISTORY:]

    try:
        response = client.messages.create(
            model=MODEL,
            max_tokens=1024,
            system=SYSTEM_PROMPT,
            messages=history,
        )

        # Extract the text from the first content block
        assistant_text = response.content[0].text

        # Append the assistant's reply to the history
        history.append({"role": "assistant", "content": assistant_text})

        # Persist the updated history back into the session
        session["conversation_history"] = history

        return assistant_text

    except anthropic.AuthenticationError:
        logger.error("Anthropic API authentication failed. Check ANTHROPIC_API_KEY.")
        return "Sorry, there was an authentication error. Please contact the administrator."
    except anthropic.RateLimitError:
        logger.error("Anthropic API rate limit exceeded.")
        return "I'm a bit busy right now. Please try again in a moment."
    except anthropic.APIError as e:
        logger.error("Anthropic API error: %s", e)
        return "Sorry, something went wrong. Please try again."

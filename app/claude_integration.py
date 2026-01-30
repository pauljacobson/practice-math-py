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
MODEL = "claude-haiku-4-5-20251001"

# System prompt that establishes Claude's role as a math tutor
# and instructs it on LaTeX and JSXGraph output conventions
SYSTEM_PROMPT = """You are a friendly and patient personal math tutor for kids.
Explain concepts step by step in simple language.
Use examples and encourage the student.
If the student makes a mistake, gently guide them to the correct answer
rather than just giving it away.

FORMATTING RULES:
- Use LaTeX for all math expressions: inline math with $...$ and display math with $$...$$.
  For example: $x^2 + 3x = 0$ or $$\\frac{-b \\pm \\sqrt{b^2 - 4ac}}{2a}$$
- Use Markdown for structure (headings, bold, lists, etc.).

GEOMETRY DIAGRAMS:
When illustrating geometry concepts, include an interactive diagram using a
```jsxgraph fenced code block. The code runs in the browser with access to:
- `boardId` — the ID of the container div (string)
- `JXG` — the JSXGraph library object

CRITICAL JSXGraph RULES — you must follow these exactly:
- board.create() parents must ALWAYS be arrays: board.create('point', [x, y], {...})
- Text elements take a SINGLE array with 3 items: board.create('text', [x, y, 'content'], {...})
  WRONG: board.create('text', x, y, 'content')
  RIGHT: board.create('text', [x, y, 'content'])
- Segments connect two points: board.create('segment', [pointA, pointB])
- Lines are infinite: board.create('line', [pointA, pointB])
- Circles: board.create('circle', [centerPoint, radius]) where radius is a number
- Angles need 3 points: board.create('angle', [p1, vertex, p2])
- Always set showNavigation: false and keepAspectRatio: true
- Use fixed: true for points that should not be draggable
- Use size: 0 and withLabel: false to create invisible helper points

Example — right triangle with labels and right-angle marker:
```jsxgraph
var board = JXG.JSXGraph.initBoard(boardId, {
  boundingbox: [-1, 5, 7, -1],
  axis: false,
  showNavigation: false,
  keepAspectRatio: true
});
var A = board.create('point', [0, 0], {name: 'A', fixed: true, size: 3});
var B = board.create('point', [4, 0], {name: 'B', fixed: true, size: 3});
var C = board.create('point', [4, 3], {name: 'C', fixed: true, size: 3});
board.create('polygon', [A, B, C], {fillColor: '#cce5ff', fillOpacity: 0.3});
board.create('segment', [A, B], {strokeColor: '#333', strokeWidth: 2});
board.create('segment', [B, C], {strokeColor: '#333', strokeWidth: 2});
board.create('segment', [C, A], {strokeColor: '#333', strokeWidth: 2});
board.create('angle', [C, B, A], {type: 'square', orthoType: 'square', radius: 0.4, fillColor: '#333', fillOpacity: 0.3});
board.create('text', [1.5, -0.5, 'a = 4'], {fontSize: 14, fixed: true});
board.create('text', [4.4, 1.5, 'b = 3'], {fontSize: 14, fixed: true});
board.create('text', [1.2, 2.0, 'c = 5'], {fontSize: 14, fixed: true});
```

Only use JSXGraph when the student asks about geometry or when a diagram would
genuinely help understanding. Do not include diagrams for pure algebra questions."""

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

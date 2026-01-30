/**
 * Chat client using Socket.IO for real-time communication with the server.
 *
 * Rendering pipeline for bot messages:
 *   1. Protect LaTeX expressions from Markdown parsing by replacing them
 *      with placeholders.
 *   2. Parse remaining text as Markdown via marked.
 *   3. Sanitize the HTML output with DOMPurify.
 *   4. Restore LaTeX placeholders and render them with KaTeX.
 *   5. Convert ```jsxgraph code blocks into interactive JSXGraph boards.
 */
var socket = io();

// Counter for generating unique JSXGraph board IDs
var boardCounter = 0;

// ---- Marked configuration ----
marked.setOptions({
  breaks: false,
  gfm: true
});

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
 * Render LaTeX math expressions in the given text using KaTeX.
 *
 * Strategy: Before Markdown parsing, we extract LaTeX expressions and
 * replace them with unique placeholders. After Markdown + DOMPurify,
 * we swap the placeholders back with KaTeX-rendered HTML.
 *
 * This prevents Markdown from mangling LaTeX syntax (e.g. treating
 * underscores as emphasis).
 *
 * @param {string} text - Raw text from Claude
 * @returns {{ text: string, placeholders: Object }} processed text and map
 */
function extractLatex(text) {
  var placeholders = {};
  var counter = 0;

  // Replace display math ($$...$$) first — greedy across newlines
  text = text.replace(/\$\$([\s\S]+?)\$\$/g, function (match, latex) {
    var id = "LATEXPLACEHOLDER" + counter++ + "END";
    try {
      placeholders[id] = katex.renderToString(latex.trim(), {
        displayMode: true,
        throwOnError: false
      });
    } catch (e) {
      placeholders[id] = match; // fall back to raw text
    }
    return id;
  });

  // Replace inline math ($...$) — single line only, no nested $
  text = text.replace(/\$([^\$\n]+?)\$/g, function (match, latex) {
    var id = "LATEXPLACEHOLDER" + counter++ + "END";
    try {
      placeholders[id] = katex.renderToString(latex.trim(), {
        displayMode: false,
        throwOnError: false
      });
    } catch (e) {
      placeholders[id] = match;
    }
    return id;
  });

  return { text: text, placeholders: placeholders };
}

/**
 * Restore LaTeX placeholders in the HTML string with rendered KaTeX.
 *
 * @param {string} html - HTML string containing placeholders
 * @param {Object} placeholders - Map of placeholder ID to rendered HTML
 * @returns {string} HTML with KaTeX rendered in place
 */
function restoreLatex(html, placeholders) {
  for (var id in placeholders) {
    html = html.split(id).join(placeholders[id]);
  }
  return html;
}

/**
 * After the message element is in the DOM, find any ```jsxgraph code
 * blocks that were rendered as <pre><code class="language-jsxgraph">
 * and replace them with live interactive JSXGraph boards.
 *
 * Claude is instructed to output JSXGraph code using the JXG.JSXGraph API.
 * The code receives a variable `boardId` containing the container div ID.
 *
 * SECURITY NOTE: The code executed here comes from Claude's API responses
 * (server-side, authenticated), not from untrusted user input. The Function
 * constructor is used intentionally to run JSXGraph drawing commands that
 * produce interactive geometry diagrams.
 *
 * @param {HTMLElement} messageEl - The <li> element containing the message
 */
function activateJsxGraphBlocks(messageEl) {
  var codeBlocks = messageEl.querySelectorAll('code.language-jsxgraph');

  for (var i = 0; i < codeBlocks.length; i++) {
    var codeEl = codeBlocks[i];
    var pre = codeEl.parentElement; // the <pre> wrapper
    var jsxCode = codeEl.textContent;

    // Create a container div for the JSXGraph board
    var boardId = "jsxgraph-board-" + (boardCounter++);
    var container = document.createElement("div");
    container.id = boardId;
    container.className = "jsxgraph-container";

    // Replace the <pre> block with the board container
    pre.parentNode.replaceChild(container, pre);

    // Execute the JSXGraph code — intentional dynamic evaluation of
    // Claude API output to render interactive geometry diagrams.
    // The code has access to `boardId` (the container div ID) and `JXG`.
    try {
      /* jshint -W054 */ // suppress "Function constructor is eval"
      var fn = new Function("boardId", "JXG", jsxCode);  // eslint-disable-line no-new-func
      fn(boardId, JXG);
    } catch (e) {
      container.textContent = "Diagram error: " + e.message;
      container.className = "jsxgraph-error";
    }
  }
}

/**
 * Append a message to the chat messages container.
 * User messages are inserted as plain text for safety.
 * Bot messages go through the full rendering pipeline:
 *   LaTeX extraction -> Markdown -> DOMPurify -> LaTeX restore -> JSXGraph
 *
 * @param {string} text - The message text
 * @param {string} className - CSS class to apply (user-message or bot-message)
 */
function appendMessage(text, className) {
  var messages = document.getElementById("messages");
  var newMessage = document.createElement("li");
  newMessage.className = className;

  if (className === "bot-message") {
    // Step 1: Extract LaTeX before Markdown can mangle it
    var extracted = extractLatex(text);

    // Step 2: Parse remaining text as Markdown
    var rawHtml = marked.parse(extracted.text);

    // Step 3: Sanitize the HTML (DOMPurify)
    var cleanHtml = DOMPurify.sanitize(rawHtml);

    // Step 4: Restore LaTeX placeholders with rendered KaTeX HTML
    var finalHtml = restoreLatex(cleanHtml, extracted.placeholders);

    newMessage.innerHTML = DOMPurify.sanitize(finalHtml, {
      // Allow KaTeX's inline styles and SVG elements needed for math rendering
      ADD_TAGS: ["math", "semantics", "mrow", "mi", "mn", "mo", "msup",
                 "msub", "mfrac", "mspace", "mtext", "annotation",
                 "svg", "line", "path", "rect", "circle", "g", "use",
                 "defs", "symbol", "span"],
      ADD_ATTR: ["xmlns", "xlink:href", "viewBox", "width", "height",
                 "preserveAspectRatio", "focusable", "role", "aria-hidden",
                 "style", "d", "x", "y", "x1", "y1", "x2", "y2",
                 "fill", "stroke", "stroke-width", "transform", "class"]
    });

    // Step 5: Activate any JSXGraph code blocks now that the element is in DOM
    messages.appendChild(newMessage);
    activateJsxGraphBlocks(newMessage);
  } else {
    // User messages stay as plain text — no need to parse
    newMessage.textContent = text;
    messages.appendChild(newMessage);
  }

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

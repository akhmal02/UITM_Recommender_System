const chatForm = document.getElementById("chatForm");
const messageInput = document.getElementById("messageInput");
const sendButton = document.getElementById("sendButton");
const chatMessages = document.getElementById("chatMessages");
const typingIndicator = document.getElementById("typingIndicator");
const errorBox = document.getElementById("errorBox");

const MAX_MESSAGE_LENGTH = 600;

function escapeHtml(value) {
  const div = document.createElement("div");
  div.textContent = value;
  return div.innerHTML;
}

function appendMessage(text, sender) {
  const bubble = document.createElement("div");
  bubble.className = `bubble ${sender}`;
  bubble.innerHTML = escapeHtml(text);
  chatMessages.appendChild(bubble);
  chatMessages.scrollTop = chatMessages.scrollHeight;
}

function showError(message) {
  errorBox.textContent = message;
  errorBox.classList.remove("hidden");
}

function hideError() {
  errorBox.textContent = "";
  errorBox.classList.add("hidden");
}

function setLoading(isLoading) {
  sendButton.disabled = isLoading;
  messageInput.disabled = isLoading;
  typingIndicator.classList.toggle("hidden", !isLoading);
}

chatForm.addEventListener("submit", async (event) => {
  event.preventDefault();
  hideError();

  const message = messageInput.value.trim();
  if (!message) {
    showError("Please enter a message before sending.");
    return;
  }

  if (message.length > MAX_MESSAGE_LENGTH) {
    showError(`Message is too long. Max ${MAX_MESSAGE_LENGTH} characters.`);
    return;
  }

  appendMessage(message, "user");
  messageInput.value = "";
  setLoading(true);

  try {
    const response = await fetch("/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message }),
    });

    let data = null;
    try {
      data = await response.json();
    } catch (jsonError) {
      showError("Invalid response from server. Please try again.");
      return;
    }

    if (!response.ok) {
      showError(data?.error || "Something went wrong. Please try again.");
      return;
    }

    if (!data || typeof data.reply !== "string") {
      showError("Server returned an unexpected response format.");
      return;
    }

    appendMessage(data.reply, "bot");
  } catch (networkError) {
    showError("Cannot connect to server. Check your internet and try again.");
  } finally {
    setLoading(false);
    messageInput.focus();
  }
});

const chatContainer = document.getElementById("chatContainer");
const userInput = document.getElementById("userInput");
const sendBtn = document.getElementById("sendBtn");
const languageSelect = document.getElementById("languageSelect");
const micBtn = document.getElementById("micBtn");
const stopBtn = document.getElementById("stopBtn");

let recognition = null;
let isRecording = false;

// Initialize Speech Recognition
if ('webkitSpeechRecognition' in window || 'SpeechRecognition' in window) {
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    recognition = new SpeechRecognition();
    recognition.continuous = false;
    recognition.interimResults = false;
} else {
    micBtn.style.display = 'none';
    console.warn("Speech Recognition API not supported in this browser.");
}

function getVoiceForLanguage(lang) {
    const voices = window.speechSynthesis.getVoices();
    // Try to find an exact match first, then a partial match
    let voice = voices.find(v => v.lang.startsWith(lang));
    return voice || voices[0]; // Fallback to default
}

function speak(text) {
    if (!('speechSynthesis' in window)) return;

    // Cancel any ongoing speech
    window.speechSynthesis.cancel();

    const utterance = new SpeechSynthesisUtterance(text);
    const lang = languageSelect.value;

    // Map simplified lang codes to BCP 47 tags for better matching
    const langMap = {
        'en': 'en-US',
        'hi': 'hi-IN',
        'bn': 'bn-IN',
        'mr': 'mr-IN',
        'ta': 'ta-IN',
        'te': 'te-IN'
    };

    utterance.lang = langMap[lang] || lang;

    // Wait for voices to be loaded (needed for Chrome)
    if (window.speechSynthesis.getVoices().length === 0) {
        window.speechSynthesis.addEventListener('voiceschanged', () => {
            utterance.voice = getVoiceForLanguage(utterance.lang);
            window.speechSynthesis.speak(utterance);
        }, { once: true });
    } else {
        utterance.voice = getVoiceForLanguage(utterance.lang);
        window.speechSynthesis.speak(utterance);
    }
}



// Stop Button Handler
if (stopBtn) {
    stopBtn.addEventListener("click", () => {
        if ('speechSynthesis' in window) {
            window.speechSynthesis.cancel();
        }
    });
}

function addMessage(text, sender) {
    const messageDiv = document.createElement("div");
    messageDiv.className = `message ${sender}`;

    const bubble = document.createElement("div");
    bubble.className = "bubble";
    bubble.innerText = text;

    messageDiv.appendChild(bubble);
    chatContainer.appendChild(messageDiv);

    chatContainer.scrollTop = chatContainer.scrollHeight;

    // Speak bot messages
    if (sender === "bot") {
        speak(text);
    }
}

async function sendMessage() {
    const text = userInput.value.trim();
    if (!text) return;

    addMessage(text, "user");
    userInput.value = "";

    // Show loading state
    const loadingDiv = document.createElement("div");
    loadingDiv.className = "message bot loading-msg";
    loadingDiv.innerHTML = '<div class="bubble">Thinking...</div>';
    chatContainer.appendChild(loadingDiv);
    chatContainer.scrollTop = chatContainer.scrollHeight;

    const payload = {
        message: text,
        language: languageSelect.value
    };

    try {
        const response = await fetch("/api/chat", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(payload)
        });

        const data = await response.json();

        // Remove loading message
        chatContainer.removeChild(loadingDiv);

        if (response.ok) {
            addMessage(data.response, "bot");
        } else {
            addMessage("Something went wrong. Please try again.", "bot");
        }
    } catch (error) {
        if (chatContainer.contains(loadingDiv)) {
            chatContainer.removeChild(loadingDiv);
        }
        addMessage("Server is not reachable.", "bot");
    }
}

// Mic Button Handler
if (recognition) {
    micBtn.addEventListener("click", () => {
        if (isRecording) {
            recognition.stop();
        } else {
            const lang = languageSelect.value;
            const langMap = {
                'en': 'en-US',
                'hi': 'hi-IN',
                'bn': 'bn-IN',
                'mr': 'mr-IN',
                'ta': 'ta-IN',
                'te': 'te-IN'
            };
            recognition.lang = langMap[lang] || 'en-US';
            recognition.start();
        }
    });

    recognition.onstart = () => {
        isRecording = true;
        micBtn.classList.add("recording");
    };

    recognition.onend = () => {
        isRecording = false;
        micBtn.classList.remove("recording");
    };

    recognition.onresult = (event) => {
        const transcript = event.results[0][0].transcript;
        userInput.value = transcript;
        // Optional: Auto-send or just focus
        userInput.focus();
    };

    recognition.onerror = (event) => {
        console.error("Speech recognition error", event.error);
        isRecording = false;
        micBtn.classList.remove("recording");
    };
}

sendBtn.addEventListener("click", sendMessage);

userInput.addEventListener("keypress", (e) => {
    if (e.key === "Enter") {
        sendMessage();
    }
});

// Update TTS voices when they are loaded
window.speechSynthesis.onvoiceschanged = () => {
    // Just ensures voices are ready
};

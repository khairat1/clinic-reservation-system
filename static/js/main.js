// ─── CHATBOT WIDGET ────────────────────────────────────────────────────────
const mcLauncher = document.getElementById("mcLauncher");
const mcWindow = document.getElementById("mcWindow");
const mcClose = document.getElementById("mcClose");
const mcHint = document.getElementById("mcHint");
const mcInput = document.getElementById("mcInput");
const mcSend = document.getElementById("mcSend");
const mcBody = document.getElementById("mcBody");
const mcTyping = document.getElementById("mcTyping");
const mcActions = document.querySelectorAll(".mc-actions button");

if (mcLauncher) {
    mcLauncher.addEventListener("click", () => {
        mcWindow.classList.toggle("active");
        mcHint.classList.add("hide");
    });

    mcClose.addEventListener("click", () => {
        mcWindow.classList.remove("active");
    });

    function addMessage(text, type) {
        const msg = document.createElement("div");
        msg.className = `mc-message ${type}`;
        msg.textContent = text;
        mcBody.insertBefore(msg, mcTyping);
        mcBody.scrollTop = mcBody.scrollHeight;
    }

    function sendMessage(text) {
    if (!text.trim()) return;
    addMessage(text, "user");
    mcInput.value = "";
    mcTyping.classList.add("show");

    fetch("/chatbot/send/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": getCookie("csrftoken"),
        },
        body: JSON.stringify({ message: text }),
    })
    .then(response => response.json())
    .then(data => {
        mcTyping.classList.remove("show");
        addMessage(data.message, "bot");
    })
    .catch(() => {
        mcTyping.classList.remove("show");
        addMessage("Sorry, something went wrong. Please try again.", "bot");
    });
}

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

    mcSend.addEventListener("click", () => {
        sendMessage(mcInput.value);
    });

    mcInput.addEventListener("keydown", (e) => {
        if (e.key === "Enter") sendMessage(mcInput.value);
    });

    mcActions.forEach((btn) => {
        btn.addEventListener("click", () => {
            sendMessage(btn.dataset.message);
        });
    });

    setTimeout(() => {
        mcHint.classList.add("hide");
    }, 7000);
}
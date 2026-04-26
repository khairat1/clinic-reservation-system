// ─── CHATBOT WIDGET ────────────────────────────────────────────────────────
const mcLauncher = document.getElementById("mcLauncher");

if (mcLauncher) {
    const mcWindow = document.getElementById("mcWindow");
    const mcClose = document.getElementById("mcClose");
    const mcHint = document.getElementById("mcHint");
    const mcInput = document.getElementById("mcInput");
    const mcSend = document.getElementById("mcSend");
    const mcBody = document.getElementById("mcBody");
    const mcTyping = document.getElementById("mcTyping");
    const mcHeader = mcWindow.querySelector(".mc-header");
    const mcActions = document.querySelectorAll(".mc-actions button");

    // ─── STATE ──────────────────────────────────────────────────────────────
    let lastDepartment = ""; 

    // ─── DYNAMIC INJECTION (No HTML touch) ──────────────────────────────────
    // Add "+ New Chat" button to header
    const mcNewChatBtn = document.createElement("button");
    mcNewChatBtn.id = "mcNewChat";
    mcNewChatBtn.innerHTML = "<b>+</b> New Chat";
    mcNewChatBtn.style = "background: #27d66f; border: none; color: #071a55; border-radius: 20px; padding: 6px 14px; cursor: pointer; font-size: 13px; font-weight: bold; box-shadow: 0 4px 10px rgba(0,0,0,0.15); transition: 0.2s ease; margin: 0 10px;";
    
    // Hover effect
    mcNewChatBtn.onmouseover = () => { mcNewChatBtn.style.background = "#22c364"; mcNewChatBtn.style.transform = "scale(1.05)"; };
    mcNewChatBtn.onmouseout = () => { mcNewChatBtn.style.background = "#27d66f"; mcNewChatBtn.style.transform = "scale(1)"; };

    // Insert before the close button
    mcHeader.insertBefore(mcNewChatBtn, mcClose);

    // Add related icons CSS
    const style = document.createElement('style');
    style.innerHTML = `
        .mc-message { position: relative; padding-left: 45px !important; margin-bottom: 20px; border-radius: 18px !important; }
        .mc-message.user { padding-left: 15px !important; padding-right: 45px !important; text-align: right; margin-left: auto; }
        .mc-message::before { 
            content: "🤖"; position: absolute; left: 5px; top: 0; 
            width: 32px; height: 32px; background: #eef2f7; 
            border-radius: 50%; display: flex; align-items: center; 
            justify-content: center; font-size: 18px; border: 1px solid #d1d9e6;
        }
        .mc-message.user::before { content: "👤"; left: auto; right: 5px; background: #0D47A1; border: none; color: white; }
        .mc-message.bot-neurology::before { content: "🧠"; background: #f3e5f5; }
        .mc-message.bot-cardiology::before { content: "❤️"; background: #ffebee; }
        .mc-message.bot-pediatrics::before { content: "👶"; background: #e3f2fd; }
        .mc-message.bot-general::before { content: "🩺"; background: #e8f5e9; }
    `;
    document.head.appendChild(style);

    // ─── CORE LOGIC ─────────────────────────────────────────────────────────
    
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

    function addMessage(text, type, dept = "", skipScroll = false) {
        const msg = document.createElement("div");
        let extraClass = "";
        if (type === "bot" && dept) {
            const lowerDept = dept.toLowerCase();
            if (lowerDept.includes("neuro")) extraClass = " bot-neurology";
            else if (lowerDept.includes("cardio")) extraClass = " bot-cardiology";
            else if (lowerDept.includes("pedia")) extraClass = " bot-pediatrics";
            else extraClass = " bot-general";
        }
        
        msg.className = `mc-message ${type}${extraClass}`;
        msg.innerHTML = text.replace(/\n/g, '<br>');
        mcBody.insertBefore(msg, mcTyping);
        if (!skipScroll) {
            mcBody.scrollTop = mcBody.scrollHeight;
        }
    }

    function loadHistory() {
        fetch("/chatbot/history/")
            .then(res => res.json())
            .then(data => {
                if (data.history && data.history.length > 0) {
                    const initialMsg = mcBody.querySelector(".mc-message.bot");
                    if (initialMsg) initialMsg.remove();
                    
                    data.history.forEach(chat => {
                        addMessage(chat.message, "user", "", true);
                        addMessage(chat.response, "bot", chat.department, true);
                        if (chat.department) lastDepartment = chat.department;
                    });
                    mcBody.scrollTop = mcBody.scrollHeight;
                }
            });
    }

    let isSending = false;

    function sendMessage(text) {
        if (!text.trim() || isSending) return;
        isSending = true;
        addMessage(text, "user");
        mcInput.value = "";
        mcTyping.classList.add("show");

        fetch("/chatbot/send/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": getCookie("csrftoken"),
            },
            body: JSON.stringify({ 
                message: text,
                department: lastDepartment 
            }),
        })
        .then(response => {
            if (!response.ok) throw new Error("Server error");
            return response.json();
        })
        .then(data => {
            mcTyping.classList.remove("show");
            if (data.department) lastDepartment = data.department;
            addMessage(data.message, "bot", data.department);
        })
        .catch(() => {
            mcTyping.classList.remove("show");
            addMessage("I'm sorry, I'm having trouble connecting to the medical assistant right now. Please describe your symptoms again.", "bot");
        })
        .finally(() => {
            isSending = false;
        });
    }

    // ─── EVENT LISTENERS ────────────────────────────────────────────────────

    mcLauncher.addEventListener("click", () => {
        mcWindow.classList.toggle("active");
        mcHint.classList.add("hide");
        if (mcWindow.classList.contains("active")) {
            mcBody.scrollTop = mcBody.scrollHeight;
        }
    });

    mcClose.addEventListener("click", () => {
        mcWindow.classList.remove("active");
    });

    mcNewChatBtn.addEventListener("click", (e) => {
        e.preventDefault();
        fetch("/chatbot/new-chat/")
            .then(res => res.json())
            .then(() => {
                const messages = mcBody.querySelectorAll(".mc-message");
                messages.forEach(m => m.remove());
                lastDepartment = "";
                addMessage("Hello 👋 Welcome to MediClinic.<br>How can I help you today?", "bot");
            });
    });

    mcSend.addEventListener("click", () => {
        sendMessage(mcInput.value);
    });

    mcInput.addEventListener("keydown", (e) => {
        if (e.key === "Enter") sendMessage(mcInput.value);
    });

    mcActions.forEach((btn) => {
        btn.addEventListener("click", () => {
            if (btn.id === "mcResetAction") {
                fetch("/chatbot/new-chat/")
                    .then(res => res.json())
                    .then(() => {
                        const messages = mcBody.querySelectorAll(".mc-message");
                        messages.forEach(m => m.remove());
                        lastDepartment = "";
                        addMessage("Hello 👋 Welcome to MediClinic.<br>How can I help you today?", "bot");
                    });
                return;
            }
            sendMessage(btn.dataset.message);
        });
    });

    loadHistory();
    setTimeout(() => { if(mcHint) mcHint.classList.add("hide"); }, 7000);
}
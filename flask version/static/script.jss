
// Ask AI
function askAI() {
    let input = document.getElementById("question");
    let question = input.value.trim();
    let responseBox = document.getElementById("response");

    if (!question) return;

    responseBox.innerText = "Thinking...";

    fetch("/ask", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ question: question })
    })
    .then(res => res.json())
    .then(data => {

        let answer = data.answer || "No response";

        // Show response
        responseBox.innerHTML = marked.parse(answer);

        // SAVE HISTORY
        let history = JSON.parse(localStorage.getItem("history")) || [];
        history.push({ question, answer });
        localStorage.setItem("history", JSON.stringify(history));

    })
    .catch(() => {
        responseBox.innerText = "⚠️ Error occurred.";
    });
}

// Enter key
document.getElementById("question").addEventListener("keydown", function(e) {
    if (e.key === "Enter") {
        e.preventDefault();
        askAI();
    }
});

// NAVIGATION
const dashboard = document.getElementById("dashboard-section");
const historySection = document.getElementById("history-section");

document.querySelectorAll(".sidebar li").forEach(item => {
    item.addEventListener("click", () => {

        let text = item.innerText;

        if (text === "Dashboard") {
            dashboard.style.display = "block";
            historySection.style.display = "none";
        }

        if (text === "History") {
            dashboard.style.display = "none";
            historySection.style.display = "block";
            loadHistory();
        }
    });
});
const tutorialSection = document.getElementById("tutorial-section");
const settingsSection = document.getElementById("settings-section");

document.querySelectorAll(".sidebar li").forEach(item => {
    item.addEventListener("click", () => {

        let text = item.innerText;

        // hide all
        dashboard.style.display = "none";
        historySection.style.display = "none";
        tutorialSection.style.display = "none";
        settingsSection.style.display = "none";

        if (text === "Dashboard") dashboard.style.display = "block";
        if (text === "History") {
            historySection.style.display = "block";
            loadHistory();
        }
        if (text === "Tutorials") tutorialSection.style.display = "block";
        if (text === "Settings") settingsSection.style.display = "block";
    });
});
// LOAD HISTORY
function loadHistory() {
    let list = document.getElementById("history-list");
    list.innerHTML = "";

    let history = JSON.parse(localStorage.getItem("history")) || [];

    history.forEach(item => {
        let li = document.createElement("li");
        li.innerText = item.question;

        // click to show answer
        li.addEventListener("click", () => {
            document.getElementById("response").innerHTML = marked.parse(item.answer);
            dashboard.style.display = "block";
            historySection.style.display = "none";
        });

        list.appendChild(li);
    });
}
function loadTutorial(topic) {
    document.getElementById("question").value = topic;
    document.getElementById("dashboard-section").style.display = "block";
    document.getElementById("tutorial-section").style.display = "none";
}
if (text === "Playground") {
    alert("Playground mode: Ask anything!");
}
function clearHistory() {
    localStorage.removeItem("history");
    alert("History cleared!");
}

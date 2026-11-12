const startBtn = document.getElementById("startBtn");
const promptInput = document.getElementById("promptInput");
const errorBox = document.getElementById("errorBox");
const resultCard = document.getElementById("resultCard");
const evalIdDisplay = document.getElementById("evalIdDisplay");
const statusBadge = document.getElementById("statusBadge");
const metricsContainer = document.getElementById("metricsContainer");

let pollTimer = null;

function showError(message) {
    errorBox.textContent = message;
    errorBox.classList.remove("hidden");
}

function clearError() {
    errorBox.textContent = "";
    errorBox.classList.add("hidden");
}

function updateStatusUI(status) {
    statusBadge.textContent = status;
    statusBadge.className = "status-badge status-" + status;
}

function renderMetrics(metrics) {
    metricsContainer.innerHTML = "";
    for (const [key, value] of Object.entries(metrics)) {
        const box = document.createElement("div");
        box.className = "metric-box";
        box.innerHTML = `<div>${key}</div><div class="metric-value">${value}</div>`;
        metricsContainer.appendChild(box);
    }
    metricsContainer.classList.remove("hidden");
}

async function pollStatus(evalId) {
    try {
        const response = await fetch(`/api/status/${evalId}`);
        const data = await response.json();

        if (!response.ok) {
            clearInterval(pollTimer);
            startBtn.disabled = false;
            showError(data.error || "Fehler beim Abrufen des Status.");
            return;
        }

        updateStatusUI(data.status);

        if (data.status === "done") {
            clearInterval(pollTimer);
            startBtn.disabled = false;
            if (data.metrics) {
                renderMetrics(data.metrics);
            }
        }
    } catch (err) {
        clearInterval(pollTimer);
        startBtn.disabled = false;
        showError("Verbindungsfehler zum Server.");
    }
}

startBtn.addEventListener("click", async () => {
    clearError();
    if (pollTimer) {
        clearInterval(pollTimer);
    }

    const promptText = promptInput.value;
    startBtn.disabled = true;
    metricsContainer.classList.add("hidden");

    try {
        const response = await fetch("/api/evaluate", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ prompt: promptText })
        });
        const data = await response.json();

        if (!response.ok) {
            startBtn.disabled = false;
            showError(data.error || "Ungültige Eingabe.");
            return;
        }

        evalIdDisplay.textContent = data.id;
        updateStatusUI(data.status);
        resultCard.classList.remove("hidden");

        pollTimer = setInterval(() => pollStatus(data.id), 1500);
    } catch (err) {
        startBtn.disabled = false;
        showError("Server nicht erreichbar.");
    }
});

async function sendCommand(url, data = {}) {
    await fetch(url, {
        method: "POST",
        headers: {
            "Content-Type": "application/x-www-form-urlencoded"
        },
        body: new URLSearchParams(data)
    });
    updateDashboard();
}

async function updateDashboard() {
    const res = await fetch("/api/status");
    const data = await res.json();

    document.getElementById("battery").innerText = data.battery + "%";
    document.getElementById("status").innerText = data.status;
    document.getElementById("point").innerText = data.current_point;
    document.getElementById("speed").innerText = data.speed;

    const logBox = document.getElementById("logs");
    if (data.logs) {
        logBox.innerHTML = data.logs.map(l => `<div>${l}</div>`).join("");
        logBox.scrollTop = logBox.scrollHeight;
    }
}

/* BUTTON ACTIONS */
function startMission() {
    sendCommand("/start");
}

function stopMission() {
    sendCommand("/stop");
}

function resetRobot() {
    sendCommand("/reset");
}

function setPoint() {
    const point = document.getElementById("point_select").value;
    sendCommand("/set_point", { point_id: point });
}

function connectRobot() {
    const ip = document.getElementById("robot_ip").value;
    sendCommand("/connect", { ip: ip });
}

/* AUTO REFRESH */
setInterval(updateDashboard, 2000);

window.onload = updateDashboard;
let alertAudio;

export function initAlerts() {
    alertAudio = new Audio('https://assets.mixkit.co/sfx/preview/mixkit-alarm-digital-clock-beep-989.mp3');
}

export function showAlert(data) {
    
    const modal = document.getElementById('alertModal');
    if (!modal) {
        console.error("❌ Modal element not found!");
        return;
    }

    const details = document.getElementById('alertDetails');
    if (!details) {
        return;
    }

    details.innerHTML = `
        <p><strong>🚨 Spoof Detected!</strong></p>
        <p>Location: ${data.latitude.toFixed(6)}, ${data.longitude.toFixed(6)}</p>
        <p>Signal: ${data.signal_strength} </p>
    `;

    console.log("Setting modal to visible...");
    modal.style.display = 'block';
    
    // Debug z-index issues
    console.log("Current modal z-index:", window.getComputedStyle(modal).zIndex);
    modal.style.zIndex = '10000';
    
    // Test audio separately
    console.log("Playing alert sound...");
    new Audio('https://assets.mixkit.co/sfx/preview/mixkit-alarm-digital-clock-beep-989.mp3')
        .play()
        .then(() => console.log("Audio played successfully"))
        .catch(e => console.error("Audio error:", e));

    setTimeout(() => {
        console.log("Hiding modal after timeout");
        modal.style.display = 'none';
    }, 5000);
}
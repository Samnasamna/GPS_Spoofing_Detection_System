import { initMap, updateMap } from './map.js';
import { initChart, updateChart } from './graph.js';
import { showAlert } from './alert.js';
let eventSource;
let chart;
let map;

document.addEventListener('DOMContentLoaded', () => {
    // Initialize components
    map = initMap();
    chart = initChart();
    setupEventStream();
    setupControls();
});
function setupEventStream() {
    eventSource = new EventSource('/stream');
    
    eventSource.onmessage = (event) => {
        const data = JSON.parse(event.data);
        
        updateDisplay(data);
        
        if (data.is_spoofed){
            showAlert(data);
        }
    };

    eventSource.onerror = (err) => {
        console.error("EventSource error:", err);
    };
}

function setupControls() {
    document.getElementById('forceJump').addEventListener('click', () => {
        fetch('/simulate-jump');
    });
}

function updateDisplay(data) {
    // Update map
    updateMap(data);
    
    // Update chart
    updateChart(data);
    
    // Update log
    updateLog(data);
    
    // Update signal indicator
    updateSignalStatus(data.signal_strength);
}

function updateSignalStatus(strength) {
    const indicator = document.getElementById('signalStatus');
    if (strength > 60) {
        indicator.style.backgroundColor = '#4CAF50';
    } else if (strength > 30) {
        indicator.style.backgroundColor = '#FFC107';
    } else {
        indicator.style.backgroundColor = '#F44336';
    }
}

function updateLog(data) {
    const tbody = document.getElementById('logBody');
    const row = document.createElement('tr');
    
    if (data.is_spoofed) row.classList.add('spoofed');
    
    row.innerHTML = `
        <td>${new Date(data.timestamp).toLocaleTimeString()}</td>
        <td>${data.latitude.toFixed(6)}</td>
        <td>${data.longitude.toFixed(6)}</td>
        <td>${data.is_spoofed ? '⚠️ Spoofed' : 'Normal'}</td>
    `;
    
    tbody.insertBefore(row, tbody.firstChild);
    if (tbody.children.length > 50) tbody.removeChild(tbody.lastChild);
}



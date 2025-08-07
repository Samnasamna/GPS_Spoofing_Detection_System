let signalChart;

export function initChart() {
    const ctx = document.getElementById('signalChart').getContext('2d');
    signalChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: [],
            datasets: [{
                label: 'Signal Strength',
                data: [],
                borderColor: '#2196F3',
                tension: 0.1,
                pointBackgroundColor: [],
                pointRadius: 3
            }]
        },
        options: {
            animation: false,
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                x: {
                    type: 'time', // Change 'realtime' to 'time' scale
                    time: {
                        unit: 'second',
                        tooltipFormat: 'll HH:mm',
                    }
                },
                y: {
                    min: 0,
                    max: 100
                }
            }
        }
    });
}

export function updateChart(data) {
    const now = new Date(data.timestamp);

    // Maintain only last 60 seconds of data
    if (signalChart.data.labels.length > 30) {
        signalChart.data.labels.shift();
        signalChart.data.datasets[0].data.shift();
        signalChart.data.datasets[0].pointBackgroundColor.shift();
    }

    signalChart.data.labels.push(now);
    signalChart.data.datasets[0].data.push(data.signal_strength);
    signalChart.data.datasets[0].pointBackgroundColor.push(
        data.is_spoofed ? '#FF5252' : '#2196F3'
    );

    signalChart.update('none');
}

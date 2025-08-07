let map;
let marker;
let polyline;
let heatmapLayer = null;
let gpsHistory = [];

export function initMap() {
    map = L.map('map').setView([37.7749, -122.4194], 13);
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '© OpenStreetMap'
    }).addTo(map);

    // Custom marker with pulsing effect
    marker = L.marker([37.7749, -122.4194], {
        icon: L.divIcon({
            className: 'pulsing-marker',
            html: `<div class="marker-pulse"></div>
                   <img src="https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-icon.png">`,
            iconSize: [25, 41]
        })
    }).addTo(map);

    polyline = L.polyline([], {
        color: '#2196F3',
        weight: 3,
        lineJoin: 'round'
    }).addTo(map);
}

export function updateMap(data) {
    const newPos = [data.latitude, data.longitude];
    gpsHistory.push(data);
    
    // Update marker with smooth transition
    marker.setLatLng(newPos, {
        smoothMovement: true,
        duration: 1.5
    });

    // Update path (limit to last 100 points for performance)
    const recentPoints = gpsHistory.slice(-100).map(p => [p.latitude, p.longitude]);
    polyline.setLatLngs(recentPoints);

    // Auto-zoom and highlight jumps
    if (data.is_spoofed) {
        // Flash red for spoofed points
        marker.getElement().classList.add('spoofed-marker');
        setTimeout(() => {
            marker.getElement().classList.remove('spoofed-marker');
        }, 1000);
        
        // Zoom to show both last position and jump
        const lastPos = gpsHistory.length > 1 ? 
            [gpsHistory[gpsHistory.length-2].latitude, 
             gpsHistory[gpsHistory.length-2].longitude] : newPos;
        
        map.flyToBounds([lastPos, newPos], {
            padding: [50, 50],
            duration: 1
        });
    }
}

export function toggleHeatmap() {
    if (heatmapLayer) {
        map.removeLayer(heatmapLayer);
        heatmapLayer = null;
    } else {
        const heatData = gpsHistory
            .filter(entry => entry.is_spoofed)
            .map(entry => [entry.latitude, entry.longitude, 1]);
        
        heatmapLayer = L.heatLayer(heatData, {
            radius: 25,
            blur: 15,
            maxZoom: 17,
            gradient: {0.1: 'blue', 0.5: 'lime', 1: 'red'}
        }).addTo(map);
    }
}
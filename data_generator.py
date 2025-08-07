import pandas as pd
import numpy as np
import random
import time
from datetime import datetime

def generate_live_gps_stream(interval=2, base_lat=37.7749, base_lng=-122.4194):
    """Generate continuous GPS data with forced alert after 20 seconds"""
    start_time = time.time()
    alert_triggered = False
    
    while True:
        current_time = time.time()
        elapsed = current_time - start_time
        
        # Force a spoof after 20 seconds if not already triggered
        if elapsed >= 20 and not alert_triggered:
            is_spoofed = True
            alert_triggered = True
            print("⚠️ FORCING SPOOF ALERT AFTER 20 SECONDS ⚠️")
        else:
            # 10% chance of random spoofing (original behavior)
            is_spoofed = random.random() < 0.1
        
        if is_spoofed:
            # Spoofed jump (100m-1km)
            lat = base_lat + random.uniform(0.001, 0.01)
            lng = base_lng + random.uniform(0.001, 0.01)
            signal = random.randint(10, 30)
            print(f"🚨 Generated spoofed data at {elapsed:.1f}s - Lat: {lat:.6f}, Lng: {lng:.6f}")
        else:
            # Normal movement (random walk)
            lat = base_lat + np.random.normal(0, 0.0001)
            lng = base_lng + np.random.normal(0, 0.0001)
            signal = random.randint(40, 70)

        yield {
            'timestamp': datetime.now().isoformat(),
            'latitude': lat,
            'longitude': lng,
            'signal_strength': signal,
            'is_spoofed': int(is_spoofed),
            'lat_change': 0,  # Will be calculated later
            'lng_change': 0,
            'speed': 0,
            'elapsed_seconds': elapsed  # Added for debugging
        }
        time.sleep(interval)
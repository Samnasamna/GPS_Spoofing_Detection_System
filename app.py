from flask import Flask, render_template, Response, jsonify
import json
import time
import random
import numpy as np
from datetime import datetime
import joblib
import smtplib
from email.mime.text import MIMEText
from data_generator import generate_live_gps_stream

app = Flask(__name__)

# Load ML model
model = joblib.load('models/spoof_model.pkl')

# In-memory storage
gps_log = []
alerts = []

# Email config
EMAIL_CONFIG = {
    'sender': 'your_email@example.com',
    'password': 'your_password',
    'receiver': 'admin@example.com',
    'smtp_server': 'smtp.example.com',
    'smtp_port': 587
}

def generate_live_data():
    """Generate continuous GPS data stream"""
    base_lat, base_lng = 37.7749, -122.4194
    while True:
        # 95% chance of normal movement
        if random.random() < 0.95:
            lat = base_lat + np.random.normal(0, 0.00001)
            lng = base_lng + np.random.normal(0, 0.00001)
            signal = random.randint(40, 70)
            is_spoofed = 0
        else:  # 5% chance of spoofed jump
            lat = base_lat + random.uniform(0.001, 0.01)
            lng = base_lng + random.uniform(0.001, 0.01)
            signal = random.randint(10, 30)
            is_spoofed = 1

        data = {
            'timestamp': datetime.now().isoformat(),
            'latitude': lat,
            'longitude': lng,
            'signal_strength': signal,
            'is_spoofed': is_spoofed
        }

        # Calculate movement features
        if gps_log:
            last = gps_log[-1]
            data.update({
                'lat_change': abs(lat - last['latitude']),
                'lng_change': abs(lng - last['longitude']),
                'signal_change': abs(signal - last['signal_strength']),
                'speed': np.sqrt((lat - last['latitude'])**2 + (lng - last['longitude'])**2) * 1e5 / 2  # m/s
            })
        else:
            data.update({'lat_change': 0, 'lng_change': 0, 'signal_change': 0, 'speed': 0})

        # Predict spoofing
        features = np.array([data['lat_change'], data['lng_change'], 
                             data['signal_change'], data['speed']]).reshape(1, -1)
        data['spoof_prob'] = model.predict_proba(features)[0][1]
        data['is_spoofed'] = int(data['spoof_prob'] > 0.9)

        yield data
        time.sleep(2)  # 2-second updates

@app.route('/stream')
def stream():
    def event_stream():
        generator = generate_live_gps_stream()
        while True:
            data = next(generator)
            
            # Calculate movement features if previous data exists
            if gps_log:
                last = gps_log[-1]
                data.update({
                    'lat_change': abs(data['latitude'] - last['latitude']),
                    'lng_change': abs(data['longitude'] - last['longitude']),
                    'speed': np.sqrt((data['latitude'] - last['latitude'])**2 + 
                                   (data['longitude'] - last['longitude'])**2) * 1e5 / 2
                })
            
            gps_log.append(data)
            yield f"data: {json.dumps(data)}\n\n"
    
    return Response(event_stream(), mimetype="text/event-stream")

def trigger_alert(data):
    alerts.append(data)
    # Send email
    msg = MIMEText(f"Spoof detected!\nTime: {data['timestamp']}\nLocation: {data['latitude']:.6f}, {data['longitude']:.6f}")
    msg['Subject'] = 'GPS Spoof Alert'
    msg['From'] = EMAIL_CONFIG['sender']
    msg['To'] = EMAIL_CONFIG['receiver']
    
    try:
        with smtplib.SMTP(EMAIL_CONFIG['smtp_server'], EMAIL_CONFIG['smtp_port']) as server:
            server.starttls()
            server.login(EMAIL_CONFIG['sender'], EMAIL_CONFIG['password'])
            server.send_message(msg)
    except Exception as e:
        print(f"Email error: {e}")

@app.route('/simulate-jump')
def simulate_jump():
    # Force a spoofed jump
    last = gps_log[-1] if gps_log else {'latitude': 37.7749, 'longitude': -122.4194}
    jump_data = {
        'latitude': last['latitude'] + random.uniform(0.01, 0.1),
        'longitude': last['longitude'] + random.uniform(0.01, 0.1),
        'signal_strength': random.randint(10, 30),
        'is_spoofed': 1,
        'timestamp': datetime.now().isoformat()
    }
    gps_log.append(jump_data)
    return jsonify(jump_data)

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True, threaded=True)

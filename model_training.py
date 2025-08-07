import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import joblib
from sklearn.metrics import classification_report

def train_and_save_model():
    # Load simulated data
    df = pd.read_csv(r'D:\User\gps_spoofing_detection_system\data\simulated_gps.csv')
    
    # Feature engineering
    df['distance'] = np.sqrt(df['lat_change']**2 + df['lng_change']**2)
    df['speed'] = df['distance'] * 1e5 / 2  # Convert to m/s
    
    # Select features
    features = ['lat_change', 'lng_change', 'signal_strength', 'speed']
    X = df[features]
    y = df['is_spoofed']
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, stratify=y)
    
    # Train model
    model = RandomForestClassifier(
        n_estimators=150,
        max_depth=8,
        class_weight='balanced',
        random_state=42
    )
    model.fit(X_train, y_train)
    
    # Evaluate
    y_pred = model.predict(X_test)
    print(classification_report(y_test, y_pred))
    
    # Save model
    joblib.dump(model, r'D:\User\gps_spoofing_detection_system\models\spoof_model.pkl')
    print("Model saved successfully")

if __name__ == "__main__":
    train_and_save_model()
import numpy as np
import pandas as pd
from sklearn.ensemble import GradientBoostingClassifier
import joblib

class FederatedLearningSystem:
    def __init__(self, num_clients=3):
        self.clients = [GradientBoostingClassifier() for _ in range(num_clients)]
        self.global_model = None  # Will be set after training
        self.data = pd.read_csv(r'D:\User\gps_spoofing_detection_system\data\simulated_gps.csv')

    def train_round(self):
        # Split data into non-overlapping chunks
        client_data = np.array_split(self.data, len(self.clients))

        # Client-side training
        for i, client in enumerate(self.clients):
            print(f"Training client {i+1}")
            X = client_data[i][['lat_change', 'lng_change', 'signal_strength', 'speed']]
            y = client_data[i]['is_spoofed']
            
            # Drop rows with missing values
            mask = X.notna().all(axis=1) & y.notna()
            X = X[mask]
            y = y[mask]

            client.fit(X, y)

        # Aggregate knowledge (simple strategy)
        self._aggregate_models()

    def _aggregate_models(self):
        # Pick the first trained client as the global model
        self.global_model = self.clients[0]
        joblib.dump(self.global_model, r'D:\User\gps_spoofing_detection_system\models\federated_model.pkl')
        print("Federated model saved (from client 1)")

if __name__ == "__main__":
    fl = FederatedLearningSystem()
    fl.train_round()

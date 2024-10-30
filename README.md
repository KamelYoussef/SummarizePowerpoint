import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta

# Configuration
num_records = 5000
anomaly_fraction = 0.05  # 5% of the data will be anomalies

# Initialize data lists
timestamps = []
temperatures = []
pressures = []
vibrations = []
rpms = []
humidities = []
power_consumptions = []
sound_levels = []
oil_levels = []
load_weights = []
labels = []  # 0 for normal, 1 for anomaly

# Generate data
start_time = datetime.now()
for i in range(num_records):
    # Generate timestamp
    timestamps.append(start_time + timedelta(minutes=i))
    
    # Base Components (C1, C2, C3)
    C1 = np.random.normal(60, 5)  # Power-related component
    C2 = np.random.normal(50, 5)  # Load and Vibration component
    C3 = np.random.normal(40, 5)  # Environmental component
    
    # Derived features based on components
    power_consumption = C1 * 10 + np.random.normal(0, 5)  # Power as main driver for C1
    temperature = C1 + np.random.normal(0, 1)  # Temperature influenced by power
    pressure = C1 * 0.05 + np.random.normal(2, 0.1)  # Pressure lightly tied to power

    load_weight = C2 + np.random.normal(0, 1)  # Load weight driven by C2
    vibration = C2 * 0.03 + np.random.normal(0.5, 0.1)  # Vibration depends on load weight
    sound_level = vibration * 20 + np.random.normal(60, 3)  # Sound level amplified by vibration

    oil_level = max(0, 100 - C3 + np.random.normal(0, 3))  # Oil levels inversely tied to C3
    humidity = C3 + np.random.normal(5, 2)  # Humidity affected by environment
    rpm = C2 * 24 + np.random.normal(1200, 30)  # RPM reacts to load conditions (C2)

    label = 0  # Normal condition by default

    # Introduce anomalies
    if random.random() < anomaly_fraction:
        label = 1  # Anomaly
        anomaly_type = random.choice(['temperature', 'pressure', 'vibration', 'rpm', 'humidity', 'power', 'sound', 'oil', 'load'])
        if anomaly_type == 'temperature':
            temperature = np.random.normal(100, 10)  # Overheat
        elif anomaly_type == 'pressure':
            pressure = np.random.choice([np.random.normal(5, 0.5), np.random.normal(0.5, 0.2)])  # Leak or blockage
        elif anomaly_type == 'vibration':
            vibration = np.random.normal(3, 0.5)  # Mechanical fault
        elif anomaly_type == 'rpm':
            rpm = np.random.normal(2000, 100)  # Speed fluctuation
        elif anomaly_type == 'humidity':
            humidity = np.random.normal(80, 5)  # Humidity spike
        elif anomaly_type == 'power':
            power_consumption = np.random.choice([np.random.normal(700, 50), np.random.normal(300, 20)])  # Power surge or drop
        elif anomaly_type == 'sound':
            sound_level = np.random.normal(95, 5)  # Loud noise
        elif anomaly_type == 'oil':
            oil_level = np.random.normal(30, 5)  # Low oil level
        elif anomaly_type == 'load':
            load_weight = np.random.normal(200, 20)  # High load

    # Append data
    temperatures.append(temperature)
    pressures.append(pressure)
    vibrations.append(vibration)
    rpms.append(rpm)
    humidities.append(humidity)
    power_consumptions.append(power_consumption)
    sound_levels.append(sound_level)
    oil_levels.append(oil_level)
    load_weights.append(load_weight)
    labels.append(label)

# Create DataFrame
data = pd.DataFrame({
    'Timestamp': timestamps,
    'Temperature': temperatures,
    'Pressure': pressures,
    'Vibration': vibrations,
    'RPM': rpms,
    'Humidity': humidities,
    'PowerConsumption': power_consumptions,
    'SoundLevel': sound_levels,
    'OilLevel': oil_levels,
    'LoadWeight': load_weights,
    'Anomaly': labels
})

# Save to CSV
data.to_csv('/mnt/data/sensor_data_anomaly_pca_correlated.csv', index=False)
print("PCA-correlated dataset created and saved as 'sensor_data_anomaly_pca_correlated.csv'")

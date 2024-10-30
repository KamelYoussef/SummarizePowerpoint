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
labels = []  # 0 for normal, 1 for anomaly

# Generate data
start_time = datetime.now()
for i in range(num_records):
    # Generate timestamp
    timestamps.append(start_time + timedelta(minutes=i))
    
    # Normal data
    temperature = np.random.normal(60, 5)
    pressure = np.random.normal(2, 0.3)
    vibration = np.random.normal(0.8, 0.2)
    rpm = np.random.normal(1200, 50)
    label = 0  # Normal
    
    # Introduce anomalies
    if random.random() < anomaly_fraction:
        label = 1  # Anomaly
        anomaly_type = random.choice(['temperature', 'pressure', 'vibration', 'rpm'])
        if anomaly_type == 'temperature':
            temperature = np.random.normal(100, 10)  # Overheat
        elif anomaly_type == 'pressure':
            pressure = np.random.choice([np.random.normal(5, 0.5), np.random.normal(0.5, 0.2)])  # Leak or blockage
        elif anomaly_type == 'vibration':
            vibration = np.random.normal(3, 0.5)  # Mechanical fault
        elif anomaly_type == 'rpm':
            rpm = np.random.normal(2000, 100)  # Speed fluctuation
    
    # Append data
    temperatures.append(temperature)
    pressures.append(pressure)
    vibrations.append(vibration)
    rpms.append(rpm)
    labels.append(label)

# Create DataFrame
data = pd.DataFrame({
    'Timestamp': timestamps,
    'Temperature': temperatures,
    'Pressure': pressures,
    'Vibration': vibrations,
    'RPM': rpms,
    'Anomaly': labels
})

# Save to CSV
data.to_csv('/mnt/data/sensor_data_anomaly.csv', index=False)
print("Dataset created and saved as 'sensor_data_anomaly.csv'")

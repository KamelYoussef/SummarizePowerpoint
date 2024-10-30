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
    
    # Base values for normal data
    temperature = np.random.normal(60, 5)
    pressure = np.random.normal(2, 0.3)
    vibration = np.random.normal(0.8, 0.2)
    rpm = np.random.normal(1200, 50)
    humidity = np.random.normal(45, 5)
    power_consumption = np.random.normal(500, 30)
    sound_level = np.random.normal(70, 5)
    oil_level = np.random.normal(80, 10)
    load_weight = np.random.normal(100, 15)
    label = 0  # Normal

    # Apply correlations
    # Correlation 1: Power Consumption -> Temperature
    temperature += (power_consumption - 500) * 0.02  # Small increase in temperature with power

    # Correlation 2: Load Weight -> Vibration
    vibration += (load_weight - 100) * 0.005  # Heavier load, more vibration

    # Correlation 3: Vibration -> Sound Level
    sound_level += vibration * 10  # Directly correlate sound level with vibration

    # Correlation 4: Temperature -> Pressure
    pressure += (temperature - 60) * 0.05  # Increase in temperature raises pressure

    # Correlation 5: Oil Level -> Temperature and Vibration (lower oil, higher values)
    if oil_level < 60:
        temperature += (80 - oil_level) * 0.1  # Low oil level causes temperature rise
        vibration += (80 - oil_level) * 0.02   # Low oil level causes vibration increase

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
data.to_csv('/mnt/data/sensor_data_anomaly_correlated.csv', index=False)
print("Correlated dataset created and saved as 'sensor_data_anomaly_correlated.csv'")

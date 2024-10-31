import pandas as pd
import numpy as np

# Set random seed for reproducibility
np.random.seed(42)

# Define the number of rows
num_rows = 500

# Generate realistic data ranges with correlations
surface = np.random.normal(loc=100, scale=30, size=num_rows).astype(int)  # Average 100 m², realistic urban variation
surface = np.clip(surface, 50, 300)  # Clamp to range between 50 and 300 m²

nombre_de_pieces = np.clip((surface // 20) + np.random.randint(-1, 2, size=num_rows), 2, 10)  # Approximate rooms by size

age = np.random.randint(0, 70, size=num_rows)  # Ages up to 70 years, typical for urban areas

# Calculate 'prix' based on a formula with added noise
# We assume average price per m² is 2500 CAD in Montreal with a discount based on age
prix = (
    surface * 2500 +               # Base price proportional to surface
    nombre_de_pieces * 15000 -     # Extra cost per room
    age * 2000 +                   # Depreciation factor based on age
    np.random.normal(0, 15000, size=num_rows)  # Random noise for variance
).astype(int)

# Construct the DataFrame
data = {
    'surface': surface,
    'nombre_de_pieces': nombre_de_pieces,
    'age': age,
    'prix': prix
}

df = pd.DataFrame(data)

# Display the first few rows to check
print(df.head())

# Save to CSV
df.to_csv('montreal_house_data_500_rows.csv', index=False)

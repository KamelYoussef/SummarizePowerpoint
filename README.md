import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the dataset
data = pd.read_csv('/mnt/data/winequality(1).csv', sep=';')

# Display the first few rows of the dataset
print("First few rows of the dataset:")
print(data.head())

# Summary statistics
print("\nSummary statistics:")
print(data.describe())

# Check for missing values
print("\nMissing values in each column:")
print(data.isnull().sum())

# Visualizations
plt.figure(figsize=(10, 6))
plt.title("Distribution of Quality")
sns.countplot(x='quality', data=data, palette='viridis')
plt.xlabel("Wine Quality")
plt.ylabel("Count")
plt.show()

# Pairplot of numerical features
plt.figure(figsize=(15, 10))
sns.pairplot(data, hue='quality', palette='viridis')
plt.show()

# Correlation heatmap
plt.figure(figsize=(12, 8))
plt.title("Correlation Heatmap")
sns.heatmap(data.corr(), annot=True, cmap='coolwarm', fmt='.2f')
plt.show()

# Boxplot of quality vs. alcohol
plt.figure(figsize=(10, 6))
plt.title("Boxplot of Quality vs Alcohol")
sns.boxplot(x='quality', y='alcohol', data=data, palette='viridis')
plt.xlabel("Wine Quality")
plt.ylabel("Alcohol")
plt.show()

# Analysis of volatile acidity vs. quality
plt.figure(figsize=(10, 6))
plt.title("Volatile Acidity vs Quality")
sns.boxplot(x='quality', y='volatile acidity', data=data, palette='viridis')
plt.xlabel("Wine Quality")
plt.ylabel("Volatile Acidity")
plt.show()

# Analysis of residual sugar vs. quality
plt.figure(figsize=(10, 6))
plt.title("Residual Sugar vs Quality")
sns.boxplot(x='quality', y='residual sugar', data=data, palette='viridis')
plt.xlabel("Wine Quality")
plt.ylabel("Residual Sugar")
plt.show()

# Alcohol content distribution
plt.figure(figsize=(10, 6))
plt.title("Alcohol Content Distribution")
sns.histplot(data['alcohol'], kde=True, color='blue')
plt.xlabel("Alcohol")
plt.ylabel("Frequency")
plt.show()

# Fixed acidity distribution
plt.figure(figsize=(10, 6))
plt.title("Fixed Acidity Distribution")
sns.histplot(data['fixed acidity'], kde=True, color='green')
plt.xlabel("Fixed Acidity")
plt.ylabel("Frequency")
plt.show()

# Quality comparison with citric acid
plt.figure(figsize=(10, 6))
plt.title("Quality vs Citric Acid")
sns.boxplot(x='quality', y='citric acid', data=data, palette='viridis')
plt.xlabel("Wine Quality")
plt.ylabel("Citric Acid")
plt.show()

# Quality comparison with chlorides
plt.figure(figsize=(10, 6))
plt.title("Quality vs Chlorides")
sns.boxplot(x='quality', y='chlorides', data=data, palette='viridis')
plt.xlabel("Wine Quality")
plt.ylabel("Chlorides")
plt.show()

# Analyzing pH distribution by quality
plt.figure(figsize=(10, 6))
plt.title("pH vs Quality")
sns.boxplot(x='quality', y='pH', data=data, palette='viridis')
plt.xlabel("Wine Quality")
plt.ylabel("pH")
plt.show()

# Sulphates comparison with quality
plt.figure(figsize=(10, 6))
plt.title("Sulphates vs Quality")
sns.boxplot(x='quality', y='sulphates', data=data, palette='viridis')
plt.xlabel("Wine Quality")
plt.ylabel("Sulphates")
plt.show()

# Density vs alcohol scatterplot
plt.figure(figsize=(10, 6))
plt.title("Density vs Alcohol")
sns.scatterplot(x='density', y='alcohol', hue='quality', data=data, palette='viridis')
plt.xlabel("Density")
plt.ylabel("Alcohol")
plt.show()

# Free sulfur dioxide vs total sulfur dioxide scatterplot
plt.figure(figsize=(10, 6))
plt.title("Free Sulfur Dioxide vs Total Sulfur Dioxide")
sns.scatterplot(x='free sulfur dioxide', y='total sulfur dioxide', hue='quality', data=data, palette='viridis')
plt.xlabel("Free Sulfur Dioxide")
plt.ylabel("Total Sulfur Dioxide")
plt.show()

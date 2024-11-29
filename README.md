import pandas as pd
from sklearn.model_selection import train_test_split

def load_data(file_path):
    """Load data from a file."""
    return pd.read_csv(file_path)

def preprocess_data(df):
    """Clean and preprocess the data."""
    # Example: Fill missing values
    df.fillna(0, inplace=True)
    return df

def split_data(df, target_column, test_size=0.2, random_state=42):
    """Split data into train and test sets."""
    X = df.drop(columns=[target_column])
    y = df[target_column]
    return train_test_split(X, y, test_size=test_size, random_state=random_state)

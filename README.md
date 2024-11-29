import mlflow
import mlflow.sklearn
from sklearn.ensemble import RandomForestClassifier
from src.data import load_data, preprocess_data, split_data

def train_model(data_path, target_column):
    """Train a machine learning model."""
    # Load and preprocess data
    data = load_data(data_path)
    data = preprocess_data(data)
    X_train, X_test, y_train, y_test = split_data(data, target_column)
    
    # Initialize and train model
    model = RandomForestClassifier()
    model.fit(X_train, y_train)
    
    # Evaluate and log to MLflow
    accuracy = model.score(X_test, y_test)
    mlflow.log_metric("accuracy", accuracy)
    mlflow.sklearn.log_model(model, "model")
    
    print(f"Model trained with accuracy: {accuracy:.2f}")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Train a model.")
    parser.add_argument("--data-path", type=str, required=True, help="Path to the data file")
    parser.add_argument("--target-column", type=str, required=True, help="Target column name")
    args = parser.parse_args()
    
    with mlflow.start_run():
        train_model(args.data_path, args.target_column)

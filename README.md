import mlflow
import mlflow.sklearn
from sklearn.metrics import classification_report
from src.data import load_data, preprocess_data, split_data

def evaluate_model(model_path, data_path, target_column):
    """Evaluate the model."""
    # Load and preprocess data
    data = load_data(data_path)
    data = preprocess_data(data)
    _, X_test, _, y_test = split_data(data, target_column)
    
    # Load model
    model = mlflow.sklearn.load_model(model_path)
    
    # Evaluate
    predictions = model.predict(X_test)
    report = classification_report(y_test, predictions)
    print(report)

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Evaluate a model.")
    parser.add_argument("--model-path", type=str, required=True, help="Path to the MLflow model")
    parser.add_argument("--data-path", type=str, required=True, help="Path to the data file")
    parser.add_argument("--target-column", type=str, required=True, help="Target column name")
    args = parser.parse_args()
    
    evaluate_model(args.model_path, args.data_path, args.target_column)

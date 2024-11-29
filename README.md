import mlflow
from src.data import get_processed_data, split_data
from src.train import train_and_log_model
from src.evaluate import evaluate_model

def run_pipeline(data_path, target_column, processed_data_path):
    """Run the full ML pipeline."""
    # Step 1: Load or preprocess data
    mlflow.log_param("data_path", data_path)
    data = get_processed_data(data_path, processed_data_path)

    # Step 2: Split data
    X_train, X_test, y_train, y_test = split_data(data, target_column)
    mlflow.log_param("target_column", target_column)

    # Step 3: Train and log model
    model_uri = train_and_log_model(X_train, y_train, X_test, y_test)

    # Step 4: Evaluate the model
    evaluate_model(model_uri, X_test, y_test)

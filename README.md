import mlflow

# Define the model path where your GGUF model is stored
model_path = "./path_to_your_model_directory"

# Initialize the custom model wrapper
gguf_model = GGUFModelWrapper(model_path=model_path)

# Log the model
with mlflow.start_run():
    mlflow.pyfunc.log_model(
        artifact_path="gguf_model",
        python_model=gguf_model,
        registered_model_name="GGUF_Model"
    )

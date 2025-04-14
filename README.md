import mlflow

# Load the model
model_uri = "models:/GGUF_Model/1"  # Adjust the version number as needed
loaded_model = mlflow.pyfunc.load_model(model_uri=model_uri)

# Prepare input data
input_data = {"input_text": "Your input text here"}

# Make predictions
predictions = loaded_model.predict(input_data)
print(predictions["output_text"])

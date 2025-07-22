# Move to GPU if available
device = "cuda" if torch.cuda.is_available() else "cpu"
model.to(device)
inputs = {k: v.to(device) for k, v in inputs.items()}

# Run inference
output = model.generate(**inputs, max_length=512, early_stopping=True)

# Decode the predicted answer
answer = processor.batch_decode(output, skip_special_tokens=True)[0]
answer = answer.replace("<s_answer>", "").strip()

print(f"Predicted Answer: {answer}")

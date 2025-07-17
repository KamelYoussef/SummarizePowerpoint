from transformers import DonutProcessor, VisionEncoderDecoderModel
from PIL import Image
import torch

# Load processor and model from your local folder (replace with your actual path)
processor = DonutProcessor.from_pretrained("path/to/donut-base")
model = VisionEncoderDecoderModel.from_pretrained("path/to/donut-base")

# Load your PNG image
image = Image.open("path/to/your-image.png").convert("RGB")

# Prepare image for model
pixel_values = processor(image, return_tensors="pt").pixel_values

# Generate output (assuming no prompt)
task_prompt = "<s>"  # Default for inference
decoder_input_ids = processor.tokenizer(task_prompt, add_special_tokens=False, return_tensors="pt").input_ids

# Run model
outputs = model.generate(pixel_values, decoder_input_ids=decoder_input_ids, max_length=512)

# Decode output
result = processor.batch_decode(outputs, skip_special_tokens=True)[0]
print("🔍 Extracted Text:")
print(result)

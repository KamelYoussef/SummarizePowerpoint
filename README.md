from transformers import DonutProcessor, VisionEncoderDecoderModel
from PIL import Image
import torch

# Load pretrained model and processor
model_id = "naver-clova-ix/donut-base-finetuned-docvqa"
processor = DonutProcessor.from_pretrained(model_id)
model = VisionEncoderDecoderModel.from_pretrained(model_id)

# Load and preprocess image
image = Image.open("your-form.png").convert("RGB")  # replace with your actual PNG path

# Ask a question about the image
question = "What information is written on this form?"  # or a specific one like "What is the invoice number?"

# Format for Donut input
prompt = f"<s_docvqa><question>{question}</question><image>"

# Tokenize prompt
decoder_input_ids = processor.tokenizer(prompt, add_special_tokens=False, return_tensors="pt").input_ids

# Preprocess image
pixel_values = processor(image, return_tensors="pt").pixel_values

# Generate answer
outputs = model.generate(
    pixel_values=pixel_values,
    decoder_input_ids=decoder_input_ids,
    max_length=512,
    num_beams=4,
    early_stopping=True,
)

# Decode and print
result = processor.batch_decode(outputs, skip_special_tokens=True)[0]
print("📝 Answer:", result)

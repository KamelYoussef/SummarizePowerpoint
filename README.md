from transformers import DonutProcessor, VisionEncoderDecoderModel
from PIL import Image
import torch

# Load image
image_path = "/mnt/data/TP-1.R--User1_page1.png"
image = Image.open(image_path).convert("RGB")  # Force RGB

# Load processor and model
processor = DonutProcessor.from_pretrained("naver-clova-ix/donut-base-finetuned-docvqa")
model = VisionEncoderDecoderModel.from_pretrained("naver-clova-ix/donut-base-finetuned-docvqa")
model.config.forced_bos_token_id = None
model.eval()

# Preprocess image (default size: 256x256)
encoding = processor(image, return_tensors="pt")
pixel_values = encoding.pixel_values

# 🧪 Check pixel values
print("Pixel values range:", pixel_values.min().item(), "to", pixel_values.max().item())

# Prompt
task_prompt = "<s_docvqa><question>What is the address?</question><image>"
decoder_input_ids = processor.tokenizer(task_prompt, add_special_tokens=False, return_tensors="pt").input_ids

# Generate answer
with torch.no_grad():
    outputs = model.generate(
        pixel_values=pixel_values,
        decoder_input_ids=decoder_input_ids,
        max_length=512,
        num_beams=4,
        pad_token_id=processor.tokenizer.pad_token_id
    )

# Decode
result = processor.batch_decode(outputs, skip_special_tokens=True)[0]
print("📋 Answer:", result)

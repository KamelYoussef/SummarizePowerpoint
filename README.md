from PIL import Image
import torch
from transformers import DonutProcessor, VisionEncoderDecoderModel

# Load model and processor
model_name = "naver-clova-ix/donut-base"
processor = DonutProcessor.from_pretrained(model_name)
model = VisionEncoderDecoderModel.from_pretrained(model_name)

device = "cuda" if torch.cuda.is_available() else "cpu"
model.to(device)
model.eval()

# Load image
try:
    image = Image.open("path/to/your/image.png").convert("RGB")
except FileNotFoundError:
    from PIL import ImageDraw
    image = Image.new('RGB', (800, 600), color = 'white')
    d = ImageDraw.Draw(image)
    d.text((10,10), "This is a simple test document.", fill=(0,0,0))
    d.text((10,50), "Line 2 of text.", fill=(0,0,0))
    print("Using a dummy image for demonstration.")

# Prepare image
pixel_values = processor(image, return_tensors="pt").pixel_values
pixel_values = pixel_values.to(device)

# Define task prompt
task_prompt = "<s_donut>"
decoder_input_ids = processor.tokenizer(task_prompt, add_special_tokens=False, return_tensors="pt").input_ids
decoder_input_ids = decoder_input_ids.to(device)

# Generate output
outputs = model.generate(
    pixel_values,
    decoder_input_ids=decoder_input_ids,
    max_length=model.decoder.config.max_position_embeddings,
    early_stopping=True,
    pad_token_id=processor.tokenizer.pad_token_id,
    eos_token_id=processor.tokenizer.eos_token_id,
    use_cache=True,
    num_beams=1,
    bad_words_ids=[[processor.tokenizer.unk_token_id]],
    return_dict_in_generate=True,
)

# Decode output
sequence = processor.batch_decode(outputs.sequences)[0]
sequence = sequence.replace(processor.tokenizer.eos_token, "").replace(processor.tokenizer.pad_token, "")
sequence = sequence.replace(task_prompt, "")

print("Generated Text:")
print(sequence)

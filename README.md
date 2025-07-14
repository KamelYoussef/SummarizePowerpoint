processor = DonutProcessor.from_pretrained("naver-clova-ix/donut-base")

def transform(example):
    image = Image.open(example["image_path"]).convert("RGB")
    pixel_values = processor.image_processor(image, return_tensors="pt").pixel_values[0]
    labels = processor.tokenizer(example["labels"], truncation=True, return_tensors="pt").input_ids[0]
    example["pixel_values"] = pixel_values
    example["labels"] = labels
    return example

ds = ds.map(transform)
# Split train/val e.g. 80/20
ds = ds.train_test_split(test_size=0.2)

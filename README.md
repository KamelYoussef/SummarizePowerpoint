def preprocess(examples):
    # Load and preprocess the image
    images = [Image.open(img_path).convert("RGB") for img_path in examples["image_path"]]
    pixel_values = processor(images, return_tensors="pt", padding=True).pixel_values

    # Tokenize the target JSON
    labels = []
    for target in examples["target_json"]:
        gt = json.dumps({"gt_parse": target}, ensure_ascii=False)
        label = processor.tokenizer(gt, add_special_tokens=False).input_ids
        labels.append(label)

    # Pad the labels to the same length
    max_length = max(len(label) for label in labels)
    labels = [label + [processor.tokenizer.pad_token_id] * (max_length - len(label)) for label in labels]
    labels = torch.tensor(labels)

    return {"pixel_values": pixel_values, "labels": labels}

# Apply preprocessing
dataset = DatasetDict({
    "train": dataset["train"].map(preprocess, batched=True),
    "test": dataset["test"].map(preprocess, batched=True)
})

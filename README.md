def preprocess(ex):
    img = Image.open(ex["image_path"]).convert("RGB")
    prompt = "<s_docvqa><s_question>extract info</s_question><s_answer>"
    enc = processor(img, prompt, return_tensors="pt")

    pixel_values = enc.pixel_values.squeeze(0)  # shape [C, H, W]
    labels = processor.tokenizer(
        ex["target"],
        padding="max_length",
        truncation=True,
        max_length=model.config.decoder.max_length,
        return_tensors="pt"
    ).input_ids.squeeze(0)  # shape [seq_len]

    labels[labels == processor.tokenizer.pad_token_id] = -100

    return {
        "pixel_values": pixel_values,
        "labels": labels
    }

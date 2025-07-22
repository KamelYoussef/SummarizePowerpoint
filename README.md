import os, json, torch
from PIL import Image
from datasets import Dataset, DatasetDict
from transformers import (
    DonutProcessor, 
    VisionEncoderDecoderModel, 
    Seq2SeqTrainer, 
    Seq2SeqTrainingArguments
)

# 1. Load processor + model
processor = DonutProcessor.from_pretrained("naver-clova-ix/donut-base-finetuned-docvqa")
model = VisionEncoderDecoderModel.from_pretrained("naver-clova-ix/donut-base-finetuned-docvqa")

# 2. Add JSON field tokens if needed
new_fields = ["invoice_number", "date", "total_amount"]  # adjust to your JSON keys
new_specials = [f"<s_{f}>" for f in new_fields] + [f"</s_{f}>" for f in new_fields]
processor.tokenizer.add_tokens(new_specials)
model.decoder.resize_token_embeddings(len(processor.tokenizer))

# 3. Freeze encoder optional
model.encoder.requires_grad_(False)

# 4. Update config for image size and decoder length
model.config.encoder.image_size = [1280, 960]  # width, height
model.config.decoder.max_length = 768
model.config.pad_token_id = processor.tokenizer.pad_token_id
model.config.decoder_start_token_id = processor.tokenizer.convert_tokens_to_ids([processor.tokenizer.cls_token])[0]

# 5. Load your data
def load_examples(folder):
    out = []
    for js in os.listdir(folder):
        if not js.endswith(".json"): continue
        img = js.replace(".json", ".png")
        p_img, p_js = os.path.join(folder, img), os.path.join(folder, js)
        if os.path.exists(p_img):
            with open(p_js, encoding="utf-8") as f:
                tgt = json.dumps(json.load(f), ensure_ascii=False)
            out.append({"image_path": p_img, "target": tgt})
    return out

train = load_examples("./donut-data/train")
val   = load_examples("./donut-data/test")
ds = DatasetDict(train=Dataset.from_list(train), validation=Dataset.from_list(val))

# 6. Preprocessing: add prompt, pad labels to -100
def preprocess(ex):
    img = Image.open(ex["image_path"]).convert("RGB")
    prompt = "<s_docvqa><s_question>extract info</s_question><s_answer>"
    inp = processor(img, prompt, return_tensors="pt")
    tgt_ids = processor.tokenizer(
        ex["target"], padding="max_length", truncation=True,
        max_length=model.config.decoder.max_length
    ).input_ids
    labels = [(i if i != processor.tokenizer.pad_token_id else -100) for i in tgt_ids]
    return {
        "input_ids": inp.input_ids.squeeze(),
        "pixel_values": inp.pixel_values.squeeze(),
        "labels": torch.tensor(labels)
    }

tokenized = ds.map(preprocess, remove_columns=ds["train"].column_names)

# 7. Define training args
training_args = Seq2SeqTrainingArguments(
    output_dir="./donut-finetuned",
    per_device_train_batch_size=1,
    per_device_eval_batch_size=1,
    predict_with_generate=True,
    evaluation_strategy="steps",
    logging_steps=10,
    save_steps=50,
    eval_steps=50,
    save_total_limit=2,
    num_train_epochs=10,
    learning_rate=5e-5,
    remove_unused_columns=False,
    # fp16=True,  # uncomment if GPU
)

# 8. Trainer
trainer = Seq2SeqTrainer(
    model=model,
    tokenizer=processor.tokenizer,
    args=training_args,
    train_dataset=tokenized["train"],
    eval_dataset=tokenized["validation"],
)

# 9. Start fine‑tuning
trainer.train()

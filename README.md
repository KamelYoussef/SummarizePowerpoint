import os
import json
from PIL import Image
from datasets import load_dataset, Dataset, DatasetDict
from transformers import DonutProcessor, VisionEncoderDecoderModel, Seq2SeqTrainer, Seq2SeqTrainingArguments

# Path to your dataset
train_dir = "./donut-data/train"
val_dir = "./donut-data/val"

# Load processor and model
processor = DonutProcessor.from_pretrained("naver-clova-ix/donut-base")
model = VisionEncoderDecoderModel.from_pretrained("naver-clova-ix/donut-base")

# Freeze encoder (optional, speeds up training)
model.encoder.requires_grad_(False)

# Helper to load (image, target) pairs
def load_examples_from_dir(folder):
    data = []
    for filename in os.listdir(folder):
        if filename.endswith(".json"):
            img_path = os.path.join(folder, filename.replace(".json", ".png"))
            json_path = os.path.join(folder, filename)
            if not os.path.exists(img_path):
                continue
            with open(json_path, "r", encoding="utf-8") as f:
                label = json.load(f)
            target_str = json.dumps(label, ensure_ascii=False)
            data.append({"image_path": img_path, "target": target_str})
    return data

# Load datasets
train_data = load_examples_from_dir(train_dir)
val_data = load_examples_from_dir(val_dir)

# Convert to Hugging Face Dataset
train_dataset = Dataset.from_list(train_data)
val_dataset = Dataset.from_list(val_data)
dataset = DatasetDict(train=train_dataset, validation=val_dataset)

# Preprocessing
def preprocess(example):
    image = Image.open(example["image_path"]).convert("RGB")
    question_prompt = "<s_docvqa><s_question>extract info</s_question><s_answer>"
    inputs = processor(image, question_prompt, return_tensors="pt")
    input_ids = inputs.input_ids.squeeze()
    pixel_values = inputs.pixel_values.squeeze()

    # Prepare decoder input
    target = processor.tokenizer(
        example["target"],
        padding="max_length",
        truncation=True,
        max_length=512,
        return_tensors="pt"
    ).input_ids.squeeze()

    return {
        "input_ids": input_ids,
        "pixel_values": pixel_values,
        "labels": target
    }

# Apply preprocessing
tokenized_ds = dataset.map(preprocess)

# Training arguments
training_args = Seq2SeqTrainingArguments(
    output_dir="./donut-finetuned",
    per_device_train_batch_size=1,
    per_device_eval_batch_size=1,
    predict_with_generate=True,
    evaluation_strategy="steps",
    num_train_epochs=10,
    logging_steps=10,
    save_steps=50,
    eval_steps=50,
    save_total_limit=2,
    learning_rate=5e-5,
    fp16=True,  # if using GPU
    remove_unused_columns=False,
)

# Trainer
trainer = Seq2SeqTrainer(
    model=model,
    tokenizer=processor.tokenizer,
    args=training_args,
    train_dataset=tokenized_ds["train"],
    eval_dataset=tokenized_ds["validation"],
)

# Start training
trainer.train()
